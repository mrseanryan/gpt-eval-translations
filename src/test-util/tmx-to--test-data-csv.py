"""
Takes a TMX file (XML) from https://opus.nlpl.eu/GNOME/en&es/v1/GNOME or similar and outputs CSV file for testing gpt-eval-translations
"""

import sys

from cornsnake import util_file, util_pick, util_print
import xml.etree.ElementTree as ET

def _parse_tu_elem(tu_elem):
    texts = []
    for e in tu_elem.iter():
        if e.tag == 'seg':
            texts.append(e.text.replace(",", " "))
    return texts

def _transform_tmx_to_csv(path_to_input_tmx_file, path_to_output_csv_file, row_count):
    print(f"Reading {row_count} random entries from TMX file...")
    tmx_text = util_file.read_text_from_file(path_to_input_tmx_file)

    root = ET.fromstring(tmx_text)
    tu_elems = list(root.findall('.//tu'))

    header_row = ['# original_text', 'translation_a__good', 'translation_b__bad', 'known_good']
    rows = [header_row]
    while (len(rows) - 1) < row_count:
        tu_elem = util_pick.pick_one_random(tu_elems)
        other_tu_elem = tu_elem
        while other_tu_elem == tu_elem:
            other_tu_elem = util_pick.pick_one_random(tu_elems)

        texts = _parse_tu_elem(tu_elem)
        original = texts[0]
        translation = texts[1]

        other_texts = _parse_tu_elem(other_tu_elem)
        bad_translation = other_texts[1]

        rows.append([original, translation, bad_translation, translation])

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
