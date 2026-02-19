from sentence_transformers import SentenceTransformer, util

# lazily-loaded transformer model; allows import to succeed in offline/no-network
_model = None


def _get_model():
    """Return a cached SentenceTransformer (loading on first call).

    If the model is unavailable locally we fall back to a simpler matcher
    instead of blocking the UI trying to download at runtime.
    """
    global _model
    if _model is not None:
        return _model
    try:
        _model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
    except Exception as exc:
        print("[semantic_matcher] warning: failed to load transformer model:", exc)
        _model = None
    return _model


def semantic_skill_match(user_skills, job_skills):
    model = _get_model()
    if model is None:
        matched_skills = []
        lowered = [s.lower() for s in user_skills]
        for js in job_skills:
            if any(usk in js.lower() or js.lower() in usk for usk in lowered):
                matched_skills.append(js)
        return matched_skills

    if not user_skills or not job_skills:
        return []

    # Batch embeddings + matrix cosine similarity for speed.
    user_embeddings = model.encode(user_skills, convert_to_tensor=True)
    job_embeddings = model.encode(job_skills, convert_to_tensor=True)
    similarity = util.cos_sim(job_embeddings, user_embeddings)
    best_scores = similarity.max(dim=1).values

    return [js for js, score in zip(job_skills, best_scores) if score.item() > 0.7]
