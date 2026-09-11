from bedrock_agentcore.runtime import BedrockAgentCoreApp
from qa_system import HRQuestionAnswerer
import os

app = BedrockAgentCoreApp()
collection_url = os.environ.get("OPENSEARCH_ENDPOINT", "8x5ymmu9jd4t8stecpe6.aoss.us-east-1.on.aws")
qa = HRQuestionAnswerer(collection_endpoint=collection_url)

@app.entrypoint
def invoke(payload):
    # AWS passes the payload here automatically
    question = payload.get("prompt", "")
    
    # Generate the RAG answer
    answer = qa.ask(question)
    
    # Return the dictionary; AWS automatically converts it to JSON for your CLI
    return {"answer": answer}