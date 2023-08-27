
from uuid import uuid4
import os
import json
import pinecone
from dotenv import load_dotenv

PINECONE_INDEX_NAME = None
PINECONE_ENVIRONMENT = None
PINECONE_API_KEY = None

try:
    load_dotenv()
    PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME')
    PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
except:
    pass

def json2vector(jsonpath):
    
    if os.path.exists(jsonpath):
        with open(jsonpath, 'r', encoding='utf-8') as f:
            json_data=json.load(f)
    else:
        return
    
    vector_list=[]
    for item in json_data:
        vector=item['embedding']
        meta=item['metadata']
        id=str(uuid4())
        vector_list.append((id,vector,meta))
    
    return vector_list

def json2pinecone(jsonpath,pinecone_index=PINECONE_INDEX_NAME,pinecone_env=PINECONE_ENVIRONMENT,pinecone_api=PINECONE_API_KEY):
    
    main_vector_list=json2vector(jsonpath)
    
    # Initialize Pinecone
    pinecone.init(api_key=pinecone_api, environment=pinecone_env)
    # Create or retrieve the index
    if len(pinecone.list_indexes())==0:
        pinecone.create_index(pinecone_index, dimension=1536,pod_type="starter")
    elif pinecone_index not in pinecone.list_indexes():
        pinecone.create_index(pinecone_index, dimension=1536)
    # connect to index
    index = pinecone.Index(pinecone_index)
    batch_size = 100
    try:
        for i in range(0, len(main_vector_list), batch_size):
            try:
                batch_vector = main_vector_list[i:i+batch_size]
                ids, embeddings, metas = zip(*batch_vector)
                to_upsert = list(zip(ids, embeddings, metas))
                index.upsert(vectors=to_upsert)
            except:
                continue
        return jsonpath
    except:
        return