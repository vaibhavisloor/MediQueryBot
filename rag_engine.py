import pandas as pd
import requests
import json
import faiss
import numpy as np
import os


embeddings_file = 'embedded_medicine_data.json'
llm_api = 'http://127.0.0.1:1234/v1/chat/completions'
embeddings_api = 'http://127.0.0.1:1234/v1/embeddings'
headers = {"Content-Type":"application/json"}

df = pd.read_csv(r"C:\Users\admin\Desktop\RAG\archive\Medicine_Details.csv")

def create_string(row):
    return (
        f"Medicine name: {row['Medicine Name']}. "
        f"Composition: {row['Composition']}. "
        f"Used for: {row['Uses']}. "
        f"Possible side effects: {row['Side_effects']}. "
        f"Manufacturer: {row['Manufacturer']}."
    )

df['text_chunk'] = df.apply(create_string,axis=1)
embedded_data = []

if os.path.exists(embeddings_file):
    with open(embeddings_file, "r") as f:
        embedded_data = json.load(f)
    print("✅ Loaded embeddings from file.")
else:
    print("🔁 No saved embeddings found — embedding all rows now.")
    embedded_data = []
    for i,row in df.iterrows():
        text = row['text_chunk']

        payload={
        'model':'all-minilm-l6-v2',
        'input':text
        }

        response = requests.post(embeddings_api,headers=headers,data=json.dumps(payload))

        if response.ok:
            embedding = response.json()['data'][0]['embedding']

            embedded_data.append({
            "embedding" : embedding,
            "text" : text,
            "medicine_name": row['Medicine Name'],
            "uses": row['Uses'],
            "manufacturer": row['Manufacturer'],
            "image_url": row['Image URL']
            })

            print(f"✅ Embedded: {row['Medicine Name']}")
        else:
            print(f"❌ Error embedding row {i}: {response.text}")

    with open(embeddings_file, 'w') as f:
        json.dump(embedded_data, f, indent=2)


embedding_vectors = np.array([entry['embedding'] for entry in embedded_data]).astype('float32')

dimension = len(embedding_vectors[0])
index = faiss.IndexFlatL2(dimension)
index.add(embedding_vectors)

metadata = [ 
    {
        "text": entry["text"],
        "medicine_name": entry["medicine_name"],
        "uses": entry["uses"],
        "manufacturer": entry["manufacturer"],
        "image_url": entry["image_url"]
    }
    for entry in embedded_data
]

def search_medicines(query,top_k=3):

    payload={
        'model':'all-minilm-l6-v2',
        'input':query
    }

    response = requests.post(embeddings_api,headers=headers,data=json.dumps(payload))

    if not response.ok:
        print("Failed to embed query")
        return
    
    query_embedding = np.array(response.json()['data'][0]['embedding']).astype('float32').reshape(1,-1)

    distances,indices = index.search(query_embedding,top_k)
    print(f"Distance = {distances}")
    print(f"Indices = {indices}")
    results = [metadata[i] for i in indices[0]]
    return results

def answer_with_llm(question,results):
    context = "\n\n".join([r["text"] for r in results])
    prompt = f'''Answer the following question from the below text . 
        Question: {question}
        -----
        Context : {context}
        
       '''
    
    response = requests.post(llm_api,headers=headers,
                             json={
                                'model':'llama-3.2-1b-instruct',
                                "messages":[
                                    {"role":"user","content":prompt}
                                ]
                             })

    if response.ok:
        return response.json()['choices'][0]['message']['content']
    else:
        print("❌ LLM error:", response.text)
        return "Sorry, I couldn't generate a response."
