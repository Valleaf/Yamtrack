"""Helpers for deriving curated lists from verified award fixtures."""

from app.awards_data import AWARDS


def list_from_award(
    award_slug,
    *,
    slug,
    name=None,
    icon=None,
    source_url=None,
    limit=None,
):
    """Build a ranked list from one award's already-verified winners.

    Keeping this conversion in one place prevents award and list snapshots from
    drifting when the same winners are exposed in both statistics sections.
    The award fixture remains the source of truth for provider IDs and order.
    """
    award = next((entry for entry in AWARDS if entry["slug"] == award_slug), None)
    if award is None:
        raise ValueError(f"Unknown award fixture: {award_slug}")

    id_key = f"{award['source']}_id"
    winners = [winner for winner in award["winners"] if winner.get(id_key)]
    if limit is not None:
        winners = winners[:limit]

    result = {
        "slug": slug,
        "name": name or award["name"],
        "icon": icon or award["icon"],
        "media_type": award["media_type"],
        "source": award["source"],
        "items": [
            {"rank": rank, id_key: winner[id_key]}
            for rank, winner in enumerate(winners, start=1)
        ],
    }
    if source_url:
        result["source_url"] = source_url
    return result
