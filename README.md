# Student Performance Prediction (Django + ML)

## Quick Start
```bash
cd student_performance_django_ml
python -m venv venv
# Windows: venv\Scripts\activate ; Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Train ML Model (optional)
Prepare a CSV with columns:
`attendance,study_hours,past_score,assignments_submitted,extracurricular,final_result`

Then run:
```bash
python ml_model/train_model.py --csv path/to/your.csv --target final_result
```
This will create `ml_model/model.pkl` used by the app. If not present, a heuristic fallback is used.

## Features
- Student Registration/Login/Logout
- Profile Page
- Performance Prediction form
- SQLite by default
