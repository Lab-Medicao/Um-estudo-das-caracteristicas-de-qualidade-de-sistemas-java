import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def salvar_grafico(nome_arquivo):
    pasta = './docs/charts'
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f'{nome_arquivo}.png')
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print(f'Gráfico salvo em: {caminho}')

# RQ 01: Popularidade vs Qualidade
def grafico_popularidade_qualidade(df):
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']
    for metric in metrics:
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=df['stars'], y=df[metric])
        plt.xlabel('Estrelas (Popularidade)')
        plt.ylabel(f'{metric}')
        plt.title(f'Popularidade vs {metric} (LM06)')
        salvar_grafico(f'RQ01.popularidade_{metric.lower()}')

# RQ 02: Maturidade vs Qualidade
def grafico_maturidade_qualidade(df):
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']
    for metric in metrics:
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=df['age_years'], y=df[metric])
        plt.xlabel('Idade do Repositório (anos)')
        plt.ylabel(f'{metric}')
        plt.title(f'Maturidade vs {metric} (LM01)')
        salvar_grafico(f'RQ02.maturidade_{metric.lower()}')

# RQ 03: Atividade vs Qualidade
def grafico_atividade_qualidade(df):
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']
    for metric in metrics:
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=df['releases_count'], y=df[metric])
        plt.xlabel('Número de Releases')
        plt.ylabel(f'{metric}')
        plt.title(f'Atividade vs {metric} (LM03)')
        salvar_grafico(f'RQ03.atividade_{metric.lower()}')

# RQ 04: Tamanho (LOC) vs Qualidade
def grafico_tamanho_qualidade(df):
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']
    for metric in metrics:
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=df['LOC_Média'], y=df[metric])
        plt.xlabel('Linhas de Código (LOC)')
        plt.ylabel(f'{metric}')
        plt.title(f'Tamanho (LOC) vs {metric} (LM08)')
        salvar_grafico(f'RQ04.tamanho_loc_{metric.lower()}')

    plt.figure(figsize=(10,6))
    sns.scatterplot(x=df['LOC_Média'], y=df['Coment/LOC'])
    plt.xlabel('Linhas de Código (LOC)')
    plt.ylabel('Coment/LOC')
    plt.title('Tamanho (LOC) vs Coment/LOC (AM05)')
    salvar_grafico('RQ04.tamanho_loc_comentloc')

    plt.figure(figsize=(10,6))
    sns.scatterplot(x=df['LOC_Média'], y=df['Média_Coment_Classe'])
    plt.xlabel('Linhas de Código (LOC)')
    plt.ylabel('Média de Comentários por Classe')
    plt.title('Tamanho (LOC) vs Média de Comentários por Classe (AM06)')
    salvar_grafico('RQ04.tamanho_loc_comentclasse')

# Gráfico de Correlação entre Métricas CK
def grafico_correlacao_metrics():
    df_ck = pd.read_csv('../results/metrics_correlations.csv')

    metric_mapping = {
        'cbo': 'CBO_Média',
        'dit': 'DIT_Média', 
        'lcom': 'LCOM_Média',
        'loc': 'LOC_Média'
    }
    
    df_ck['metric_x'] = df_ck['metric_x'].map(metric_mapping)
    df_ck['metric_y'] = df_ck['metric_y'].map(metric_mapping)
    
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média', 'LOC_Média']
    
    df_ck = df_ck[df_ck['metric_x'].isin(metrics) & df_ck['metric_y'].isin(metrics)]
    
    df_mean = df_ck.groupby(['metric_x', 'metric_y']).agg({'pearson':'mean', 'spearman':'mean'}).reset_index()
    
    symmetric_pairs = []
    for _, row in df_mean.iterrows():
        symmetric_pairs.append({
            'metric_x': row['metric_y'],
            'metric_y': row['metric_x'],
            'pearson': row['pearson'],
            'spearman': row['spearman']
        })
    
    df_complete = pd.concat([df_mean, pd.DataFrame(symmetric_pairs)], ignore_index=True)
    
    diagonal_pairs = []
    for metric in metrics:
        diagonal_pairs.append({
            'metric_x': metric,
            'metric_y': metric,
            'pearson': 1.0,
            'spearman': 1.0
        })
    
    df_complete = pd.concat([df_complete, pd.DataFrame(diagonal_pairs)], ignore_index=True)

    df_complete = df_complete.drop_duplicates(subset=['metric_x', 'metric_y'])
    
    heatmap_pearson = df_complete.pivot(index='metric_x', columns='metric_y', values='pearson').reindex(index=metrics, columns=metrics)
    heatmap_spearman = df_complete.pivot(index='metric_x', columns='metric_y', values='spearman').reindex(index=metrics, columns=metrics)

    # Heatmap Pearson
    plt.figure(figsize=(8,6))
    sns.heatmap(heatmap_pearson, annot=True, cmap='coolwarm', center=0, fmt='.3f')
    plt.title('Heatmap de Correlação CK (Pearson)')
    salvar_grafico('heatmap_ck_pearson')

    # Heatmap Spearman
    plt.figure(figsize=(8,6))
    sns.heatmap(heatmap_spearman, annot=True, cmap='coolwarm', center=0, fmt='.3f')
    plt.title('Heatmap de Correlação CK (Spearman)')
    salvar_grafico('heatmap_ck_spearman')

# Gráficos Estatísticos das Métricas
def graficos_estatisticos(df):
    processo_metrics = [
        'age_years',
        'stars',
        'releases_count',
        'forks_count',
        'LOC_Média',
        'merged_pr_count'
    ]

    if 'dias_desde_ultima_atualizacao' not in df.columns and 'updated_at' in df.columns:
        from datetime import datetime, timezone
        df['updated_at'] = pd.to_datetime(df['updated_at'], utc=True)
        hoje = pd.Timestamp(datetime.now(timezone.utc))
        df['dias_desde_ultima_atualizacao'] = (hoje - df['updated_at']).dt.days
    if 'percent_issues_fechadas' not in df.columns and 'closed_issues_count' in df.columns and 'issues_count' in df.columns:
        df['percent_issues_fechadas'] = (df['closed_issues_count'] / df['issues_count']) * 100
        df['percent_issues_fechadas'] = df['percent_issues_fechadas'].fillna(0)

    if 'dias_desde_ultima_atualizacao' in df.columns:
        processo_metrics.append('dias_desde_ultima_atualizacao')
    if 'percent_issues_fechadas' in df.columns:
        processo_metrics.append('percent_issues_fechadas')

    qualidade_metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']

    # Histogramas
    for metric in qualidade_metrics:
        if metric in df.columns:
            plt.figure(figsize=(8,5))
            sns.histplot(df[metric].dropna(), kde=True, bins=30)
            plt.title(f'Histograma de {metric}')
            plt.xlabel(metric)
            plt.ylabel('Frequência')
            safe_metric = metric.lower().replace('/', '_').replace(' ', '_')
            salvar_grafico(f'histograma_{safe_metric}')

    # Boxplots
    for metric in processo_metrics:
        if metric in df.columns:
            plt.figure(figsize=(6,4))
            sns.boxplot(x=df[metric].dropna())
            plt.title(f'Boxplot de {metric}')
            plt.xlabel(metric)
            safe_metric = metric.lower().replace('/', '_').replace(' ', '_')
            salvar_grafico(f'boxplot_{safe_metric}')

def main():
    df_proc = pd.read_csv('../results/top_java_repos.csv')
    df_qual = pd.read_csv('../results/metrics_results.csv')
    
    df = pd.merge(df_proc, df_qual, left_on=['owner', 'name'], right_on=['owner', 'repo'])

    grafico_popularidade_qualidade(df)
    grafico_maturidade_qualidade(df)
    grafico_atividade_qualidade(df)
    grafico_tamanho_qualidade(df)

    grafico_correlacao_metrics()

    graficos_estatisticos(df)

if __name__ == '__main__':
    main()