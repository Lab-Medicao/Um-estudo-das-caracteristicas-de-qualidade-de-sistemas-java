import os
import time
import pandas as pd

BASE_DIR = "../ck_output"
CSV_NAME = "class.csv"
COMMENTS_CSV = "comments_by_class.csv"
TARGET_COLS = ["cbo", "dit", "loc", "lcom"]

results = []
correlations = []

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
        df.columns = df.columns.str.strip().str.lower()

        if not all(col in df.columns for col in TARGET_COLS):
            print(f"[AVISO] Colunas faltando no CSV de métricas em {folder}")
            continue

        if df.empty or df[TARGET_COLS].dropna(how="all").empty:
            print(f"[AVISO] CSV de métricas vazio em {folder}")
            continue

        stats = {}

        # Total de classes
        stats["total_classes"] = int(df[TARGET_COLS].dropna(how="all").shape[0])

        # Estatísticas CK (sem min, com max e P90)
        for col in TARGET_COLS:
            stats[f"{col}_mean"] = df[col].mean()
            stats[f"{col}_median"] = df[col].median()
            stats[f"{col}_std"] = df[col].std()
            stats[f"{col}_max"] = df[col].max()
            stats[f"{col}_p90"] = df[col].quantile(0.9)

            # % outliers (|z| > 2)
            if df[col].std(ddof=0) != 0:
                zscores = (df[col] - df[col].mean()) / df[col].std(ddof=0)
                stats[f"{col}_outlier_pct"] = (abs(zscores) > 2).mean() * 100
            else:
                stats[f"{col}_outlier_pct"] = 0.0

        # Percentuais acima dos thresholds
        stats["pct_cbo_high"] = (df["cbo"] > 14).mean() * 100
        stats["pct_dit_high"] = (df["dit"] > 7).mean() * 100
        stats["pct_loc_high"] = (df["loc"] > 500).mean() * 100

        # Comentários
        if os.path.exists(comments_path):
            df_comments = pd.read_csv(comments_path)
            df_comments = df_comments[df_comments["class"] != "<file_level>"].copy()

            if not df_comments.empty:
                mean_comment_lines = df_comments.groupby("class")["comment_lines"].sum().mean()
                stats["mean_comment_lines_per_class"] = mean_comment_lines

                total_comment_lines = df_comments["comment_lines"].sum()
                total_loc = df["loc"].sum() if "loc" in df.columns else None
                stats["ratio_comment_lines_loc"] = (
                    total_comment_lines / total_loc if total_loc and total_loc > 0 else None
                )

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

        # Correlações (apenas entre TARGET_COLS: cbo, dit, loc, lcom)
        corr_pearson = df[TARGET_COLS].corr(method="pearson")
        corr_spearman = df[TARGET_COLS].corr(method="spearman")

        for i, col1 in enumerate(TARGET_COLS):
            for col2 in TARGET_COLS[i+1:]:
                correlations.append({
                    "owner": folder.split("_", 1)[0] if "_" in folder else folder,
                    "repo": folder.split("_", 1)[1] if "_" in folder else "",
                    "metric_x": col1,
                    "metric_y": col2,
                    "pearson": corr_pearson.loc[col1, col2],
                    "spearman": corr_spearman.loc[col1, col2]
                })

        # Extrair owner/repo
        format_folder_name = folder.replace("_", "/", 1)
        if "/" in format_folder_name:
            owner, repo = format_folder_name.split("/", 1)
        else:
            owner, repo = format_folder_name, ""

        results.append({
            "owner": owner,
            "repo": repo,
            **stats
        })

    except Exception as e:
        print(f"[ERRO] Falha ao processar {folder}: {e}")

# DataFrames finais
df_results = pd.DataFrame(results).dropna(how="all").round(3)
df_corr = pd.DataFrame(correlations).round(3)

# Salvar arquivos
df_results.to_csv("../results.csv", index=False)
df_corr.to_csv("../correlations.csv", index=False)

print(df_results)
print("\n✅ Arquivos 'results.csv' e 'correlations.csv' gerados com sucesso!")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo total de execução: {elapsed_time:.2f} segundos")