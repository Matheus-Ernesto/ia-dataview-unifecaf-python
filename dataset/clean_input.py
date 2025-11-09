import os
import json
import csv

# Caminhos ajustados
INFO_PATH = "info.json"  # fora da pasta dataset
INPUT_DIR = "input"
OUTPUT_DIR = "output"

def load_info():
    """Lê o info.json e retorna a lista de arquivos a processar."""
    with open(INFO_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Detecta formato automaticamente
    if isinstance(data, dict):
        if "arquivos" in data:
            return data["arquivos"]
        elif "files" in data:
            return data["files"]
        else:
            # Pode ser um dicionário único representando 1 arquivo
            return [data]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Formato de info.json inválido! Esperado: {'arquivos': [...]} ou lista direta.")      

def process_csv(file_path):
    """Organiza o CSV em um dicionário estruturado por paciente."""
    patients = {}

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            baby_id = row["baby_id"]

            if baby_id not in patients:
                patients[baby_id] = {
                    "baby_id": baby_id,
                    "name": row["name"],
                    "gender": row["gender"],
                    "gestational_age_weeks": row["gestational_age_weeks"],
                    "birth": {
                        "weight_kg": row["birth_weight_kg"],
                        "length_cm": row["birth_length_cm"],
                        "head_circumference_cm": row["birth_head_circumference_cm"]
                    },
                    "records": []
                }

            # Adiciona dados de monitoramento diário
            record = {
                "date": row["date"],
                "age_days": row["age_days"],
                "weight_kg": row["weight_kg"],
                "length_cm": row["length_cm"],
                "head_circumference_cm": row["head_circumference_cm"],
                "temperature_c": row["temperature_c"],
                "heart_rate_bpm": row["heart_rate_bpm"],
                "respiratory_rate_bpm": row["respiratory_rate_bpm"],
                "oxygen_saturation": row["oxygen_saturation"],
                "feeding_type": row["feeding_type"],
                "feeding_frequency_per_day": row["feeding_frequency_per_day"],
                "urine_output_count": row["urine_output_count"],
                "stool_count": row["stool_count"],
                "jaundice_level_mg_dl": row["jaundice_level_mg_dl"],
                "apgar_score": row["apgar_score"],
                "immunizations_done": row["immunizations_done"],
                "reflexes_normal": row["reflexes_normal"],
                "risk_level": row["risk_level"]
            }

            patients[baby_id]["records"].append(record)

    return patients


def save_output(file_name, data):
    """Salva o JSON em dataset/output."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_name)[0]}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Arquivo salvo em: {output_path}")


def main():
    files_info = load_info()

    for entry in files_info:
        # agora entry é garantido como dicionário
        file_name = entry["arquivo"]
        file_type = entry["tipo"]

        if file_type == "kaggle csv":
            file_path = os.path.join(INPUT_DIR, file_name)
            structured_data = process_csv(file_path)
            save_output(file_name, structured_data)


if __name__ == "__main__":
    main()
