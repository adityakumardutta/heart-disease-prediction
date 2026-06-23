Setup and run the Heart Disease Prediction project

1) Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

Notes: `mlflow`, `xgboost`, and `catboost` are optional. The training pipeline will run without them but will skip models that require those libraries.

3) Prepare dataset

- The project expects `Notebook_Experiments/Data/heart.csv`. A small sample is included for quick verification.
- To run full training, replace that file with the original dataset (same columns as sample) or restore it via DVC if you use it.

4) Run training pipeline (creates Artifacts/Preprocessor.pkl and Artifacts/Model.pkl)

```bash
# from repository root
python -m src.Heart.pipeline.Training_pipeline
```

5) Run the web app

```bash
python app.py
# then open http://0.0.0.0:8080 or http://localhost:8080
```

6) Troubleshooting

- If you see ModuleNotFoundError for `xgboost`/`catboost`/`mlflow`, either install them (`pip install xgboost catboost mlflow`) or run training; the code now skips unavailable optional libs.
- If `Artifacts/Model.pkl` or `Artifacts/Preprocessor.pkl` are missing, run the training pipeline in step 4.

Files changed to make running smoother:
- `app.py` — casts form values to proper numeric types before prediction.
- `src/Heart/components/Data_ingestion.py` — uses `os.path.join` for dataset path and returns `(train_path, test_path)` correctly.
- `src/Heart/components/Model_trainer.py` — optional imports for `xgboost`/`catboost` and dynamic `n_neighbors` for KNN.
- `src/Heart/components/Model_evaluation.py` — optional `mlflow` logging; prints metrics when `mlflow` unavailable.
- `requirements.txt` — updated with minimal version pins and helper packages.

If you want, I can run the app and open the prediction page next.