# train_model.py
import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting the model training process")

    # Sample training data
    data = [
        ("for i in range(5): print(i)", "No Issue"),
        ("eval(input())", "Issue Found"),  # Unsafe usage of eval
        ("print('Hello World')", "No Issue"),
        ("exec('print(hello)')", "Issue Found"),  # Unsafe usage of exec
        ("import os; os.system('rm -rf /')", "Issue Found")  # Dangerous command
    ]
    logger.info("Sample training data loaded successfully")

    # Split data into inputs and labels
    texts, labels = zip(*data)
    logger.info("Data split into texts and labels")

    # Create a pipeline with CountVectorizer and Naive Bayes classifier
    logger.info("Initializing the model pipeline")
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])

    # Train the model
    logger.info("Training the model on sample data")
    pipeline.fit(texts, labels)
    logger.info("Model training complete")

    # Save the model
    model_path = "simple_code_review_model.pkl"
    joblib.dump(pipeline, model_path)
    logger.info(f"Model saved to {model_path}")


if __name__ == "__main__":
    try:
        main()
        logger.info("Model training script completed successfully")
    except Exception as e:
        logger.exception("An error occurred during the model training process")
