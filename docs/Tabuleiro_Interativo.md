---
projeto_pai: "PETCode"
nome_projeto: "Tabuleiro Interativo"
tipo: "Hardware / Automação"
status: "Em Desenvolvimento"
tecnologias: ["ESP8266EX", "Sensores RFID", "Hardware"]
---

# Contexto Geral
Inicialmente planejado como um projeto de "Automação da Sala do PET" (usando Home Assistant e Relés), o projeto precisou ser pivotado devido à impossibilidade de alterar a fiação elétrica da sala. Transformou-se então em um projeto de Hardware focado em construir um Tabuleiro Interativo para jogos (como RPG ou Escape Rooms), permitindo a integração de quem gosta de programar lógica com a equipe de eletrônica.

# Evolução e Arquitetura do Projeto
- **A Ideia Original (Modular):** A intenção inicial era criar um tabuleiro 100% modular, onde peças individuais (quadrados) se conectariam magneticamente (usando conectores magnéticos - Pogo Pins). Cada módulo teria seu próprio microcontrolador (módulo WiFi ESP8266EX) e leitores RFID para detectar onde os "bonecos" e "armadilhas" estavam, comunicando-se com uma central. Ao detectar uma peça, a central poderia acionar motores, luzes ou animações.
- **A Mudança de Escopo (Pivot):** O maior desafio da ideia modular era a lógica de mapeamento espacial (fazer a rede de ESPs descobrir exatamente onde cada peça foi conectada). Para viabilizar a entrega do projeto, a equipe decidiu dar um passo atrás e desenvolver um **tabuleiro de matriz fixa** (não modular) como prova de conceito inicial, facilitando o mapeamento das posições e o roteamento eletrônico.