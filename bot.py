from google import genai

client = genai.Client()
chat = client.chats.create(model="models/gemini-3.5-flash-lite")

print("AI chatbot is ready! Type 'bye' to exit.")

while True:
    user = input("You: ")

    if user.lower() == "bye":
        print("Bot: Goodbye!")
        break

    response = chat.send_message(user)
    print("Bot", response.text)