import os
import numpy as np
import openai
from functools import lru_cache

openai.api_key = os.getenv("OPENAI_API_KEY")

GOAL_DESCRIPTION = "final structured analysis with conclusion and recommendation"

@lru_cache(maxsize=2)
def get_embedding(text):
    response = openai.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding)

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

@lru_cache(maxsize=1)
def get_goal_embedding():
    return get_embedding(GOAL_DESCRIPTION)

def compute_progress(state):
    output = getattr(state, 'output', '')
    if not output:
        return 0.0
    output_embedding = get_embedding(output)
    goal_embedding = get_goal_embedding()
    similarity = cosine_similarity(output_embedding, goal_embedding)
    return similarity
