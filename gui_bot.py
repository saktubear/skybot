import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from google import genai

client = genai.Client()
chat = client.chats.create(model="models/gemini-3.5-flash-lite")


def add_text(text):
    box.config(state="normal")
    box.insert(tk.END, text + "\n\n")
    box.config(state="disabled")
    box.see(tk.END)


def get_reply(message):
    try:
        reply = chat.send_message(message).text
    except Exception:
        reply = "Sorry, something went wrong. Please try again."
    root.after(0, lambda: show_reply(reply))


def show_reply(reply):
    add_text("Bot: " + reply)
    send_button.config(state="normal")


def send(event=None):
    message = entry.get().strip()
    if message == "":
        return
    entry.delete(0, tk.END)
    add_text("You: " + message)
    send_button.config(state="disabled")
    threading.Thread(target=get_reply, args=(message,), daemon=True).start()


root = tk.Tk()
root.title("AI Chatbot")
root.geometry("500x600")

box = ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Arial", 12))
box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

bottom = tk.Frame(root)
bottom.pack(padx=10, pady=(0, 10), fill=tk.X)

entry = tk.Entry(bottom, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", send)

send_button = tk.Button(bottom, text="Send", command=send)
send_button.pack(side=tk.RIGHT, padx=(10, 0))

entry.focus()
root.mainloop()