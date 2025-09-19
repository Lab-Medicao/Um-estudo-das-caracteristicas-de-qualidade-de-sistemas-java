# Relatório Técnico: Um Estudo das Características de Qualidade de Sistemas Java

## 1. Informações do grupo

- **🎓 Curso:** Engenharia de Software
- **📘 Disciplina:** Laboratório de Experimentação de Software
- **🗓 Período:** 6° Período
- **👨‍🏫 Professor(a):** Prof. Dr. João Paulo Carneiro Aramuni
- **👥 Membros do Grupo:** Ana Luiza Machado Alves, Lucas Henrique Chaves de Barros e Raquel Calazans

---

## 2. Introdução

### Análise de Qualidade de Repositórios Java com CK

Este projeto tem como objetivo analisar aspectos da qualidade interna de repositórios desenvolvidos em **Java**, correlacionando-os com características do seu processo de desenvolvimento.

A análise é realizada sob a perspectiva de métricas de produto, calculadas por meio da ferramenta **CK (Chidamber & Kemerer Java Metrics)**, contemplando atributos como:

- **Modularidade**
- **Manutenibilidade**
- **Legibilidade**

O estudo está inserido no contexto de sistemas **open-source**, onde múltiplos desenvolvedores colaboram em diferentes partes do código. Nessa abordagem, práticas como **revisão de código** e **análise estática** (via ferramentas de CI/CD) são fundamentais para mitigar riscos e preservar a qualidade do software.

**💡 Hipóteses Informais**

- **IH-01:** Repositórios mais populares tendem a apresentar melhor legibilidade e modularidade, já que atraem mais colaboradores e passam por revisões frequentes.
- **IH-02:** Projetos maduros, mantidos por mais tempo, possuem métricas de qualidade mais consistentes, refletindo evolução gradual e práticas consolidadas de desenvolvimento.
- **IH-03:** Repositórios com maior atividade (commits e pull requests frequentes) apresentam maior manutenibilidade, uma vez que o código é constantemente atualizado e ajustado.
- **IH-04:** Repositórios maiores tendem a apresentar desafios na manutenção e modularidade, já que o aumento de tamanho pode impactar negativamente a simplicidade e legibilidade do código.

#### CK Metrics Extractor

Nesse projeto, utilizamos o **CK Metrics Extractor** como ferramenta de coleta. O CK Tool é usado para análise de métricas de código-fonte Java, focando em aspectos de qualidade e complexidade. Ele automatiza a extração de métricas importantes para classes, métodos, campos e variáveis, auxiliando na avaliação e melhoria do projeto. 

A ferramenta gera um arquivo `.csv` contendo as métricas extraídas de cada repositório Java analisado. Esse arquivo será utilizado para análises estatísticas, visualização de dados e comparação entre diferentes projetos, facilitando a identificação de padrões e tendências relacionadas à qualidade do código.


#### Métricas analisadas pelo CK

##### 1. Class Metrics

- **LOC (Lines of Code):** Conta o número de linhas de código na classe. Ajuda a identificar classes muito grandes ou complexas.
- **WMC (Weighted Methods per Class):** Soma das complexidades dos métodos. Classes com WMC alto podem ser difíceis de manter.
- **DIT (Depth of Inheritance Tree):** Mede a profundidade da herança. Classes muito profundas podem ser difíceis de entender.
- **NOC (Number of Children):** Número de subclasses. Indica o nível de reutilização e extensão da classe.
- **CBO (Coupling Between Objects):** Mede o acoplamento entre classes. Alto acoplamento pode dificultar a manutenção.

### 2. Method Metrics

- **LOC:** Linhas de código por método. Métodos longos podem ser difíceis de testar e manter.
- **Cyclomatic Complexity:** Mede o número de caminhos independentes. Métodos complexos são mais propensos a erros.
- **Number of Parameters:** Muitos parâmetros podem indicar métodos com responsabilidades excessivas.

### 3. Field Metrics

- **Number of Fields:** Quantidade de atributos na classe. Muitas variáveis podem indicar alta complexidade.
- **Field Visibility:** Avalia o nível de encapsulamento dos campos.

### 4. Variable Metrics

- **Number of Local Variables:** Quantidade de variáveis locais por método. Muitos podem indicar métodos complexos.
- **Variable Scope:** Analisa o escopo das variáveis para identificar possíveis melhorias de design.

---

## 3. Tecnologias e ferramentas utilizadas

- **💻 Linguagem de Programação:** Python 3.x
- **🛠 Frameworks:** CK Tool, GraphQL
- **🌐 API utilizada:** GitHub GraphQL API
- **📦 Dependências/Bibliotecas:**
  - Python: pandas, matplotlib, seaborn, gitpython, requests, keyring, tdqm
  - Java 21
  - Maven

---

## 4. Metodologia

O experimento foi conduzido em quatro etapas principais: **coleta de dados**, **extração de métricas de qualidade**, **análise dos dados** e **visualização dos resultados**.

### 4.1 Seleção e coleta de dados

- Foram coletados os **top-1.000 repositórios em Java** mais populares do GitHub, utilizando a **GitHub GraphQL API**.
- Critério de seleção: repositórios classificados pela quantidade de estrelas.
- A coleta foi implementada no script `main.py`.

### 4.2 Extração de métricas de qualidade

- Os repositórios coletados foram processados com a ferramenta **CK** (Chidamber & Kemerer Metrics), executada via Java 21 e Maven.
- O script `ck_metrics.py` foi responsável por chamar a ferramenta CK e consolidar os arquivos `.csv` gerados.
- Métricas de qualidade consideradas:
  - **CBO:** Coupling Between Objects
  - **DIT:** Depth of Inheritance Tree
  - **LCOM:** Lack of Cohesion of Methods

### 4.3 Definição de métricas de processo

- Para responder às questões de pesquisa, também foram coletadas métricas de processo:
  - **Popularidade:** número de estrelas
  - **Tamanho:** linhas de código (LOC) e linhas de comentários
  - **Atividade:** número de releases
  - **Maturidade:** idade (em anos) do repositório

### 4.4 Análise e filtragem de dados

- Os dados brutos foram organizados e filtrados no script `analizy.py`.
- Foram realizadas operações de limpeza e sumarização dos resultados de diferentes níveis de análise (classes, métodos e pacotes).

### 4.5 Visualização dos resultados

- Gráficos e distribuições das métricas foram gerados utilizando **Seaborn**.
- Essa etapa permitiu correlacionar as métricas de qualidade com popularidade, tamanho, atividade e maturidade dos repositórios.

<img width="768" height="62" alt="image" src="https://github.com/user-attachments/assets/9eb77bec-e399-454f-b8ab-d0b20da74092" />

---

## 5. Questões de pesquisa

As questões de pesquisa (RQs) deste estudo buscam analisar a relação entre métricas de processo e métricas de qualidade de repositórios Java.

**🔍 Questões de Pesquisa - Research Questions (RQs):**

| RQ   | Pergunta                                                                                      | Métrica de Processo                               | Métricas de Qualidade (CK) | Código da Métrica |
| ---- | --------------------------------------------------------------------------------------------- | ------------------------------------------------- | -------------------------- | ----------------- |
| RQ01 | Qual a relação entre a **popularidade** dos repositórios e suas características de qualidade? | ⭐ Número de estrelas                             | CBO, DIT, LCOM             | RQ01              |
| RQ02 | Qual a relação entre a **maturidade** dos repositórios e suas características de qualidade?   | 🕰 Idade (anos)                                    | CBO, DIT, LCOM             | RQ02              |
| RQ03 | Qual a relação entre a **atividade** dos repositórios e suas características de qualidade?    | 📦 Número de releases                             | CBO, DIT, LCOM             | RQ03              |
| RQ04 | Qual a relação entre o **tamanho** dos repositórios e suas características de qualidade?      | 📏 Linhas de código (LOC) e linhas de comentários | CBO, DIT, LCOM             | RQ04              |

---

## 6. Resultados

Apresente os resultados obtidos, com tabelas e gráficos sempre que possível.

---

### 6.1 Métricas

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

### 6.2 Distribuição por categoria

Para métricas categóricas, como linguagem de programação, faça contagens e tabelas de frequência:

| Linguagem     | Quantidade de Repositórios |
| ------------- | -------------------------- |
| 🐍 Python     | 350                        |
| 💻 JavaScript | 300                        |
| ☕ Java       | 200                        |
| 📦 Outros     | 150                        |

---

### 6.3 Relação das RQs com as Métricas

| RQ   | Pergunta                                                                                                                                      | Métrica utilizada                                                                                           | Código                 |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------- |
| RQ01 | Sistemas populares são maduros/antigos?                                                                                                       | 🕰 Idade do Repositório (calculado a partir da data de criação)                                              | LM01                   |
| RQ02 | Sistemas populares recebem muita contribuição externa?                                                                                        | ✅ Total de Pull Requests Aceitas                                                                           | LM02                   |
| RQ03 | Sistemas populares lançam releases com frequência?                                                                                            | 📦 Total de Releases                                                                                        | LM03                   |
| RQ04 | Sistemas populares são atualizados com frequência?                                                                                            | ⏳ Tempo desde a Última Atualização (dias)                                                                  | LM04                   |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares?                                                                                | 💻 Linguagem primária de cada repositório                                                                   | AM01                   |
| RQ06 | Sistemas populares possuem alto percentual de issues fechadas?                                                                                | 📋 Razão entre número de issues fechadas pelo total de issues                                               | LM05                   |
| RQ07 | Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência? | ✅ Pull Requests Aceitas, 📦 Número de Releases, ⏳ Tempo desde a Última Atualização, 💻 Linguagem primária | LM02, LM03, LM04, AM01 |

---

### 6.4 Sugestões de gráficos

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

### 6.5 Estatísticas Descritivas

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

## 7. Discussão

Nesta seção, compare os resultados obtidos com as hipóteses informais levantadas pelo grupo no início do experimento.

- **✅ Confirmação ou refutação das hipóteses**: identifique quais hipóteses foram confirmadas pelos dados e quais foram refutadas.
- **❌ Explicações para resultados divergentes**: caso algum resultado seja diferente do esperado, tente levantar possíveis causas ou fatores que possam ter influenciado.
- **🔍 Padrões e insights interessantes**: destaque tendências ou comportamentos relevantes observados nos dados que não haviam sido previstos nas hipóteses.
- **📊 Comparação por subgrupos (opcional)**: se houver segmentação dos dados (ex.: por linguagem de programação, tamanho do repositório), discuta como os resultados se comportam em cada grupo.

> Relacione sempre os pontos observados com as hipóteses informais definidas na introdução, fortalecendo a análise crítica do experimento.

---

## 8. Conclusão

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

## 9. Referências

Liste as referências bibliográficas ou links utilizados.

- [📌 GitHub API Documentation](https://docs.github.com/en/graphql)
- [📌 CK Metrics Tool](https://ckjm.github.io/)
- [📌 Biblioteca Pandas](https://pandas.pydata.org/)
- [📌 Power BI](https://docs.microsoft.com/en-us/power-bi/fundamentals/service-get-started)

---

## 10. Apêndices

- 💾 Scripts utilizados para coleta e análise de dados.
- 🔗 Consultas GraphQL ou endpoints REST.
- 📊 Planilhas e arquivos CSV gerados.

---
