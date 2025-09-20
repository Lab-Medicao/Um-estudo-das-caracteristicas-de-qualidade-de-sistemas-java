import os
import time
import pandas as pd

BASE_DIR = "ck_output"
CSV_NAME = "class.csv"
TARGET_COLS = ["cbo", "dit", "loc"]

resultados = []

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
        
        # Calcula as médias
        medias = df[TARGET_COLS].mean().to_dict()
        
        try:
            repo_owner, repo_name = folder.split("-", 1)
        except ValueError:
            repo_owner, repo_name = folder, folder
        
        resultados.append({
            "repo_owner": repo_owner,
            "repo_name": repo_name,
            **medias
        })
    except Exception as e:
        print(f"[ERRO] Falha ao processar {folder}: {e}")

df_resultados = pd.DataFrame(resultados)

print(df_resultados)

df_resultados.to_csv("resultado_final.csv", index=False)
print("\n✅ Arquivo 'resultado_final.csv' gerado com sucesso!")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTempo total de execução: {elapsed_time:.2f} segundos")