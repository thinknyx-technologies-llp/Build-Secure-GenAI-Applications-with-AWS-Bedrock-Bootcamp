import boto3
client = boto3.client(service_name ='bedrock-runtime', region_name='us-east-1')
model_id = "amazon.nova-lite-v1:0"
messages = []
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    messages.append({
        "role": "user",
        "content": [
            {
                "text": user_input
            }
        ]
    })
    response = client.converse(modelId=model_id, messages=messages)
    assistant_response = response["output"]["message"]["content"][0]["text"]
    print("Bot: ",assistant_response)
    messages.append(
        response["output"]["message"]
    )