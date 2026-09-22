import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.callbacks import EarlyStopping


# =========================================================
# LOAD DATASET
# =========================================================

DATASET_PATH = "DATASET/real_estate_sales.csv"

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# =========================================================
# FEATURES AND TARGET
# =========================================================

features = [
    "Total_Units",
    "Average_Price_Cr",
    "Current_Leads",
    "Site_Visits",
    "Marketing_Spend_Lakh",
    "Broker_Leads",
    "Previous_Month_Bookings",
    "Avg_3_Month_Bookings",
    "Avg_6_Month_Bookings",
    "Previous_Month_Revenue_Cr"
]

target = "Bookings"

X = df[features]
y = df[target]


# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# =========================================================
# FEATURE SCALING
# =========================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# =========================================================
# BUILD NEURAL NETWORK
# =========================================================

model = Sequential([
    Input(shape=(X_train_scaled.shape[1],)),

    Dense(64, activation="relu"),
    Dense(32, activation="relu"),
    Dense(16, activation="relu"),

    Dense(1)
])


# =========================================================
# COMPILE MODEL
# =========================================================

model.compile(
    optimizer="adam",
    loss="mse",
    metrics=["mae"]
)


# =========================================================
# EARLY STOPPING
# =========================================================

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)


# =========================================================
# TRAIN MODEL
# =========================================================

print("\nTraining Neural Network...")

history = model.fit(
    X_train_scaled,
    y_train,
    validation_split=0.20,
    epochs=200,
    batch_size=4,
    callbacks=[early_stopping],
    verbose=1
)


# =========================================================
# MODEL EVALUATION
# =========================================================

predictions = model.predict(
    X_test_scaled,
    verbose=0
).flatten()

mae = mean_absolute_error(y_test, predictions)

mse = mean_squared_error(y_test, predictions)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, predictions)


print("\n========================================")
print("MODEL EVALUATION")
print("========================================")

print(f"MAE  : {mae:.2f} bookings")
print(f"MSE  : {mse:.2f}")
print(f"RMSE : {rmse:.2f} bookings")
print(f"R²   : {r2:.2f}")


# =========================================================
# SAVE MODEL
# =========================================================

MODEL_PATH = "MODEL/property_sales_model.keras"

model.save(MODEL_PATH)


# =========================================================
# SAVE SCALER
# =========================================================

SCALER_PATH = "MODEL/property_scaler.pkl"

with open(SCALER_PATH, "wb") as file:
    pickle.dump(scaler, file)


print("\n========================================")
print("TRAINING COMPLETED SUCCESSFULLY!")
print("========================================")

print(f"Model saved to: {MODEL_PATH}")
print(f"Scaler saved to: {SCALER_PATH}")