from django.urls import path
from . import views

urlpatterns = [
    # List all collections
    path("", views.collections, name="collections"),
    
    # Detail page for a specific collection
    path("<int:collection_id>/", views.collection_detail, name="collection_detail"),
    
    # Create a new collection
    path("create/", views.create, name="collection_create"),
    
    # Sync logic endpoints (assuming sync_from_source handles the main POST request)
    path("sync/<str:source_key>/<int:collection_id>/<int:source_id>", 
         views.sync_from_source, name="sync_from_source"),
    
    # Source search endpoint
    path("search/<str:source_key>/<str:query>", views.search_source, name="search_source"),

    # AJAX for listing sources in modal
    path("modal/", views.collections_modal, name="collections_modal"),
    
    # AJAX for item toggle (add/remove)
    path("item_toggle/", views.collection_item_toggle, name="collection_item_toggle"),
    
    # Search all sources endpoint (placeholder)
    path("search_all/", views.search_source_items, name="search_source_items"),
]