# Relatório de Pesquisa: RQs 01 a 03 (Amostra de 100 Repositórios)

## 1. Metodologia e Parâmetros de Coleta

* **Tamanho da Amostra:** 100 repositórios com maior número de estrelas no GitHub.
* **Mecanismo de Extração:** API GraphQL do GitHub v4, com requisições paginadas em lotes (*batch size* de 10) utilizando a busca `stars:>10000 sort:stars-desc`.
* **Dataset Gerado:** `repositorios_100.csv`.

---

## 2. Tabela Resumo das Estatísticas Descritivas

| Métrica Estatística | RQ 01: Idade (anos) | RQ 02: PRs Aceitas | RQ 03: Total de Releases |
| :--- | :--- | :--- | :--- |
| **Mediana** | **8,27** | **1.255,0** | **15,0** |
| **Média** | 7,67 | 7.311,2 | 133,89 |
| **Desvio Padrão** | 4,81 | 14.123,65 | 243,74 |
| **Primeiro Quartil (Q1)** | 3,29 | 243,0 | 0,0 |
| **Terceiro Quartil (Q3)** | 11,66 | 7.033,75 | 167,25 |
| **Intervalo Interquartil (IQR)** | 8,37 | 6.790,75 | 167,25 |
| **Valor Mínimo** | 0,37 (`ultraworkers/claw-code`) | 0 (`awesome-selfhosted`, `linux`, `FreeDomain`) | 0 (41 repositórios) |
| **Valor Máximo** | 16,96 (`ohmyzsh/ohmyzsh`) | 73.464 (`rust-lang/rust`) | 1.000 (`llama.cpp`, `next.js`, `electron`, `langchain`) |

---

## RQ 01: Sistemas populares são maduros/antigos?

### 1. Hipótese Informal
* **Hipótese:** Repositórios populares no GitHub tendem a ser maduros e antigos (em média mais de 6 anos de histórico).
* **Justificativa:** A obtenção de volumes expressivos de estrelas (*stargazers*) decorre predominantemente de um processo gradual de consolidação na comunidade, maturação técnica e efeitos de rede ao longo dos anos.

### 2. Metodologia e Definição da Métrica
* **Métrica:** Idade do repositório calculada a partir da data de criação (`createdAt`).
* **Fórmula de Cálculo:**
  $$\text{Idade (em anos)} = \frac{\text{Data da Coleta} - \text{createdAt}}{365.25}$$

### 3. Resultados ($N = 100$)
* **Mediana:** **8,27 anos**
* **Média:** 7,67 anos (desvio padrão de 4,81 anos)
* **Faixa Interquartil (IQR):** 3,29 a 11,66 anos (IQR = 8,37 anos)
* **Extremos:** `ohmyzsh/ohmyzsh` (16,96 anos) vs. `ultraworkers/claw-code` (0,37 anos)

### 4. Discussão (Hipótese vs. Resultado)
A hipótese foi **confirmada**. A mediana de **8,27 anos** demonstra que o topo do GitHub é amplamente dominado por ecossistemas e ferramentas veteranas com mais de 8 a 16 anos de estrada (como `ohmyzsh`, `three.js` e `rust-lang/rust`). 

Entretanto, observou-se uma cauda inferior de projetos com crescimento acelerado (menos de 1 ano de existência, como `ultraworkers/claw-code`, `garrytan/gstack` e `mattpocock/skills`), impulsionados pelo interesse recente em ferramentas e recursos de IA generativa.

---

## RQ 02: Sistemas populares recebem muita contribuição externa?

### 1. Hipótese Informal
* **Hipótese:** Repositórios populares apresentam um volume elevado de contribuições externas aceitas.
* **Justificativa:** O alto alcance e visibilidade atraem desenvolvedores ativos motivados a submeter correções de bugs, melhorias de infraestrutura e novas funcionalidades.

### 2. Metodologia e Definição da Métrica
* **Métrica:** Quantidade total de Pull Requests aceitas (estado `MERGED`).
* **Consulta GraphQL:** `pullRequests(states: MERGED) { totalCount }`.

### 3. Resultados ($N = 100$)
* **Mediana:** **1.255,0 PRs aceitas**
* **Média:** 7.311,2 PRs aceitas (desvio padrão de 14.123,65)
* **Faixa Interquartil (IQR):** 243,0 a 7.033,75 PRs (IQR = 6.790,75 PRs)
* **Extremos:** `rust-lang/rust` (73.464 PRs) vs. `torvalds/linux` (0 PRs)

### 4. Discussão (Hipótese vs. Resultado)
A hipótese foi **confirmada**. A mediana de **1.255 PRs aceitas** comprova a alta abertura comunitária da maioria dos projetos populares, com gigantes do ecossistema superando dezenas de milhares de contribuições integradas (`rust-lang/rust` com 73.464 PRs, `kubernetes/kubernetes` com 65.646 PRs e `microsoft/vscode` com 51.947 PRs).

Casos com 0 a 1 PR aceita (como `torvalds/linux` e `golang/go`) não representam falta de contribuição, mas sim particularidades de governança: o fluxo de submissão ocorre fora do GitHub (via *Mailing Lists* no Linux e *Gerrit* no Go), servindo o repositório no GitHub apenas como espelho (*mirror*).

---

## RQ 03: Sistemas populares lançam releases com frequência?

### 1. Hipótese Informal
* **Hipótese:** Repositórios populares mantêm uma cadência regular de publicação de releases formais.
* **Justificativa:** Softwares com ampla base instalada dependem de versões demarcadas (*tags/releases*) e versionamento semântico para garantir estabilidade e previsibilidade de atualização.

### 2. Metodologia e Definição da Métrica
* **Métrica:** Quantidade total de releases publicadas no repositório.
* **Consulta GraphQL:** `releases { totalCount }`.

### 3. Resultados ($N = 100$)
* **Mediana:** **15,0 releases**
* **Média:** 133,89 releases (desvio padrão de 243,74)
* **Faixa Interquartil (IQR):** 0,0 a 167,25 releases (IQR = 167,25 releases)
* **Repositórios sem Releases (0):** **41% da amostra** (41 repositórios)
* **Máximo de Releases:** 1.000 releases (limite atingido por `llama.cpp`, `next.js`, `electron` e `langchain`)

### 4. Discussão (Hipótese vs. Resultado)
A hipótese foi **parcialmente confirmada**, apresentando forte comportamento bimodal:

1. **Repositórios de Conteúdo e Listas (41% com 0 releases):** Projetos como `build-your-own-x`, `awesome`, `public-apis` e `free-programming-books` funcionam como repositórios informacionais e não distribuem executáveis ou bibliotecas, atualizando o conteúdo diretamente no branch principal sem emitir releases.
2. **Bibliotecas, Ferramentas e Frameworks:** Softwares consolidados utilizam ativamente o mecanismo de releases do GitHub (com dezenas a centenas de lançamentos), demonstrando ciclos contínuos de entrega de versão.