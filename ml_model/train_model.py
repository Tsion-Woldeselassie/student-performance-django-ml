# Optional training script. Run locally after placing your CSV.
# Usage:
#   python ml_model/train_model.py --csv data/student_data.csv --target final_result
import argparse, pickle, os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True)
    ap.add_argument('--target', default='final_result')
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    features = ['attendance','study_hours','past_score','assignments_submitted','extracurricular']
    X = df[features]
    y = df[args.target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f'Validation Accuracy: {acc:.3f}')

    out = os.path.join(os.path.dirname(__file__), 'model.pkl')
    with open(out, 'wb') as f:
        pickle.dump(model, f)
    print('Saved model to', out)

if __name__ == '__main__':
    main()
