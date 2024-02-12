import json

def EVAL_TWO_TRANSLATIONS(source_text, source_language, target_language, translation_a, translation_b):
    return f"""Evaluate these 2 translations from {source_language} to {target_language}, indicating is A or B better:

{source_language.upper()}: {source_text}

a) `{translation_a}`
b) `{translation_b}`

Output *only* in JSON, with properties: translationScoreOutOf10A, translationScoreOutOf10B, AorB, translationAcomment, translationBcomment"""

def parse_response(response):
    """Expected format:
    {
    "translationScoreOutOf10A": 8,
    "translationScoreOutOf10B": 9,
    "AorB": "B",
    "translationAcomment": "Translation A is grammatically correct and conveys the intended meaning, but it could be improved by using the verb 'llegar' to ask 'How do I arrive at the beach?'",
    "translationBcomment": "Translation B is grammatically correct and natural-sounding. It directly asks 'How do I get to the beach?' and is the better option."
    }
    """
    return json.loads(response)
