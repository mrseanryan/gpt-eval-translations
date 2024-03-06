# Evaluate translations via Chat-GPT

With a simple prompt, we can ask the LLM to evaluate two translation results, assigning each a score, and indicating which is best. A simple prompt engineering trick is to pick suitable JSON property names - the LLM will figure out implicitly what is required. For example: “translationScoreOutOf10” or “aOrB”.

- a complete prompt resulting in predictable JSON structure:

```
Evaluate these 2 translations from {source_language} to {target_language}, indicating is A or B better:

{source_language.upper()}: {source_text}

a) `{translation_a}`
b) `{translation_b}`

Output *only* in JSON, with properties: translationScoreOutOf10A, translationScoreOutOf10B, AorB, translationAcomment, translationBcomment
```

Note the overall structure of the prompt:
- the task
- the input (with ‘data text’ enclosed with back-ticks, to distinguish it from ‘prompt text’).
- the output format, with a whitelist of acceptable properties

This prompt structure helps the LLM to ‘focus’ on the required task, and generate concise and relevant output. The output will be in a predictable JSON format, which is important if we wish to consume the LLM output via a script.

## Example output

```
=== INPUT ===
Evaluate these 2 translations from English to Spanish, indicating is A or B better:

ENGLISH: How do I get to the beach?

a) `cómo puedo llegar a la playa`
b) `Cómo llego a la playa`

Output *only* in JSON, with properties: translationScoreOutOf10A, translationScoreOutOf10B, AorB, translationAcomment, translationBcomment
=== RESPONSE ===
{
  "translationScoreOutOf10A": 8,
  "translationScoreOutOf10B": 9,
  "AorB": "B",
  "translationAcomment": "The translation 'cómo puedo llegar a la playa' is grammatically correct, but it is more common to use the verb 'llegar' in the first person singular form.",
  "translationBcomment": "The translation 'Cómo llego a la playa' is grammatically correct and uses the verb 'llegar' in the first person singular form, which makes it more natural and commonly used."
}
'How do I get to the beach?' -> 'Cómo llego a la playa' [B is best] [known good = 'cómo puedo llegar a la playa']
```

## Set up

```
pip3 install --upgrade openai==0.28.1 sentence-transformers==2.2.2
```

Set environment variable with your OpenAI key:

```
export OPENAI_API_KEY="xxx"
```

Add that to your shell initializing script (`~/.zprofile` or similar)

Load in current terminal:

```
source ~/.zprofile
```

## Test

`test.bat`

or

`python main.py ..\..\test-resources\english-to-spanish.csv` 3
