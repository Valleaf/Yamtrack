from django.urls import path
from media_collections import views

urlpatterns = [
    path("media_collections", views.collections, name="media_collections"),
    path("collection/create", views.create, name="collection_create"),
    path("collection/search_source", views.search_source, name="collection_search_source"),
    path("collection_item_toggle", views.collection_item_toggle, name="collection_item_toggle"),
    path("collection/<int:collection_id>", views.collection_detail, name="collection_detail"),
    path("collection/<int:collection_id>/edit", views.edit, name="collection_edit"),
    path("collection/<int:collection_id>/delete", views.delete, name="collection_delete"),
    path("collection/<int:collection_id>/sync", views.sync_from_source, name="collection_sync"),
    path("collections_modal/<str:source>/<str:media_type>/<str:media_id>",
         views.collections_modal, name="collections_modal"),
    path("collections_modal/<str:source>/<str:media_type>/<str:media_id>/<int:season_number>",
         views.collections_modal, name="collections_modal_season"),
]
