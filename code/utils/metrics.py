import pandas as pd
from scipy import stats
from datetime import datetime, timezone

# Carregue os arquivos
df_proc = pd.read_csv('./code/results/top_java_repos.csv')
df_qual = pd.read_csv('./code/results/metrics_results.csv')

# Calcule LM04: Tempo desde a Última Atualização (dias)
df_proc['updated_at'] = pd.to_datetime(df_proc['updated_at'], utc=True)
hoje = pd.Timestamp(datetime.now(timezone.utc))
df_proc['dias_desde_ultima_atualizacao'] = (hoje - df_proc['updated_at']).dt.days

# Calcule LM05: Percentual de Issues Fechadas (%)
df_proc['percent_issues_fechadas'] = (df_proc['closed_issues_count'] / df_proc['issues_count']) * 100
df_proc['percent_issues_fechadas'] = df_proc['percent_issues_fechadas'].fillna(0)

# Junte os dados pelo nome do repositório
df = pd.merge(df_proc, df_qual, left_on=['owner', 'name'], right_on=['owner', 'repo'])

# Defina as métricas que deseja analisar
metricas = {
    'Idade do Repositório (anos)': 'age_years',
    'Pull Requests Aceitas': 'merged_pr_count',
    'Número de Releases': 'releases_count',
    'Tempo desde a Última Atualização (dias)': 'dias_desde_ultima_atualizacao',
    'Percentual de Issues Fechadas (%)': 'percent_issues_fechadas',
    'Número de Estrelas': 'stars',
    'Número de Forks': 'forks_count',
    'Tamanho do Repositório (LOC)': 'LOC_Média',
    'CBO': 'CBO_Média',
    'DIT': 'DIT_Média',
    'LCOM': 'LCOM_Média'
}

# Função para extrair estatísticas
def estatisticas(col):
    serie = df[col].dropna()
    media = serie.mean()
    mediana = serie.median()
    moda = serie.mode().iloc[0] if not serie.mode().empty else None
    desvio = serie.std()
    minimo = serie.min()
    maximo = serie.max()
    return media, mediana, moda, desvio, minimo, maximo

# Extrai e imprime os valores para cada métrica
for nome, coluna in metricas.items():
    if coluna and coluna in df.columns:
        X, Y, Z, A, B, C = estatisticas(coluna)
        print(f"{nome}: Média={X:.2f}, Mediana={Y:.2f}, Moda={Z}, Desvio Padrão={A:.2f}, Mínimo={B}, Máximo={C}")
    else:
        print(f"{nome}: coluna não encontrada ou requer cálculo manual.")