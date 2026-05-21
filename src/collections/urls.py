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
