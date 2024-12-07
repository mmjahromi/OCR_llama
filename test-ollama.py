import ollama

try:
    response = ollama.chat(
        model="llama3.2-vision",
        messages=[{"role": "user", "content": "Test message"}]
    )
    print("Connection successful. Response:", response)
except Exception as e:
    print("Connection failed:", e)
