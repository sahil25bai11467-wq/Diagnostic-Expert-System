/*  rules.pl
    Simple rule base for the Diagnostic Expert System.

    Python side asserts facts like:
        symptom(patient, fever_high).
        symptom(patient, duration_long).

    Then calls:
        get_diagnosis(X, T).

    where:
        X = diagnosis atom
        T = recommended treatment text
*/

:- dynamic symptom/2.
% We only modify symptom/2 from Python.
% diagnosis/1 and treatment/2 are static rules/facts.


/* ------------------------------------------------------------------
   DIAGNOSIS RULES
   ------------------------------------------------------------------
   These rules decide a diagnosis/1 based on the presence of
   symptom(patient, fever_high/fever_low) and
   symptom(patient, duration_long/duration_short).
------------------------------------------------------------------ */

% Very high fever and long-lasting symptoms → severe infection
diagnosis(severe_infection) :-
    symptom(patient, fever_high),
    symptom(patient, duration_long).

% High fever but short duration → acute infection (emerging)
diagnosis(acute_infection) :-
    symptom(patient, fever_high),
    symptom(patient, duration_short).

% Low-grade fever and short duration → mild viral fever
diagnosis(mild_viral_fever) :-
    symptom(patient, fever_low),
    symptom(patient, duration_short).

% Low-grade fever but persisting → prolonged viral/secondary infection
diagnosis(prolonged_fever) :-
    symptom(patient, fever_low),
    symptom(patient, duration_long).

% No fever facts asserted (e.g., temp < 37.5 in Python side)
% → no clear diagnosis from this simple rule base
diagnosis(no_clear_diagnosis) :-
    \+ symptom(patient, fever_high),
    \+ symptom(patient, fever_low).


/* ------------------------------------------------------------------
   TREATMENT RECOMMENDATIONS
   ------------------------------------------------------------------
   treatment(Diagnosis, PlanText).

   PlanText is an atom (single-quoted string). In Python, pyswip
   will give you this as an Atom, and str(Atom) will be the text.
------------------------------------------------------------------ */

treatment(severe_infection,
  'High risk: seek immediate medical attention. Visit a hospital or emergency department as soon as possible. Do not self-medicate without consulting a doctor.'
).

treatment(acute_infection,
  'Moderate risk: rest, maintain hydration, and monitor temperature every 4–6 hours. Consider paracetamol as per medical advice. If symptoms worsen or persist beyond 3 days, consult a doctor.'
).

treatment(mild_viral_fever,
  'Low to medium risk: drink plenty of fluids, rest, and use light fever reducers if prescribed. Monitor symptoms; if new symptoms appear or fever persists, seek medical advice.'
).

treatment(prolonged_fever,
  'Ongoing fever: schedule a clinical evaluation and basic lab tests (CBC, etc.) as recommended by a doctor. Continue hydration and avoid overuse of antipyretics without supervision.'
).

treatment(no_clear_diagnosis,
  'No clear rule-based diagnosis. Recheck temperature and duration, monitor symptoms, and consult a healthcare professional if you feel unwell.'
).


/* ------------------------------------------------------------------
   MAIN ENTRY POINT FOR PYTHON
   ------------------------------------------------------------------
   get_diagnosis(Diagnosis, TreatmentText) is what your Python code
   calls via:

       prolog.query("get_diagnosis(X, T)")

   X will be bound to Diagnosis, T to TreatmentText.
------------------------------------------------------------------ */

get_diagnosis(Diagnosis, TreatmentText) :-
    diagnosis(Diagnosis),
    treatment(Diagnosis, TreatmentText).

