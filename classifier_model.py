import csv
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

RISK_MAPPING = {'Low': 0, 'Medium': 1, 'High': 2}
REVERSE_RISK_MAPPING = {0: 'Low', 1: 'Medium', 2: 'High'}

def load_data_and_train(filepath='symptoms_data.csv'):
    """Loads CSV data using the built-in CSV module and trains the ML model."""
    if not os.path.exists(filepath):
        return False
    
    X = [] 
    y = [] 
    
    with open(filepath, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        
        for row in reader:
            try:
                temp = float(row[0])
                duration = float(row[1])
                risk = row[2]
                
                X.append([temp, duration])
                y.append(RISK_MAPPING[risk])
            except: 
                continue
                
    X = np.array(X)
    y = np.array(y)
    
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)
    joblib.dump(model, 'risk_classifier.pkl')
    return True

def load_and_predict_risk(temp, duration):

    try:
        model = joblib.load('risk_classifier.pkl')
        input_data = np.array([[temp, duration]])
        prediction_numerical = model.predict(input_data)
        return REVERSE_RISK_MAPPING[prediction_numerical[0]]
    except FileNotFoundError:
        return "ERROR: Model not trained."
    except Exception as e:
        return f"Prediction Error: {e}"

if __name__ == '__main__':
    load_data_and_train()
    print(f"Test Prediction (39.0 C, 5 days): {load_and_predict_risk(39.0, 5)}")
