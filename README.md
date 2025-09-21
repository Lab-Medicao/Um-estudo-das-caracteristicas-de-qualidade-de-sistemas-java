# 📝 [LAB02] Relatório Técnico: Um Estudo das Características de Qualidade de Sistemas Java

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

### 2.1. Questões de Pesquisa (Research Questions – RQs)

As questões de pesquisa (RQs) deste estudo buscam analisar a relação entre métricas de processo e métricas de qualidade de repositórios Java.

**🔍 Questões de Pesquisa - Research Questions (RQs):**

| RQ   | Pergunta                                                                                      | Métrica de Processo                               | Métricas de Qualidade (CK) | Código da Métrica |
| ---- | --------------------------------------------------------------------------------------------- | ------------------------------------------------- | -------------------------- | ----------------- |
| RQ01 | Qual a relação entre a **popularidade** dos repositórios e suas características de qualidade? | ⭐ Número de estrelas                             | CBO, DIT, LCOM             | RQ01              |
| RQ02 | Qual a relação entre a **maturidade** dos repositórios e suas características de qualidade?   | 🕰 Idade (anos)                                    | CBO, DIT, LCOM             | RQ02              |
| RQ03 | Qual a relação entre a **atividade** dos repositórios e suas características de qualidade?    | 📦 Número de releases                             | CBO, DIT, LCOM             | RQ03              |
| RQ04 | Qual a relação entre o **tamanho** dos repositórios e suas características de qualidade?      | 📏 Linhas de código (LOC) e linhas de comentários | CBO, DIT, LCOM             | RQ04              |

### 2.2. Hipóteses Informais (Informal Hypotheses – IH)

As **Hipóteses Informais** foram elaboradas a partir das RQs, estabelecendo expectativas sobre os resultados esperados do estudo:

**💡 Hipóteses Informais - Informal Hypotheses (IH):**

| IH   | Descrição                                                                                                                                                                        |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IH01 | Repositórios mais populares tendem a apresentar melhor legibilidade e modularidade, já que atraem mais colaboradores e passam por revisões frequentes.                           |
| IH02 | Projetos maduros, mantidos por mais tempo, possuem métricas de qualidade mais consistentes, refletindo evolução gradual e práticas consolidadas de desenvolvimento.              |
| IH03 | Repositórios com maior atividade (commits e pull requests frequentes) apresentam maior manutenibilidade, uma vez que o código é constantemente atualizado e ajustado.            |
| IH04 | Repositórios maiores tendem a apresentar desafios na manutenção e modularidade, já que o aumento de tamanho pode impactar negativamente a simplicidade e legibilidade do código. |

---

## 3. Tecnologias e ferramentas utilizadas

- **💻 Linguagem de Programação:** Python 3.x
- **🛠 Frameworks:** CK Tool, GraphQL
- **🌐 API utilizada:** GitHub GraphQL API, GitHub REST API
- **📦 Dependências/Bibliotecas:**
  - Python: pandas, matplotlib, seaborn, gitpython, requests, keyring, tqdm
  - Java 21
  - Maven

---

## 4. Metodologia

O experimento foi conduzido em cinco etapas principais: **coleta de dados**, **extração de métricas de processo e de qualidade**, **sumarização**, **análise dos dados** e **visualização dos resultados**.

---

### 4.1 Coleta de dados

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

### 4.2 Filtragem e paginação

- Devido ao limite de requisições da **GitHub API**, a coleta exigiu o uso de uma **paginação** de **25 repositórios** por página, permitindo recuperar lotes sucessivos de dados sem perda de registros.
- Para maior confiabilidade, foi implementado um sistema de **retry com backoff exponencial** para lidar com erros temporários ou rate limiting da API.
- ⏱ O tempo médio estimado de coleta foi de aproximadamente **3 minutos e 38 segundos** para o conjunto completo de repositórios.

---

### 4.3 Normalização e pré-processamento

- Após a coleta, os dados foram organizados em um **banco/tabulação unificada**, estruturada por repositório.
- Foram aplicadas etapas de pré-processamento:
  - **Conversão de datas** para formato padronizado (ISO 8601) e cálculo de intervalos (ex.: idade em anos, tempo desde a última atualização em dias).
  - Para auxiliar na análise das métricas de processo, o script também calcula informações como **idade** (`age_years`) e o **tamanho total em bytes** (`size_bytes`) do repositório com base nos dados obtidos pela API.
  - Os dados coletados são organizados em um arquivo CSV (`top_java_repos.csv`) para facilitar análise posterior.

---

### 4.4 Métricas Analisadas

Métricas de Qualidade (CK Tool):

- **LCOM (Lack of Cohesion of Methods):** Mede o grau de coesão dos métodos de uma classe. Valores altos indicam que os métodos são pouco relacionados, sugerindo necessidade de refatoração.
- **DIT (Depth of Inheritance Tree):** Mede a profundidade da herança. Classes muito profundas podem ser difíceis de entender.
- **CBO (Coupling Between Objects):** Mede o acoplamento entre classes. Alto acoplamento pode dificultar a manutenção.

Métricas de Processo:

- **Popularidade:** número de estrelas
- **Tamanho:** linhas de código (LOC) e linhas de comentários
- **Atividade:** número de releases
- **Maturidade:** idade (em anos) do repositório

---

### 4.5 Extração das Métricas

#### 4.5.1 Coleta de repositórios

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

#### 4.5.2 Extração de métricas com CK Tool

Após obter o código-fonte:

- Executa o **CK Tool (Java JAR)** no repositório.
- CK Tool gera métricas de classe, método, campo e variável em CSV:
  - **Classe** (`class.csv`): acoplamento (CBO, fan-in/fan-out), complexidade (WMC, RFC), coesão (LCOM, TCC), herança (DIT, NOC), quantidade de métodos/campos, LOC, estruturas de controle, literais, operadores, classes internas, lambdas, etc.
  - **Método** (`method.csv`): complexidade, acoplamento, LOC, parâmetros, variáveis, métodos invocados, loops, comparações, try/catch, literais e operadores.
  - **Campo** (`field.csv`): informações sobre variáveis de classe.
  - **Variável** (`variable.csv`): uso de variáveis.
- Garante que apenas CSVs existentes e não vazios sejam processados.

#### 4.5.3 Exibição e filtragem de métricas

O script contém funções para carregar e imprimir métricas de cada CSV:

- `load_and_print_class_metrics`
- `load_and_print_method_metrics`
- `load_and_print_field_metrics`
- `load_and_print_variable_metrics`

Observações importantes:

- Filtra apenas colunas relevantes para análise.
- Imprime apenas as primeiras linhas para visualização rápida.
- Garante robustez contra arquivos corrompidos ou vazios.

#### 4.5.4 Gestão de repositórios já processados

Antes de processar, verifica se já existem CSVs na pasta ck_output. Se sim, pula o repositório para evitar duplicação. Isso ajuda a manter controle de tempo estimado restante usando média do tempo por repositório.

#### 4.5.5 Robustez e tolerância a falhas

O script adota várias estratégias para lidar com problemas:

- Timeouts ao baixar ZIP, acessar API ou rodar CK.
- Fallbacks (ZIP → Git clone, git ls-remote → GitHub API → default main).
- Tratamento de erros em CSVs (ignora arquivos vazios ou corrompidos).
- Limpeza de arquivos temporários (temp_extract, ZIP baixado).
- Continuação do processamento mesmo que algum repositório falhe.

---

### 4.6 Sumarização dos Dados

- Os dados brutos foram organizados e filtrados pelo script `analyzer.py`.
- Foram realizadas operações de limpeza (linhas vazias) e sumarização dos resultados especificamente para classes, agrupando um resumo dos resultados em uma única tabela.
- Foi calculado a **média**, **mediana**, **desvio padrão** e o valor **máximo** e **mínimo** para as métricas de qualidade.

---

### 4.7 Métricas

Inclua métricas relevantes de repositórios do GitHub, separando **métricas do laboratório** e **métricas adicionais trazidas pelo grupo**:

#### 📊 Métricas de Laboratório - Lab Metrics (LM)

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

#### 💡 Métricas adicionais trazidas pelo grupo - Additional Metrics (AM)

| Código | Métrica                           | Descrição                                                                         |
| ------ | --------------------------------- | --------------------------------------------------------------------------------- |
| AM01   | 💻 Linguagem Primária             | Linguagem de programação principal do repositório (ex.: Python, JavaScript, Java) |
| AM02   | 🔗 Forks vs Pull Requests Aceitas | Relação entre número de forks e pull requests aceitas                             |
| AM03   | 📈 Evolução Temporal              | Evolução temporal de releases e pull requests aceitas                             |
| AM04   | 🌟 Big Numbers                    | Métricas com valores expressivos (commits, branches, stars, releases)             |

> Obs.: Adapte ou acrescente métricas conforme o seu dataset.

---

### 4.8 Cálculo de métricas

- As métricas definidas na seção **4.4** foram obtidas a partir de dados brutos retornados pela **GitHub API**.
- Para cada métrica, foram aplicadas operações de transformação simples, tais como:
  - **Diferença de datas** → cálculo da idade do repositório e tempo desde a última atualização.
  - **Contagens absolutas** → número de pull requests aceitas, releases, forks e estrelas.
  - **Proporções** → percentual de issues fechadas em relação ao total.
  - **Identificação categórica** → linguagem primária de cada repositório.
- Em alguns casos, os valores foram agregados em séries temporais para observar **evolução ao longo do tempo** (ex.: releases e pull requests).
- Além das métricas individuais, foi proposto um **índice composto de popularidade**, calculado como uma **combinação linear ponderada** de métricas representativas (⭐ estrelas, 🍴 forks, 📦 releases, ✅ pull requests aceitas). Esse índice foi utilizado para ranqueamento complementar e comparação entre repositórios.

---

### 4.9 Ordenação e análise inicial

- Repositórios ordenados pelo **índice composto de popularidade** ou, alternativamente, pelo número de estrelas.
- A análise inicial foi conduzida a partir de **valores medianos, distribuições** e **contagem de categorias** (como linguagens e tipos de contribuições).
- Essa etapa teve como objetivo fornecer uma **visão exploratória** do dataset, identificando padrões gerais antes de análises mais detalhadas.

---

### 4.10. Relação das RQs com as Métricas

As **Questões de Pesquisa (Research Questions – RQs)** foram associadas a métricas específicas, previamente definidas na seção de métricas (Seção 4.4), garantindo que a investigação seja **sistemática e mensurável**.

A tabela a seguir apresenta a relação entre cada questão de pesquisa e as métricas utilizadas para sua avaliação:

**🔍 Relação das RQs com Métricas:**

| RQ   | Pergunta                                                                                                                                      | Métrica utilizada                                                                                           | Código da Métrica      |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------- |
| RQ01 | Sistemas populares são maduros/antigos?                                                                                                       | 🕰 Idade do repositório (calculado a partir da data de criação)                                              | LM01                   |
| RQ02 | Sistemas populares recebem muita contribuição externa?                                                                                        | ✅ Total de Pull Requests Aceitas                                                                           | LM02                   |
| RQ03 | Sistemas populares lançam releases com frequência?                                                                                            | 📦 Total de Releases                                                                                        | LM03                   |
| RQ04 | Sistemas populares são atualizados com frequência?                                                                                            | ⏳ Tempo desde a última atualização (dias)                                                                  | LM04                   |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares?                                                                                | 💻 Linguagem primária de cada repositório                                                                   | AM01                   |
| RQ06 | Sistemas populares possuem um alto percentual de issues fechadas?                                                                             | 📋 Razão entre número de issues fechadas pelo total de issues                                               | LM05                   |
| RQ07 | Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência? | ✅ Pull Requests Aceitas, 📦 Número de Releases, ⏳ Tempo desde a Última Atualização, 💻 Linguagem primária | LM02, LM03, LM04, AM01 |

---

## 5. Resultados

Apresente os resultados obtidos, com tabelas e gráficos.

---

### 5.1 Distribuição por categoria

Para métricas categóricas, como linguagem de programação, faça contagens e tabelas de frequência:

| Linguagem     | Quantidade de Repositórios |
| ------------- | -------------------------- |
| 🐍 Python     | 350                        |
| 💻 JavaScript | 300                        |
| ☕ Java       | 200                        |
| 📦 Outros     | 150                        |

---

### 5.2 Estatísticas Descritivas

Apresente as estatísticas descritivas das métricas analisadas, permitindo uma compreensão mais detalhada da distribuição dos dados.

| Métrica                                    | Código | Média | Mediana | Moda | Desvio Padrão | Mínimo | Máximo |
| ------------------------------------------ | ------ | ----- | ------- | ---- | ------------- | ------ | ------ |
| 🕰 Idade do Repositório (anos)              | LM01   | X     | Y       | Z    | A             | B      | C      |
| ✅ Pull Requests Aceitas                   | LM02   | X     | Y       | Z    | A             | B      | C      |
| 📦 Número de Releases                      | LM03   | X     | Y       | Z    | A             | B      | C      |
| ⏳ Tempo desde a Última Atualização (dias) | LM04   | X     | Y       | Z    | A             | B      | C      |
| 📋 Percentual de Issues Fechadas (%)       | LM05   | X     | Y       | Z    | A             | B      | C      |
| ⭐ Número de Estrelas (Stars)              | LM06   | X     | Y       | Z    | A             | B      | C      |
| 🍴 Número de Forks                         | LM07   | X     | Y       | Z    | A             | B      | C      |
| 📏 Tamanho do Repositório (LOC)            | LM08   | X     | Y       | Z    | A             | B      | C      |

> 💡 Dica: Inclua gráficos como histogramas ou boxplots junto com essas estatísticas para facilitar a interpretação.

---

### 5.3 Gráficos

Para criar visualizações das métricas, recomenda-se utilizar como referência o projeto **Seaborn Samples**:

- 🔗 Repositório: [Projeto Seaborn Samples](https://github.com/joaopauloaramuni/laboratorio-de-experimentacao-de-software/tree/main/PROJETOS/Projeto%20Seaborn%20Samples)

- **📊 Histograma**: `grafico_histograma.png` → distribuição de idade, PRs aceitas ou estrelas.
- **📈 Boxplot**: `grafico_boxplot.png` → dispersão de métricas como forks, issues fechadas ou LOC.
- **📊 Gráfico de Barras**: `grafico_barras.png` → comparação de métricas entre linguagens.
- **🥧 Gráfico de Pizza**: `grafico_pizza.png` → percentual de repositórios por linguagem.
- **📈 Gráfico de Linha**: `grafico_linha.png` → evolução de releases ou PRs ao longo do tempo.
- **🔹 Scatterplot / Dispersão**: `grafico_dispersao.png` → relação entre estrelas e forks.
- **🌡 Heatmap**: `grafico_heatmap.png` → correlação entre métricas (idade, PRs, stars, forks, issues).
- **🔗 Pairplot**: `grafico_pairplot.png` → análise de múltiplas métricas simultaneamente.
- **🎻 Violin Plot**: `grafico_violin.png` → distribuição detalhada de métricas por subgrupo.
- **📊 Barras Empilhadas**: `grafico_barras_empilhadas.png` → comparação de categorias dentro de métricas.

> 💡 Dica: combine tabelas e gráficos para facilitar a interpretação e evidenciar padrões nos dados.

---

### 5.4. Discussão dos resultados

Nesta seção, compare os resultados obtidos com as hipóteses informais levantadas pelo grupo no início do experimento.

- **✅ Confirmação ou refutação das hipóteses**: identifique quais hipóteses foram confirmadas pelos dados e quais foram refutadas.
- **❌ Explicações para resultados divergentes**: caso algum resultado seja diferente do esperado, tente levantar possíveis causas ou fatores que possam ter influenciado.
- **🔍 Padrões e insights interessantes**: destaque tendências ou comportamentos relevantes observados nos dados que não haviam sido previstos nas hipóteses.
- **📊 Comparação por subgrupos (opcional)**: se houver segmentação dos dados (ex.: por linguagem de programação, tamanho do repositório), discuta como os resultados se comportam em cada grupo.

> Relacione sempre os pontos observados com as hipóteses informais definidas na introdução, fortalecendo a análise crítica do experimento.

---

## 6. Conclusão

Resumo das principais descobertas do laboratório.

- **🏆 Principais insights:**

  - Big numbers encontrados nos repositórios, popularidade e métricas destacadas.
  - Descobertas relevantes sobre padrões de contribuição, releases, issues fechadas ou linguagens mais utilizadas.
  - Confirmações ou refutações das hipóteses informais levantadas pelo grupo.

- **⚠️ Problemas e dificuldades enfrentadas:**

  - Limitações da API do GitHub e paginação de grandes volumes de dados.
  - Normalização e tratamento de dados inconsistentes ou ausentes.
  - Desafios com cálculos de métricas ou integração de múltiplos arquivos CSV.

- **🚀 Sugestões para trabalhos futuros:**
  - Analisar métricas adicionais ou aprofundar correlações entre métricas de qualidade e métricas de processo.
  - Testar outras linguagens de programação ou frameworks.
  - Implementar dashboards interativos para visualização de grandes volumes de dados.
  - Explorar métricas de tendências temporais ou evolução de repositórios ao longo do tempo.

---

## 7. Referências

Liste as referências bibliográficas ou links utilizados.

- [📌 GitHub API Documentation](https://docs.github.com/en/graphql)
- [📌 CK Metrics Tool](https://ckjm.github.io/)
- [📌 Biblioteca Pandas](https://pandas.pydata.org/)
- [📌 Power BI](https://docs.microsoft.com/en-us/power-bi/fundamentals/service-get-started)

---

## 8. Apêndices

- 💾 Scripts utilizados para coleta e análise de dados.
- 🔗 Consultas GraphQL ou endpoints REST.
- 📊 Planilhas e arquivos CSV gerados.

---
