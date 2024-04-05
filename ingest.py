from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch 
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 

vector_store_address: str = "https://carevoice.search.windows.net"
vector_store_password: str = "9NH4jxlqsNMddpusYXO5mlndrJiwn9LMnBqt1EDrOlAzSeDqeCQH"
DATA_PATH = '/home/ubuntu/Desktop/CareVoice_projects/CareAPP/data/'
DB_AzureSearch_PATH = 'vectorstore/db_azuresearch'

# Create vector database
def create_vector_db():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
    index_name: str = "carevoicedemo"
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint = vector_store_address,
        azure_search_key = vector_store_password,
        index_name = index_name,
        embedding_function = embeddings.embed_query,
)
    loader = DirectoryLoader(DATA_PATH,glob='*.pdf',loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    vector_store.add_documents(documents = texts)

if __name__ == "__main__":
    create_vector_db()
