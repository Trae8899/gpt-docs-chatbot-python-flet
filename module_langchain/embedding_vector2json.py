from dotenv import load_dotenv
import openai
# PDF Loaders. If unstructured gives you a hard time, try PyPDFLoader
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import datetime
import json
import os
import glob
from uuid import uuid4

OPENAI_API_KEY = None
MODEL = "text-embedding-ada-002"
try:
    load_dotenv()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
except:
    pass

def embeddingfolder2json(curreut_dir=None,openai_api=OPENAI_API_KEY):
    if current_dir:
        current_dir = os.path.dirname(os.path.realpath(__file__))
    docs_dir = os.path.join(current_dir, "docs")
    pdf_files = glob.glob(os.path.join(docs_dir, "*.pdf"))
    word_files = glob.glob(os.path.join(docs_dir, "*.docx"))

    openai.api_key = openai_api
    # embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    #embedding
    texts=[]
    for file_path in pdf_files:
        loader = PyPDFLoader(file_path)
        document = loader.load()
        text = text_splitter.split_documents(document)
        texts.extend(text)

    for file_path in word_files:
        loader = Docx2txtLoader(file_path)
        document = loader.load()
        text = text_splitter.split_documents(document)
        texts.extend(text)

    meta = [{'text': line.page_content,'source':os.path.basename(line.metadata['source']),'page':str(int(line.metadata['page']))} for line in texts]
    embeddingdata = openai.Embedding.create(input=[line['text'] for line in meta], engine=MODEL)
    embed = [em_data['embedding'] for em_data in embeddingdata['data']]
    embed_index = [str(uuid4()) for _ in embeddingdata['data']]
    main_vector=zip(embed_index,embed,meta)
    main_vector_json = [{'id': v[0], 'embedding': v[1], 'metadata': v[2]} for v in main_vector]

    # Save the converted data to a JSON file
    today=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    json_path = os.path.join(current_dir, "dataset_"+today+".json")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(main_vector_json, f, ensure_ascii=False, indent=4)
    
    return json_path

def embeddingfiles2json(filepaths:[],openai_api=OPENAI_API_KEY):
    # embedding_openai=openai()
    openai.api_key = openai_api
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    #fileread
    json_paths=[]
    for filepath in filepaths:
        basename = os.path.basename(filepath)
        filenames=os.path.splitext(basename)
        ext=filenames[1]
        filename=filenames[0]
        if ext.upper()==".PDF":
            loader = PyPDFLoader(filepath)
        elif ext.upper()==".DOCX":
            loader = Docx2txtLoader(filepath)
        else:
            continue
        document = loader.load()
        text = text_splitter.split_documents(document)
        # texts.extend(text)
    
        meta = []
        embed = []
        embed_index = []
        for line in text:
            # meta 데이터 생성
            meta_data = {
                'text': line.page_content,
                'source': basename,
                'page': str(int(line.metadata['page']))
            }
            meta.append(meta_data)
            embed_index.append(str(uuid4()))
        
        # 각 텍스트에 대한 임베딩 데이터 생성
        embeddingdata = openai.Embedding.create(input=[line['text'] for line in meta], engine=MODEL)
        embed = [em_data['embedding'] for em_data in embeddingdata['data']]

        # 각 데이터를 합친 후 Json 형식으로 변환
        main_vector = list(zip(embed_index, embed, meta))
        main_vector_json = [{'id': v[0], 'embedding': v[1], 'metadata': v[2]} for v in main_vector]

        # Save the converted data to a JSON file
        json_path = os.path.join(os.path.dirname(filepath), f"{filename}.json")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(main_vector_json, f, ensure_ascii=False, indent=4)
            json_paths.append(json_path)
    return json_paths
    