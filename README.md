AI-Driven Expert Medical Diagnostic System
1. Introduction
The Hybrid Expert Diagnostic System is designed to provide patients with a two-pronged medical evaluation based on two primary symptoms: body temperature and duration of symptoms. This system uniquely combines two AI paradigms:

Symbolic AI (Prolog): Used for rule-based diagnosis and generating treatment recommendations.

Machine Learning (ML): Utilized for probabilistic risk assessment (categorizing risk as Low, Medium, or High).

The primary goal is to demonstrate how logical inference (rule-based) and pattern recognition (ML) can work together in a single medical application.

2. Problem Statement
Modern diagnostics often require both data-driven risk assessments and precise clinical guidance based on expert rules. This project addresses the challenge of creating a cohesive system that:

Accepts numerical patient inputs (temperature and symptom duration).

Provides a quick, data-driven Risk Category evaluation.

Uses expert rules to deduce a conclusive diagnosis and treatment plan.

Displays findings through a user-friendly Graphical User Interface (GUI).

3. Technology Stack
Language: Python 3.x (Main Logic & GUI), Prolog (Expert Knowledge Base).

Libraries: * Tkinter: For the Graphical User Interface.

PySwip: To bridge Python and Prolog.

Scikit-learn: For the Decision Tree ML model.

Joblib: For saving/loading the trained model.

External Dependency: SWI-Prolog must be installed for the logic engine to work.

4. System Features
Input Validation: Ensures valid temperature (≥ 35°C) and duration (> 0 days).

Automated ML Training: If the model file (risk_classifier.pkl) is missing, the system trains itself using symptoms_data.csv.

Real-time Risk Prediction: Uses a Decision Tree classifier to predict risk levels.

Rule-based Diagnosis: Uses Prolog to categorize fever types (High Fever: ≥ 39°C, Long Duration: ≥ 5 days) and provide medical advice.

5. File Structure
app.py: The main GUI application.

classifier_model.py: Contains the ML model training and prediction logic.

rules.pl: The Prolog file containing medical rules and treatments.

symptoms_data.csv: Training data for the ML model.

requirements.txt: List of dependencies.

6. Future Enhancements
Integrating more complex ML models like SVM or Random Forest.

Expanding the symptom list to include cough, headache, and fatigue.

Adding "Fuzzy Logic" to Prolog for handling uncertain or partial diagnoses.

Moving from a desktop GUI to a web-based dashboard (Flask/Django)
