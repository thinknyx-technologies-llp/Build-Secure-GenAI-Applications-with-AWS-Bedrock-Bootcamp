import PyPDF2
import tiktoken
import boto3
from datetime import datetime
import json
class DocumentProcessor:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.s3 = boto3.client('s3', region_name='us-east-1')
    def extract_text(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text()
        return text
    def count_tokens(self, text):
        tokens = self.encoding.encode(text)
        return len(tokens)
    def chunk_text(self, text):
        chunk_size = 800 * 4  # 800 tokens = ~3200 chars
        overlap = 100 * 4     # 100 tokens = ~400 chars
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if len(chunk) > 50:
                chunks.append(chunk)
            start = end - overlap  # KEY LINE            
        return chunks
    def validate_chunks(self, chunks):
        token_counts = [self.count_tokens(c) for c in chunks]
        print(f"Total chunks: {len(chunks)}")
        print(f"Avg tokens: {sum(token_counts)//len(token_counts)}")
        print(f"Min: {min(token_counts)}, Max: {max(token_counts)}")
    def upload_to_s3(self, chunks, doc_name, bucket):
        for i, chunk in enumerate(chunks):
            data = {
                "chunk_id": f"{doc_name}-chunk-{i:03d}",
                "content": chunk,
                "tokens": self.count_tokens(chunk),
                "timestamp": datetime.now().isoformat()
            }
            key = f"chunks/{doc_name}/chunk-{i:03d}.json"
            self.s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(data, indent=2)
            )
        print(f"Uploaded {len(chunks)} chunks to S3")
    def process(self, pdf_path, doc_name, bucket):
        print(f"\n=== Processing {doc_name} ===\n")        
        text = self.extract_text(pdf_path)
        print(f"Extracted: {self.count_tokens(text)} tokens\n")        
        chunks = self.chunk_text(text)
        self.validate_chunks(chunks)        
        self.upload_to_s3(chunks, doc_name, bucket)
        print(f"Location: s3://{bucket}/chunks/{doc_name}/")
