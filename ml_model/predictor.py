import pickle, os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

_model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        _model = pickle.load(f)

def predict_performance(features):
    """features = [attendance, study_hours, past_score, assignments_submitted, extracurricular]"""
    if _model is None:
        # default heuristic if model isn't trained yet
        attendance, study_hours, past_score, assignments_submitted, extracurricular = features
        score = 0.4*attendance + 0.3*past_score + 0.2*study_hours + 0.05*assignments_submitted + 0.05*extracurricular*10
        label = 'Pass' if score >= 50 else 'Fail'
        prob = min(max((score/100), 0), 1)
        return label, prob
    pred = _model.predict([features])[0]
    if hasattr(_model, 'predict_proba'):
        prob = float(_model.predict_proba([features]).max())
    else:
        prob = 0.7
    return str(pred), prob
