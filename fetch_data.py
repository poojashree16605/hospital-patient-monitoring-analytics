import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import matplotlib.pyplot as plt

# Load Firebase key
cred = credentials.Certificate("firebase_key.json")

# Initialize Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://safe-drip-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Fetch data
ref = db.reference('safe_drip')
data = ref.get()

print("Raw Data:", data)

# Convert to DataFrame
records = []

for device_id, device_data in data.items():
    live = device_data.get("live", {})
    
    health = live.get("health", {})
    iv = live.get("iv", {})
    
    records.append({
        "device_id": device_id,
        "heart_rate": health.get("heartRate"),
        "spo2": health.get("spo2"),
        "flow_rate": iv.get("current_flow_rate_ml_per_min"),
        "remaining_ml": iv.get("remaining_ml")
    })

df = pd.DataFrame(records)

print("\nDataFrame:\n", df.head())

# Handle missing values
df = df.fillna(0)

# Create Status Column
def get_status(row):
    if row["heart_rate"] == 0 and row["spo2"] == 0:
        return "No Data"
    elif row["spo2"] < 90:
        return "Critical"
    else:
        return "Normal"

df["status"] = df.apply(get_status, axis=1)

# Create Alert Column
def alert(row):
    if row["heart_rate"] == 0 and row["spo2"] == 0:
        return "⚠ No Signal"
    elif row["spo2"] < 90:
        return "⚠ Low Oxygen"
    elif row["remaining_ml"] < 50:
        return "⚠ Low IV"
    else:
        return "Normal"

df["alert"] = df.apply(alert, axis=1)

print("\nFinal Data:\n", df.head())

# Analysis
print("\nStatus Count:\n", df["status"].value_counts())
print("\nAverage Heart Rate:", df["heart_rate"].mean())
print("\nAverage SpO2:", df["spo2"].mean())

# Visualization
df["status"].value_counts().plot(kind="bar")
plt.title("Patient Status Distribution")
plt.xlabel("Status")
plt.ylabel("Count")
plt.show(block=False)
plt.pause(3)
plt.close()

# Export for Power BI
df.to_csv("final_data.csv", index=False)

print("\nCSV file exported successfully ✅")