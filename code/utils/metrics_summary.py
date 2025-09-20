import os
import time
import pandas as pd

BASE_DIR = "../ck_output"
CSV_NAME = "class.csv"
TARGET_COLS = ["cbo", "dit", "loc", "lcom"]

results = []

start_time = time.time()

for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)
    
    if not os.path.isdir(folder_path):
        continue
    
    csv_path = os.path.join(folder_path, CSV_NAME)
    
    if not os.path.exists(csv_path):
        print(f"[AVISO] CSV não encontrado em: {folder}")
        continue
    
    try:
        df = pd.read_csv(csv_path)
        
        # Normaliza os nomes das colunas para evitar problemas de maiúscula/minúscula
        df.columns = df.columns.str.strip().str.lower()
        
        # Verifica se as colunas existem
        if not all(col in df.columns for col in TARGET_COLS):
            print(f"[AVISO] Colunas faltando no CSV de {folder}")
            continue
        
        # Se o CSV está vazio ou só tem valores nulos, pula
        if df.empty or df[TARGET_COLS].dropna(how="all").empty:
            print(f"[AVISO] CSV vazio em {folder}")
            continue
        
        # Calcula as médias, medianas, desvios padrão, mínimos e máximos
        stats = {}
        for col in TARGET_COLS:
            stats[f"{col}_mean"] = df[col].mean()
            stats[f"{col}_median"] = df[col].median()
            stats[f"{col}_std"] = df[col].std()
            stats[f"{col}_min"] = df[col].min()
            stats[f"{col}_max"] = df[col].max()
        
        results.append({
            "repository": folder,
            **stats
        })
    except Exception as e:
        print(f"[ERRO] Falha ao processar {folder}: {e}")

df_results = pd.DataFrame(results)

df_results.dropna(how="all", inplace=True)

print(df_results)

df_results.to_csv("../results.csv", index=False)
print("\n✅ Arquivo 'results.csv' gerado com sucesso!")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo total de execução: {elapsed_time:.2f} segundos")