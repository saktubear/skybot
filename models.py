from google import genai

client = genai.Client()
for m in client.models.list():
    name = m.name
    if "flash" in name and "live" not in name and "audio" not in name and "image" not in name:
        print(name)