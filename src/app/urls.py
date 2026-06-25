from django.urls import path, register_converter, include

from app import converters, views

register_converter(converters.MediaTypeChecker, "media_type")
register_converter(converters.SourceChecker, "source")


urlpatterns = [
    path("", views.home, name="home"),
    path("medialist/<media_type:media_type>", views.media_list, name="medialist"),
    path("search", views.media_search, name="search"),
    path("artist/musicbrainz/<str:artist_id>", views.music_artist, name="music_artist"),
    path("movies/directors", views.movie_directors, name="movie_directors"),
    path("movie/director/<int:director_id>/filmography", views.movie_director_filmography, name="movie_director_filmography"),
    path("movie/director/<int:director_id>/bio", views.movie_director_bio, name="movie_director_bio"),
    path("movie/director/<int:director_id>/<slug:name>", views.movie_director, name="movie_director"),
    path("artist/musicbrainz/<str:artist_id>/bio", views.music_artist_bio, name="music_artist_bio"),
    path("music/artists", views.music_artists, name="music_artists"),
    path("games/studios", views.game_studios, name="game_studios"),
    path("game/studio/<str:studio_id>/<slug:name>", views.game_studio, name="game_studio"),
    path("comics/creators", views.comic_people, name="comic_people"),
    path("comic/creator/<str:person_id>/<slug:name>", views.comic_person, name="comic_person"),
    path("manga/authors", views.manga_authors, name="manga_authors"),
    path("manga/author/<str:author_id>/<slug:name>/items", views.manga_author_items, name="manga_author_items"),
    path("manga/author/<str:author_id>/<slug:name>", views.manga_author, name="manga_author"),
    path("books/authors", views.book_authors, name="book_authors"),
    path("book/author/<str:author_id>/<slug:name>", views.book_author, name="book_author"),
    path(
        "details/<source:source>/<media_type:media_type>/<str:media_id>/<str:title>",
        views.media_details,
        name="media_details",
    ),
    path(
        "details/<source:source>/tv/<str:media_id>/<str:title>/season/<int:season_number>",
        views.season_details,
        name="season_details",
    ),
    path(
        "update-score/<media_type:media_type>/<int:instance_id>",
        views.update_media_score,
        name="update_media_score",
    ),
    path(
        "details/sync/<source:source>/<media_type:media_type>/<str:media_id>",
        views.sync_metadata,
        name="sync_metadata",
    ),
    path(
        "details/sync/<source:source>/<media_type:media_type>/<str:media_id>/<int:season_number>",
        views.sync_metadata,
        name="sync_metadata",
    ),
    path(
        "track_modal/<source:source>/<media_type:media_type>/<str:media_id>",
        views.track_modal,
        name="track_modal",
    ),
    path(
        "track_modal/<source:source>/<media_type:media_type>/<str:media_id>/<int:season_number>",
        views.track_modal,
        name="track_modal",
    ),
    path(
        "progress_edit/<media_type:media_type>/<int:instance_id>",
        views.progress_edit,
        name="progress_edit",
    ),
    # Include URLs from other modules here (e.g., api_urls)
    # path("api/v1/", include("rest_framework.routers.DefaultRouter")),
    path("media_save", views.media_save, name="media_save"),
    path("media_delete", views.media_delete, name="media_delete"),
    path(
        "user_messages/mark_shown",
        views.mark_user_messages_shown,
        name="mark_user_messages_shown",
    ),
    path("episode_save", views.episode_save, name="episode_save"),
    path(
        "history_modal/<source:source>/<media_type:media_type>/<str:media_id>",
        views.history_modal,
        name="history_modal",
    ),
    path(
        "history_modal/<source:source>/<media_type:media_type>/<str:media_id>/<int:season_number>",
        views.history_modal,
        name="history_modal",
    ),
    path(
        "history_modal/<source:source>/<media_type:media_type>/<str:media_id>/<int:season_number>/<int:episode_number>",
        views.history_modal,
        name="history_modal",
    ),
    path(
        "media/history/<str:media_type>/<int:history_id>/delete/",
        views.delete_history_record,
        name="delete_history_record",
    ),
    path("create", views.create_entry, name="create_entry"),
    path("search/parent_tv", views.search_parent_tv, name="search_parent_tv"),
    path(
        "search/parent_season",
        views.search_parent_season,
        name="search_parent_season",
    ),
    path("statistics", views.statistics, name="statistics"),
    path(
        "statistics/awards/<slug:award_slug>",
        views.award_progress_detail,
        name="award_progress_detail",
    ),
    path("serviceworker.js", views.service_worker, name="service_worker"),
]
