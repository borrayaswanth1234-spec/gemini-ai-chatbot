from google import genai

client = genai.Client(api_key="AIzaSyAAql_fmScCibtd-e66X01fsls_xsyuD-Y")

questions = [
    "What is the capital of France?",
    "Write me a short poem",
    "Explain quantum physics simply"
]

for question in questions:
    print(f"\nQuestion: {question}")
    print("-" * 40)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )
    print(response.text)