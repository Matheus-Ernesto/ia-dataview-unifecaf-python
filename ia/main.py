import json
import pandas as pd
import joblib
import os

# ===== Função auxiliar =====
def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


# ===== Caminhos =====
MODEL_PATH = "./weight/model.pkl"
DATA_PATH = "../dataset/output/newborn_health_monitoring_with_risk.json"
OUTPUT_PATH = "../dashboard/data.json"

# ===== Carregar modelo =====
print("[INFO] Carregando modelo...")
model = joblib.load(MODEL_PATH)
print("[INFO] Modelo carregado com sucesso!")

# ===== Carregar dados =====
print("[INFO] Lendo dados de pacientes...")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

# ===== Preparar dados =====
for paciente_id, paciente in data.items():
    info_basica = {
        "baby_id": paciente_id,
        "name": paciente.get("name"),
        "gender": paciente.get("gender"),
        "gestational_age_weeks": safe_float(paciente.get("gestational_age_weeks")),
        "birth_weight_kg": safe_float(paciente["birth"]["weight_kg"]),
        "birth_length_cm": safe_float(paciente["birth"]["length_cm"]),
        "birth_head_circumference_cm": safe_float(paciente["birth"]["head_circumference_cm"]),
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
        }
        rows.append(linha)

df = pd.DataFrame(rows)
print(f"[INFO] Dados carregados: {len(df)} registros")

# ===== Codificação (igual ao train.py) =====
df["gender_encoded"] = df["gender"].map({"Male": 1, "Female": 0}).fillna(0)

# ===== Selecionar features (mesmas do train.py) =====
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
    "gender_encoded",
]

X = df[features]

# ===== Fazer previsões =====
print("[INFO] Gerando previsões...")
df["predicted_risk_encoded"] = model.predict(X)

# Se quiser decodificar para texto (Low, Medium, High etc.), crie um mapeamento:
# Exemplo genérico, ajuste conforme o label_encoder do treino
label_map = {0: "Low", 1: "Medium", 2: "High", 3: "Unknown"}
df["predicted_risk_label"] = df["predicted_risk_encoded"].map(label_map)

# ===== Exibir resultados =====
print("\n[RESULTADOS - AMOSTRA]")
print(df[["baby_id", "date", "predicted_risk_label"]].head(10))

# ===== Salvar resultados =====
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_json(OUTPUT_PATH, orient="records", indent=4)
print(f"\n[INFO] Resultados salvos em: {OUTPUT_PATH}")
