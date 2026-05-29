"""Run this once from the yamtrack-fork root to create the two new templates."""
from pathlib import Path

BASE = Path(r"C:\yamtrack-fork\src\templates\app")

PERSONS_LIST = r"""{% extends "base.html" %}
{% load app_tags %}

{% block title %}{{ page_title }} - Yamtrack{% endblock title %}

{% block content %}
<div class="space-y-6">
  <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
    <h1 class="text-3xl font-bold">{{ page_title }}</h1>
    <div class="flex flex-wrap gap-2">
      <a href="{% url medialist_url_name media_type %}"
         class="px-4 py-2 rounded-full bg-[#39404b] text-gray-300 hover:bg-[#454d5a] transition-colors duration-200">
        {{ media_type|media_type_readable_plural }}
      </a>
      <a href="{% url list_url_name %}"
         class="px-4 py-2 rounded-full bg-indigo-600 text-white transition-colors duration-200">
        {{ person_type_plural }}
      </a>
    </div>
  </div>

  {% if persons %}
    <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4">
      {% for person in persons %}
        <a href="{% url detail_url_name person.id person.name|slugify %}"
           class="min-w-0 block rounded-2xl bg-[#2a2f35] p-5 hover:bg-[#343a40] transition-colors duration-200">
          <div class="flex items-center gap-3 mb-4">
            {% if person.image %}
              <img src="{{ person.image }}" alt="{{ person.name }}"
                   class="w-12 h-12 rounded-full object-cover flex-shrink-0"
                   onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
              <div class="w-12 h-12 rounded-full bg-indigo-600 items-center justify-center text-white text-lg flex-shrink-0 hidden">{{ person.name|slice:"0:1" }}</div>
            {% else %}
              <div class="w-12 h-12 rounded-full bg-indigo-600 flex items-center justify-center text-white text-lg flex-shrink-0">{{ person.name|slice:"0:1" }}</div>
            {% endif %}
            <div class="min-w-0">
              <h2 class="text-sm font-semibold truncate">{{ person.name }}</h2>
              <p class="text-xs text-gray-400">{{ person.media_count }} {{ media_type|media_type_readable }}{{ person.media_count|pluralize }}</p>
            </div>
          </div>
          <div class="flex items-center justify-between text-xs text-gray-300">
            <span>Tracked</span>
            <span class="font-semibold text-white">{{ person.percentage }}%</span>
          </div>
        </a>
      {% endfor %}
    </div>
  {% else %}
    <div class="rounded-2xl bg-[#2a2f35] p-8 text-center text-gray-400">
      No {{ person_type_plural|lower }} found. Track some {{ media_type|media_type_readable_plural|lower }} to populate this page.
    </div>
  {% endif %}
</div>
{% endblock content %}
"""

PERSON_DETAIL = r"""{% extends "base.html" %}
{% load app_tags %}

{% block title %}{{ person.name }} - Yamtrack{% endblock title %}

{% block content %}
<div class="space-y-6">
  <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between p-5 rounded-xl bg-gradient-to-b from-[#1e2329] to-[#171b20] ring-1 ring-white/5 shadow-lg">
    <div class="flex items-center gap-5">
      {% if person.image %}
        <img src="{{ person.image }}" alt="{{ person.name }}"
             class="w-16 h-16 rounded-full object-cover flex-shrink-0"
             onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
        <div class="w-16 h-16 rounded-full bg-indigo-600 items-center justify-center text-white text-2xl flex-shrink-0 hidden">{{ person.name|slice:"0:1" }}</div>
      {% else %}
        <div class="w-16 h-16 rounded-full bg-indigo-600 flex items-center justify-center text-white text-2xl flex-shrink-0">{{ person.name|slice:"0:1" }}</div>
      {% endif %}
      <div>
        <h1 class="text-3xl font-bold">{{ person.name }}</h1>
        <p class="text-gray-400 mt-1">{{ person.media_count }} {{ media_type|media_type_readable }}{{ person.media_count|pluralize }} tracked &bull; {{ person.percentage }}%</p>
      </div>
    </div>
    <div class="flex flex-wrap gap-2">
      <a href="{% url medialist_url_name media_type %}"
         class="px-4 py-2 rounded-full bg-[#2a2f35] text-gray-300 hover:bg-[#3a404a] ring-1 ring-white/5 transition-colors duration-200">
        {{ media_type|media_type_readable_plural }}
      </a>
      <a href="{% url list_url_name %}"
         class="px-4 py-2 rounded-full bg-indigo-600 text-white shadow-md shadow-indigo-600/20 ring-1 ring-indigo-300/30 transition-colors duration-200">
        {{ person_type_plural }}
      </a>
    </div>
  </div>

  {% if media_items %}
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-8 gap-4">
      {% for item in media_items %}
        <a href="{{ item.link }}"
           class="relative min-w-0 block rounded-2xl overflow-hidden bg-[#1e2329] ring-1 ring-white/5 shadow-md hover:shadow-xl hover:ring-white/10 transition-all duration-200 {% if item.completed %}ring-2 ring-emerald-500/40{% endif %}"
           {% if item.external %}target="_blank" rel="noreferrer noopener"{% endif %}>
          {% if item.completed %}
            <div class="absolute top-3 right-3 z-10 inline-flex items-center gap-1 rounded-full bg-emerald-500/15 text-emerald-300 ring-1 ring-emerald-400/30 backdrop-blur-md text-[11px] font-semibold px-2 py-1">
              {% include "app/icons/states/completed.svg" with classes="w-3 h-3" %}
              Completed
            </div>
          {% endif %}
          <div class="h-60 overflow-hidden bg-[#1f2429] {% if item.completed %}ring-2 ring-emerald-500/70{% endif %}">
            {% if item.image %}
              <img src="{{ item.image }}" alt="{{ item.title }}" class="w-full h-full object-cover" />
            {% else %}
              <div class="h-full flex items-center justify-center text-gray-500">No image</div>
            {% endif %}
          </div>
          <div class="p-4">
            <h2 class="text-sm font-semibold mb-1 line-clamp-2 text-white">{{ item.title }}</h2>
            <div class="flex flex-wrap items-center gap-2 text-xs text-gray-400">
              {% if item.release_year %}
                <span>{{ item.release_year }}</span>
              {% endif %}
              {% if item.tracked %}
                <span class="inline-flex items-center gap-1 rounded-full bg-indigo-500 px-3 py-1 text-xs font-semibold text-white ring-1 ring-indigo-300/40">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  Tracked
                </span>
              {% endif %}
            </div>
            {% if item.status %}
              <p class="text-xs text-gray-400 mt-2">{{ item.status|media_status_readable }}</p>
            {% endif %}
          </div>
        </a>
      {% endfor %}
    </div>
  {% else %}
    <div class="rounded-2xl bg-[#2a2f35] p-8 text-center text-gray-400">
      No tracked {{ media_type|media_type_readable_plural|lower }} found.
    </div>
  {% endif %}
</div>
{% endblock content %}
"""

(BASE / "persons_list.html").write_text(PERSONS_LIST, encoding="utf-8")
print("  OK   persons_list.html")
(BASE / "person_detail.html").write_text(PERSON_DETAIL, encoding="utf-8")
print("  OK   person_detail.html")
print("Done. Rebuild the container.")
