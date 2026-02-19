from sentence_transformers import SentenceTransformer, util

# lazily-loaded transformer model; allows import to succeed in offline/no-network
_model = None

def _get_model():
    """Return a cached SentenceTransformer (loading on first call).

    If the model cannot be downloaded (e.g. no network) we catch the
    exception and return None.  Callers should handle the None case by
    falling back to a simpler matching strategy.
    """
    global _model
    if _model is not None:
        return _model
    try:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as exc:
        # warn but do not crash the import
        print("[semantic_matcher] warning: failed to load transformer model:", exc)
        _model = None
    return _model


def semantic_skill_match(user_skills, job_skills):
    matched_skills = []

    model = _get_model()
    if model is None:
        # fallback: simple case‑insensitive substring match
        lowered = [s.lower() for s in user_skills]
        for js in job_skills:
            if any(usk in js.lower() or js.lower() in usk for usk in lowered):
                matched_skills.append(js)
        return matched_skills

    # Encode user skills once
    user_embeddings = {skill: model.encode(skill, convert_to_tensor=True) for skill in user_skills}

    for job_skill in job_skills:
        job_embedding = model.encode(job_skill, convert_to_tensor=True)

        # Check if job_skill matches any user_skill
        for user_skill, user_embedding in user_embeddings.items():
            similarity = util.cos_sim(job_embedding, user_embedding)

            if similarity.item() > 0.7:
                matched_skills.append(job_skill)
                break  # Only add once per job_skill

    return matched_skills