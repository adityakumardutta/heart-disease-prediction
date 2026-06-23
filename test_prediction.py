"""Test script to verify prediction pipeline works without errors."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.Heart.pipeline.Prediction_pipeline import CustomData, PredictPipeline

# Test with sample patient data
test_data = {
    'age': 52,
    'sex': 1,
    'cp': 0,
    'trestbps': 125,
    'chol': 212,
    'fbs': 0,
    'restecg': 1,
    'thalach': 168,
    'exang': 0,
    'oldpeak': 1.0,
    'slope': 2,
    'ca': 2,
    'thal': 3
}

print("Testing prediction pipeline...")
print(f"Input data: {test_data}")

try:
    custom_data = CustomData(**test_data)
    df = custom_data.get_data_as_dataframe()
    print(f"DataFrame created: {df.shape}")
    
    pipeline = PredictPipeline()
    result = pipeline.predict_with_details(df, patient=test_data)
    
    print("\n✅ Prediction successful!")
    print(f"Prediction: {result['prediction']}")
    print(f"Risk Percent: {result['risk_percent']}%")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Model: {result['model_name']}")
    
except Exception as e:
    print(f"\n❌ Prediction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All tests passed!")
