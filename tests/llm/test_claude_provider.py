import json

from llm.providers.claude_provider import ClaudeProvider


def test_parse_json_plain():
    assert ClaudeProvider._parse_json('{"strategy":"role"}') == {"strategy": "role"}


def test_parse_json_code_fence():
    assert ClaudeProvider._parse_json('```json\n{"strategy":"role"}\n```') == {
        "strategy": "role"
    }
