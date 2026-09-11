import boto3
import json
import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
class VectorDBIntegrator:
    def __init__(self, bucket_name, collection_endpoint):
        load_dotenv()
        self.bucket=bucket_name
        self.s3= boto3.client('s3', region_name='us-east-1')
        self.bedrock=boto3.client('bedrock-runtime', region_name='us-east-1')
        credentials=boto3.Session().get_credentials()
        auth = AWSV4SignerAuth(credentials, 'us-east-1', 'aoss')
        self.os_client = OpenSearch(
           hosts=[{'host': collection_endpoint, 'port': 443}],
           http_auth=auth,
           use_ssl=True,
           verify_certs=True,
           connection_class=RequestsHttpConnection, 
           timeout=300
        )
    def fetch_chunks(self, doc_name):
         chunks = []
         response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=f"chunks/{doc_name}/") 
         for item in response.get('Contents', []):
               obj = self.s3.get_object(Bucket=self.bucket, Key=item['Key'])
               chunk_data = json.loads(obj['Body'].read().decode('utf-8'))
               chunks.append(chunk_data)
         print(f"Fetched {len(chunks)} chunks from S3")
         return chunks
    def generate_embedding(self, text):
         body = json.dumps({"inputText":text})
         response=self.bedrock.invoke_model(
           body=body, 
           modelId='amazon.titan-embed-text-v1',
           accept='application/json',
           contentType='application/json'              
         )
    def index_chunks(self, chunks, index_name="hr-policy-index"):
         if not self.os_client.indices.exists(index=index_name): 
            index_body = { 
                "settings": { 
                    "index.knn": True 
                }, 
                "mappings": { 
                    "properties": { 
                        "embedding_vector": {
                            "type": "knn_vector",
                            "dimension": 1536, 
                            "method": {
                                "name": "hnsw",
                                "space_type": "l2" 
                            } 
                        } 
                    } 
                } 
            }
            self.os_client.indices.create(index=index_name, body=index_body)
            print(f"Created '{index_name}' with strict knn_vector mapping.")
            for chunk in chunks:
                 vector=self.generate_embedding(chunk['content'])
                 document={
                      "chunk_id": chunk['chunk_id'],
                      "content": chunk['content'],
                      "embedding_vector": vector,
                      "timestamp": chunk['timestamp']                      
                 }
                 self.os_client.index(
                      index=index_name,
                      body=document,
                      id = chunk['chunk_id']                    
                 )
            print(f"Successfully indexed {len(chunks)} vectors into OpenSearch")            

