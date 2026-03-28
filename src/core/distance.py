from __future__ import annotations
from typing import Optional

def state_distance(
    s1,
    s2,
    *,
    output_length_weight: float = 1.0,
    use_cosine_placeholder: bool = False,
    cosine_similarity: Optional[float] = None,
) -> float:
    """
    Compute a simple distance between two states.

    Args:
        s1: State-like object with an 'output' attribute.
        s2: State-like object with an 'output' attribute.
        output_length_weight: Weight for output length difference.
        use_cosine_placeholder: Whether to include a cosine similarity placeholder term.
        cosine_similarity: Optional precomputed cosine similarity in [0, 1].

    Returns:
        Numeric distance (lower means more similar).
    """
    length_diff = abs(len(getattr(s1, "output", "")) - len(getattr(s2, "output", "")))
    distance = output_length_weight * float(length_diff)

    if use_cosine_placeholder:
        # Placeholder for future embedding-based similarity.
        # When embeddings are available, replace this with a real cosine similarity.
        if cosine_similarity is None:
            cosine_similarity = 0.0
        distance += 1.0 - float(cosine_similarity)
    return distance
