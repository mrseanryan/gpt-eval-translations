"""
Takes a TMX file (XML) from https://opus.nlpl.eu/GNOME/en&es/v1/GNOME or similar and outputs CSV file for testing gpt-eval-translations
"""

import sys
import xml.etree.ElementTree as ET

from cornsnake import util_file, util_pick, util_print
# pip install iso639-lang
from iso639 import Lang

problem_langs = set()

def _lang_name_or_code(code):
    if code == 'iw':
        code = 'he'  # Hebrew, new code
    if code == 'in':
        code = 'id'  # Indonesian, new code
    try:
        return Lang(code).name
    except:
        problem_langs.add(code)
        return code

def _parse_tu_elem(tu_elem):
    texts = []
    langs = []
    for e in tu_elem.iter():
        if e.tag == 'tuv':
            tmx_lang = "(unknown)"
            for a in e.attrib:
                if a.endswith('lang'):
                    tmx_lang = e.attrib[a]
                    break
            current_lang = _lang_name_or_code(tmx_lang)
            langs.append(current_lang)
        elif e.tag == 'seg':
            texts.append(e.text.replace(",", " "))
    return (texts, langs)

def _transform_tmx_to_csv(path_to_input_tmx_file, path_to_output_csv_file, row_count):
    print(f"Reading {row_count} random entries from TMX file...")
    tmx_text = util_file.read_text_from_file(path_to_input_tmx_file)

    root = ET.fromstring(tmx_text)
    tu_elems = list(root.findall('.//tu'))

    header_row = ['# original_text', 'source_language', 'target_language', 'translation_a__good', 'translation_b__bad', 'known_good']
    rows = [header_row]
    while (len(rows) - 1) < row_count:
        tu_elem = util_pick.pick_one_random(tu_elems)
        other_tu_elem = tu_elem
        while other_tu_elem == tu_elem:
            other_tu_elem = util_pick.pick_one_random(tu_elems)

        (texts, langs) = _parse_tu_elem(tu_elem)
        original = texts[0]
        translation = texts[1]

        (other_texts, _) = _parse_tu_elem(other_tu_elem)
        bad_translation = other_texts[1]

        source_lang = langs[0]
        target_lang = langs[1]

        rows.append([original, source_lang, target_lang, translation, bad_translation, translation])

    lines = []
    for row in rows:
        lines.append(",".join(row))
    util_print.print_result(f"Writing CSV to {path_to_output_csv_file}")
    util_file.write_text_lines_to_file(lines, path_to_output_csv_file)

def _print_usage_and_exit():
    print(f"USAGE: {sys.argv[0]} [path to input TMX file] [path to output CSV file] [row count]")
    exit(42)

if __name__ == '__main__':
    len_args = len(sys.argv)
    if len_args == 4:
        path_to_input_tmx_file = sys.argv[1]
        path_to_output_csv_file = sys.argv[2]
        row_count = int(sys.argv[3])
        _transform_tmx_to_csv(path_to_input_tmx_file, path_to_output_csv_file, row_count)
    else:
        _print_usage_and_exit()
