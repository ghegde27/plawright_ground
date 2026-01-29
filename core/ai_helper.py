from fastapi import FastAPI
import ollama

app = FastAPI()

@app.post("/mcp")
async def mcp_handler(payload: dict):
    prompt = payload["prompt"]

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a web automation assistant. Always return only Playwright locators, no explanations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {"response": response["message"]["content"]}
