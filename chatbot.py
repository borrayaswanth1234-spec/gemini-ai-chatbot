from google import genai
from google.genai import types
from datetime import datetime

client = genai.Client(api_key="YOUR_API_KEY_HERE")

history = []

log = open("chat_history.txt", "a")
log.write(f"\n=== Chat started at {datetime.now().strftime('%d %b %Y, %I:%M %p')} ===\n")

print("Hey! I'm your AI assistant. Type 'quit' to exit.")
print("-" * 45)

while True:
    user_msg = input("You: ").strip()


    if not user_msg:
        continue

    if user_msg.lower() == "quit":
        print("See you later!")
        log.write("=== Chat ended ===\n")
        log.close()
        break

    history.append(
        types.Content(role="user", parts=[types.Part(text=user_msg)])
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history
    )
    reply = response.text

    print(f"Bot: {reply}")
    print("-" * 45)
    log.write(f"You: {user_msg}\nBot: {reply}\n")
    log.flush()


    history.append(
        types.Content(role="model", parts=[types.Part(text=reply)])
    )