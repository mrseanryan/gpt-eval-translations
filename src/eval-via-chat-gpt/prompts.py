import json

import config

def EVAL_TWO_TRANSLATIONS(pair):
    return f'''Evaluate these 2 translations from {pair.source_language} to {pair.target_language}, indicating is A or B better:

{pair.source_language.upper()}: {pair.source_text}

a) `{pair.translation_a}`
b) `{pair.translation_b}`

Output *only* in JSON, with properties: translationScoreOutOf10A, translationScoreOutOf10B, AorB, translationAcomment, translationBcomment'''

def EVAL_MANY_TRANSLATIONS(source_language, target_language, pairs):
    def PROMPT_TEMPLATE(source_language, target_language, pair_prompts):
        pairs = "\n".join(pair_prompts)
        exampleJson = '{ "results": [{ "pair": 1, "AorB": "A" }, { "pair": 2, "AorB": "A" }]}'
        return f'''Evaluate these translation pairs from {source_language} to {target_language}, indicating is A or B better:

{pairs}

Output *only* in JSON, like this: {exampleJson}'''

    def PAIR_PROMPT_TEMPLATE(N, source_language, source_text, translation_a, translation_b):
        return f'''PAIR: {N}
{source_language.upper()}: {source_text}
{N}.A) `{translation_a}`
{N}.B) `{translation_b}`

'''

    def assert_equal(expected, actual, message):
        if expected != actual:
            raise ValueError(message)

    def validate_pair(pair):
        assert_equal(source_language, pair.source_language, f"Expected pair to have source_language={source_language} but was {pair.source_language}")
        assert_equal(target_language, pair.target_language, f"Expected pair to have target_language={target_language} but was {pair.target_language}")

    pair_prompts = []
    for pair in pairs:
        validate_pair(pair)

        pair_prompts.append(PAIR_PROMPT_TEMPLATE(pair.line_num, source_language, pair.source_text, pair.translation_a, pair.translation_b))

    return PROMPT_TEMPLATE(source_language, target_language, pair_prompts)

def _clean_response(response):
    if "```json" in response:
        return response.replace('```json', '').replace('```', '')
    return response.replace('```', '')

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
    return json.loads(_clean_response(response))


def parse_reponse_for_batch(response):
    """Expected format:
    "results": [{
    "pair": 1,
    "AorB": "A"
    },
    {
    "pair": 2,
    "AorB": "A"
    },
    {
    "pair": 3,
    "AorB": "A"
    }]}
    """
    return json.loads(_clean_response(response))

def dummy_response(is_batch):
    if not config.is_dry_run:
        return None
    if is_batch:
        return '''{"results": [{
"pair": 1,
"AorB": "A"
},
{
"pair": 2,
"AorB": "B"
},
{
"pair": 3,
"AorB": "Z"
}]}'''

    return '''
{
"translationScoreOutOf10A": 8,
"translationScoreOutOf10B": 9,
"AorB": "B",
"translationAcomment": "Translation A is grammatically correct and conveys the intended meaning, but it could be improved by using the verb 'llegar' to ask 'How do I arrive at the beach?'",
"translationBcomment": "Translation B is grammatically correct and natural-sounding. It directly asks 'How do I get to the beach?' and is the better option."
}
'''
