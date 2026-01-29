import requests

MCP_BASE = "http://localhost:8000/mcp"

def register_page_locators(page_name, locators):
    try:
        requests.post(f"{MCP_BASE}/register", json={
            "page_name": page_name,
            "locators": locators
        }, timeout=2)
    except:
        pass


def get_locator(page_name, element_name):
    try:
        r = requests.get(f"{MCP_BASE}/locator/{page_name}/{element_name}", timeout=2)
        return r.json().get("locator")
    except:
        return None


def heal_locator(page_name, element_name, dom_json, question):
    r = requests.post(f"{MCP_BASE}/heal", json={
        "page_name": page_name,
        "element_name": element_name,
        "dom_json": dom_json,
        "question": question
    }, timeout=60)

    return r.json()["healed_locator"]
