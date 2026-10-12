import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from google import genai
from google.genai import types

MODEL = "models/gemini-3.5-flash-lite"
PERSONALITY = "You are a helpful, friendly AI assistant. Answer clearly and naturally, like a normal chatbot."
client = genai.Client()


def new_chat():
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=PERSONALITY),
    )


chat = new_chat()


def add_text(name, text, name_tag):
    box.config(state="normal")
    box.insert(tk.END, name + "\n", name_tag)
    box.insert(tk.END, text + "\n\n", "body")
    box.config(state="disabled")
    box.see(tk.END)


def start_reply():
    box.config(state="normal")
    box.insert(tk.END, "SkyGPT\n", "bot_name")
    box.config(state="disabled")
    status.config(text="")


def add_piece(text):
    box.config(state="normal")
    box.insert(tk.END, text, "body")
    box.config(state="disabled")
    box.see(tk.END)


def finish_reply():
    add_piece("\n\n")
    send_button.config(state="normal")


def get_reply(message):
    root.after(0, start_reply)
    try:
        for chunk in chat.send_message_stream(message):
            piece = chunk.text or ""
            root.after(0, lambda p=piece: add_piece(p))
    except Exception:
        root.after(0, lambda: add_piece("Sorry, something went wrong. Please try again."))
    root.after(0, finish_reply)


def send(event=None):
    message = entry.get().strip()
    if message == "":
        return
    entry.delete(0, tk.END)
    add_text("You", message, "you_name")
    status.config(text="Bot is typing...")
    send_button.config(state="disabled")
    threading.Thread(target=get_reply, args=(message,), daemon=True).start()


def clear_chat():
    global chat
    chat = new_chat()
    box.config(state="normal")
    box.delete("1.0", tk.END)
    box.config(state="disabled")
    status.config(text="Chat cleared.")


def save_chat():
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        f.write(box.get("1.0", tk.END))
    status.config(text="Saved to chat_history.txt")


root = tk.Tk()
root.title("SkyBot : An AI Chatbot")
root.geometry("520x650")
root.config(bg="#1e1e1e")

box = ScrolledText(
    root, wrap=tk.WORD, state="disabled", font=("Arial", 12),
    bg="#1e1e1e", fg="#eeeeee", bd=0, padx=10, pady=10,
)
box.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)
box.tag_config("you_name", foreground="#4fc3f7", font=("Arial", 11, "bold"))
box.tag_config("bot_name", foreground="#81c784", font=("Arial", 11, "bold"))
box.tag_config("body", foreground="#eeeeee")

status = tk.Label(root, text="", bg="#1e1e1e", fg="#aaaaaa", anchor="w")
status.pack(padx=12, fill=tk.X)

bottom = tk.Frame(root, bg="#1e1e1e")
bottom.pack(padx=10, pady=(0, 10), fill=tk.X)

entry = tk.Entry(
    bottom, font=("Arial", 12), bg="#2d2d2d", fg="white",
    insertbackground="white", bd=0,
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
entry.bind("<Return>", send)

send_button = tk.Button(bottom, text="Send", command=send)
send_button.pack(side=tk.LEFT, padx=(8, 0))

tk.Button(bottom, text="Clear", command=clear_chat).pack(side=tk.LEFT, padx=(5, 0))
tk.Button(bottom, text="Save", command=save_chat).pack(side=tk.LEFT, padx=(5, 0))

entry.focus()
root.mainloop()