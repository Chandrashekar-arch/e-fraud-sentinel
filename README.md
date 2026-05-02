# e-fraud-sentinel
E-Fraud Sentinel
E-Fraud Sentinel is a Python-based E-fraud detection project for online payment transactions. It includes a clean web dashboard, transaction risk checker, case dataset, explainable scoring model, tests, project report, and PowerPoint presentation.

Main Features
Python fraud scoring engine.
Browser dashboard served by Python.
Transaction risk checker with live form input.
Synthetic fraud dataset for study and demonstration.
Risk categories: Low, Watch, High, Critical.
Explainable evidence for every fraud score.
Review queue for suspicious transactions.
Sample evaluation with accuracy, precision, recall, and confusion matrix.
No external Python packages required.
Project Structure
E-Fraud Sentinel/
  app.py
  fraud_detector/
    __init__.py
    models.py
    sample_data.py
    scoring.py
    web.py
  data/
    sample_transactions.csv
  tests/
    test_scoring.py
  presentation/
    E-Fraud-Sentinel-Presentation.pptx
  PROJECT_REPORT.md
  EXECUTION_STEPS.md
  requirements.txt
  run_project.bat
How To Run
python app.py
Then open:

http://127.0.0.1:8000
Risk Levels
Score	Level	Decision
0-34	Low	Approve with monitoring
35-54	Watch	Step-up authentication
55-74	High	Manual review required
75-100	Critical	Block and escalate
Detection Signals
The Python model uses these signals:

Amount
Hour
Payment method
Channel
Device age
Account age
Email age
Failed logins
24-hour transaction velocity
Merchant risk index
IP reputation index
Shipping distance
Chargeback history
Country mismatch
Card country match
Testing
python -m unittest discover tests
Presentation
The final PowerPoint file is saved in the presentation folder.
