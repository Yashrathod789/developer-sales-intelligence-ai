import numpy as np
import pickle
from tensorflow.keras.models import load_model


# ==============================
# STEP 1: LOAD TRAINED MODEL
# ==============================

model = load_model("MODEL/sales_prediction_model.keras")

print("Model loaded successfully!")


# ==============================
# STEP 2: LOAD FEATURE SCALER
# ==============================

with open("MODEL/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

print("Scaler loaded successfully!")


# ==============================
# STEP 3: SAMPLE INPUT
# ==============================

sample_data = np.array([[
    1,      # Store
    1,      # DayOfWeek
    1,      # Open
    1,      # Promo
    0,      # SchoolHoliday
    2015,   # Year
    6,      # Month
    15,     # Day
    25,     # WeekOfYear
    1,      # StateHoliday_0
    0,      # StateHoliday_a
    0,      # StateHoliday_b
    0       # StateHoliday_c
]])


# ==============================
# STEP 4: SCALE INPUT
# ==============================

sample_scaled = scaler.transform(sample_data)


# ==============================
# STEP 5: MAKE PREDICTION
# ==============================

prediction = model.predict(
    sample_scaled,
    verbose=0
)


# ==============================
# STEP 6: DISPLAY RESULT
# ==============================

predicted_sales = float(prediction[0][0])

print("\n==============================")
print("SALES PREDICTION")
print("==============================")

print("Predicted Sales:", round(predicted_sales, 2))
