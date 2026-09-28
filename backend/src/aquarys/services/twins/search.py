"""Twin search service using vector embeddings and structured scoring."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.models import StreamEmbedding, StreamProfile, StreamSimilarity
from aquarys.services.twins.scoring import calculate_twin_similarity


async def search_twins(
    db: AsyncSession,
    target_site_id: str,
    limit: int = 5,
    min_similarity: float = 0.5,
) -> list[StreamSimilarity]:
    """Find ecological twins for a target site."""

    # Get target profile and embedding
    target_prof_res = await db.execute(
        select(StreamProfile).where(StreamProfile.site_id == target_site_id)
    )
    target_profile = target_prof_res.scalar_one_or_none()

    target_emb_res = await db.execute(
        select(StreamEmbedding).where(StreamEmbedding.site_id == target_site_id)
    )
    target_embedding = target_emb_res.scalar_one_or_none()

    if not target_profile or not target_embedding:
        return []

    # Get all other profiles and embeddings
    # In a real system with pgvector, we'd use embedding.vector.l2_distance() in the SQL query.
    # For DB-agnostic support (sqlite for dev), we do a full scan or simple heuristic.
    # # ponytail: naive full scan in memory, add pgvector KNN query when scale demands it.

    profiles_res = await db.execute(
        select(StreamProfile).where(StreamProfile.site_id != target_site_id)
    )
    other_profiles = {p.site_id: p for p in profiles_res.scalars().all()}

    embeddings_res = await db.execute(
        select(StreamEmbedding).where(StreamEmbedding.site_id != target_site_id)
    )
    other_embeddings = {e.site_id: e for e in embeddings_res.scalars().all()}

    results = []

    for site_id, other_prof in other_profiles.items():
        other_emb = other_embeddings.get(site_id)
        if not other_emb:
            continue

        sim = calculate_twin_similarity(
            site_a_id=target_site_id,
            profile_a=target_profile,
            vector_a=target_embedding.vector,
            site_b_id=site_id,
            profile_b=other_prof,
            vector_b=other_emb.vector,
        )

        # always include candidate; min_similarity filter applied later via slicing
        results.append(sim)

    filtered = [r for r in results if r.overall_similarity >= min_similarity]
    # Sort by overall similarity descending
    filtered.sort(key=lambda x: x.overall_similarity, reverse=True)
    return filtered[:limit]
