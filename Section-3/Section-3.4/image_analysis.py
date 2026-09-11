import boto3
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)
with open("C:\\Users\\student\\bedrock-python-api\\office.jpeg", "rb") as image_file:
    image_bytes = image_file.read()
model_id = "amazon.nova-lite-v1:0"
messages = [ {
    "role": "user",
    "content": [
        { "image": {
            "format": "jpeg",
            "source": {
                "bytes": image_bytes  } }},
                {"text": "What objects are present on the table?"}
    ]
}]
response = client.converse(modelId=model_id, messages=messages)
print(response["output"]["message"]["content"][0]["text"])
