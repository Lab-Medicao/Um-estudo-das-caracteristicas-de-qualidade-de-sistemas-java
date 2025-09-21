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

        # Estatísticas CK
        for col in TARGET_COLS:
            stats[f"{col}_mean"] = df[col].mean() # média
            stats[f"{col}_median"] = df[col].median() # mediana
            stats[f"{col}_std"] = df[col].std() # desvio padrão
            stats[f"{col}_min"] = df[col].min() # mínimo
            stats[f"{col}_max"] = df[col].max() # máximo
            stats[f"{col}_p90"] = df[col].quantile(0.9) # percentil 90 (serve para entender a cauda da distribuição, que seria o "pico" dos valores mais altos)

            # % outliers (|z| > 2): serve para identificar classes que estão acima de 2 desvios padrão da média
            if df[col].std(ddof=0) != 0:
                zscores = (df[col] - df[col].mean()) / df[col].std(ddof=0)
                stats[f"{col}_outlier_pct"] = (abs(zscores) > 2).mean() * 100
            else:
                stats[f"{col}_outlier_pct"] = 0.0

        # Percentuais acima dos thresholds: classes críticas que passaram de thresholds conhecidos na literatura 
        # (14 para CBO = alto acoplamento, 7 para DIT = herança muito profunda, 500 para LOC = candidata a God Class)
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

rename_map = {
    "total_classes": "Total_Classes",

    "cbo_mean": "CBO_Média",
    "cbo_median": "CBO_Mediana",
    "cbo_std": "CBO_DesvioPadrao",
    "cbo_min": "CBO_Mínimo",
    "cbo_max": "CBO_Máximo",
    "cbo_p90": "CBO_P90",
    "cbo_outlier_pct": "%CBO_Outliers",

    "dit_mean": "DIT_Média",
    "dit_median": "DIT_Mediana",
    "dit_std": "DIT_DesvioPadrao",
    "dit_min": "DIT_Mínimo",
    "dit_max": "DIT_Máximo",
    "dit_p90": "DIT_P90",
    "dit_outlier_pct": "%DIT_Outliers",

    "loc_mean": "LOC_Média",
    "loc_median": "LOC_Mediana",
    "loc_std": "LOC_DesvioPadrao",
    "loc_min": "LOC_Mínimo",
    "loc_max": "LOC_Máximo",
    "loc_p90": "LOC_P90",
    "loc_outlier_pct": "%LOC_Outliers",

    "lcom_mean": "LCOM_Média",
    "lcom_median": "LCOM_Mediana",
    "lcom_std": "LCOM_DesvioPadrao",
    "lcom_min": "LCOM_Mínimo",
    "lcom_max": "LCOM_Máximo",
    "lcom_p90": "LCOM_P90",
    "lcom_outlier_pct": "%LCOM_Outliers",

    "pct_cbo_high": "%CBO_Acima_14",
    "pct_dit_high": "%DIT_Acima_7",
    "pct_loc_high": "%LOC_Acima_500",

    "mean_comment_lines_per_class": "Média_Coment_Classe",
    "ratio_comment_lines_loc": "Coment/LOC",
    "mean_comment_lines_per_repo": "Média_Coment_Repo"
}

df_results.rename(columns=rename_map, inplace=True)

ordered_cols = [
    "owner", "repo", "Total_Classes",
    "CBO_Média", "CBO_Mediana", "CBO_DesvioPadrao", "CBO_Mínimo", "CBO_Máximo", "CBO_P90", "%CBO_Outliers", "%CBO_Acima_14",
    "DIT_Média", "DIT_Mediana", "DIT_DesvioPadrao", "DIT_Mínimo", "DIT_Máximo", "DIT_P90", "%DIT_Outliers", "%DIT_Acima_7",
    "LOC_Média", "LOC_Mediana", "LOC_DesvioPadrao", "LOC_Mínimo", "LOC_Máximo", "LOC_P90", "%LOC_Outliers", "%LOC_Acima_500",
    "LCOM_Média", "LCOM_Mediana", "LCOM_DesvioPadrao", "LCOM_Mínimo", "LCOM_Máximo", "LCOM_P90", "%LCOM_Outliers",
    "Média_Coment_Classe", "Coment/LOC", "Média_Coment_Repo"
]

df_results = df_results[ordered_cols]

# Salvar arquivos
df_results.to_csv("../results/metrics_results.csv", index=False)
df_corr.to_csv("../results/metrics_correlations.csv", index=False)

print(df_results)
print("\n✅ Arquivos 'metrics_results.csv' e 'metrics_correlations.csv' gerados com sucesso!")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo total de execução: {elapsed_time:.2f} segundos")