import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

print("[INFO] Lendo dados do JSON...")

# Caminho do arquivo
DATA_PATH = "../dataset/output/newborn_health_monitoring_with_risk.json"
WEIGHT_PATH = "./weight/model.pkl"

# --- Leitura dos dados ---

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

# --- Estruturação dos dados ---
for paciente_id, paciente in data.items():
    info_basica = {
        "baby_id": paciente_id,
        "name": paciente.get("name"),
        "gender": paciente.get("gender"),
        "gestational_age_weeks": float(paciente.get("gestational_age_weeks", 0)),
        "birth_weight_kg": float(paciente["birth"].get("weight_kg", 0)),
        "birth_length_cm": float(paciente["birth"].get("length_cm", 0)),
        "birth_head_circumference_cm": float(paciente["birth"].get("head_circumference_cm", 0)),
    }

    for rec in paciente.get("records", []):
        linha = {
            **info_basica,
            "date": rec.get("date"),
            "age_days": safe_float(rec.get("age_days")),
            "weight_kg": safe_float(rec.get("weight_kg")),
            "length_cm": safe_float(rec.get("length_cm")),
            "head_circumference_cm": safe_float(rec.get("head_circumference_cm")),
            "temperature_c": safe_float(rec.get("temperature_c")),
            "heart_rate_bpm": safe_float(rec.get("heart_rate_bpm")),
            "respiratory_rate_bpm": safe_float(rec.get("respiratory_rate_bpm")),
            "oxygen_saturation": safe_float(rec.get("oxygen_saturation")),
            "feeding_frequency_per_day": safe_float(rec.get("feeding_frequency_per_day")),
            "urine_output_count": safe_float(rec.get("urine_output_count")),
            "stool_count": safe_float(rec.get("stool_count")),
            "jaundice_level_mg_dl": safe_float(rec.get("jaundice_level_mg_dl")),
            "apgar_score": safe_float(rec.get("apgar_score")),
            "risk_level": rec.get("risk_level", paciente.get("risk_level", "Unknown"))
        }
        rows.append(linha)

# --- Criação do DataFrame ---
df = pd.DataFrame(rows)
print(f"[INFO] Dados carregados: {df.shape[0]} registros")

# --- Pré-processamento ---
df = df.dropna(subset=["risk_level"])
label_encoder = LabelEncoder()
df["risk_level_encoded"] = label_encoder.fit_transform(df["risk_level"])
df["gender_encoded"] = label_encoder.fit_transform(df["gender"])

features = [
    "gestational_age_weeks",
    "birth_weight_kg",
    "birth_length_cm",
    "birth_head_circumference_cm",
    "age_days",
    "weight_kg",
    "length_cm",
    "head_circumference_cm",
    "temperature_c",
    "heart_rate_bpm",
    "respiratory_rate_bpm",
    "oxygen_saturation",
    "feeding_frequency_per_day",
    "urine_output_count",
    "stool_count",
    "jaundice_level_mg_dl",
    "apgar_score",
    "gender_encoded"
]

X = df[features]
y = df["risk_level_encoded"]

# --- Divisão treino/teste ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Treinamento ---
print("[INFO] Treinando modelo...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Avaliação ---
y_pred = model.predict(X_test)
print("[INFO] Avaliação do modelo:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# --- Salvando modelo ---
os.makedirs(os.path.dirname(WEIGHT_PATH), exist_ok=True)
joblib.dump(model, WEIGHT_PATH)
print(f"[INFO] Modelo salvo em: {WEIGHT_PATH}")
