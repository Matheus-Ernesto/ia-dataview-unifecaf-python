import os
import json
import pandas as pd

# Caminhos base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
INFO_PATH = os.path.join(BASE_DIR, "info.json")

def detectar_tipo(arquivo):
    """Detecta o tipo do arquivo baseado na extensão ou nome."""
    nome = arquivo.lower()
    if nome.endswith(".csv"):
        if "kaggle" in nome or "health" in nome:
            return "kaggle csv"
        return "csv"
    elif nome.endswith(".json"):
        return "json"
    elif nome.endswith(".xlsx") or nome.endswith(".xls"):
        return "excel"
    elif nome.endswith(".parquet"):
        return "parquet"
    else:
        return "desconhecido"

def contar_linhas(caminho, tipo):
    """Conta o número de linhas do arquivo (para CSV e texto)."""
    try:
        if tipo.endswith("csv"):
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f) - 1  # menos o cabeçalho
        elif tipo == "json":
            data = json.load(open(caminho, "r", encoding="utf-8"))
            if isinstance(data, list):
                return len(data)
            return 1
        elif tipo == "excel":
            df = pd.read_excel(caminho, nrows=5)
            return len(df)  # lê só algumas linhas
    except Exception as e:
        print(f"[!] Erro ao contar linhas de {caminho}: {e}")
    return None

def gerar_info():
    arquivos = os.listdir(INPUT_DIR)
    info_lista = []

    for idx, arquivo in enumerate(arquivos):
        caminho = os.path.join(INPUT_DIR, arquivo)
        if not os.path.isfile(caminho):
            continue

        tipo = detectar_tipo(arquivo)
        tamanho_kb = round(os.path.getsize(caminho) / 1024, 2)
        linhas = contar_linhas(caminho, tipo)

        info_lista.append({
            "id": idx,
            "arquivo": arquivo,
            "tipo": tipo,
            "tamanho_kb": tamanho_kb,
            "linhas": linhas
        })

    info_data = {"arquivos": info_lista}

    with open(INFO_PATH, "w", encoding="utf-8") as f:
        json.dump(info_data, f, indent=4, ensure_ascii=False)

    print(f"[OK] info.json atualizado com {len(info_lista)} arquivo(s).")

if __name__ == "__main__":
    gerar_info()
