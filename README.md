# Student Performance Prediction System
### Django + Machine Learning

**Tsion Woldeselassie**  
### B.S. Data Science with Biology Concentration (Honors) — University of Texas at Arlington  
### M.S. Applied Statistics and Data Science — University of Texas at Arlington
---

## Why I Built This

During my time as a Student Tutor and a Physics Learning Assistant, I noticed that students fall behind not because they lacked ability, but because there was no early signal to alert educators or the students themselves that intervention was needed. I wanted to combine machine learning with a real web application to create a tool that could help identify at-risk students proactively before they fail, not after.

---

## What It Does

This is a full-stack web application that predicts a student's academic performance based on behavioral and academic indicators. Students enter data about their attendance, study habits, past scores, assignment completion, and extracurricular involvement and the system returns a predicted performance grade along with a probability score.

- **Students** can register, log in, submit academic data, receive predictions, and track their performance history over time through visual dashboards
- **Administrators** can manage student profiles, courses, and monitor all prediction results across the platform
- **Prediction history** is saved per student so trends can be monitored over time
- **Role-based authentication** ensures students and admins have separate, secure access

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Machine Learning | scikit-learn, pandas, NumPy |
| Model Serialization | joblib |
| Frontend | HTML5, CSS3, Bootstrap / Bulma |
| Database | SQLite (default) |
| Visualization | matplotlib |

---

## ML Model

The prediction model uses classification algorithms — Logistic Regression, Decision Tree, and Random Forest — trained on student academic data. The best performing model is serialized with joblib and loaded at runtime when a student submits the prediction form.

**Features used for prediction:**
- Attendance (%)
- Study Hours per week
- Past Score (%)
- Assignments Submitted
- Extracurricular Activity Score

**Output:** Predicted performance grade — Excellent, Good, Average, or Poor — along with a confidence probability score.

---

## Getting Started

### Requirements
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Tsion-Woldeselassie/student-performance-django-ml.git
cd student-performance-django-ml

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create an admin account
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

Then open your browser and go to: **http://127.0.0.1:8000/**

---

## Train the ML Model (Optional)

To retrain the model on your own dataset, prepare a CSV file with these columns:

```
attendance, study_hours, past_score, assignments_submitted, extracurricular, final_result
```

Then run:

```bash
python ml_model/train_model.py --csv path/to/your_data.csv --target final_result
```

This generates `ml_model/model.pkl` which the app loads automatically. If no model file is present, the system falls back to a heuristic-based prediction.

---

## Project Structure

```
student_performance_django_ml/
├── custom_admin/        # Admin panel app (manage students, courses, predictions)
├── students/            # Student app (registration, login, prediction, profile)
├── ml_model/            # Machine learning model training and prediction logic
├── student_performance/ # Django project settings and URL configuration
├── templates/           # Shared base templates (home page, base layout)
├── static/              # Static files (CSS, JS, images)
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

---

## Future Improvements

This project is a starting point. The features I most want to add are:

- Integration with real Learning Management Systems (LMS) like Canvas or Moodle to pull live data instead of manual entry
- Personalized study recommendations generated from prediction results not just a grade, but actionable next steps
- Early alert system that notifies instructors when a student's predicted outcome drops below a threshold
- Deep learning models for capturing longer-term academic trends
- Mobile app so students can access their data anywhere

---

## Connect

I'm passionate about using data science to solve problems in education and public health. If you're working on something similar or want to collaborate, feel free to reach out.

- LinkedIn: linkedin.com/in/tsion-woldeselassie
