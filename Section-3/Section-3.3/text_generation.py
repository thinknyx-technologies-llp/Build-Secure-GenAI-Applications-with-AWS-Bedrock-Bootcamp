import boto3
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'   
)   
model_id = "amazon.nova-lite-v1:0"
response =client.converse(modelId=model_id,messages=[
    {
        "role": "user",
        "content": [
            {
                "text": "Explain cloud computing in simple terms."
            }
        ]}
])
print(response["output"]["message"]["content"][0]["text"])
inferenceConfig={
    "temperature": 0.9,
    "maxTokens":400,
    "topP":0.9
}
