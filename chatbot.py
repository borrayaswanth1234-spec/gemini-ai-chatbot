from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY_HERE")

conversation_history = []

print(" AI Chatbot (type 'quit' to exit)")
print("-" * 40)

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    conversation_history.append(
        types.Content(role="user", parts=[types.Part(text=user_input)])
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history
    )
    
    bot_reply = response.text
    print(f"Bot: {bot_reply}")
    print("-" * 40)
    
    conversation_history.append(
        types.Content(role="model", parts=[types.Part(text=bot_reply)])
    )