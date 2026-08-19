from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json
import ollama

from db import init_db, get_locator, upsert_locator

init_db()
app = FastAPI()


class RegisterLocators(BaseModel):
    page_name: str
    locators: list   # [{element_name, primary_locator}]


class HealRequest(BaseModel):
    page_name: str
    element_name: str
    dom_json: dict
    question: str


@app.post("/mcp/register")
async def register_locators(data: RegisterLocators):
    for loc in data.locators:
        upsert_locator(
            data.page_name,
            loc["element_name"],
            loc["primary_locator"],
            None,
            datetime.utcnow().isoformat()
        )
    return {"status": "registered"}


@app.get("/mcp/locator/{page_name}/{element_name}")
async def fetch_locator(page_name: str, element_name: str):
    locator = get_locator(page_name, element_name)
    return {"locator": locator}


@app.post("/mcp/heal")
async def heal_locator(req: HealRequest):

    prompt = f"""
You are a test automation healer.
Given DOM JSON, find a reliable Playwright locator.

DOM:
{json.dumps(req.dom_json)}

Question:
{req.question}

Return ONLY Playwright locator. No explanation.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    healed_locator = response["message"]["content"].strip()

    upsert_locator(
        req.page_name,
        req.element_name,
        primary_locator="",
        healed_locator=healed_locator,
        timestamp=datetime.utcnow().isoformat()
    )

    return {"healed_locator": healed_locator}
