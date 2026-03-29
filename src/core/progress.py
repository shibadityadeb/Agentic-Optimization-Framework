import numpy as np
from functools import lru_cache

# STEP 2: Define goal description
GOAL_DESCRIPTION = "structured stock analysis including trends, risks, insights, and final recommendation"

# STEP 3: Embedding + cosine similarity
def get_shared_vocab(text):
    words = set(text.lower().split()) | set(GOAL_DESCRIPTION.lower().split())
    return sorted(words)
def get_embedding(text, vocab=None):
    if vocab is None:
        vocab = get_shared_vocab(text)
    vec = np.zeros(len(vocab))
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    for w in text.lower().split():
        if w in word_to_idx:
            vec[word_to_idx[w]] += 1
    return vec
def get_similarity(text1, text2):
    vocab = get_shared_vocab(text1 + ' ' + text2)
    emb1 = get_embedding(text1, vocab)
    emb2 = get_embedding(text2, vocab)
    print("EMB1 LEN:", len(emb1), "EMB2 LEN:", len(emb2))
    if np.linalg.norm(emb1) == 0 or np.linalg.norm(emb2) == 0:
        print("Zero norm embedding, fallback to 0.0")
        return 0.0
    sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    if sim is None or np.isnan(sim):
        print("NaN similarity, fallback to 0.0")
        return 0.0
    sim = max(0.0, min(1.0, sim))
    print("SIMILARITY:", sim)
    return sim

# STEP 5: Cache goal embedding
@lru_cache(maxsize=1)
def get_goal_embedding():
    return get_embedding(GOAL_DESCRIPTION)
# STEP 4: Hybrid progress function
def compute_progress(state):
    # Diagnostic: confirm function call
    with open('progress_debug.txt', 'a') as f:
        f.write('CALLED compute_progress\n')
    print("=== ENTERED compute_progress ===")
    output = state.output or ""
    print("RAW OUTPUT REPR:", repr(output))
    # Normalize whitespace and lowercase
    lines = [line.strip().lower() for line in output.splitlines() if line.strip()]
    print("OUTPUT LINES:", lines)
    score = 0
    found = set()
    for line in lines:
        print("LINE:", repr(line))
        if "analysis" in line:
            print("Detected 'analysis' in line")
            found.add('analysis')
        if "trends" in line:
            print("Detected 'trends' in line")
            found.add('trends')
        if "risks" in line or "risk" in line:
            print("Detected 'risks' in line")
            found.add('risks')
        if "final recommendation" in line or "recommendation" in line:
            print("Detected 'recommendation' in line")
            found.add('recommendation')
    # Fallback: check for keywords anywhere in output
    out_lower = output.lower()
    if 'analysis' not in found and 'analysis' in out_lower:
        print("Fallback found 'analysis' in output")
        found.add('analysis')
    if 'trends' not in found and 'trends' in out_lower:
        print("Fallback found 'trends' in output")
        found.add('trends')
    if 'risks' not in found and ('risks' in out_lower or 'risk' in out_lower):
        print("Fallback found 'risks' in output")
        found.add('risks')
    if 'recommendation' not in found and 'recommendation' in out_lower:
        print("Fallback found 'recommendation' in output")
        found.add('recommendation')
    # Calculate score using the final found set
    score = 0
    if 'analysis' in found:
        score += 0.3
    if 'trends' in found:
        score += 0.3
    if 'risks' in found:
        score += 0.2
    if 'recommendation' in found:
        score += 0.4
    progress = min(score, 1.0)
    # Write debug info to file for workflow visibility (after all detection)
    with open('progress_debug.txt', 'a') as f:
        f.write('OUTPUT: ' + repr(output) + '\n')
        f.write('FOUND SECTIONS: ' + repr(found) + '\n')
        f.write('PROGRESS: ' + str(progress) + '\n')
        return progress
    out_lower = output.lower()
    if 'analysis' not in found and 'analysis' in out_lower:
        print("Fallback found 'analysis' in output")
        found.add('analysis')
    if 'trends' not in found and 'trends' in out_lower:
        print("Fallback found 'trends' in output")
        found.add('trends')
    if 'risks' not in found and ('risks' in out_lower or 'risk' in out_lower):
        print("Fallback found 'risks' in output")
        found.add('risks')
    if 'recommendation' not in found and 'recommendation' in out_lower:
        print("Fallback found 'recommendation' in output")
        found.add('recommendation')
    print("FOUND SECTIONS (final):", found)
    print("PROGRESS (final):", min(score, 1.0))
    score = 0
    if 'analysis' in found:
        score += 0.3
    if 'trends' in found:
        score += 0.3
    if 'risks' in found:
        score += 0.2
    if 'recommendation' in found:
        score += 0.4
    progress = min(score, 1.0)
    print("PROGRESS:", progress)
    return progress

GOAL_DESCRIPTION = "final structured analysis with conclusion and recommendation"

def get_shared_vocab(text):
    # Build a shared vocabulary from both goal and current text
    words = set(text.lower().split()) | set(GOAL_DESCRIPTION.lower().split())
    return sorted(words)

def get_embedding(text, vocab=None):
    # Use provided vocab or build from text+goal
    if vocab is None:
        vocab = get_shared_vocab(text)
    vec = np.zeros(len(vocab))
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    for w in text.lower().split():
        if w in word_to_idx:
            vec[word_to_idx[w]] += 1
    return vec

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def get_goal_embedding(vocab):
    return get_embedding(GOAL_DESCRIPTION, vocab)

