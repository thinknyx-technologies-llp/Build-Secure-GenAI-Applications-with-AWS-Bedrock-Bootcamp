from qa_system import HRQuestionAnswerer
qa = HRQuestionAnswerer(
    collection_endpoint="8x5ymmu9jd4t8stecpe6.aoss.us-east-1.on.aws"
)

question = "How many Sick leaves do I get if I join the company in February?"
answer = qa.ask(question)
print("=== FINAL ANSWER ===")
print(answer)