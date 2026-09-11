import boto3 
import uuid
import sys

client = boto3.client('bedrock-agentcore', region_name='us-east-1')
session_id = str(uuid.uuid4())
harness_arn = "arn:aws:bedrock-agentcore:us-east-1:554660509057:harness/thinknyx_support_harness-KS0OHPc9hm"
print("==================================================") 
print(" 🛒 ThinkNyx Retail Support Agent (Gateway Enabled)")
print("==================================================") 
print("Ask about our return policies, or type 'quit' to exit.\n") 
while True:
    user_input = input("User: ")
    if user_input.lower() == "quit":
        print("Exiting the chat. Goodbye!")
        sys.exit(0)
    print(" Agent is processing your request...\n")
    try:
        response = client.invoke_harness(
        harnessArn=harness_arn,
        runtimeSessionId=session_id,
        messages=[{"role": "user", "content": [{"text": user_input}]}]
    )
        for event in response['stream']: 
                     
        # 1. Safely grab the 'delta' (for text) and 'start' (for tools) blocks 
            delta = event.get('contentBlockDelta', {}).get('delta', {}) 
            start = event.get('contentBlockStart', {}).get('start', {})         
        # 2. If it contains text, print it 
            if 'text' in delta: 
                print(delta['text'], end="", flush=True) 
         # 3. If it contains a tool, print the tool name 
            if 'toolUse' in start: 
                tool_name = start['toolUse']['name'] 
                print(f"\n[SYSTEM] Agent is querying the Gateway using tool: '{tool_name}'...\n Agent: ", end="", flush=True)
        print("\n")
    except Exception as e:
    
        print(f"\n[SYSTEM ERROR] {e}\n") 