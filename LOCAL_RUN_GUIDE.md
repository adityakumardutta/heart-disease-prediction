# Local Run Guide

## Prerequisites
- Python 3.10.11 or compatible version
- pip package manager
- Git (optional, for version control)

## Step 1: Navigate to Project Directory
```bash
cd c:/Users/ADITYA/Downloads/Heart-Disease-Prediction-main/Heart-Disease-Prediction-main
```

## Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

## Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

## Step 4: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 5: Train the Model
```bash
python train.py
```

This will:
- Load the heart disease dataset
- Split into train/test sets
- Train multiple models (Logistic Regression, Random Forest, SVM, XGBoost)
- Select the best model based on ROC-AUC, F1, and accuracy
- Save the model and preprocessor to `Artifacts/` directory
- Generate evaluation metrics and charts

## Step 6: Test Prediction Pipeline
```bash
python test_prediction.py
```

This will verify the prediction pipeline works correctly with sample data.

## Step 7: Run the Flask Application

**Development Mode (with debug enabled):**
```bash
set FLASK_DEBUG=1
python app.py
```

**Production Mode:**
```bash
python app.py
```

The application will start on `http://localhost:8080`

## Step 8: Access the Application
Open your browser and navigate to:
- Home page: `http://localhost:8080`
- Dashboard: `http://localhost:8080/dashboard`
- Prediction History: `http://localhost:8080/history`

## Alternative: Using Gunicorn (Production)
```bash
gunicorn --bind 0.0.0.0:8080 --workers 4 app:app
```

## Troubleshooting

### SimpleImputer _fill_dtype Error
If you encounter this error, it means the pickle files are incompatible with your sklearn version. Solution:
```bash
# Delete old artifacts
Remove-Item Artifacts\Model.pkl -Force
Remove-Item Artifacts\Preprocessor.pkl -Force

# Retrain the model
python train.py
```

### Module Not Found Errors
Ensure you're in the correct directory and have activated the virtual environment:
```bash
cd c:/Users/ADITYA/Downloads/Heart-Disease-Prediction-main/Heart-Disease-Prediction-main
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Port Already in Use
Change the port by setting the PORT environment variable:
```bash
set PORT=5000
python app.py
```

## Quick Start (All-in-One)
```bash
cd c:/Users/ADITYA/Downloads/Heart-Disease-Prediction-main/Heart-Disease-Prediction-main
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train.py
python app.py
```
