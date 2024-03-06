import sys

from cornsnake import util_file, util_wait

import prompts
import service_chat
from translation_pair import TranslationPair

def _evaluate_a_or_b(pair):
    response = service_chat.send_prompt(prompts.EVAL_TWO_TRANSLATIONS(pair), dummy_response = prompts.dummy_response(False))
    result = prompts.parse_response(response)
    aOrB = result['AorB']
    return aOrB

def _evaluate_a_or_b_pairs_same_languages(source_language, target_language, pairs):
    response = service_chat.send_prompt(prompts.EVAL_MANY_TRANSLATIONS(source_language, target_language, pairs), dummy_response = prompts.dummy_response(True))
    result = prompts.parse_reponse_for_batch(response)
    return result

def _parse_response(aOrB, source_text, translation_a, translation_b):
    best = None
    if aOrB is None:
        print(f"'{source_text}' -> '(both A and B are poor quality)")
        return None
    elif aOrB == "A":
        best = translation_a
    elif aOrB == "B":
        best = translation_b
    else:
        raise ValueError(f"Expected A or B or None - but got {aOrB}")
    return best

def percent(num, denom, ndigits = 0):
    if denom == 0:
        return format(0, f'.{ndigits}f')
    return str(round((num * 100.0) / denom, ndigits)) + '%'

def evaluate_from_csv(path_to_csv_file, pairs_per_prompt):
    lines = util_file.read_lines_from_file(path_to_csv_file, True)

    a_is_best_count = 0
    b_is_best_count = 0
    unknown_best_count = 0

    if pairs_per_prompt == 1:
        line_num = 0
        for line in lines:
            line_num += 1
            pair = TranslationPair(line, line_num)
            aOrB = _evaluate_a_or_b(pair)
            best = _parse_response(aOrB, pair.source_text, pair.translation_a, pair.translation_b)
            if best is None:
                continue
            print(f"'{pair.source_text}' -> '{best}' [{aOrB} is best] [known good = '{pair.translation_a}']")
            if aOrB == 'A':
                a_is_best_count += 1
            elif aOrB == 'B':
                b_is_best_count += 1
            else:
                unknown_best_count += 1
    else:
        pairs = []
        line_num = 1
        for line in lines:
            pairs.append(TranslationPair(line, line_num))
            line_num += 1

        pairs_chunks_same_languages = []
        source_language = None
        target_language = None
        new_chunk = []
        for pair in pairs:
            if source_language is None:
                source_language = pair.source_language
            if target_language is None:
                target_language = pair.target_language

            need_new_chunk = len(new_chunk) == pairs_per_prompt or pair.source_language != source_language or pair.target_language != target_language
            if need_new_chunk:
                pairs_chunks_same_languages.append(new_chunk)
                source_language = pair.source_language
                target_language = pair.target_language
                new_chunk = [pair]
            else:
                new_chunk.append(pair)
        pairs_chunks_same_languages.append(new_chunk)

        for chunk in pairs_chunks_same_languages:
            source_language = chunk[0].source_language
            target_language = chunk[0].target_language
            result = _evaluate_a_or_b_pairs_same_languages(source_language, target_language, chunk)
            for pairResult in result['results']:
                aOrB = pairResult['AorB']
                if aOrB == 'A':
                    a_is_best_count += 1
                elif aOrB == 'B':
                    b_is_best_count += 1
                else:
                    unknown_best_count += 1

            util_wait.wait_seconds(1)

    print("")
    print("OVERALL RESULT:")
    print(f"A is best for {a_is_best_count} of {len(lines)} pairs [{percent(a_is_best_count, len(lines))}]")
    print(f"B is best for {b_is_best_count} of {len(lines)} pairs [{percent(b_is_best_count, len(lines))}]")
    print(f"Unknown best for {unknown_best_count} of {len(lines)} pairs [{percent(unknown_best_count, len(lines))}]")

def _print_usage_and_exit():
    print(f"USAGE: {sys.argv[0]} <path to CSV file> [batch size]")
    print("    - format of CSV file is: source_text, source_language, target_language, translation_a, translation_b")
    print("    - default batch size is 1 (for a more detailed response)")
    exit(42)

if __name__ == '__main__':
    len_args = len(sys.argv)
    path_to_csv_file = None
    batch_size = 1
    if len_args == 2:
        path_to_csv_file = sys.argv[1]
    elif len_args == 3:
        path_to_csv_file = sys.argv[1]
        batch_size = int(sys.argv[2])
    else:
        _print_usage_and_exit()
    evaluate_from_csv(path_to_csv_file, batch_size)
