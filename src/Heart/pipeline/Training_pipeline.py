from src.Heart.components.Data_ingestion import DataIngestion
from src.Heart.components.Data_transformation import DataTransformation
from src.Heart.components.Model_trainer import ModelTrainer
from src.Heart.components.Model_evaluation import ModelEvaluation


def main():
    train_data_path, test_data_path = DataIngestion().initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr = data_transformation.initialize_data_transformation(
        train_data_path, test_data_path
    )

    best_model_name, _, _, _, _ = ModelTrainer().initate_model_training(train_arr, test_arr)
    ModelEvaluation().initate_model_evaluation(train_arr, test_arr, best_model_name)


if __name__ == "__main__":
    main()
