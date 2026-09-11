import boto3 

import json 

from dotenv import load_dotenv 

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth 

class HRQuestionAnswerer: 

    def __init__(self, collection_endpoint): 

        load_dotenv() 

        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1') 

        credentials = boto3.Session().get_credentials()  

        auth = AWSV4SignerAuth(credentials, 'us-east-1', 'aoss') 

        self.os_client = OpenSearch(  

           hosts=[{'host': collection_endpoint, 'port': 443}],  

           http_auth=auth,  

           use_ssl=True,  

           verify_certs=True,  

           connection_class=RequestsHttpConnection, 

           timeout=300    

       ) 

    def get_embedding(self, text): 

        body = json.dumps({"inputText": text}) 

        response = self.bedrock.invoke_model(  

            body=body,  

            modelId='amazon.titan-embed-text-v1',  

            accept='application/json',  

            contentType='application/json'  

        ) 

        response_body = json.loads(response.get('body').read()) 

        return response_body.get('embedding') 

    def search_documents(self, query_vector, index_name="hr-policy-index"): 

         query = {  

           "size": 3,  

           "query": {  

               "knn": {  

                   "embedding_vector": {  

                       "vector": query_vector,  

                       "k": 3  

                   }  

               }  

           }  

        } 

         response = self.os_client.search(index=index_name, body=query) 

         chunks = [] 

         for hit in response['hits']['hits']: 

             chunks.append(hit['_source']['content']) 

         return chunks 

    def generate_answer(self, question, context_chunks): 

        context_text = "\n\n".join(context_chunks) 

        prompt = f"""You are a secure, internal HR assistant for Thinknyx Technologies.  

Answer the user's question strictly using the provided HR policy context below.  

If the answer is not contained in the context, explicitly state "I do not have information on this topic." Do not guess. 

 

Context: 

{context_text} 

 

Question: {question} 

Answer: """ 

        response = self.bedrock.converse( 

        modelId="us.amazon.nova-2-lite-v1:0", 

        messages=[ 

            { 

                "role": "user", 

                "content": [ 

                    { 

                        "text": prompt 

                    } 

                ] 

            } 

        ], 

        inferenceConfig={ 

            "maxTokens": 500, 

            "temperature": 0.0 

        },
        guardrailConfig={
                "guardrailIdentifier": "lhe4mg49pqhg",
                "guardrailVersion": "1"
            }
        )

        # Check if Bedrock Guardrail intervened
        if response.get("stopReason") == "guardrail_intervened":
            return response["output"]["message"]["content"][0]["text"].strip() 

       
        return response["output"]["message"]["content"][0]["text"].strip() 

    def ask(self, question): 

        print(f"Question: {question}\n")  

 

        print("1. Generating embedding for the question...")  

        vector = self.get_embedding(question) 

 

        print("2. Searching OpenSearch for relevant policy chunks...")  

        context = self.search_documents(vector) 

 

        print("3. Generating final answer with Amazon Titan...\n")  

        answer = self.generate_answer(question, context) 

        return answer            