# train_model.py
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Sample training data
data = [
    ("for i in range(5): print(i)", "No Issue"),
    ("eval(input())", "Issue Found"),  # Unsafe usage of eval
    ("print('Hello World')", "No Issue"),
    ("exec('print(hello)')", "Issue Found"),  # Unsafe usage of exec
    ("import os; os.system('rm -rf /')", "Issue Found")  # Dangerous command
]

# Split data into inputs and labels
texts, labels = zip(*data)

# Create a pipeline with CountVectorizer and Naive Bayes classifier
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# Train the model
pipeline.fit(texts, labels)

# Save the model
joblib.dump(pipeline, "simple_code_review_model.pkl")
