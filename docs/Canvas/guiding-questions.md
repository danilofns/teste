# Resolução das Guiding Questions

Este documento tem como objetivo registrar as **respostas, decisões técnicas e alinhamentos da equipe** para cada uma das perguntas orientadoras do projeto.

---

## 1. Dados

### 1.1. Qual será o formato de dado recebido do usuário?

**Decisão:**  
Link de uma publicação do Instagram.

**Detalhes técnicos:**  
O usuário fornecerá o link da publicação, obtido diretamente por meio da opção de **compartilhamento** disponibilizada pelo Instagram.

---

### 1.2. De qual modo as notícias das nossas fontes divergem das encontradas no Instagram?

**Resposta / Diagnóstico:**

A definir.

**Exemplos observados:**

A definir.

---

### 1.3. De quais fontes vamos obter nossos dados base e como validar sua confiabilidade?

**Fonte base definida:**  

Utilizaremos o **Portal de Dados Abertos do Tribunal Superior Eleitoral (TSE)** como uma das principais fontes oficiais de dados.

- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/dataset/candidatos-2026)

**Critérios de confiabilidade e validação:**

A definir.

---

## 2. Usuário

### 2.1. Como será o fluxo de uso da nossa aplicação?

O fluxo de utilização da aplicação será composto pelas seguintes etapas:

1. O usuário acessa a plataforma e insere o **link da publicação do Instagram** que deseja verificar.
2. O sistema valida o link e realiza a extração das informações relevantes da publicação, como **imagem, texto e legenda**.
3. O sistema apresenta as informações extraídas para que o usuário possa confirmar se o conteúdo foi obtido corretamente.
4. Após a confirmação, o sistema encaminha os dados para análise.
5. O modelo compara a alegação presente na publicação com as **propostas de governo e informações oficiais** disponíveis nas fontes utilizadas pelo projeto.
6. A aplicação processa os resultados e classifica a alegação.
7. O usuário visualiza o **veredito e sua justificativa**, juntamente com as evidências utilizadas na análise.
8. O usuário pode fornecer um **feedback sobre a resposta** ou realizar uma nova consulta.

**Diagrama do fluxo de uso:**

![Diagrama de Fluxo](../imgs/Fluxo.png)

---

### 2.2. Como vamos receber feedbacks do usuário?

**Canal de coleta:**  

O feedback será coletado por meio de um **formulário disponibilizado após a apresentação do resultado da análise**.

**Métricas e perguntas de avaliação:**

A definir.

---

## 3. Modelo

### 3.1. Quais métricas vamos apresentar para explicar o pensamento da IA?

**Abordagem de explicabilidade (XAI):**

A definir.

**Métricas e indicadores exibidos na interface:**

A definir.

---

### 3.2. Como vamos evitar que o modelo seja enviesado?

**Estratégias de mitigação de viés:**

A definir.

**Processo de auditoria e testes:**

A definir.

---

### 3.3. Como vamos hospedar o modelo?

**Infraestrutura / plataforma escolhida:**

A definir.

**Estimativa de custos e latência:**

A definir.

---

## 4. Ética

### 4.1. Como vamos diferenciar notícias políticas de informações da vida pessoal do político?

**Critérios de escopo e filtragem:**

A aplicação terá como foco exclusivamente informações relacionadas a **propostas, planos de governo e posicionamentos políticos relevantes para a verificação da alegação apresentada**.

Informações relacionadas exclusivamente à vida pessoal do político, sem relação direta com uma proposta ou posicionamento político, não farão parte do escopo principal da análise.

**Tratamento de casos limítrofes:**

A definir.

---

## 5. Produção

### 5.1. Qual modelo vamos utilizar como base?

**Modelo selecionado:**  
[Pixtral-12B-2409](https://huggingface.co/mistralai/Pixtral-12B-2409)

**Justificativa da escolha:**

A equipe escolheu o **Pixtral-12B-2409** devido às suas capacidades de compreensão contextual e ao suporte a entradas multimodais.

No contexto da aplicação, o modelo poderá auxiliar na análise das relações semânticas entre as **descrições textuais das publicações do Instagram** e as **propostas oficiais utilizadas como referência**, contribuindo para a identificação de possíveis distorções ou inconsistências entre a alegação e as informações oficiais.

Além disso, por possuir arquitetura multimodal, o modelo mantém a possibilidade de trabalhar diretamente com **imagens e capturas de tela** em etapas futuras do projeto, evitando a necessidade de substituir a arquitetura do modelo caso essa funcionalidade seja incorporada posteriormente.

---

## 📌 Resumo das decisões

| Área | Decisão |
|---|---|
| **Entrada do usuário** | Link de uma publicação do Instagram |
| **Extração de dados** | Imagem, texto e legenda da publicação |
| **Fonte oficial de dados** | Portal de Dados Abertos do TSE |
| **Feedback** | Formulário após a análise |
| **Modelo base** | Pixtral-12B-2409 |
| **Multimodalidade** | Suporte para imagens e texto |
| **Escopo** | Verificação de alegações relacionadas a propostas e posicionamentos políticos |
| **Hospedagem** | A definir |
| **Métricas XAI** | A definir |
| **Mitigação de viés** | A definir |