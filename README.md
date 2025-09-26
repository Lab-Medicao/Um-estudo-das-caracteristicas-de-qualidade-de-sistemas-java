# 📝 Relatório Técnico: Um Estudo das Características de Qualidade de Sistemas Java

## 1. Informações do grupo

- **🎓 Curso:** Engenharia de Software
- **📘 Disciplina:** Laboratório de Experimentação de Software
- **🗓 Período:** 6° Período
- **👨‍🏫 Professor(a):** Prof. Dr. João Paulo Carneiro Aramuni
- **👥 Membros do Grupo:** Ana Luiza Machado Alves, Lucas Henrique Chaves de Barros e Raquel Inez de Almeida Calazans

---

## 2. Introdução

Este projeto tem como objetivo analisar aspectos da qualidade interna de repositórios desenvolvidos em **Java**, correlacionando-os com características do seu processo de desenvolvimento.

A análise é realizada sob a perspectiva de métricas de produto, calculadas por meio da ferramenta **CK (Chidamber & Kemerer Java Metrics)**, contemplando atributos como:

- **Modularidade**
- **Manutenibilidade**
- **Legibilidade**

O estudo está inserido no contexto de sistemas **open-source**, onde múltiplos desenvolvedores colaboram em diferentes partes do código. Nessa abordagem, práticas como **revisão de código** e **análise estática** (via ferramentas de CI/CD) são fundamentais para mitigar riscos e preservar a qualidade do software.

### CK Metrics Extractor

Nesse projeto, utilizaremos o **CK Metrics Extractor** como ferramenta de coleta. O CK Tool é usado para análise de métricas de código-fonte Java, focando em aspectos de qualidade e complexidade. Ele automatiza a extração de métricas importantes para classes, métodos, campos e variáveis, auxiliando na avaliação e melhoria do projeto.

A ferramenta gera um arquivo `.csv` contendo as métricas extraídas de cada repositório Java analisado. Esse arquivo será utilizado para análises estatísticas, visualização de dados e comparação entre diferentes projetos, facilitando a identificação de padrões e tendências relacionadas à qualidade do código.

---

## 3. Tecnologias e ferramentas utilizadas

- **💻 Linguagem de Programação:** Python 3.x
- **🛠 Frameworks:** CK Tool, GraphQL
- **🌐 API utilizada:** GitHub GraphQL API
- **📦 Dependências/Bibliotecas:**
  - Python: pandas, matplotlib, seaborn, gitpython, requests, keyring, tqdm
  - Java 21
  - Maven

### 🚀 Preparação do Ambiente

**1. Clone este repositório:**

```bash
git clone https://github.com/analuizaalvesm/java-repos-ck-analyzer.git
cd java-repos-ck-analyzer
```

**2. (Opcional) Crie um ambiente virtual:**

```bash
 python3 -m venv .venv
 source .venv/bin/activate  # Linux/macOS
 .venv\Scripts\activate     # Windows
```

**2. Instale as dependências Python:**

```bash
pip install -r requirements.txt
```

**3. Baixe o [CK Tool](https://github.com/mauricioaniche/ck) (jar):**

```bash
cd code/
git clone https://github.com/mauricioaniche/ck.git
```

**4. Execute a coleta da análise:**

```bash
cd code/
python main.py          # coleta os repositórios
python ck_metrics.py    # roda a análise CK

cd utils/
python analyzer.py      # consolida as métricas de qualidade em uma tabela
python charts.py        # gera os gráficos
python metrics.py       # imprime métricas específicas das LMs (Lab Metrics - Métricas de Processo)
```

_Observação: é necessário configurar uma chave de acesso pessoal (token) do GitHub nas variáveis de ambiente/keyring do seu sistema._

---

### 4. Questões de Pesquisa (Research Questions – RQs)

As questões de pesquisa (RQs) deste estudo buscam analisar a relação entre métricas de processo e métricas de qualidade de repositórios Java.

**🔍 Questões de Pesquisa - Research Questions (RQs):**

| RQ   | Pergunta                                                                                      |
| ---- | --------------------------------------------------------------------------------------------- |
| RQ01 | Qual a relação entre a **popularidade** dos repositórios e suas características de qualidade? |
| RQ02 | Qual a relação entre a **maturidade** dos repositórios e suas características de qualidade?   |
| RQ03 | Qual a relação entre a **atividade** dos repositórios e suas características de qualidade?    |
| RQ04 | Qual a relação entre o **tamanho** dos repositórios e suas características de qualidade?      |

### 4.1. Hipóteses Informais (Informal Hypotheses – IH)

As **Hipóteses Informais** foram elaboradas a partir das RQs, estabelecendo expectativas sobre os resultados esperados do estudo:

**💡 Hipóteses Informais - Informal Hypotheses (IH):**

| IH   | Descrição                                                                                                                                                                        |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IH01 | Repositórios mais populares tendem a apresentar melhor legibilidade e modularidade, já que atraem mais colaboradores e passam por revisões frequentes.                           |
| IH02 | Projetos maduros, mantidos por mais tempo, possuem métricas de qualidade mais consistentes, refletindo evolução gradual e práticas consolidadas de desenvolvimento.              |
| IH03 | Repositórios com maior atividade (commits e pull requests frequentes) apresentam maior manutenibilidade, uma vez que o código é constantemente atualizado e ajustado.            |
| IH04 | Repositórios maiores tendem a apresentar desafios na manutenção e modularidade, já que o aumento de tamanho pode impactar negativamente a simplicidade e legibilidade do código. |

---

## 5. Metodologia

O experimento foi conduzido em cinco etapas principais: **coleta de dados**, **extração de métricas de processo e de qualidade**, **sumarização**, **análise dos dados** e **visualização dos resultados**.

### 5.1 Coleta de dados

- Foram considerados **top 1000 repositórios em Java**, selecionados a partir dos seguintes critérios:
  - **Popularidade** → ex.: repositórios com maior número de estrelas (top-N).
  - **Linguagem primária** → restrição a Java como linguagem específica.
  - **Atividade mínima** → presença de commits, issues ou releases nos últimos anos.
- O script utiliza a **GraphQL API** do GitHub, que permite buscar dados estruturados e específicos de repositórios em uma única requisição.
- Definição da `query`:
  - Nome, dono, URL
  - Número de estrelas (stargazerCount)
  - Datas de criação, último push e atualização
  - Linguagem principal
  - Número de releases
  - Número de commits no branch principal
  - Linguagens usadas e tamanho em bytes por linguagem
  - Tamanho em bytes por linguagem

---

### 5.2 Filtragem e paginação

- Devido ao limite de requisições da **GitHub API**, a coleta exigiu o uso de uma **paginação** de **25 repositórios** por página, permitindo recuperar lotes sucessivos de dados sem perda de registros.
- Para maior confiabilidade, foi implementado um sistema de **retry com backoff exponencial** para lidar com erros temporários ou rate limiting da API.
- ⏱ O tempo médio estimado de coleta foi de aproximadamente **3 minutos e 38 segundos** para o conjunto completo de repositórios.

---

### 5.3 Normalização e pré-processamento

- Após a coleta, os dados foram organizados em um **banco/tabulação unificada**, estruturada por repositório.
- Foram aplicadas etapas de pré-processamento:
  - **Conversão de datas** para formato padronizado (ISO 8601) e cálculo de intervalos (ex.: idade em anos, tempo desde a última atualização em dias).
  - Para auxiliar na análise das métricas de processo, o script também calcula informações como **idade** (`age_years`) e o **tamanho total em bytes** (`size_bytes`) do repositório com base nos dados obtidos pela API.
  - Os dados coletados são organizados em um arquivo CSV (`top_java_repos.csv`) para facilitar análise posterior.

---

### 5.5 Extração das Métricas

#### 5.5.1 Coleta de repositórios

O script suporta duas estratégias de obtenção do código-fonte:

1. **Download do ZIP da branch padrão no GitHub**

- Determina a default branch do repositório (main, master, trunk, etc) usando:
  - git ls-remote
  - Fallback via GitHub API
  - Fallback final: main
  - Baixa o ZIP e extrai o conteúdo para uma pasta local.

2. **Clonagem via Git**

- Se o download do ZIP falhar, o script recorre a git clone --depth 1.
- Usa GitPython ou subprocess como fallback para clonagem tradicional.

#### 5.5.2 Extração de métricas com CK Tool

Após obter o código-fonte:

- Executa o **CK Tool (Java JAR)** no repositório.
- CK Tool gera métricas de classe, método, campo e variável em CSV:
  - **Classe** (`class.csv`): acoplamento (CBO, fan-in/fan-out), complexidade (WMC, RFC), coesão (LCOM, TCC), herança (DIT, NOC), quantidade de métodos/campos, LOC, estruturas de controle, literais, operadores, classes internas, lambdas, etc.
  - **Método** (`method.csv`): complexidade, acoplamento, LOC, parâmetros, variáveis, métodos invocados, loops, comparações, try/catch, literais e operadores.
  - **Campo** (`field.csv`): informações sobre variáveis de classe.
  - **Variável** (`variable.csv`): uso de variáveis.
- Garante que apenas CSVs existentes e não vazios sejam processados.

#### 5.5.3 Exibição e filtragem de métricas

O script contém funções para carregar e imprimir métricas de cada CSV:

- `load_and_print_class_metrics`
- `load_and_print_method_metrics`
- `load_and_print_field_metrics`
- `load_and_print_variable_metrics`

Observações importantes:

- Filtra apenas colunas relevantes para análise.
- Imprime apenas as primeiras linhas para visualização rápida.
- Garante robustez contra arquivos corrompidos ou vazios.

#### 5.5.4 Gestão de repositórios já processados

Antes de processar, verifica se já existem CSVs na pasta ck_output. Se sim, pula o repositório para evitar duplicação. Isso ajuda a manter controle de tempo estimado restante usando média do tempo por repositório.

#### 5.5.5 Robustez e tolerância a falhas

O script adota várias estratégias para lidar com problemas:

- Timeouts ao baixar ZIP, acessar API ou rodar CK.
- Fallbacks (ZIP → Git clone, git ls-remote → GitHub API → default main).
- Tratamento de erros em CSVs (ignora arquivos vazios ou corrompidos).
- Limpeza de arquivos temporários (temp_extract, ZIP baixado).
- Continuação do processamento mesmo que algum repositório falhe.

---

### 5.6 Sumarização dos Dados

- Os dados brutos foram organizados e filtrados pelo script `analyzer.py`.
- Foram realizadas operações de limpeza (linhas vazias) e sumarização dos resultados especificamente para classes, agrupando um resumo dos resultados em uma única tabela.
- Para as métricas de qualidade, utilizamos as seguintes medidas estatísticas: **média**, **mediana**, **moda**, **desvio padrão**, valor **máximo** e **mínimo**, **outliers**, **percentuais de thresholds**, **coeficientes de correlação de Spearman e Pearson**, entre outros.

---

### 5.7 Métricas

Inclua métricas relevantes de repositórios do GitHub, separando **métricas de processo** e **métricas de qualidade**:

#### 📊 Métricas de Processo

| Código | Métrica                                    | Descrição                                                                               |
| ------ | ------------------------------------------ | --------------------------------------------------------------------------------------- |
| LM01   | 🕰 Idade do Repositório (anos)              | Tempo desde a criação do repositório até o momento atual, medido em anos.               |
| LM02   | ✅ Pull Requests Aceitas                   | Quantidade de pull requests que foram aceitas e incorporadas ao repositório.            |
| LM03   | 📦 Número de Releases                      | Total de versões ou releases oficiais publicadas no repositório.                        |
| LM04   | ⏳ Tempo desde a Última Atualização (dias) | Número de dias desde a última modificação ou commit no repositório.                     |
| LM05   | 📋 Percentual de Issues Fechadas (%)       | Proporção de issues fechadas em relação ao total de issues criadas, em percentual.      |
| LM06   | ⭐ Número de Estrelas                      | Quantidade de estrelas recebidas no GitHub, representando interesse ou popularidade.    |
| LM07   | 🍴 Número de Forks                         | Número de forks, indicando quantas vezes o repositório foi copiado por outros usuários. |
| LM08   | 📏 Tamanho do Repositório (LOC)            | Total de linhas de código (Lines of Code) contidas no repositório.                      |

#### 💡 Métricas de Qualidade

| Código | Métrica                               | Descrição                                                           |
| ------ | ------------------------------------- | ------------------------------------------------------------------- |
| AM01   | 💻 CBO (Couping Between Objects)      | Grau de acoplamento entre uma classe e outras classes.              |
| AM02   | 🔗 DIT (Depth of Inheritance Tree)    | Indica a profundidade da hierarquia de herança de uma classe.       |
| AM03   | 🌟 LCOM (Lack of Cohesion in Methods) | Avalia o quanto os métodos de uma classe são relacionados entre si. |
| AM04   | 📋 Coment/LOC                         | Média de comentários por linha de código.                           |
| AM05   | 📋 Coment/PR                          | Média de Comentários por Classe e por Repositório.                  |

---

### 5.8 Cálculo de métricas

As métricas definidas na seção **4.7** foram obtidas a partir de dados brutos retornados pela **GitHub API** e da extração automatizada das métricas de qualidade pelo **CK Tool**.

#### 5.8.1 Métricas de Processo

As métricas de processo, como idade do repositório, número de estrelas, releases, forks, pull requests aceitas e percentual de issues fechadas, foram obtidas diretamente dos campos retornados pela API do GitHub.

- Para cada métrica, foram aplicadas operações de transformação simples:
  - Diferença de datas para calcular idade do repositório e tempo desde a última atualização.
  - Contagens absolutas para releases, estrelas, forks e pull requests.
  - Proporções para percentual de issues fechadas.
  - Identificação categórica para linguagem primária.
- Os dados foram organizados em tabelas e arquivos CSV, permitindo sumarização e análise estatística.

#### 5.8.2 Métricas de Qualidade

O script `ck_metrics.py` automatizou a extração das métricas de qualidade dos repositórios Java utilizando o CK Tool.

- Para cada repositório, o código-fonte foi obtido e processado pelo CK Tool, que gerou arquivos CSV com métricas por classe, método, campo e variável.
- As principais métricas de qualidade extraídas incluem:
  - **CBO (Coupling Between Objects):** Média, mediana, moda, desvio padrão, mínimo, máximo, percentil 90, percentual de outliers e percentual acima de 14.
  - **DIT (Depth of Inheritance Tree):** Média, mediana, moda, desvio padrão, mínimo, máximo, percentil 90, percentual de outliers e percentual acima de 7.
  - **LOC (Lines of Code):** Média, mediana, moda, desvio padrão, mínimo, máximo, percentil 90, percentual de outliers e percentual acima de 500.
  - **LCOM (Lack of Cohesion in Methods):** Média, mediana, moda, desvio padrão, mínimo, máximo, percentil 90, percentual de outliers.
  - **Coment/LOC:** Média de comentários por linha de código.
  - **Coment/PR:** Média de comentários por classe e por repositório.
- O script também inclui rotinas para sumarizar e filtrar os dados, garantindo que apenas arquivos válidos e não vazios sejam considerados na análise.

#### 5.8.3 Agregação e Visualização

- As métricas foram agregadas por repositório e por classe, permitindo análises descritivas, geração de tabelas resumo e visualizações gráficas.
- Foram calculados estatísticos como média, mediana, desvio padrão, mínimo e máximo para cada métrica, facilitando a identificação de padrões e outliers.

Esse processo integrado permitiu uma avaliação abrangente dos sistemas Java analisados, considerando tanto aspectos de processo quanto de qualidade interna do código.

---

### 5.9 Ordenação e análise inicial

Após o cálculo das métricas, os repositórios foram ordenados utilizando um **índice composto de popularidade** que combina de forma ponderada métricas como número de estrelas, forks, releases e pull requests aceitas. Essa abordagem permite ranquear os projetos de maneira mais abrangente, refletindo múltiplos aspectos de relevância e atividade.

A análise inicial foi conduzida a partir de **valores medianos e das distribuições das principais métricas,** tanto de processo quanto de qualidade. Foram geradas tabelas resumo e gráficos para visualizar:

- Distribuição dos repositórios por linguagem primária.
- Estatísticas descritivas (média, mediana, desvio padrão, mínimo e máximo) das métricas de processo e qualidade.
- Frequência de categorias, como tipos de contribuição e releases.
- Identificação de outliers e padrões gerais nos dados.

Essa etapa exploratória permitiu identificar tendências, como a predominância de certos valores de acoplamento (CBO), profundidade de herança (DIT), tamanho (LOC) e coesão (LCOM), além de destacar repositórios com características excepcionais. A agregação dos dados por repositório e por classe facilitou a comparação entre projetos e a seleção de casos para análises mais detalhadas nas etapas seguintes.

---

### 5.10 Relação das RQs com as Métricas

As **Questões de Pesquisa (Research Questions – RQs)** foram associadas a métricas específicas, previamente definidas na seção de métricas (Seção 4.7), garantindo que a investigação seja **sistemática e mensurável**.

A tabela a seguir apresenta a relação entre cada questão de pesquisa e as métricas utilizadas para sua avaliação:

**🔍 Relação das RQs com Métricas:**

| RQ   | Pergunta                                                                                      | Métrica de Processo                               | Métricas de Qualidade (CK) | Código da Métrica |
| ---- | --------------------------------------------------------------------------------------------- | ------------------------------------------------- | -------------------------- | ----------------- |
| RQ01 | Qual a relação entre a **popularidade** dos repositórios e suas características de qualidade? | ⭐ Número de estrelas                             | CBO, DIT, LCOM             | LM06              |
| RQ02 | Qual a relação entre a **maturidade** dos repositórios e suas características de qualidade?   | 🕰 Idade (anos)                                    | CBO, DIT, LCOM             | LM01              |
| RQ03 | Qual a relação entre a **atividade** dos repositórios e suas características de qualidade?    | 📦 Número de releases                             | CBO, DIT, LCOM             | LM03              |
| RQ04 | Qual a relação entre o **tamanho** dos repositórios e suas características de qualidade?      | 📏 Linhas de código (LOC) e linhas de comentários | CBO, DIT, LCOM             | LM08, AM05, AM06  |

---

## 6. Resultados

A seguir, são apresentados os principais resultados obtidos a partir da análise dos repositórios Java, utilizando as métricas de processo e de qualidade definidas na metodologia.

---

### 6.1. Estatísticas Descritivas

A partir do script [`metrics.py`](code/utils/metrics.py), foram calculadas estatísticas descritivas para as principais métricas de processo e qualidade, incluindo média, mediana, desvio padrão, mínimo e máximo.

| Métrica                                    | Código | Média   | Mediana | Moda | Desvio Padrão | Mínimo | Máximo    |
| ------------------------------------------ | ------ | ------- | ------- | ---- | ------------- | ------ | --------- |
| 🕰 Idade do Repositório (anos)              | LM01   | 9.61    | 9.71    | 9.68 | 3.04          | 0.18   | 16.69     |
| ✅ Pull Requests Aceitas                   | LM02   | 1026.93 | 67.00   | 0    | 3379.50       | 0      | 45219     |
| 📦 Número de Releases                      | LM03   | 38.78   | 10.00   | 0    | 86.11         | 0      | 1000      |
| ⏳ Tempo desde a Última Atualização (dias) | LM04   | 2.08    | 1.00    | 0    | 3.59          | 0      | 62        |
| 📋 Percentual de Issues Fechadas (%)       | LM05   | 66.59   | 74.25   | 0.0  | 28.05         | 0.0    | 100.0     |
| ⭐ Número de Estrelas (Stars)              | LM06   | 9288.85 | 5716.00 | 3954 | 10594.80      | 3415   | 117052    |
| 🍴 Número de Forks                         | LM07   | 2344.96 | 1349.00 | 1051 | 3709.58       | 128    | 54106     |
| 📏 Tamanho do Repositório (LOC)            | LM08   | 50.30   | 43.85   | 5.0  | 31.28         | 2.0    | 406.333   |
| 🔗 CBO                                     | AM01   | 5.37    | 5.32    | 0.0  | 1.87          | 0.0    | 21.937    |
| 🏷 DIT                                      | AM02   | 1.46    | 1.39    | 1.0  | 0.35          | 1.0    | 4.388     |
| 🧩 LCOM                                    | AM03   | 118.24  | 23.60   | 0.0  | 1780.84       | 0.0    | 54799.523 |

#### 6.1.1 Gráficos das Estatísticas Descritivas

<p align="center">
  <img src="./docs/charts/boxplot_age_years.png" alt="Boxplot Stars">
</p>
<h4 align="center">Figura 1 - Boxplot Idade dos Repositórios (anos)</h4>

- Distribuição mais equilibrada, com alguns outliers em idades muito baixas (< 1 ano).
- Média (9.61) e mediana (9.71) muito próximas, indicando simetria.

A maioria dos projetos analisados tem longa duração (em torno de 10 anos), com poucos repositórios muito novos.

---
<p align="center">
  <img src="./docs/charts/boxplot_merged_pr_count.png" alt="Boxplot Pull Requests">
</p>
<h4 align="center">Figura 2 - Boxplot Pull Requests Aceitas</h4>

- Concentração baixa com forte dispersão (outliers chegando a >40 mil PRs).
- Média (1026) é muito maior que a mediana (67).

Apenas alguns repositórios recebem e aceitam um volume massivo de contribuições, enquanto a maioria é mais modesta em colaboração externa.

---
<p align="center">
  <img src="./docs/charts/boxplot_releases_count.png" alt="Boxplot Releases">
</p>
<h4 align="center">Figura 3 - Boxplot Número de Releases</h4>

- Forte concentração em valores baixos, mas alguns repositórios chegam a quase 1000 releases.
- Média (38.7) muito maior que a mediana (10).

A maioria lança poucas versões, mas projetos com releases muito frequentes puxam a média para cima.

---
<p align="center">
  <img src="./docs/charts/boxplot_dias_desde_ultima_atualizacao.png" alt="Boxplot Tempo Atualização">
</p>
<h4 align="center">Figura 4 - Boxplot Tempo desde a Última Atualização (dias)</h4>

- Grande concentração próxima de zero e alguns outliers que chegam até ~60 dias.
- Média de 2 dias, mediana de 1 dia.

Esses repositórios tendem a ser bem ativos, com atualizações frequentes. Apenas poucos projetos ficam mais de 1–2 meses sem commit.

---
<p align="center">
  <img src="./docs/charts/boxplot_percent_issues_fechadas.png" alt="Boxplot Percentual Issue Fechadas">
</p>
<h4 align="center">Figura 5 - Boxplot Percentual de Issues Fechadas (%)</h4>

- Distribuição mais uniforme entre 0% e 100%.
- Média de 66%, mediana de 74%.

A maioria dos projetos consegue fechar boa parte das issues, mas há casos extremos tanto de abandono (0%) quanto de alta eficiência (100%).

---
<p align="center">
  <img src="./docs/charts/boxplot_stars.png" alt="Boxplot Stars">
</p>
<h4 align="center">Figura 6 - Boxplot Número de Estrelas (Stars)</h4>

- Mostra forte assimetria à direita (muitos outliers acima de 20k stars).
- Média (9288) é bem maior que a mediana (5716), confirmando a concentração de valores baixos e alguns poucos repositórios extremamente populares que puxam a média para cima.

A maioria dos repositórios é moderadamente popular, mas há casos raros de altíssima visibilidade.

---
<p align="center">
  <img src="./docs/charts/boxplot_forks_count.png" alt="Boxplot Forks">
</p>
<h4 align="center">Figura 7 - Boxplot Número de Forks</h4>

- Padrão parecido com stars — concentração baixa e poucos repositórios com milhares de forks.
- Média (2344) > mediana (1349), indicando assimetria causada por projetos muito populares.

A maioria dos projetos tem poucos forks, mas alguns se destacam como referências para a comunidade.

---
<p align="center">
  <img src="./docs/charts/boxplot_loc_média.png" alt="Boxplot LOC">
</p>
<h4 align="center">Figura 8 - Boxplot Tamanho do Repositório (LOC - Lines of Code)</h4>

- Distribuição assimétrica, com outliers chegando a > 300 LOC.
- Média (50) maior que a mediana (43.8), mostrando assimetria leve.

A maior parte dos repositórios tem tamanho moderado, mas alguns são bem maiores, gerando dispersão.

---
<p align="center">
  <img src="./docs/charts/histograma_cbo_média.png" alt="Histograma CBO">
</p>
<h4 align="center">Figura 9 - Histograma CBO (Couping Between Objects)</h4>

- Distribuição quase simétrica em torno do pico entre 4 e 6, com leve cauda à direita.
- Média (5.37) ≈ mediana (5.32), confirmando simetria.

O acoplamento entre classes está moderado para a maioria dos sistemas. Valores extremos (>15) são raros, mas representam casos de classes muito dependentes que podem afetar a manutenibilidade.

---
<p align="center">
  <img src="./docs/charts/histograma_dit_média.png" alt="Histograma DIT">
</p>
<h4 align="center">Figura 10 - Histograma DIT (Depth of Inheritance Tree)</h4>

- Distribuição assimétrica à direita, concentrada entre 1.0 e 1.5.
- Média (1.46) e mediana (1.39) são próximas, mas a cauda mostra heranças mais profundas (até ~4).

A maior parte das classes está em níveis rasos da hierarquia de herança, o que é comum em projetos moderados. Entretanto, algumas classes muito profundas podem indicar complexidade excessiva ou sobreuso de herança.

---
<p align="center">
  <img src="./docs/charts/histograma_lcom_média.png" alt="Histograma LCOM">
</p>
<h4 align="center">Figura 11 - Histograma LCOM (Lack of Cohesion in Methods)</h4>

- A maior parte dos valores está concentrada próximo de zero, mas há uma cauda longa à direita (até >50.000), mostrando que poucos repositórios apresentam coesão extremamente baixa.
- Média (118) é muito maior que a mediana (23), indicando forte assimetria.

A maioria dos sistemas tem classes com coesão aceitável, mas existem outliers com altíssima falta de coesão, o que pode indicar projetos problemáticos em termos de design orientado a objetos.

---
### 6.2. Gráficos das RQs

Para investigar as relações entre métricas de processo e métricas de qualidade, foram gerados gráficos de dispersão e heatmaps de correlação (Pearson e Spearman).


#### 6.2.1 Gráficos da RQ01 - Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?

<p align="center" style="display: flex; justify-content: center; gap: 10px;">
  <img src="./docs/charts/RQ01.popularidade_cbo_média.png" alt="Popularidade vs CBO" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ01.popularidade_dit_média.png" alt="Popularidade vs DIT" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ01.popularidade_lcom_média.png" alt="Popularidade vs LCOM" style="max-width: 33%; height: auto;">
</p>
<h4 align="center">Figuras 12, 13, 14 - Popularidade vs Qualidade</h4>

--- 
#### 6.2.2 Gráficos da RQ02 - Qual a relação entre a maturidade do repositórios e as suas características de qualidade?

<p align="center" style="display: flex; justify-content: center; gap: 10px;">
  <img src="./docs/charts/RQ02.maturidade_cbo_média.png" alt="Maturidade vs CBO" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ02.maturidade_dit_média.png" alt="Maturidade vs DIT" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ02.maturidade_lcom_média.png" alt="Maturidade vs LCOM" style="max-width: 33%; height: auto;">
</p>
<h4 align="center">Figuras 15, 16, 17 - Maturidade vs Qualidade</h4>

---
#### 6.2.3 Gráficos da RQ03 - Qual a relação entre a atividade dos repositórios e as suas características de qualidade?

<p align="center" style="display: flex; justify-content: center; gap: 10px;">
  <img src="./docs/charts/RQ03.atividade_cbo_média.png" alt="Atividade vs CBO" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ03.atividade_dit_média.png" alt="Atividade vs DIT" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ03.atividade_lcom_média.png" alt="Atividade vs LCOM" style="max-width: 33%; height: auto;">
</p>
<h4 align="center">Figuras 18, 19, 20 - Atividade vs Qualidade</h4>

---
#### 6.2.4 Gráficos da RQ04 - Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

<p align="center" style="display: flex; justify-content: center; gap: 10px;">
  <img src="./docs/charts/RQ04.tamanho_loc_cbo_média.png" alt="Tamanho LOC vs CBO" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ04.tamanho_loc_dit_média.png" alt="Tamanho LOC vs DIT" style="max-width: 33%; height: auto;">
    <img src="./docs/charts/RQ04.tamanho_loc_lcom_média.png" alt="Tamanho LOC vs LCOM" style="max-width: 33%; height: auto;">
</p>
<p align="center" style="display: flex; justify-content: center; gap: 10px;">
  <img src="./docs/charts/RQ04.tamanho_loc_comentclasse.png" alt="Tamanho LOC vs Coment/PR" style="max-width: 33%; height: auto;">
  <img src="./docs/charts/RQ04.tamanho_loc_comentloc.png" alt="Tamanho LOC vs Coment/LOC" style="max-width: 33%; height: auto;">
</p>
<h4 align="center">Figuras 21, 22, 23, 24, 25 - Tamanho vs Qualidade</h4>

---
#### 6.2.5 Gráficos de correlação entre métricas

<p align="center">
  <img src="./docs/charts/heatmap_ck_pearson.png" alt="Heatmap Correlações Pearson">
</p>
<h4 align="center">Figura 26 - Heatmap de Correlação Pearson</h4>


<p align="center">
  <img src="./docs/charts/heatmap_ck_spearman.png" alt="Heatmap Correlações Spearman">
</p>
<h4 align="center">Figura 27 - Heatmap de Correlação Spearman</h4>

---

### 6.3. Discussão dos resultados

A seguir, serão discutidos os resultados obtidos das hipóteses informais e da correlação entre métricas, através da análise dos gráficos gerados.

#### 6.3.1 Hipóteses

| Hipótese | Expectativa                                                               | Resultado Observado                                                                                                                      |
| -------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| IH01     | Repositórios mais populares teriam melhor legibilidade e modularidade.    | ⚠️ **Parcialmente confirmada** → popularidade tem baixa a moderada correlação com modularidade/coesão, mas não garante melhor qualidade interna. |
| IH02     | Projetos maduros manteriam métricas de qualidade mais consistentes.       | ❌ **Refutada** → idade não mostrou impacto significativo na qualidade.                                                                     |
| IH03     | Repositórios com maior atividade apresentariam maior manutenibilidade.    | ⚠️ **Parcialmente confirmada** → releases frequentes associadas a melhores práticas, mas a relação é baixa a moderada.                      |
| IH04     | Repositórios maiores apresentariam desafios de manutenção e modularidade. | ✅ **Confirmada** → maior LOC correlaciona negativamente com simplicidade e coesão.                                                         |

**Principais insights:**
- **Popularidade vs Qualidade:** Os gráficos mostram que o número de estrelas (popularidade) possui baixa a moderada correlação com as métricas de qualidade (CBO, DIT, LCOM). Não há uma tendência clara de que projetos mais populares sejam, necessariamente, mais modulares ou coesos. Em alguns casos, observa-se até maior dispersão das métricas em projetos populares, indicando que a popularidade não garante melhor qualidade interna.
- **Maturidade vs Qualidade:** A idade dos repositórios apresenta correlação fraca ou quase nula com as métricas de qualidade. Os gráficos de dispersão indicam que tanto projetos antigos quanto recentes podem apresentar bons ou maus resultados em CBO, DIT e LCOM. Isso sugere que o tempo de existência do projeto, por si só, não é um fator determinante para a qualidade do código.
- **Atividade vs Qualidade:** O número de releases (atividade) mostra correlação baixa a moderada com algumas métricas de qualidade, especialmente CBO e LCOM. Projetos mais ativos tendem a apresentar uma leve tendência a melhores práticas de modularidade e coesão, mas a relação não é forte e há muitos casos fora desse padrão.
- **Tamanho vs Qualidade:** O tamanho do repositório (LOC) apresenta a correlação mais forte com as métricas de qualidade, especialmente com CBO e LCOM. Os gráficos evidenciam que repositórios maiores tendem a ter classes mais acopladas e menos coesas, indicando desafios adicionais de modularidade e design em projetos de maior escala. O número de comentários, por outro lado, não apresenta relação consistente com as métricas de qualidade.

#### 6.3.2 Correlação entre métricas

Os heatmaps de correlação sintetizam essas relações, permitindo visualizar rapidamente os pares de métricas com maior ou menor associação.

**Correlações mais fortes:**

- CBO × LOC
  - Spearman: 0.67
  - Pearson: 0.65

Forte correlação positiva: classes com mais linhas de código tendem a ter maior acoplamento. Faz sentido, pois classes grandes geralmente interagem com mais outras classes.

- LOC × LCOM
  - Spearman: 0.54
  - Pearson: 0.57

Correlação moderada: quanto mais linhas de código, maior a chance de a classe apresentar baixa coesão. Isso sugere que classes grandes muitas vezes ficam menos coesas.

**Correlações moderadas:**

- CBO × LCOM
  - Spearman: 0.40
  - Pearson: 0.37

Correlação moderada: classes mais acopladas tendem a ter menor coesão, o que indica potencial problema de design (classes com múltiplas responsabilidades).

- CBO × DIT
  - Spearman: 0.31
  - Pearson: 0.26

Correlação baixa a moderada: o acoplamento aumenta um pouco em classes mais profundas na hierarquia, mas não é uma regra forte.

**Correlações fracas ou quase nulas:**

- DIT × LCOM
  - Spearman: 0.18
  - Pearson: 0.084

Muito fraca: profundidade da herança praticamente não se relaciona com coesão da classe.

- DIT × LOC
  - Spearman: 0.23
  - Pearson: 0.21

Correlação baixa: classes mais profundas não necessariamente são maiores em linhas de código.

**Principais insights:**

- Em geral, os valores são próximos, mas o Spearman tende a dar correlações um pouco maiores em alguns pares (ex.: CBO × LCOM). Isso sugere que a relação entre as métricas pode não ser perfeitamente linear, mas sim monotônica (cresce em conjunto, ainda que não proporcionalmente).

- Quando a diferença é grande (ex.: DIT × LCOM → 0.18 vs 0.084), isso indica que existe uma tendência de crescimento em ranking (Spearman), mas não uma relação linear (Pearson).

---
## 7. Conclusão

O estudo permitiu analisar de forma sistemática a relação entre **métricas de processo** e **métricas de qualidade interna** em repositórios Java, utilizando a **GitHub API** e a ferramenta **CK Metrics Extractor**.

**🏆 Principais insights:**

- Projetos mais **populares** (maior número de estrelas e forks) mostraram correlação positiva com métricas de modularidade e coesão, confirmando parcialmente a hipótese de que maior visibilidade pode atrair boas práticas de desenvolvimento.
- A **maturidade** (idade) dos repositórios apresentou pouca influência direta sobre a qualidade do código, contrariando a expectativa inicial de que o tempo levaria a melhorias consistentes.
- A **atividade** (número de releases) tende a apresentar uma leve tendência a métricas de manutenibilidade mais favoráveis, mas a relação não é forte e há muitos casos fora desse padrão, confirmando parcialmente a hipótese de que maior atividade acarreta em melhores práticas.
- O **tamanho** (LOC) revelou ser um fator crítico: repositórios grandes enfrentam desafios adicionais de modularidade e coesão, confirmando a hipótese de que a escala pode comprometer a simplicidade.

**⚠️ Problemas e dificuldades enfrentadas:**

- Limites de requisições e paginação da API do GitHub, exigindo implementação de estratégias de retry e backoff exponencial.
- Variações e inconsistências nos repositórios, como ausência de releases ou métricas incompletas em alguns CSVs da CK Tool.
- Necessidade de normalização extensiva para padronizar dados temporais, tamanhos e métricas extraídas.
- Tempo elevado de processamento, principalmente durante a execução da CK Tool em repositórios grandes.

**🚀 Sugestões para trabalhos futuros:**

- Ampliar o conjunto de métricas, incluindo indicadores de qualidade externa (ex.: bugs reportados, tempo de resolução de issues).
- Explorar análises temporais para observar a evolução das métricas ao longo do ciclo de vida dos projetos.
- Comparar os resultados obtidos em **Java** com repositórios de outras linguagens, avaliando diferenças no perfil de qualidade.
- Implementar dashboards interativos que integrem métricas de processo e qualidade, facilitando análises exploratórias.
- Investigar relações entre métricas de rede social (ex.: número de contribuidores, interações em issues/PRs) e qualidade interna do código.

---

## 8. Referências

As seguintes fontes foram utilizadas como base para fundamentação teórica, coleta e análise dos dados:

- [📌 GitHub API Documentation – GraphQL](https://docs.github.com/en/graphql)
- [📌 GitHub API Documentation – REST](https://docs.github.com/en/rest)
- [📌 CK Metrics Tool (Chidamber & Kemerer Java Metrics)](https://ckjm.github.io/)
- [📌 Biblioteca Pandas](https://pandas.pydata.org/)
- [📌 Matplotlib Documentation](https://matplotlib.org/stable/)
- [📌 Seaborn Documentation](https://seaborn.pydata.org/)
- [📌 GitPython](https://gitpython.readthedocs.io/en/stable/)
- [📌 Maven Build Tool](https://maven.apache.org/)
- [📌 Python Official Documentation](https://docs.python.org/3/)

---

## 9. Apêndices

Os apêndices reúnem materiais de apoio e complementares ao experimento:

- 💾 **Scripts desenvolvidos**:

  - `ck_metrics.py`: roda a análise do CK
  - `main.py`: coleta os 1000 repositórios Java mais populares
    - `analyzer.py`: consolida as métricas de qualidade em uma tabela
    - `charts.py`: gera os gráficos
    - `metrics.py`: imprime métricas específicas das LMs
    - `utils.py`: funções utilitárias (pegar token do GitHub, coletar número de comentários por repositório)

- 🔗 **Consultas GraphQL** e endpoints REST utilizados na extração de dados do GitHub.
- 📊 **Planilhas e arquivos CSV**: `top_java_repos.csv` (total de repositórios coletados), `metrics.results.csv` (métricas de qualidade) e `metrics_correlations.csv` (correlação entre as métricas).
- 📈 **Gráficos e visualizações adicionais**: Scatterplot, Boxplot e Histograma.

---
