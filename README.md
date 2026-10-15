# Sistema Web de Gestão Logística e Controle de Donativos – ONG Bairro Solidário

Este projeto consiste em um Produto Mínimo Viável (MVP) desenvolvido como atividade de Extensão Universitária para o curso de **Análise e Desenvolvimento de Sistemas (ADS)**.

## 🚀 Objetivo do Software
A aplicação substitui o controle manual e analógico de triagem do galpão da **ONG Bairro Solidário**, eliminando o desperdício de insumos perecíveis e automatizando o agendamento de coletas domiciliares de itens volumosos na comunidade.

## 🛠️ Tecnologias Utilizadas
* **Linguagem Principal:** Python 3.12
* **Framework Web/API:** FastAPI (Mecanismo assíncrono de alto desempenho)
* **Motor de Renderização:** Jinja2 Templates (Interface Web Responsiva)

## 🎨 Requisitos e Diferenciais Implementados
* **RF01 (Controle de Entrada):** Triagem e cadastro digital de doações com validação de dados no servidor.
* **RF02 (Alertas Automáticos):** Varredura lógica e sinalização visual em alto contraste (WCAG) para itens com vencimento crítico inferior a 30 dias.
* **RF03 (Logística de Coletas):** Módulo de controle de status de visitas para evitar viagens perdidas.
* **RNF02 (Segurança):** Validação de tipos via Pydantic e escape nativo contra falhas de injeção.
