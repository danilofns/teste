Para ensinar o modelo de Machine Learning, dados públicos das **Candidaturas de 2026** serão utilizados, e então, será feito o cruzamento de dados junto com **propostas de governo** de todos os dados publicados. 

As **propostas de governo** tem o formato como: .pdf, havendo a necessidade de converte-los para .txt, para que a leitura seja possível de ser feita, sem a necessidade de programas externos.

Todos os dados são públicos em: [Tribunal Superior Eleitoral](https://dadosabertos.tse.jus.br/dataset/candidatos-2026)


## Converter propostas

Para realizar a conversão das **propostas de governo**, será utilizado a biblioteca: **pypdf** que faz a leitura do PDF e converte ele para o formato .txt e salvo em um arquivo de leitura, como: .csv, .pandas ou .json **(Ainda não decidido)**


**PYDF**: O intuito principal do pypdf é permitir que programadores realizem operações automatizadas em documentos PDF diretamente pelo código, sem precisar de programas externos.


## Cruzamento de dados


### Estrutura

``` powershell
├─── consulta_cand_2026
    ├── consulta_cand_2026_AC.csv
    └── consulta_cand_2026_AL.csv
    └── ....
    └── consulta_cand_2026_TO.csv
```

``` powershell
├─── proposta_governo_2026
    ├── 2026BRx_01.pdf
    └── 2026BRy_01.pdf
    └── ....
    └── 2026BRz_01.pdf
```
---


### Coleta

Formato em que o .csv do **(Tribunal Superior Eleitoral) TSE** salva os respectivos dados dos candidatos: 

``` csv
"DT_GERACAO";"HH_GERACAO";"ANO_ELEICAO";"CD_TIPO_ELEICAO";"NM_TIPO_ELEICAO";"NR_TURNO";"CD_ELEICAO";"DS_ELEICAO";"DT_ELEICAO";"TP_ABRANGENCIA";"SG_UF";"SG_UE";"NM_UE";"CD_CARGO";"DS_CARGO";"SQ_CANDIDATO";"NR_CANDIDATO";"NM_CANDIDATO";"NM_URNA_CANDIDATO";"NM_SOCIAL_CANDIDATO";"NR_CPF_CANDIDATO";"DS_EMAIL";"CD_SITUACAO_CANDIDATURA";"DS_SITUACAO_CANDIDATURA";"TP_AGREMIACAO";"NR_PARTIDO";"SG_PARTIDO";"NM_PARTIDO";"NR_FEDERACAO";"NM_FEDERACAO";"SG_FEDERACAO";"DS_COMPOSICAO_FEDERACAO";"SQ_COLIGACAO";"NM_COLIGACAO";"DS_COMPOSICAO_COLIGACAO";"SG_UF_NASCIMENTO";"DT_NASCIMENTO";"NR_TITULO_ELEITORAL_CANDIDATO";"CD_GENERO";"DS_GENERO";"CD_GRAU_INSTRUCAO";"DS_GRAU_INSTRUCAO";"CD_ESTADO_CIVIL";"DS_ESTADO_CIVIL";"CD_COR_RACA";"DS_COR_RACA";"CD_OCUPACAO";"DS_OCUPACAO";"CD_SIT_TOT_TURNO";"DS_SIT_TOT_TURNO"
```

Os dados estão expostos no seguinte modelo acima.
O cruzamento de dados será feito com os dados coletados:

> "NR_CANDIDATO";"NM_CANDIDATO";"NM_URNA_CANDIDATO";"DS_CARGO"

e após isso, com as propostas convertidas para .txt e salvas em .csv, .pandas ou .json, será possível fazer o cruzamento da proposta com o nome do candidato.



## Saída

Formato exemplo que é esperado para a saída: **(Exemplo, não decidido)**

``` json
[
    "NR_CANDIDATO": NR_CANDIDATO
    "NM_CANDIDATO": NM_CANDIDATO
    "NM_URNA_CANDIDATO": NM_URNA_CANDIDATO
    "PROPOSTA": ["Proposta coletada"]
]
```