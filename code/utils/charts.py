import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def salvar_grafico(nome_arquivo):
    pasta = '../../docs/charts'
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f'{nome_arquivo}.png')
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print(f'Gráfico salvo em: {caminho}')

def grafico_popularidade_qualidade(df):
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']
    for metric in metrics:
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=df['stars'], y=df[metric])
        plt.xlabel('Estrelas (Popularidade)')
        plt.ylabel(f'{metric}')
        plt.title(f'Popularidade vs {metric} (LM06)')
        salvar_grafico(f'RQ01.popularidade_{metric.lower()}')

def grafico_maturidade_qualidade(df):
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']
    for metric in metrics:
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=df['age_years'], y=df[metric])
        plt.xlabel('Idade do Repositório (anos)')
        plt.ylabel(f'{metric}')
        plt.title(f'Maturidade vs {metric} (LM01)')
        salvar_grafico(f'RQ02.maturidade_{metric.lower()}')

def grafico_atividade_qualidade(df):
    metrics = ['CBO_Média', 'DIT_Média', 'LCOM_Média']
    for metric in metrics:
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=df['releases_count'], y=df[metric])
        plt.xlabel('Número de Releases')
        plt.ylabel(f'{metric}')
        plt.title(f'Atividade vs {metric} (LM03)')
        salvar_grafico(f'RQ03.atividade_{metric.lower()}')

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

def grafico_correlacao_metrics():
    # Carrega o CSV de correlações CK
    df_ck = pd.read_csv('../results/metrics_correlations.csv')
    # Agrupa por pares de métricas e calcula média
    df_mean = df_ck.groupby(['metric_x', 'metric_y']).agg({'pearson':'mean', 'spearman':'mean'}).reset_index()
    # Pivot para heatmap
    heatmap_pearson = df_mean.pivot(index='metric_x', columns='metric_y', values='pearson')
    heatmap_spearman = df_mean.pivot(index='metric_x', columns='metric_y', values='spearman')

    # Heatmap Pearson
    plt.figure(figsize=(6,5))
    sns.heatmap(heatmap_pearson, annot=True, cmap='coolwarm', center=0)
    plt.title('Heatmap de Correlação CK (Pearson)')
    salvar_grafico('heatmap_ck_pearson')

    # Heatmap Spearman
    plt.figure(figsize=(6,5))
    sns.heatmap(heatmap_spearman, annot=True, cmap='coolwarm', center=0)
    plt.title('Heatmap de Correlação CK (Spearman)')
    salvar_grafico('heatmap_ck_spearman')

def main():
    df_proc = pd.read_csv('../results/top_java_repos.csv')
    df_qual = pd.read_csv('../results/metrics_results.csv')

    # Junta os dados pelo nome do repositório
    df = pd.merge(df_proc, df_qual, left_on=['owner', 'name'], right_on=['owner', 'repo'])

    grafico_popularidade_qualidade(df)
    grafico_maturidade_qualidade(df)
    grafico_atividade_qualidade(df)
    grafico_tamanho_qualidade(df)

    grafico_correlacao_metrics()

if __name__ == '__main__':
    main()