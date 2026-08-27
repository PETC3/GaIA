# GaIA

Este projeto consiste em um assistente virtual inteligente desenvolvido para o **PET Ciências Computacionais (FURG)**, integrado ao subprojeto **PETCode**. 

A aplicação utiliza a técnica de **Geração Aumentada por Recuperação (RAG)** para buscar informações de forma híbrida (semântica e por correspondência de palavras-chave) na documentação operacional do grupo, respondendo de forma contextualizada às dúvidas dos membros por meio de um modelo de linguagem local.

## 🛠️ Tecnologias Utilizadas

* **Python** (Linguagem base)
* **Streamlit** (Interface gráfica web)
* **LangChain** (Orquestração do fluxo RAG)
* **ChromaDB** (Banco de dados vetorial local)
* **Ollama + Llama 3.2** (Inferência local do modelo de linguagem)
* **HuggingFace Embeddings** (`paraphrase-multilingual-MiniLM-L12-v2`)

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
1. Ter o **Python 3.10 ou superior** instalado.
2. Ter o **Ollama** instalado no computador ([Baixe aqui](https://ollama.com/)).
3. Baixar o modelo de linguagem local executando o seguinte comando no terminal:
   ```bash
   ollama run llama3.2

# Passo a Passo de Instalação e Execução - RAG Local PET C3

Siga as instruções abaixo para configurar o ambiente e executar a aplicação em seu computador.

---

## 🖥️ 1. Pré-requisitos

Antes de começar, certifique-se de ter os seguintes componentes instalados:
* **Python 3.10 ou superior**: [Download Python](https://www.python.org/downloads/)
* **Ollama**: [Download Ollama](https://ollama.com/)

### Baixar o modelo de linguagem local
Abra o seu terminal (PowerShell ou Bash) e faça o download do modelo Llama 3.2 executando o comando:

```bash
ollama run llama3.2
```

*Após a conclusão do download, você pode fechar o terminal.*

---

## 📂 2. Clonar o Repositório

Navegue até a pasta onde deseja guardar o projeto e clone os arquivos

---

## ⚙️ 3. Configurar o Ambiente Virtual (venv)

Escolha o procedimento de acordo com o seu sistema operacional:

### No Windows (Método robusto para evitar travamento de rede no venv):
1. Crie o ambiente virtual sem a instalação automática de pacotes:
   ```powershell
   python -m venv venv --without-pip
   ```
2. Ative o ambiente virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Instale o gerenciador de pacotes `pip` manualmente dentro do ambiente ativo:
   ```powershell
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python get-pip.py
   ```
4. Remova o instalador temporário:
   ```powershell
   Remove-Item .\get-pip.py
   ```

### No Linux / macOS:
1. Crie o ambiente virtual:
   ```bash
   python3 -m venv venv
   ```
2. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

---

## 📦 4. Instalar as Dependências

Com o seu ambiente virtual ativo (indicado pelo prefixo `(venv)` no terminal), instale as bibliotecas necessárias executando:

```bash
pip install -r requirements.txt
```

---

## 🗂️ 5. Adicionar os Documentos

Insira todas as documentações que deseja que a IA consulte (em formato `.md` - Markdown) dentro da pasta `/docs` que está na raiz do projeto.

---

## 🚀 6. Executar a Aplicação

Para abrir a interface gráfica no navegador, execute o comando:

```bash
streamlit run app.py
```

Se o banco de dados vetorial ainda não existir, o sistema identificará automaticamente os arquivos da pasta `/docs`, fará o fatiamento e criará o banco de dados local na primeira execução.