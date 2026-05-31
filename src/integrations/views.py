"""Contains views for importing and exporting media data from various sources."""

import json
import logging
import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

import users
from app import helpers as app_helpers
from integrations import exports, tasks
from integrations.imports import anilist, helpers, senscritique as sc_import, simkl, trakt
from integrations.webhooks import emby, jellyfin, plex

logger = logging.getLogger(__name__)


@require_POST
def trakt_oauth(request):
    """View for initiating Trakt OAuth2 authorization flow."""
    redirect_uri = app_helpers.build_absolute_app_url(
        request,
        reverse("import_trakt_private"),
    )
    url = "https://trakt.tv/oauth/authorize"
    state = {
        "mode": request.POST["mode"],
        "frequency": request.POST["frequency"],
        "time": request.POST["time"],
        "redirect_uri": redirect_uri,
    }
    state_token = secrets.token_urlsafe(32)
    request.session[state_token] = state
    return redirect(
        f"{url}?{
            urlencode(
                {
                    'client_id': settings.TRAKT_API,
                    'redirect_uri': redirect_uri,
                    'response_type': 'code',
                    'state': state_token,
                }
            )
        }",
    )


@require_GET
def import_trakt_private(request):
    """View for handling Trakt OAuth2 callback and scheduling private import."""
    state_token = request.GET.get("state")
    state = request.session.get(state_token)
    if not state:
        messages.error(request, "Invalid or expired Trakt authorization request.")
        return redirect("import_data")

    if not request.GET.get("code"):
        messages.error(request, "Trakt authorization failed.")
        return redirect("import_data")

    redirect_uri = state.get("redirect_uri") or app_helpers.build_absolute_app_url(
        request,
        reverse("import_trakt_private"),
    )
    oauth_callback = trakt.handle_oauth_callback(request, redirect_uri=redirect_uri)
    enc_token = helpers.encrypt(oauth_callback["refresh_token"])

    frequency = state["frequency"]
    mode = state["mode"]
    import_time = state["time"]

    if frequency == "once":
        tasks.import_trakt.delay(
            token=enc_token,
            user_id=request.user.id,
            mode=mode,
            username=oauth_callback["username"],
            redirect_uri=redirect_uri,
        )
        messages.info(request, "The task to import media from Trakt has been queued.")
    else:
        helpers.create_import_schedule(
            oauth_callback["username"],
            request,
            mode,
            frequency,
            import_time,
            "Trakt",
            token=enc_token,
            task_kwargs={"redirect_uri": redirect_uri},
        )
    request.session.pop(state_token, None)
    return redirect("import_data")


@require_POST
def import_trakt_public(request):
    """View for importing Trakt data using public username."""
    username = request.POST.get("user")
    if not username:
        messages.error(request, "Trakt username is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    frequency = request.POST["frequency"]
    import_time = request.POST["time"]

    if frequency == "once":
        tasks.import_trakt.delay(
            user_id=request.user.id,
            mode=mode,
            username=username,
        )
        messages.info(request, "The task to import media from Trakt has been queued.")
    else:
        helpers.create_import_schedule(
            username=username,
            request=request,
            mode=mode,
            frequency=frequency,
            import_time=import_time,
            source="Trakt",
        )
    return redirect("import_data")


@require_POST
def simkl_oauth(request):
    """View for initiating the SIMKL OAuth2 authorization flow."""
    redirect_uri = app_helpers.build_absolute_app_url(
        request,
        reverse("import_simkl_private"),
    )
    url = "https://simkl.com/oauth/authorize"

    state = {
        "mode": request.POST["mode"],
        "frequency": request.POST["frequency"],
        "time": request.POST["time"],
    }
    state_token = secrets.token_urlsafe(32)
    request.session[state_token] = state

    return redirect(
        f"{url}?{
            urlencode(
                {
                    'client_id': settings.SIMKL_ID,
                    'redirect_uri': redirect_uri,
                    'response_type': 'code',
                    'state': state_token,
                }
            )
        }",
    )


@require_GET
def import_simkl_private(request):
    """View for getting the SIMKL OAuth2 token."""
    oauth_callback = simkl.get_token(request)
    enc_token = helpers.encrypt(oauth_callback["access_token"])
    state_token = request.GET["state"]

    frequency = request.session[state_token]["frequency"]
    mode = request.session[state_token]["mode"]
    import_time = request.session[state_token]["time"]

    if frequency == "once":
        tasks.import_simkl.delay(token=enc_token, user_id=request.user.id, mode=mode)
        messages.info(request, "The task to import media from Simkl has been queued.")
    else:
        helpers.create_import_schedule(
            oauth_callback["username"],
            request,
            mode,
            frequency,
            import_time,
            "SIMKL",
            token=enc_token,
        )

    return redirect("import_data")


@require_POST
def import_mal(request):
    """View for importing anime and manga data from MyAnimeList."""
    username = request.POST.get("user")
    if not username:
        messages.error(request, "MyAnimeList username is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    frequency = request.POST["frequency"]

    if frequency == "once":
        tasks.import_mal.delay(username=username, user_id=request.user.id, mode=mode)
        messages.info(
            request,
            "The task to import media from MyAnimeList has been queued.",
        )
    else:
        import_time = request.POST["time"]
        helpers.create_import_schedule(
            username,
            request,
            mode,
            frequency,
            import_time,
            "MyAnimeList",
        )
    return redirect("import_data")


@require_POST
def anilist_oauth(request):
    """Initiate AniList OAuth flow."""
    redirect_uri = app_helpers.build_absolute_app_url(
        request,
        reverse("import_anilist_private"),
    )
    url = "https://anilist.co/api/v2/oauth/authorize"
    state = {
        "mode": request.POST["mode"],
        "frequency": request.POST["frequency"],
        "time": request.POST["time"],
    }

    state_token = secrets.token_urlsafe(32)
    request.session[state_token] = state

    return redirect(
        f"{url}?{
            urlencode(
                {
                    'client_id': settings.ANILIST_ID,
                    'redirect_uri': redirect_uri,
                    'response_type': 'code',
                    'state': state_token,
                }
            )
        }",
    )


@require_GET
def import_anilist_private(request):
    """View for getting the AniList OAuth2 token."""
    oauth_callback = anilist.get_token(request)
    enc_token = helpers.encrypt(oauth_callback["access_token"])
    state_token = request.GET["state"]
    username = oauth_callback["username"]

    if not username:
        messages.error(request, "AniList username is required.")
        return redirect("import_data")

    frequency = request.session[state_token]["frequency"]
    mode = request.session[state_token]["mode"]
    import_time = request.session[state_token]["time"]

    if frequency == "once":
        tasks.import_anilist.delay(
            user_id=request.user.id,
            mode=mode,
            username=username,
            token=enc_token,
        )
        messages.info(request, "AniList import queued.")
    else:
        helpers.create_import_schedule(
            username=username,
            request=request,
            mode=mode,
            frequency=frequency,
            import_time=import_time,
            source="AniList",
            token=enc_token,
        )
    return redirect("import_data")


@require_POST
def import_anilist_public(request):
    """View for importing anime and manga data from AniList."""
    username = request.POST.get("user")
    if not username:
        messages.error(request, "AniList username is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    frequency = request.POST["frequency"]
    import_time = request.POST["time"]

    if frequency == "once":
        tasks.import_anilist.delay(
            user_id=request.user.id,
            mode=mode,
            username=username,
        )
        messages.info(request, "AniList import queued.")
    else:
        helpers.create_import_schedule(
            username=username,
            request=request,
            mode=mode,
            frequency=frequency,
            import_time=import_time,
            source="AniList",
        )
    return redirect("import_data")


@require_POST
def import_kitsu(request):
    """View for importing anime and manga data from Kitsu by user ID."""
    kitsu_id = request.POST.get("user")
    if not kitsu_id:
        messages.error(request, "Kitsu user ID is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    frequency = request.POST["frequency"]

    if frequency == "once":
        tasks.import_kitsu.delay(username=kitsu_id, user_id=request.user.id, mode=mode)
        messages.info(request, "The task to import media from Kitsu has been queued.")
    else:
        import_time = request.POST["time"]
        helpers.create_import_schedule(
            kitsu_id,
            request,
            mode,
            frequency,
            import_time,
            "Kitsu",
        )
    return redirect("import_data")


@require_POST
def import_yamtrack(request):
    """View for importing anime and manga data from Yamtrack CSV."""
    file = request.FILES.get("yamtrack_csv")

    if not file:
        messages.error(request, "Yamtrack CSV file is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    tasks.import_yamtrack.delay(
        file=request.FILES["yamtrack_csv"],
        user_id=request.user.id,
        mode=mode,
    )
    messages.info(
        request,
        "The task to import media from Yamtrack CSV file has been queued.",
    )
    return redirect("import_data")


@require_POST
def import_hltb(request):
    """View for importing game date from HowLongToBeat."""
    file = request.FILES.get("hltb_csv")

    if not file:
        messages.error(request, "HowLongToBeat CSV file is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    tasks.import_hltb.delay(
        file=request.FILES["hltb_csv"],
        user_id=request.user.id,
        mode=mode,
    )
    messages.info(
        request,
        "The task to import media from HowLongToBeat CSV file has been queued.",
    )
    return redirect("import_data")


@require_POST
def import_steam(request):
    """View for importing game data from Steam."""
    steam_id = request.POST.get("user")
    if not steam_id:
        messages.error(request, "Steam ID is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    frequency = request.POST["frequency"]

    if frequency == "once":
        tasks.import_steam.delay(username=steam_id, user_id=request.user.id, mode=mode)
        messages.info(request, "The task to import media from Steam has been queued.")
    else:
        import_time = request.POST["time"]
        helpers.create_import_schedule(
            steam_id,
            request,
            mode,
            frequency,
            import_time,
            "Steam",
        )
    return redirect("import_data")


def import_imdb(request):
    """View for importing data from IMDB."""
    file = request.FILES.get("imdb_csv")

    if not file:
        messages.error(request, "IMDB CSV file is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    tasks.import_imdb.delay(
        file=request.FILES["imdb_csv"],
        user_id=request.user.id,
        mode=mode,
    )
    messages.info(
        request,
        "The task to import media from IMDB CSV file has been queued.",
    )
    return redirect("import_data")


@require_POST
def import_goodreads(request):
    """View for importing books data from GoodReads CSV."""
    file = request.FILES.get("goodreads_csv")

    if not file:
        messages.error(request, "GoodReads CSV file is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    tasks.import_goodreads.delay(
        file=request.FILES["goodreads_csv"],
        user_id=request.user.id,
        mode=mode,
    )
    messages.info(
        request,
        "The task to import media from GoodReads CSV file has been queued.",
    )
    return redirect("import_data")


@require_GET
def export_csv(request):
    """View for exporting all media data to a CSV file."""
    now = timezone.localtime()
    response = StreamingHttpResponse(
        streaming_content=exports.generate_rows(request.user),
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="yamtrack_{now}.csv"'},
    )
    logger.info("User %s started CSV export", request.user.username)
    return response


@login_not_required
@csrf_exempt
@require_POST
def jellyfin_webhook(request, token):
    """Handle Jellyfin webhook notifications for media playback."""
    try:
        user = users.models.User.objects.get(token=token)
    except ObjectDoesNotExist:
        logger.warning(
            "Could not process Jellyfin webhook: Invalid token: %s",
            token,
        )
        return HttpResponse(status=401)

    # Attach User instance so history_user_id is populated
    request.user = user
    data = request.body
    if not data:
        logger.warning("Missing payload in Jellyfin webhook request")
        return HttpResponse("Missing payload", status=400)

    payload = json.loads(data)
    processor = jellyfin.JellyfinWebhookProcessor()
    processor.process_payload(payload, user)
    return HttpResponse(status=200)


@login_not_required
@csrf_exempt
@require_POST
def plex_webhook(request, token):
    """Handle Plex webhook notifications for media playback."""
    try:
        user = users.models.User.objects.get(token=token)
    except ObjectDoesNotExist:
        logger.warning(
            "Could not process Plex webhook: Invalid token: %s",
            token,
        )
        return HttpResponse(status=401)

    # Attach User instance so history_user_id is populated
    request.user = user

    # https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks
    # As stated above, the payload is sent in JSON format inside a multipart
    # HTTP POST request. For the media.play and media.rate events, a second part of
    # the POST request contains a JPEG thumbnail for the media.

    data = request.POST.get("payload")
    if not data:
        logger.warning("Missing payload in Plex webhook request")
        return HttpResponse("Missing payload", status=400)

    payload = json.loads(data)
    processor = plex.PlexWebhookProcessor()
    processor.process_payload(payload, user)
    return HttpResponse(status=200)


@login_not_required
@csrf_exempt
@require_POST
def emby_webhook(request, token):
    """Handle Emby webhook notifications for media playback."""
    try:
        user = users.models.User.objects.get(token=token)
    except ObjectDoesNotExist:
        logger.warning(
            "Could not process Emby webhook: Invalid token: %s",
            token,
        )
        return HttpResponse(status=401)

    # Attach User instance so history_user_id is populated
    request.user = user

    # The payload is sent in JSON format inside a multipart
    # HTTP POST request.

    data = request.POST.get("data")
    if not data:
        logger.warning("Missing payload in Emby webhook request")
        return HttpResponse("Missing payload", status=400)

    payload = json.loads(data)
    processor = emby.EmbyWebhookProcessor()
    processor.process_payload(payload, user)
    return HttpResponse(status=200)



@require_GET
def senscritique_review(request):
    """Show uncertain SC matches for user validation before import."""
    import json
    pending = sc_import.get_pending_review(request.user.id)
    if not pending:
        messages.info(request, "No pending SensCritique items to review.")
        return redirect("import_data")

    # Build a global-index map before any filtering (id() works because list
    # items are the same Python dict objects in both lists).
    global_idx_map = {id(item): i for i, item in enumerate(pending)}

    # Media-type filter
    all_types = sorted({item["media_type"] for item in pending})
    media_type_filter = request.GET.get("type", "")
    if media_type_filter not in all_types:
        media_type_filter = ""

    filtered = (
        [item for item in pending if item["media_type"] == media_type_filter]
        if media_type_filter
        else pending
    )

    # Pagination over the (possibly filtered) list
    page_size = 50
    try:
        page_num = max(1, int(request.GET.get("page", 1)))
    except (ValueError, TypeError):
        page_num = 1

    total = len(filtered)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page_num = min(page_num, total_pages)
    start = (page_num - 1) * page_size
    page_items = filtered[start: start + page_size]

    # Enrich each page item with its global index and a safe JSON blob for
    # Alpine.js candidate-picker initialisation.
    pending_with_idx = [
        {
            **item,
            "_idx": global_idx_map[id(item)],
            "_cands_id": f"sc-cands-{global_idx_map[id(item)]}",
            # Safe JSON for <script type="application/json"> embedding:
            # escape <, >, & so the script tag can never be injected.
            "candidates_json": (
                json.dumps(item.get("candidates", []), ensure_ascii=False)
                .replace("&", "\\u0026")
                .replace("<", "\\u003c")
                .replace(">", "\\u003e")
            ),
        }
        for item in page_items
    ]

    # TTL notice
    ttl_seconds = sc_import.get_pending_review_ttl(request.user.id)
    ttl_days = max(1, ttl_seconds // 86400) if ttl_seconds and ttl_seconds > 0 else None

    return render(request, "users/senscritique_review.html", {
        "pending": pending_with_idx,
        "pending_count": len(pending),
        "filtered_count": total,
        "page_num": page_num,
        "total_pages": total_pages,
        "has_prev": page_num > 1,
        "has_next": page_num < total_pages,
        "mode": request.GET.get("mode", "new"),
        "all_types": all_types,
        "media_type_filter": media_type_filter,
        "ttl_days": ttl_days,
    })


@require_POST
def senscritique_confirm(request):
    """Process the user's review choices and import approved matches."""
    confirmed_indices = [int(i) for i in request.POST.getlist("confirmed")]
    mode = request.POST.get("mode", "new")
    next_page = request.POST.get("next_page") or "/"

    # Candidate-picker overrides: candidate_idx_{item_idx} -> int
    candidate_overrides: dict[int, int] = {}
    for key, val in request.POST.items():
        if key.startswith("candidate_idx_"):
            try:
                item_idx = int(key[len("candidate_idx_"):])
                candidate_overrides[item_idx] = int(val)
            except (ValueError, TypeError):
                pass

    # Manual re-search overrides: manual_media_id_{item_idx} etc.
    manual_overrides: dict[int, dict] = {}
    for key, val in request.POST.items():
        if not val:
            continue
        if key.startswith("manual_media_id_"):
            try:
                idx = int(key[len("manual_media_id_"):])
                manual_overrides.setdefault(idx, {})["media_id"] = val
            except (ValueError, TypeError):
                pass
        elif key.startswith("manual_source_"):
            try:
                idx = int(key[len("manual_source_"):])
                manual_overrides.setdefault(idx, {})["source"] = val
            except (ValueError, TypeError):
                pass
        elif key.startswith("manual_title_"):
            try:
                idx = int(key[len("manual_title_"):])
                manual_overrides.setdefault(idx, {})["title"] = val
            except (ValueError, TypeError):
                pass

    if confirmed_indices:
        tasks.confirm_senscritique.delay(
            user_id=request.user.id,
            confirmed_indices=confirmed_indices,
            mode=mode,
            candidate_overrides=candidate_overrides or None,
            manual_overrides=manual_overrides or None,
        )
        messages.info(
            request,
            f"Importing {len(confirmed_indices)} confirmed SensCritique items…",
        )
    return redirect(next_page)


@require_GET
def senscritique_search(request):
    """AJAX: search a provider for alternative matches (used by the review card)."""
    from difflib import SequenceMatcher

    from django.http import JsonResponse

    from integrations.imports.senscritique import SOURCE_FOR, _cached_search, _normalize_title
    from app.models import Sources

    media_type = request.GET.get("media_type", "").strip()
    query = request.GET.get("q", "").strip()
    # Allow the card to specify an explicit source (e.g. bnf for BD cards)
    explicit_source = request.GET.get("source", "").strip()

    if not media_type or not query:
        return JsonResponse({"candidates": []})

    source = explicit_source or SOURCE_FOR.get(media_type, "")
    if not source:
        return JsonResponse({"candidates": []})

    results = _cached_search(media_type, query, source)

    # For BD cards: if BnF returns nothing, also try ComicVine
    fallback_source = None
    if not results and source == Sources.BNF.value:
        fallback_source = Sources.COMICVINE.value
        results = _cached_search(media_type, query, fallback_source)
    actual_source = fallback_source or source

    normalized_q = _normalize_title(query)

    candidates = []
    for result in results[:5]:
        r_title = result.get("title") or ""
        similarity = SequenceMatcher(None, normalized_q, _normalize_title(r_title)).ratio()
        candidates.append({
            "media_id": str(result.get("media_id", "")),
            "title": r_title,
            "year": str(result.get("year") or result.get("release_date", "") or "")[:4],
            "image": result.get("image", ""),
            "confidence": round(similarity, 3),
            "source": actual_source,
        })

    return JsonResponse({"candidates": candidates})


@require_POST
def import_senscritique_csv(request):
    """View for importing data from SensCritique CSV export."""
    file = request.FILES.get("sc_csv")

    if not file:
        messages.error(request, "SensCritique CSV file is required.")
        return redirect("import_data")

    mode = request.POST["mode"]
    # sc_types is a list of SC type strings the user checked.
    # An empty list means "nothing selected" — treat as all types to avoid
    # silently importing nothing, but log a warning.
    raw_sc_types = request.POST.getlist("sc_types")
    allowed_sc_types = raw_sc_types if raw_sc_types else None

    tasks.import_senscritique.delay(
        file=request.FILES["sc_csv"],
        user_id=request.user.id,
        mode=mode,
        allowed_sc_types=allowed_sc_types,
    )
    messages.info(
        request,
        "The task to import media from SensCritique has been queued.",
    )
    return redirect("import_data")


def import_filmaffinity_html(request):
    """Handle FilmAffinity HTML export upload (movie-ratings.html or list-N.html)."""
    if request.method != "POST":
        return redirect("import_data")

    html_file = request.FILES.get("fa_html")
    if not html_file:
        messages.error(request, "No file provided.")
        return redirect("import_data")

    mode = request.POST.get("mode", "new")
    overwrite = mode == "overwrite"
    filename = html_file.name.lower()

    # Detect whether this is a ratings file or a list file
    if "list" in filename:
        import_type = "list"
    else:
        import_type = "ratings"

    try:
        html_content = html_file.read().decode("utf-8", errors="replace")
    except Exception:
        messages.error(request, "Could not read the file.")
        return redirect("import_data")

    from integrations.imports.filmaffinity import import_from_filmaffinity_html
    import_from_filmaffinity_html.delay(
        user_id=request.user.id,
        html_content=html_content,
        overwrite=overwrite,
        import_type=import_type,
    )
    label = "list" if import_type == "list" else "ratings"
    messages.info(request, f"FilmAffinity {label} import started. This may take a few minutes.")
    return redirect("import_data")

