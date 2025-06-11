from g4f.client import Client


client = Client()
model = "gpt-4o"

def init():
    client.chat.completions.create(model = model, messages = [{"role": "user", "content": " "}])
    print("[gpt module]: gpt initialization successful")

def question(message: str, messages: list) -> str:
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model = model,
        messages = messages
    )
    
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    
    return answer