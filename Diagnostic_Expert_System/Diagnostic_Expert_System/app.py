import tkinter as tk
from tkinter import ttk, messagebox
import os
from pyswip import Prolog
from classifier_model import load_data_and_train, load_and_predict_risk


if not os.path.exists('risk_classifier.pkl'):
    print("Initial run detected. Training the Classification Model...")
    if not load_data_and_train():
        print("FATAL ERROR: Could not train ML model.")

try:
    prolog = Prolog()
    prolog.consult("rules.pl")
    PROLOG_READY = True
except Exception as e:
    PROLOG_READY = False
    print(f"Prolog Initialization Error. Ensure SWI-Prolog is installed correctly. Error: {e}")


def run_diagnosis():
    if not PROLOG_READY:
        messagebox.showerror(
            "Setup Error",
            "Prolog engine failed to start. Ensure SWI-Prolog is installed correctly."
        )
        return

    try:
        temp = float(temp_entry.get())
        duration = float(duration_entry.get())

        if temp < 35 or duration <= 0:
            messagebox.showerror("Input Error", "Please enter valid temperature and duration.")
            return

        risk_category = load_and_predict_risk(temp, duration)

        rc = str(risk_category).strip()
        rc_lower = rc.lower()

        risk_text.set(f"ML RISK ASSESSMENT: {rc.upper()}")

        if rc_lower == 'high':
            risk_label.config(foreground="#FF5733")  
        elif rc_lower == 'medium':
            risk_label.config(foreground="#FFC300")  
        else:
            risk_label.config(foreground="#33FF57")  


        prolog.retractall("symptom(patient,_)")

        if temp >= 39.0:
            prolog.assertz("symptom(patient, fever_high)")
        elif temp >= 37.5:
            prolog.assertz("symptom(patient, fever_low)")

        if duration >= 5:
            prolog.assertz("symptom(patient, duration_long)")
        else:
            prolog.assertz("symptom(patient, duration_short)")

        query = prolog.query("get_diagnosis(X, T)")
        result = list(query)
        query.close()

        if result:
            diagnosis = str(result[0]['X'])
            treatment = str(result[0]['T'])
            diagnosis_text.set(f"DIAGNOSIS: {diagnosis.upper()}")
            treatment_text.set(treatment)
        else:
            diagnosis_text.set("DIAGNOSIS: UNKNOWN")
            treatment_text.set("Rule base could not find a definitive diagnosis.")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
    except Exception as e:
        messagebox.showerror("System Error", f"An unexpected error occurred: {e}")




root = tk.Tk()
root.title("Expert Diagnostic System (Vityarthi Project)")
root.geometry("600x500")
root.resizable(False, False)


BG_PRIMARY = "#2C3E50"      
FG_TEXT = "#ECF0F1"         
ACCENT_BUTTON = "#3498DB"   
FIELD_BG = "#34495E"        

root.config(bg=BG_PRIMARY)
style = ttk.Style()
try:
    style.theme_create("DiagnosticTheme", parent="alt", settings={
        "TFrame": {"configure": {"background": BG_PRIMARY, "foreground": FG_TEXT}},
        "TLabel": {"configure": {"background": BG_PRIMARY, "foreground": FG_TEXT, "font": ('Arial', 10)}},


        "TEntry": {"configure": {"fieldbackground": FIELD_BG, "foreground": FG_TEXT}},

        "TButton": {
            "configure": {
                "background": ACCENT_BUTTON,
                "foreground": FG_TEXT,
                "font": ('Arial', 11, 'bold'),
                "padding": 10,
                "relief": "flat",
                "borderwidth": 0
            },
            "map": {
                "background": [("active", "#2980B9"), ("!disabled", ACCENT_BUTTON)],
                "foreground": [("active", FG_TEXT)]
            }
        }
    })
except tk.TclError:

    pass

style.theme_use("DiagnosticTheme")

main_frame = ttk.Frame(root, padding="30")
main_frame.pack(fill='both', expand=True)

ttk.Label(
    main_frame,
    text="AI Diagnostic System ",
    font=('Arial', 16, 'bold'),
    foreground="#1ABC9C"
).grid(row=0, column=0, columnspan=2, pady=(0, 20))

ttk.Label(main_frame, text="1. Body Temperature (°C):", font=('Arial', 18)).grid(
    row=1, column=0, sticky='w', padx=5, pady=8
)
temp_entry = ttk.Entry(main_frame, width=25, font=('Arial', 18))
temp_entry.insert(0, "38.5")
temp_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=8)


ttk.Label(main_frame, text="2. Symptom Duration (Days):", font=('Arial', 18)).grid(
    row=2, column=0, sticky='w', padx=5, pady=8
)
duration_entry = ttk.Entry(main_frame, width=25, font=('Arial', 18))
duration_entry.insert(0, "3")
duration_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=8)


analyze_button = ttk.Button(
    main_frame,
    text="Run AI Analysis & Diagnosis",
    command=run_diagnosis
)
analyze_button.grid(row=3, column=0, columnspan=2, pady=(25, 30), sticky='ew')


ttk.Label(
    main_frame,
    text="-- Analysis Results --",
    font=('Arial', 12, 'italic'),
    foreground="#BDC3C7"
).grid(row=4, column=0, columnspan=2, pady=(10, 5))

ttk.Label(
    main_frame,
    text="Risk Assessment (ML):",
    font=('Arial', 18, 'bold')
).grid(row=5, column=0, sticky='w', pady=(5, 0))

risk_text = tk.StringVar(value="[Awaiting Input]")
risk_label = ttk.Label(main_frame, textvariable=risk_text, font=('Arial', 15, 'bold'))
risk_label.grid(row=5, column=1, sticky='e', pady=(5, 15))


ttk.Label(
    main_frame,
    text="Prolog Diagnosis (Rules):",
    font=('Arial', 18, 'bold')
).grid(row=6, column=0, sticky='w', pady=(10, 0))

diagnosis_text = tk.StringVar(value="[Awaiting Input]")
diagnosis_label = ttk.Label(
    main_frame,
    textvariable=diagnosis_text,
    font=('Arial', 20, 'bold'),
    foreground="#E74C3C"
)
diagnosis_label.grid(row=7, column=0, columnspan=2, sticky='w', pady=(0, 10))

ttk.Label(main_frame, text="Treatment Plan:", font=('Arial', 18, 'bold')).grid(
    row=8, column=0, sticky='w', pady=(5, 0)
)

treatment_text = tk.StringVar(
    value="The treatment recommended by the expert system will appear here."
)
treatment_label = ttk.Label(
    main_frame,
    textvariable=treatment_text,
    wraplength=550,
    justify='left',
    font=('Arial', 15, 'italic')
)
treatment_label.grid(row=9, column=0, columnspan=2, sticky='we', pady=(0, 10))
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

root.mainloop()


