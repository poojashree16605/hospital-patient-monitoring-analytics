import pandas as pd
import random

data = []

for i in range(200):
    heart = random.randint(60,120)
    spo2 = random.randint(85,100)
    iv = random.randint(10,100)

    # Status logic
    if heart == 0 and spo2 == 0:
        status = "No Data"
    elif spo2 < 90:
        status = "Critical"
    else:
        status = "Normal"

    # Alert logic
    if spo2 < 90:
        alert = "Low Oxygen"
    elif iv < 20:
        alert = "Low IV"
    elif heart > 110:
        alert = "High Heart Rate"
    else:
        alert = "Normal"

    data.append([f"P{i+1}", heart, spo2, iv, status, alert])

df = pd.DataFrame(data, columns=[
    "patient_id","heart_rate","spo2","iv_level","status","alert"
])

df.to_csv("hospital_data.csv", index=False)

print("Dataset created successfully ✅")