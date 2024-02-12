import json
import sys

from cornsnake import util_file

import prompts
import service_chat

def evaluate_a_or_b(source_text, source_language, target_language, translation_a, translation_b):
    response = service_chat.send_prompt(prompts.EVAL_TWO_TRANSLATIONS(source_text, source_language, target_language, translation_a, translation_b))
    result = prompts.parse_response(response)
    aOrB = result['AorB']
    return aOrB

def evaluate_from_csv(path_to_csv_file):
    lines = util_file.read_lines_from_file(path_to_csv_file, True)
    for line in lines:
        # source_text, source_language, target_language, translation_a, translation_b
        parts = line.split(",")
        source_text = parts[0]
        source_language = parts[1]
        target_language = parts[2]
        translation_a = parts[3]
        translation_b = parts[4]
        aOrB = evaluate_a_or_b(source_text, source_language, target_language, translation_a, translation_b)
        best = None
        if aOrB is None:
            print(f"'{source_text}' -> '(both A and B are poor quality)")
            continue
        elif aOrB == "A":
            best = translation_a
        elif aOrB == "B":
            best = translation_b
        else:
            raise ValueError(f"Expected A or B or None - but got {aOrB}")
        print(f"'{source_text}' -> '{best}' [{aOrB} is best] [known good = '{parts[3]}']")

def _print_usage_and_exit():
    print(f"USAGE: {sys.argv[0]} [path to CSV file]")
    print("    - format of CSV file is: source_text, source_language, target_language, translation_a, translation_b")
    exit(42)

if __name__ == '__main__':
    len_args = len(sys.argv)
    if len_args == 2:
        path_to_csv_file = sys.argv[1]
        evaluate_from_csv(path_to_csv_file)
    else:
        _print_usage_and_exit()
