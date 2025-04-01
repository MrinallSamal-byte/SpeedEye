import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
from database.db_operations import fetch_all_speed_data

MODEL_PATH = "models/model_weights/model.pkl"

def train_model():
    data = fetch_all_speed_data()
    df = pd.DataFrame(data)

    if df.empty:
        print("No data available for training.")
        return

    X = df[['speed']]  
    y = (df['speed'] > 80).astype(int)  # 1 = Speeding, 0 = Normal

    model = DecisionTreeClassifier()
    model.fit(X, y)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved.")

def predict_speeding(speed):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model.predict([[speed]])[0]  # Returns 1 if speeding, else 0

# Example Usage
if __name__ == "__main__":
    train_model()
    print("Prediction:", predict_speeding(90))  # Test prediction
