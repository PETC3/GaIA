import streamlit as st
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# Configurações iniciais
DOCS_DIR = "./docs"
DB_DIR = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

st.set_page_config(page_title="RAG PET C3", layout="wide")
st.title("🤖 Assistente Virtual - PET C3")
st.write("Consulte informações sobre subprojetos, mídias sociais e documentações gerais do grupo.")

# Inicializa ou carrega o banco de dados vetorial
@st.cache_resource
def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    if os.path.exists(DB_DIR) and len(os.listdir(DB_DIR)) > 0:
        return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    if not os.path.exists(DOCS_DIR) or len(os.listdir(DOCS_DIR)) == 0:
        st.warning("A pasta './docs' está vazia ou não existe. Adicione arquivos .md para começar.")
        return None

    loader = DirectoryLoader(
        DOCS_DIR, 
        glob="**/*.md", 
        loader_cls=TextLoader, 
        loader_kwargs={'encoding': 'utf-8'}
    )
    docs = loader.load()
    
    # Chunks maiores para manter listas e tabelas integradas
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=250
    )
    splits = text_splitter.split_documents(docs)
    
    vector_store = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    return vector_store

vector_store = get_vector_store()

# Barra lateral
with st.sidebar:
    st.header("Configurações do RAG")
    if st.button("Reindexar Documentos"):
        st.cache_resource.clear()
        if os.path.exists(DB_DIR):
            import shutil
            try:
                shutil.rmtree(DB_DIR)
                st.success("Banco de dados resetado com sucesso! Recarregando...")
                st.rerun()
            except PermissionError:
                st.error(
                    "Não foi possível deletar a pasta automaticamente devido a bloqueio do Windows. "
                    "Para reindexar: pare o Streamlit no terminal (Ctrl+C), delete a pasta 'chroma_db' manualmente e reinicie."
                )
    st.info("Certifique-se de que o Ollama está rodando localmente.")

# Processamento do Chat e RAG Híbrido com Ranqueamento
if vector_store:
    # A busca semântica inicial trará os 4 melhores candidatos
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    llm = ChatOllama(model="llama3.2", temperature=0.1)
    
    # Prompt do sistema para a resposta final baseada no contexto
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "Você é um assistente virtual prestativo do grupo PET C3 (Ciências Computacionais - FURG).\n"
            "Use os seguintes pedaços de contexto recuperados para responder à pergunta.\n"
            "Se você não souber a resposta ou se ela não estiver no contexto, diga honestamente que não possui essa informação.\n"
            "Evite criar informações que não constam nos documentos fornecidos.\n\n"
            "Contexto:\n{context}"
        )),
        ("human", "{input}"),
    ])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Pergunte algo sobre os projetos do PET..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Buscando informações nas documentações..."):
                try:
                    # --- PASSO 1: Reescrita de Consulta Otimizada (Foco em Conceitos Chave) ---
                    query_generator_prompt = (
                        "Você é um extrator de termos técnicos para busca em banco de dados.\n"
                        "Sua tarefa é extrair o conceito técnico, assunto, data ou nome próprio pesquisado (máximo 3 palavras).\n\n"
                        "REGRAS RÍGIDAS:\n"
                        "1. NÃO TRADUZA nomes próprios, marcas, nomes de filmes, séries ou termos em inglês (ex: mantenha 'Friends', não traduza para 'amigos').\n"
                        "2. Remova COMPLETAMENTE as palavras: 'projeto', 'petcode', 'instagram', 'postagem', 'post', 'furg', 'c3', 'existe', 'alguma', 'sobre', 'feita', 'pelo', 'grupo'.\n"
                        "3. Preserve datas exatamente como digitadas (ex: '06/05').\n"
                        "4. Não escreva explicações ou introduções. Apenas os termos de busca.\n\n"
                        f"Pergunta do usuário: {user_input}\n"
                        "Palavras-chave otimizadas:"
                    )
                    
                    search_query_response = llm.invoke(query_generator_prompt)
                    search_query = search_query_response.content.strip().replace('"', '')
                    
                    st.caption(f"🔍 *Termo otimizado para busca:* `{search_query}`")
                    
                    # --- PASSO 2: Busca Vetorial (Semântica) ---
                    semantic_docs = retriever.invoke(search_query)
                    
                    # --- PASSO 3: Busca por Palavra-Chave Híbrida com Pontuação (Ranqueada) ---
                    keyword_matched_docs = []
                    
                    stopwords = {"de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "nao", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "das", "como", "mas", "ao", "tem", "alguma", "qual", "quais", "dia", "ano", "data", "postagem", "post", "postagens", "posts", "sobre", "algum", "existe", "alguma", "fazer", "pelo", "pela"}
                    
                    # Divide a pergunta do usuário em palavras limpas de ruído
                    keywords_to_search = [
                        w.strip("?,.!-()\"'").lower() 
                        for w in user_input.split() 
                        if w.strip("?,.!-()\"'").lower() not in stopwords and len(w) > 2
                    ]
                    
                    if keywords_to_search:
                        all_chunks = vector_store.get(include=["documents", "metadatas"])
                        scored_chunks = []
                        
                        for i, doc_text in enumerate(all_chunks["documents"]):
                            doc_text_lower = doc_text.lower()
                            # Soma a quantidade de termos coincidentes neste bloco de texto
                            match_count = sum(1 for word in keywords_to_search if word in doc_text_lower)
                            
                            if match_count > 0:
                                metadata = all_chunks["metadatas"][i] if all_chunks["metadatas"] else {}
                                temp_doc = Document(page_content=doc_text, metadata=metadata)
                                scored_chunks.append((match_count, temp_doc))
                        
                        # Ordena os blocos: os que contêm mais palavras da pergunta ficam no topo
                        scored_chunks.sort(key=lambda x: x[0], reverse=True)
                        keyword_matched_docs = [doc for score, doc in scored_chunks]
                    
                    # --- PASSO 4: Fusão dos Resultados (Deduplicação de Contexto) ---
                    final_docs = list(semantic_docs)
                    for k_doc in keyword_matched_docs:
                        if k_doc.page_content not in [d.page_content for d in final_docs]:
                            final_docs.append(k_doc)
                    
                    # Mantém o limite de segurança de até 6 fatias de contexto para a IA
                    final_docs = final_docs[:6]
                    
                    # --- PASSO 5: Geração da Resposta pelo LLM ---
                    context_text = "\n\n".join(doc.page_content for doc in final_docs)
                    messages = prompt_template.format_messages(
                        context=context_text, 
                        input=user_input
                    )
                    
                    response = llm.invoke(messages)
                    answer = response.content
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Exibe fontes utilizadas no rodapé da resposta
                    if final_docs:
                        with st.expander("Ver fontes consultadas"):
                            for doc in final_docs:
                                source_path = doc.metadata.get('source', 'Desconhecida')
                                file_name = os.path.basename(source_path)
                                st.write(f"- **Documento:** `{file_name}`")
                                st.caption(doc.page_content[:200] + "...")
                                
                except Exception as e:
                    st.error(f"Erro ao processar requisição: {e}")
                    st.info("Verifique se o Ollama está ativo no sistema.")
else:
    st.info("Aguardando inserção de documentos na pasta './docs' para iniciar.")