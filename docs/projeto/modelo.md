O modelo que será utilizado para o projeto será o **mistralai/Pixtral-12B-2409**

Disponível em: [Mistralai/Pixtral-12B-2409](https://huggingface.co/mistralai/Pixtral-12B-2409)

## Motivo do Uso

A proposta do projeto é utilizar dados dos POSTs do Instagram, que possui notícias com ênfase em propostas de governo de determinado candidato, sendo possível por envio de URL, pelo usuário, e coletando **Imagens do Carrossel** e **Descrição**, dentro do periodo eleitoral. 

**Pixtral-12B-2409** possui a capacidade, pré-existente, de conseguir ler imagens e textos em português, havendo a necessidade apenas de treina-lo com as informações coletadas dos dados existentes e seguros do **Tribunal Superior Eleitoral (TSE)**.

## Treinamento Supervisionado

O modelo será treinado utilizando **dados de 2026 disponibilizados pelo Tribunal Superior Eleitoral (TSE)**.

Esses dados serão utilizados como base para o processo de **treinamento supervisionado**, permitindo que o modelo identifique padrões e relações presentes nas informações eleitorais.

> Os dados utilizados serão previamente analisados e preparados para garantir sua adequação ao treinamento do modelo.