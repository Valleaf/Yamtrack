#!/usr/bin/env python3
"""
build_collections.py
Run from C:/yamtrack-fork: python build_collections.py

Creates the full Collections feature as a separate Django app.
"""
from pathlib import Path

ROOT = Path(r"C:\yamtrack-fork")
SRC = ROOT / "src"


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  OK   {path.relative_to(ROOT)}")


def patch(path: Path, old: str, new: str, label: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        print(f"  SKIP {label} — pattern not found")
        return
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"  OK   {label}")


# ── collections/__init__.py ───────────────────────────────────────────────────
write(SRC / "collections" / "__init__.py", "")

# ── collections/apps.py ───────────────────────────────────────────────────────
write(SRC / "collections" / "apps.py", '''\
from django.apps import AppConfig


class CollectionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collections"
''')

# ── collections/models.py ─────────────────────────────────────────────────────
write(SRC / "collections" / "models.py", '''\
from django.conf import settings
from django.db import models
from django.db.models import Avg, Count, Exists, OuterRef, Prefetch, Q

from app.models import Item, MediaTypes


class CollectionManager(models.Manager):
    """Manager for collections."""

    def get_user_collections(self, user):
        return (
            self.filter(Q(owner=user) | Q(collaborators=user))
            .select_related("owner")
            .prefetch_related(
                "collaborators",
                Prefetch(
                    "collectionitem_set",
                    queryset=CollectionItem.objects.select_related("item")
                    .order_by("date_added"),
                ),
            )
            .distinct()
            .order_by("name")
        )

    def get_user_collections_with_item(self, user, item):
        return (
            self.filter(Q(owner=user) | Q(collaborators=user))
            .annotate(
                has_item=Exists(
                    CollectionItem.objects.filter(
                        collection_id=models.OuterRef("id"),
                        item=item,
                    )
                )
            )
            .prefetch_related("collaborators")
            .distinct()
            .order_by("name")
        )


class Collection(models.Model):
    """A cross-media franchise or universe collection."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collaborated_collections",
        blank=True,
    )
    items = models.ManyToManyField(
        Item,
        related_name="collections",
        blank=True,
        through="CollectionItem",
    )

    objects = CollectionManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def image(self):
        first = self.collectionitem_set.select_related("item").first()
        return first.item.image if first else settings.IMG_NONE

    def user_can_edit(self, user):
        return self.owner == user or user in self.collaborators.all()

    def user_can_delete(self, user):
        return self.owner == user

    def get_stats(self, user):
        """Compute franchise-style stats for this collection for a given user."""
        from django.apps import apps

        items = list(
            self.collectionitem_set.select_related("item").order_by("date_added")
        )
        total = len(items)
        if not total:
            return {
                "total": 0,
                "tracked": 0,
                "tracked_pct": 0,
                "by_type": {},
                "avg_score": None,
            }

        # Group items by media_type
        by_type = {}
        for ci in items:
            mt = ci.item.media_type
            by_type.setdefault(mt, [])
            by_type[mt].append(ci.item)

        type_stats = {}
        total_tracked = 0
        score_sum = 0
        score_count = 0

        for mt, type_items in by_type.items():
            try:
                model = apps.get_model("app", mt)
            except LookupError:
                continue

            item_ids = [i.id for i in type_items]
            qs = model.objects.filter(item_id__in=item_ids, user=user).select_related("item")

            tracked_ids = set(qs.values_list("item_id", flat=True))
            scores = [float(m.score) for m in qs if m.score is not None]

            type_stats[mt] = {
                "total": len(type_items),
                "tracked": len(tracked_ids),
                "tracked_pct": round(len(tracked_ids) / len(type_items) * 100) if type_items else 0,
                "avg_score": round(sum(scores) / len(scores), 1) if scores else None,
                "items": type_items,
            }
            total_tracked += len(tracked_ids)
            score_sum += sum(scores)
            score_count += len(scores)

        return {
            "total": total,
            "tracked": total_tracked,
            "tracked_pct": round(total_tracked / total * 100) if total else 0,
            "by_type": type_stats,
            "avg_score": round(score_sum / score_count, 1) if score_count else None,
        }


class CollectionItem(models.Model):
    """An item within a collection, with an optional note."""

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, blank=True, default="")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_added"]
        constraints = [
            models.UniqueConstraint(
                fields=["item", "collection"],
                name="collections_collectionitem_unique_item_collection",
            )
        ]

    def __str__(self):
        return self.item.title
''')

# ── collections/forms.py ──────────────────────────────────────────────────────
write(SRC / "collections" / "forms.py", '''\
from django import forms
from django_select2 import forms as s2forms

from collections.models import Collection


class CollaboratorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["username__icontains"]


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "description", "collaborators"]
        widgets = {
            "collaborators": CollaboratorsWidget(
                attrs={
                    "data-minimum-input-length": 1,
                    "data-placeholder": "Search users...",
                    "data-allow-clear": "false",
                }
            )
        }
''')

# ── collections/views.py ──────────────────────────────────────────────────────
write(SRC / "collections" / "views.py", '''\
import logging

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from app import helpers
from app.models import Item, MediaTypes
from app.providers import services
from collections.forms import CollectionForm
from collections.models import Collection, CollectionItem

logger = logging.getLogger(__name__)


@require_GET
def collections(request):
    """List all collections for the current user."""
    user_collections = Collection.objects.get_user_collections(request.user)
    form = CollectionForm()
    return render(request, "collections/collections.html", {
        "collections": user_collections,
        "form": form,
    })


@require_GET
def collection_detail(request, collection_id):
    """Detail page for a single collection with franchise stats."""
    collection = get_object_or_404(
        Collection.objects.select_related("owner").prefetch_related("collaborators"),
        id=collection_id,
    )
    if not collection.user_can_edit(request.user) and collection.owner != request.user:
        raise Http404

    media_type_filter = request.GET.get("type", "all")
    items_qs = collection.collectionitem_set.select_related("item").order_by("date_added")
    if media_type_filter != "all":
        items_qs = items_qs.filter(item__media_type=media_type_filter)

    stats = collection.get_stats(request.user)
    form = CollectionForm(instance=collection)

    return render(request, "collections/collection_detail.html", {
        "collection": collection,
        "collection_items": items_qs,
        "stats": stats,
        "form": form,
        "media_type_filter": media_type_filter,
        "media_types": MediaTypes.values,
    })


@require_POST
def create(request):
    form = CollectionForm(request.POST)
    if form.is_valid():
        col = form.save(commit=False)
        col.owner = request.user
        col.save()
        form.save_m2m()
        logger.info("%s collection created.", col)
    else:
        helpers.form_error_messages(form, request)
    return helpers.redirect_back(request)


@require_POST
def edit(request):
    col_id = request.POST.get("collection_id")
    col = get_object_or_404(Collection, id=col_id)
    if col.user_can_edit(request.user):
        form = CollectionForm(request.POST, instance=col)
        if form.is_valid():
            form.save()
    else:
        messages.error(request, "You do not have permission to edit this collection.")
    return helpers.redirect_back(request)


@require_POST
def delete(request):
    col_id = request.POST.get("collection_id")
    col = get_object_or_404(Collection, id=col_id)
    if col.user_can_delete(request.user):
        col.delete()
        return redirect("collections")
    messages.error(request, "You do not have permission to delete this collection.")
    return helpers.redirect_back(request)


@require_GET
def collections_modal(request, source, media_type, media_id, season_number=None):
    """Modal showing collections the user can add an item to."""
    try:
        item = Item.objects.get(
            media_id=media_id, source=source, media_type=media_type,
            season_number=season_number,
        )
    except Item.DoesNotExist:
        metadata = services.get_media_metadata(media_type, media_id, source, [season_number])
        item = Item.objects.create(
            media_id=media_id, source=source, media_type=media_type,
            season_number=season_number,
            title=metadata["title"], image=metadata["image"],
            country=metadata.get("country") or "",
        )
    user_collections = Collection.objects.get_user_collections_with_item(request.user, item)
    return render(request, "collections/components/fill_collections.html", {
        "item": item,
        "user_collections": user_collections,
    })


@require_POST
def collection_item_toggle(request):
    """Add or remove an item from a collection."""
    item_id = request.POST["item_id"]
    collection_id = request.POST["collection_id"]
    item = get_object_or_404(Item, id=item_id)
    col = get_object_or_404(Collection, id=collection_id)
    if not col.user_can_edit(request.user):
        raise Http404

    if col.items.filter(id=item.id).exists():
        col.items.remove(item)
        has_item = False
    else:
        col.items.add(item)
        has_item = True

    return render(request, "collections/components/collection_item_button.html", {
        "collection": col, "item": item, "has_item": has_item,
    })
''')

# ── collections/urls.py ───────────────────────────────────────────────────────
write(SRC / "collections" / "urls.py", '''\
from django.urls import path
from app import converters
from django.urls import register_converter

from collections import views

urlpatterns = [
    path("collections", views.collections, name="collections"),
    path("collection/<int:collection_id>", views.collection_detail, name="collection_detail"),
    path("collection/create", views.create, name="collection_create"),
    path("collection/edit", views.edit, name="collection_edit"),
    path("collection/delete", views.delete, name="collection_delete"),
    path("collection_item_toggle", views.collection_item_toggle, name="collection_item_toggle"),
    path(
        "collections_modal/<str:source>/<str:media_type>/<str:media_id>",
        views.collections_modal, name="collections_modal",
    ),
    path(
        "collections_modal/<str:source>/<str:media_type>/<str:media_id>/<int:season_number>",
        views.collections_modal, name="collections_modal",
    ),
]
''')

# ── collections/migrations/__init__.py ────────────────────────────────────────
write(SRC / "collections" / "migrations" / "__init__.py", "")

# ── collections/migrations/0001_initial.py ────────────────────────────────────
write(SRC / "collections" / "migrations" / "0001_initial.py", '''\
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("app", "0064_merge_country_migrations"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("collaborators", models.ManyToManyField(blank=True, related_name="collaborated_collections", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="CollectionItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("notes", models.CharField(blank=True, default="", max_length=255)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("collection", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="collections.collection")),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="app.item")),
            ],
            options={"ordering": ["date_added"]},
        ),
        migrations.AddField(
            model_name="collection",
            name="items",
            field=models.ManyToManyField(blank=True, related_name="collections", through="collections.CollectionItem", to="app.item"),
        ),
        migrations.AddConstraint(
            model_name="collectionitem",
            constraint=models.UniqueConstraint(
                fields=["item", "collection"],
                name="collections_collectionitem_unique_item_collection",
            ),
        ),
    ]
''')

# ── Templates ─────────────────────────────────────────────────────────────────
TMPL = SRC / "templates" / "collections"

write(TMPL / "components" / "collection_form.html", '''\
{% load static %}
<div x-show="showModal"
     x-cloak
     class="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
     @click.self="showModal = false">
  <div class="bg-[#1e2227] rounded-xl shadow-xl w-full max-w-lg mx-4 p-6">
    <h2 class="text-lg font-semibold mb-4">{% if collection %}Edit{% else %}New{% endif %} Collection</h2>
    <form method="post" action="{% if collection %}{% url 'collection_edit' %}{% else %}{% url 'collection_create' %}{% endif %}">
      {% csrf_token %}
      {% if collection %}<input type="hidden" name="collection_id" value="{{ collection.id }}">{% endif %}
      <input type="hidden" name="next" value="{{ request.path }}">
      {% for field in form %}
        <div class="mb-4">
          <label class="block text-sm text-gray-400 mb-1">{{ field.label }}</label>
          {{ field }}
          {% if field.errors %}<p class="text-red-400 text-xs mt-1">{{ field.errors.0 }}</p>{% endif %}
        </div>
      {% endfor %}
      <div class="flex justify-end gap-3 mt-6">
        <button type="button" @click="showModal = false"
                class="px-4 py-2 rounded-md bg-[#39404b] hover:bg-[#454d5a] text-sm transition-colors cursor-pointer">Cancel</button>
        <button type="submit"
                class="px-4 py-2 rounded-md bg-indigo-600 hover:bg-indigo-700 text-sm font-medium transition-colors cursor-pointer">
          {% if collection %}Save{% else %}Create{% endif %}
        </button>
      </div>
    </form>
    {% if collection and collection.user_can_delete(request.user) %}
    <form method="post" action="{% url 'collection_delete' %}" class="mt-3 text-right">
      {% csrf_token %}
      <input type="hidden" name="collection_id" value="{{ collection.id }}">
      <input type="hidden" name="next" value="{% url 'collections' %}">
      <button type="submit" class="text-red-400 hover:text-red-300 text-xs transition-colors cursor-pointer"
              onclick="return confirm('Delete this collection?')">Delete collection</button>
    </form>
    {% endif %}
  </div>
</div>
''')

write(TMPL / "components" / "fill_collections.html", '''\
<div class="p-2">
  <h3 class="text-sm font-semibold text-gray-400 mb-3 px-2">Add to Collection</h3>
  {% if user_collections %}
    <div class="space-y-1">
      {% for collection in user_collections %}
        {% include "collections/components/collection_item_button.html" with collection=collection item=item has_item=collection.has_item %}
      {% endfor %}
    </div>
  {% else %}
    <p class="text-sm text-gray-500 px-2">No collections yet. <a href="{% url 'collections' %}" class="text-indigo-400 hover:underline">Create one</a>.</p>
  {% endif %}
</div>
''')

write(TMPL / "components" / "collection_item_button.html", '''\
<button hx-post="{% url 'collection_item_toggle' %}"
        hx-vals=\'{"item_id": "{{ item.id }}", "collection_id": "{{ collection.id }}"  }\'
        hx-target="this"
        hx-swap="outerHTML"
        class="w-full flex items-center justify-between px-3 py-2 rounded-md text-sm transition-colors cursor-pointer
               {% if has_item %}bg-indigo-600/20 text-indigo-400 hover:bg-red-600/20 hover:text-red-400{% else %}text-gray-300 hover:bg-[#39404b]{% endif %}">
  <span>{{ collection.name }}</span>
  {% if has_item %}
    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
  {% else %}
    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
  {% endif %}
</button>
''')

write(TMPL / "collections.html", '''\
{% extends "base.html" %}
{% load app_tags %}

{% block extra_head %}{{ form.media.css }}{% endblock %}

{% block title %}Collections - Yamtrack{% endblock %}

{% block content %}
<div x-data="{ showModal: false }" class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold mb-1">Collections</h1>
      <p class="text-gray-400 text-sm">Franchise universes, series, and cross-media groups</p>
    </div>
    <button @click="showModal = true"
            class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors cursor-pointer">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
      New Collection
    </button>
  </div>

  {% include "collections/components/collection_form.html" %}

  {% if collections %}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {% for col in collections %}
        {% with items=col.collectionitem_set.all %}
        <a href="{% url 'collection_detail' col.id %}"
           class="group bg-[#2a2f35] rounded-lg overflow-hidden hover:bg-[#313840] transition-colors border border-transparent hover:border-indigo-500/30">
          <div class="aspect-[3/2] bg-[#1a1d20] overflow-hidden">
            {% if items %}
              <div class="grid {% if items|length >= 4 %}grid-cols-2{% else %}grid-cols-1{% endif %} h-full">
                {% for ci in items|slice:":4" %}
                  <img src="{{ ci.item.image }}" alt="{{ ci.item.title }}"
                       class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity">
                {% endfor %}
              </div>
            {% else %}
              <div class="w-full h-full flex items-center justify-center text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="2" y="3" width="20" height="14" rx="2"></rect><path d="M8 21h8M12 17v4"></path></svg>
              </div>
            {% endif %}
          </div>
          <div class="p-4">
            <h3 class="font-semibold text-white truncate group-hover:text-indigo-300 transition-colors">{{ col.name }}</h3>
            {% if col.description %}
              <p class="text-gray-400 text-xs mt-1 line-clamp-2">{{ col.description }}</p>
            {% endif %}
            <div class="flex items-center gap-3 mt-3 text-xs text-gray-500">
              <span>{{ items|length }} item{{ items|length|pluralize }}</span>
              {% with types=items|map_attr:"item.media_type"|unique_list %}
                {% if types %}
                  <span class="flex gap-1">
                    {% for mt in types|slice:":4" %}
                      <span class="px-1.5 py-0.5 bg-[#39404b] rounded text-gray-400">{{ mt|media_type_readable }}</span>
                    {% endfor %}
                  </span>
                {% endif %}
              {% endwith %}
            </div>
          </div>
        </a>
        {% endwith %}
      {% endfor %}
    </div>
  {% else %}
    <div class="flex flex-col items-center justify-center py-24 bg-[#2a2f35] rounded-lg">
      <div class="bg-[#39404b] rounded-full p-5 w-20 h-20 mx-auto mb-4 flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="3" width="20" height="14" rx="2"></rect><path d="M8 21h8M12 17v4"></path></svg>
      </div>
      <h3 class="text-xl font-semibold mb-2">No collections yet</h3>
      <p class="text-gray-400 mb-6">Group your MCU movies, Game of Thrones books and shows, or any franchise across media types.</p>
      <button @click="showModal = true"
              class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors cursor-pointer">
        Create your first collection
      </button>
    </div>
  {% endif %}
</div>
{% endblock %}

{% block js %}{{ form.media.js }}{% endblock %}
''')

write(TMPL / "collection_detail.html", '''\
{% extends "base.html" %}
{% load app_tags %}

{% block extra_head %}{{ form.media.css }}{% endblock %}

{% block title %}{{ collection.name }} - Yamtrack{% endblock %}

{% block content %}
<div x-data="{ showModal: false }" class="space-y-6">

  {# Header #}
  <div class="flex items-start justify-between gap-4">
    <div>
      <div class="flex items-center gap-2 text-gray-400 text-sm mb-1">
        <a href="{% url 'collections' %}" class="hover:text-white transition-colors">Collections</a>
        <span>/</span>
        <span class="text-white">{{ collection.name }}</span>
      </div>
      <h1 class="text-3xl font-bold">{{ collection.name }}</h1>
      {% if collection.description %}
        <p class="text-gray-400 mt-1">{{ collection.description }}</p>
      {% endif %}
    </div>
    {% if collection.user_can_edit(request.user) %}
    <button @click="showModal = true"
            class="flex-shrink-0 flex items-center gap-2 px-4 py-2 bg-[#39404b] hover:bg-[#454d5a] rounded-md text-sm transition-colors cursor-pointer">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
      Edit
    </button>
    {% endif %}
  </div>

  {% include "collections/components/collection_form.html" with collection=collection %}

  {# Stats bar #}
  {% if stats.total %}
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
    <div class="bg-[#2a2f35] rounded-lg p-4 text-center">
      <div class="text-2xl font-bold text-white">{{ stats.total }}</div>
      <div class="text-xs text-gray-400 mt-1">Total Items</div>
    </div>
    <div class="bg-[#2a2f35] rounded-lg p-4 text-center">
      <div class="text-2xl font-bold text-indigo-400">{{ stats.tracked }}</div>
      <div class="text-xs text-gray-400 mt-1">Tracked by You</div>
    </div>
    <div class="bg-[#2a2f35] rounded-lg p-4 text-center">
      <div class="text-2xl font-bold {% if stats.tracked_pct == 100 %}text-green-400{% elif stats.tracked_pct > 50 %}text-yellow-400{% else %}text-gray-300{% endif %}">
        {{ stats.tracked_pct }}%
      </div>
      <div class="text-xs text-gray-400 mt-1">Complete</div>
    </div>
    <div class="bg-[#2a2f35] rounded-lg p-4 text-center">
      <div class="text-2xl font-bold text-white">{{ stats.avg_score|default:"—" }}</div>
      <div class="text-xs text-gray-400 mt-1">Avg Score</div>
    </div>
  </div>

  {# Per-type breakdown #}
  {% if stats.by_type %}
  <div class="bg-[#2a2f35] rounded-lg p-5">
    <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-4">By Media Type</h2>
    <div class="space-y-3">
      {% for mt, ts in stats.by_type.items %}
      <div>
        <div class="flex items-center justify-between text-sm mb-1">
          <span class="text-gray-300 font-medium">{{ mt|media_type_readable_plural }}</span>
          <span class="text-gray-400">
            {{ ts.tracked }}/{{ ts.total }}
            {% if ts.avg_score %} · <span class="text-yellow-400">★ {{ ts.avg_score }}</span>{% endif %}
          </span>
        </div>
        <div class="w-full bg-[#39404b] rounded-full h-1.5">
          <div class="bg-indigo-500 h-1.5 rounded-full transition-all"
               style="width: {{ ts.tracked_pct }}%"></div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}
  {% endif %}

  {# Type filter tabs #}
  <div class="flex flex-wrap gap-2">
    <a href="?type=all"
       class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
              {% if media_type_filter == 'all' %}bg-indigo-600 text-white{% else %}bg-[#39404b] text-gray-300 hover:bg-[#454d5a]{% endif %}">
      All
    </a>
    {% for mt in media_types %}
      {% if mt in stats.by_type %}
      <a href="?type={{ mt }}"
         class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
                {% if media_type_filter == mt %}bg-indigo-600 text-white{% else %}bg-[#39404b] text-gray-300 hover:bg-[#454d5a]{% endif %}">
        {{ mt|media_type_readable_plural }}
      </a>
      {% endif %}
    {% endfor %}
  </div>

  {# Items grid #}
  {% if collection_items %}
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      {% for ci in collection_items %}
        <a href="{% url 'media_details' source=ci.item.source media_type=ci.item.media_type media_id=ci.item.media_id title=ci.item.title|slugify %}"
           class="group relative bg-[#2a2f35] rounded-lg overflow-hidden hover:ring-2 hover:ring-indigo-500 transition-all">
          <div class="aspect-[2/3] overflow-hidden bg-[#1a1d20]">
            <img src="{{ ci.item.image }}" alt="{{ ci.item.title }}"
                 class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
          </div>
          <div class="p-2">
            <p class="text-xs font-medium text-white truncate">{{ ci.item.title }}</p>
            <p class="text-xs text-gray-500">{{ ci.item.media_type|media_type_readable }}</p>
            {% if ci.notes %}
              <p class="text-xs text-indigo-400 truncate mt-0.5">{{ ci.notes }}</p>
            {% endif %}
          </div>
        </a>
      {% endfor %}
    </div>
  {% else %}
    <div class="flex flex-col items-center justify-center py-16 bg-[#2a2f35] rounded-lg">
      <p class="text-gray-400">No items yet. Add media to this collection from any detail page.</p>
    </div>
  {% endif %}
</div>
{% endblock %}

{% block js %}{{ form.media.js }}{% endblock %}
''')

# ── settings.py — add collections to INSTALLED_APPS ──────────────────────────
print("\n[Patching settings.py]")
settings_py = SRC / "config" / "settings.py"
patch(settings_py,
    old='"lists",',
    new='"lists",\n    "collections",',
    label="settings.py — add collections to INSTALLED_APPS",
)

# ── config/urls.py — include collections urls ─────────────────────────────────
print("\n[Patching config/urls.py]")
patch(SRC / "config" / "urls.py",
    old='path("", include("lists.urls")),',
    new='path("", include("lists.urls")),\n    path("", include("collections.urls")),',
    label="config/urls.py — include collections.urls",
)

# ── base.html — add Collections to sidebar ────────────────────────────────────
print("\n[Patching base.html]")
patch(SRC / "templates" / "base.html",
    old='{% url \'lists\' as lists_url %}\n                <li>',
    new='''{% url 'collections' as collections_url %}
                <li>
                  <a href="{{ collections_url }}"
                     class="flex items-center space-x-3 px-4 py-2 rounded-md transition-colors duration-200 text-sm {% if request.path == collections_url %}text-white bg-[#2c3136]{% else %}text-gray-400 hover:text-white hover:bg-[#23272b]{% endif %}">
                    {% if request.path|str_equals:collections_url %}
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"></rect><path d="M8 21h8M12 17v4"></path></svg>
                    {% else %}
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"></rect><path d="M8 21h8M12 17v4"></path></svg>
                    {% endif %}
                    <span>Collections</span>
                  </a>
                </li>
                {% url \'lists\' as lists_url %}
                <li>''',
    label="base.html — Collections sidebar entry",
)

print()
print("=" * 60)
print("✅  Done. Commit and rebuild:")
print()
print("  git add src/collections/ src/templates/collections/")
print("  git add src/config/settings.py src/config/urls.py src/templates/base.html")
print("  git commit -m 'feat: Collections — feat: Collections cross-media franchise groups with stats'")
print("  docker compose down; docker compose up -d --build")
print()
print("To add an item to a collection from a detail page, you'll need to")
print("wire the collections modal button into the existing media_details.html")
print("the same way the lists modal is wired — see fill_lists.html for the pattern.")
