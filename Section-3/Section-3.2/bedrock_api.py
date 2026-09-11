import boto3
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'   
)
print("Bedrock Runtime Client Created Successfully")

