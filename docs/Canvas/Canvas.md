# CANVAS — DA PERGUNTA CERTA AO OBJETIVO CERTO

## 1. Guiding Questions

Este tópico trata das questões elaboradas para guiar o processo de desenvolvimento do projeto, as guiding questions foram divididas nos temas dados, usuário, modelo, ética e produção. Suas devidas respostas técnicas são respondidas em [Resoluções Das Guiding Questions](resolucoesguidingquestions.md).

### Dados

* Qual será o formato de dado recebido do usuário?
* De qual modo as notícias das nossas fontes divergem das encontradas no instagram?
* De quais fontes vamos obter nossos dados base, como fazer a validação se a fonte é confiavel?

### Usuário

* Como será o fluxo de uso da nossa aplicação?
* Como vamos receber feedbacks do usuário?

### Modelo

* Quais métricas vamos apresentar para explicar o pensamento da IA?
* Como vamos evitar que o modelo seja enviesado?
* Como vamos hospedar o modelo?

### Ética

* Como vamos diferenciar nóticias políticas de informações da vida pessoal do político?

### Produção

* Qual modelo vamos utilizar como base?

## 2. Objetivos do Negócio

Este tópico contextualiza o problema central da desinformação eleitoral nas redes sociais e define os objetivos estratégicos do projeto, estabelecendo metas claras para reduzir o impacto de propostas distorcidas e mensurar a conscientização do eleitor no mundo real.
### Problema:

Pessoas leem publicações e prints no Instagram sobre propostas de governo de candidatos e não verificam se elas não são informações exageradas, distorcidas ou falsas, podendo formar opiniões equivocadas sem checar ou saber sobre fontes oficiais como o TSE (Tribunal Superior Eleitoral).

### Objetivo de Negócio:

Reduzir votos a partir de informações falsas ou equivocas e o compartilhamento de tais informações sobre proprostas de governo - medível no MUNDO (ex.: % de usuários que, após consultar o sistema, relatam o compreender melhor as propostas de governo dos candidatos).

## 3. Objetivos de ML

Classificar imagens e textos do Instagram ("Candidato X proprõe/defenderá a medida Y") em verdadeiro ou falso. EX: Com as informaçẽos disponibilizadas pelo TSE / Informação distorcida ou fora de contexto / Falsa — e indicar os trechos dos documentos oficiais que sustentam a análise. Medível no MODELO (ex.: F1-score e acurácia da classificação por categoria).

## 4. Arquitetura


## 5. Ferramentas