# How To Execute The Project

## Step 1: Open The Project Folder

Open a terminal or PowerShell in the project folder:

```powershell
cd "C:\Users\purushottam s\Documents\Codex\2026-05-01\build-a-project-on-e-fraud"
```

## Step 2: Check Python

Run:

```powershell
python --version
```

Python 3.10 or higher is recommended.

## Step 3: Install Requirements

This project does not need external packages. You can still run:

```powershell
pip install -r requirements.txt
```

It will not install anything extra because the project uses the Python standard library.

## Step 4: Run The Project

Run:

```powershell
python app.py
```

## Step 5: Open The Browser

Open this URL:

```text
http://127.0.0.1:8000
```

## Step 6: Use The Application

- Open Dashboard to view risk summary.
- Open Transaction Check to enter or load a sample transaction.
- Open Case Dataset to search and filter transactions.
- Open Model Study to view architecture and evaluation.

## Step 7: Run Tests

Run:

```powershell
python -m unittest discover tests
```

## Step 8: Stop The Server

Press:

```text
Ctrl + C
```

## Optional: Run With Batch File

Double-click `run_project.bat`, or run:

```powershell
.\run_project.bat
```
