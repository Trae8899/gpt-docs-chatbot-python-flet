import pinecone as pn
import os
import dotenv 


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from langchain.chains import LLMChain
from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain import PromptTemplate, LLMChain


try:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME')
    PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
except:
    pass

def ask_asme(query:str,chat_history=None,prompt_concept=None,openai_api=OPENAI_API_KEY,pinecone_index=PINECONE_INDEX_NAME,pinecone_env=PINECONE_ENVIRONMENT,pinecone_api=PINECONE_API_KEY):
    if openai_api and pinecone_index and pinecone_env and pinecone_api:
        pass
    else:
        return
    # initialize pinecone
    pn.init(
        api_key=pinecone_api,  # find at app.pinecone.io
        environment=pinecone_env  # next to API key in console
    )
    index_name = pinecone_index # put in the name of your pinecone index here
    index = pn.Index(index_name)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api)
    vectorstore = Pinecone(index, embeddings, "text")
    memory = ConversationBufferMemory(memory_key="chat_history", output_key='answer', return_messages=True)
    llm = OpenAI(temperature=0.3,openai_api_key=openai_api)

    prompt_template=""
    if prompt_concept:
        prompt_concept+="You are the engineer for plant engineering."
    prompt_template+="""
    Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["chat_history", "question"])
    question_generator = LLMChain(llm=llm, prompt=prompt)
    doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")

    embeddings = OpenAIEmbeddings()

    chain = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        question_generator=question_generator,
        return_source_documents=True,
        combine_docs_chain=doc_chain,
        memory=memory
    )


    if 'chat_history' not in locals():
        chat_history = []
    query = query
    query += " in detail."

    result=chain({"question": query, "chat_history": chat_history})
    result['answer']
    result['source_documents'][0]
    result['source_documents'][1]
    result['source_documents'][2]
    result['source_documents'][3]
    print (result['answer'])
    return result