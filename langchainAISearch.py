import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# print(dir(AzureSearch))
import openai

openai.api_key = 'API Key'
from openai import OpenAI
client = OpenAI(api_key =os.getenv('OPENAI_API_KEY'))

vector_store_address:str = "https://carevoice.search.windows.net"
vector_store_password:str = "c2Y3udz3LJXCsOKT43Q8raLNp8mJmyj9HVlr2UPyR9AzSeCKG0JH"
DATA_PATH = '/home/ubuntu/Desktop/CareVoice_projects/CareAPP/data'
DB_AzureSearch_PATH = 'vectorstore/db_azuresearch'

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
# llm = OpenAI()
import os

# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


# def set_custom_prompt():
#     """
#     Prompt template for QA retrieval for each vectorstore
#     """
#     prompt = PromptTemplate(template=custom_prompt_template,
#                             input_variables=['context', 'question'])
#     return prompt


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",model_kwargs={'device': 'cpu'})
index_name ="carevoicedemo"
vector_store: AzureSearch = AzureSearch(
  azure_search_endpoint = vector_store_address,
  azure_search_key = vector_store_password,
  index_name = index_name,
  embedding_function = embeddings.embed_query,
)
# loader = DirectoryLoader(DATA_PATH,glob='*.pdf',loader_cls=PyPDFLoader)
# documents = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
# texts = text_splitter.split_documents(documents)
# vector_store.add_documents(documents = texts)
# print ("Data loaded into Azure Search")

# Perform a similarity search
# docs = vector_store.similarity_search(
#     query="What is an antibiotic ?",
#     k=3,
#     search_type="similarity",
# )
# print(docs[0].page_content)

# def retrieval_qa_chain(llm, prompt, db):
#     qa_chain = RetrievalQA.from_chain_type(llm=llm,
#                                        chain_type='stuff',
#                                        retriever=db.as_retriever(search_kwargs={'k': 2}),
#                                        return_source_documents=True,
#                                        chain_type_kwargs={'prompt': prompt}
#                                        )
#     return qa_chain
# def load_llm():
#     # Load the locally downloaded model here
#     llm = CTransformers(
#         model = "TheBloke/Llama-2-7B-Chat-GGML",
#         model_type="llama",
#         max_new_tokens = 512,
#         temperature = 0.5
#     )
#     return llm
# def qa_bot():
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
#                                        model_kwargs={'device': 'cpu'})
#     # db = AzureSearch.load_local(DB_AzureSearch_PATH, embeddings)
#     llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
#     qa_prompt = set_custom_prompt()
#     qa = retrieval_qa_chain(llm, qa_prompt)


# def final_result(query):
#     qa_result = qa_bot()
#     response = qa_result({'query': query})
#     return response

def get_response_from_docs(query):
    docs = vector_store.similarity_search(
        query=query,
        k=3,
        search_type="similarity",
    )
    context=docs[0].page_content
    context=context+" "+docs[1].page_content
    context=context+" "+docs[2].page_content
    # print(context)
    compounded_query = f'''You are an AI healthcare assistant. Your role is to engage with patients in a supportive and informative manner,
    helping them to understand and implement good healthcare practices.
    You will provide personalized health tips, encourage patients to maintain a healthy lifestyle, and 
    motivate them . you will answer the patient's questions in accordance with the data provided in the context and you 
    will not add anything on your own . If you donot know the answer simply ask for more information from the patient.
    Make sure not to disapoint the patient by giving random answer out of the context.
    

            Context: {context}
            Question: {query}

            Only return the helpful answer below and nothing else.
            Helpful answer:


    '''
    # print(compounded_query)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages= [{
      "role": "user",
      "content": compounded_query
    }],
    temperature=1,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0.8,
    presence_penalty=0
    )
    # print(response.choices[0].message)
    response_dict={'content':response.choices[0].message.content}
    if response_dict!=None:
        return response_dict
    else :
        return 'Failed to Generate response!'
    

# print(get_response_from_docs("What is an antibiotic?"))