import os
import time
import pandas as pd

BASE_DIR = "../ck_output"
CSV_NAME = "class.csv"
COMMENTS_CSV = "comments_by_class.csv"
TARGET_COLS = ["cbo", "dit", "loc", "lcom"]

results = []

start_time = time.time()

for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)
    
    if not os.path.isdir(folder_path):
        continue
    
    csv_path = os.path.join(folder_path, CSV_NAME)
    comments_path = os.path.join(folder_path, COMMENTS_CSV)
    
    if not os.path.exists(csv_path):
        print(f"[AVISO] CSV de métricas não encontrado em: {folder}")
        continue
    
    try:
        df = pd.read_csv(csv_path)
        
        # Normaliza colunas
        df.columns = df.columns.str.strip().str.lower()
        
        # Verifica se as colunas de métricas existem
        if not all(col in df.columns for col in TARGET_COLS):
            print(f"[AVISO] Colunas faltando no CSV de métricas em {folder}")
            continue
        
        if df.empty or df[TARGET_COLS].dropna(how="all").empty:
            print(f"[AVISO] CSV de métricas vazio em {folder}")
            continue

        stats = {}
        
        # Total de classes (linhas) do projeto
        stats["total_classes"] = int(df[TARGET_COLS].dropna(how="all").shape[0])
        
        # Estatísticas das métricas CK
        for col in TARGET_COLS:
            stats[f"{col}_mean"] = df[col].mean()
            stats[f"{col}_median"] = df[col].median()
            stats[f"{col}_std"] = df[col].std()
            stats[f"{col}_min"] = df[col].min()
            stats[f"{col}_max"] = df[col].max()
        
        # Métricas de Linhas de Comentário
        if os.path.exists(comments_path):
            df_comments = pd.read_csv(comments_path)
            
            # Remover <file_level>
            df_comments = df_comments[df_comments["class"] != "<file_level>"].copy()
            
            if not df_comments.empty:
                # Média de linhas de comentários por classe
                mean_comment_lines = df_comments.groupby("class")["comment_lines"].sum().mean()
                stats["mean_comment_lines_per_class"] = mean_comment_lines
                
                # Densidade de comentários: total linhas comentadas ÷ total LOC
                total_comment_lines = df_comments["comment_lines"].sum()
                total_loc = df["loc"].sum() if "loc" in df.columns else None
                stats["ratio_comment_lines_loc"] = (
                    total_comment_lines / total_loc if total_loc and total_loc > 0 else None
                )
                
                # Média de comentários por repositório (total / nº classes do repo)
                stats["mean_comment_lines_per_repo"] = (
                    total_comment_lines / stats["total_classes"]
                    if stats["total_classes"] > 0 else None
                )
            else:
                stats["mean_comment_lines_per_class"] = None
                stats["ratio_comment_lines_loc"] = None
                stats["mean_comment_lines_per_repo"] = None
        else:
            print(f"[AVISO] CSV de comentários não encontrado em {folder}")
            stats["mean_comment_lines_per_class"] = None
            stats["ratio_comment_lines_loc"] = None
            stats["mean_comment_lines_per_repo"] = None
        
        results.append({
            "repository": folder,
            **stats
        })
        
    except Exception as e:
        print(f"[ERRO] Falha ao processar {folder}: {e}")

# Gera DataFrame final
df_results = pd.DataFrame(results)
df_results.dropna(how="all", inplace=True)

df_results = df_results.round(3)

print(df_results)

df_results.to_csv("../results.csv", index=False)
print("\n✅ Arquivo 'results.csv' gerado com sucesso!")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo total de execução: {elapsed_time:.2f} segundos")