---
projeto_pai: "PETCode"
nome_projeto: "Gestor de Atas / Portal PET"
tipo: "Desenvolvimento Web / Ferramenta Interna"
status: "Ativo"
tecnologias: ["Python", "PyQt5", "Flask", "HTML", "CSS", "PostgreSQL", "ReportLab", "Node.js"]
---

# Contexto Geral
Este projeto nasceu como uma ferramenta para automatizar a geração de Atas das reuniões do PET C3, salvando os arquivos em PDF. Com o tempo, a ferramenta evoluiu e foi integrada ao "Portal PET", uma plataforma unificada que centraliza as ferramentas utilizadas pelos petianos.

# Evolução Técnica
1. **Primeira Versão (2022/2023 - Desktop):** Desenvolvido em Python utilizando a biblioteca PyQt5 (interface arrasta e solta). O usuário selecionava os presentes e tópicos e o programa gerava o PDF.
2. **Segunda Versão (2024 - Web com Flask):** Para aumentar a acessibilidade, o projeto migrou para a web. O Front-end foi feito em HTML/CSS e o Back-end em Python (Flask) utilizando banco de dados relacional (SQL) e ReportLab para geração dinâmica de PDFs.
3. **Versão Atual (2025/2026 - Portal PET em Node.js):** O Gestor de Atas foi reescrito utilizando Node.js. Atualmente, ele compõe o "Portal PET", um sistema maior e integrado que possui também outras funcionalidades para o gerenciamento interno do grupo.