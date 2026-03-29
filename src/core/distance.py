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
    # Simulate more meaningful distance: use word-level difference
    out1 = getattr(s1, "output", "")
    out2 = getattr(s2, "output", "")
    words1 = set(out1.split())
    words2 = set(out2.split())
    word_diff = len(words1.symmetric_difference(words2))
    length_diff = abs(len(out1) - len(out2))
    # Weighted sum: word diff dominates, length diff secondary
    distance = output_length_weight * (0.7 * word_diff + 0.3 * (length_diff / 10))
    if use_cosine_placeholder:
        if cosine_similarity is None:
            cosine_similarity = 0.0
        distance += 1.0 - float(cosine_similarity)
    return distance
