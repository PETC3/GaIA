---
projeto_pai: "PETCode"
nome_projeto: "IA do PET C3"
tipo: "Inteligência Artificial / Recuperação de Conhecimento"
status: "Em Desenvolvimento"
tecnologias: ["Python", "LangChain", "ChromaDB", "Ollama", "Streamlit", "HuggingFace Embeddings"]
---

# Contexto Geral
Devido à grande quantidade de subprojetos e ao histórico extenso gerado pela rotatividade de membros, o PET C3 iniciou o desenvolvimento de uma Inteligência Artificial local para atuar como um "oráculo" do grupo. A IA utiliza a arquitetura RAG (Retrieval-Augmented Generation) para responder perguntas precisas baseadas nos documentos internos e manuais do PET.

# Arquitetura do Sistema
O projeto prioriza tecnologias open-source e locais para manter a gratuidade e a privacidade dos dados:
- **Interface:** Desenvolvida rapidamente em Python utilizando `Streamlit`.
- **Orquestração:** O framework `LangChain` gerencia o fluxo de documentos, separação de textos (Text Splitter) e prompts.
- **Banco Vetorial:** Os documentos (Markdown/PDFs) são convertidos em vetores usando modelos do `HuggingFace` e armazenados no banco de dados local `Chroma`.
- **LLM (Cérebro):** As respostas são geradas localmente utilizando a ferramenta `Ollama`, que roda modelos de linguagem de grande escala (como Llama) diretamente na máquina, recebendo o contexto fornecido pelo ChromaDB.