"""
Evaluates pairs of translations via sentence transformer, against a 'known good' translation.
"""
import sys

from sentence_transformers import SentenceTransformer, util
from cornsnake import util_file

print("Loading embedder model...")
# Load the model(here we use minilm)
model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_a_or_b(translation_a, translation_b, known_good, min_threshold):
    """
    Returns which is better: A or B or None
    """
    encoding_a = model.encode(translation_a)
    encoding_b = model.encode(translation_b)
    encoding_known_good = model.encode(known_good)

    # smaller is closer == better
    cos_sim_a = 1 - util.cos_sim(encoding_a, encoding_known_good)
    cos_sim_b = 1 - util.cos_sim(encoding_b, encoding_known_good)

    cos_min = min(cos_sim_a, cos_sim_b)
    if cos_min > min_threshold:
        return None  # Both A and B are poor translations
    if cos_sim_a < cos_sim_b:
        return "A"  # A is better
    else:
        return "B"  # B is better

def _print_usage_and_exit():
    print(f"USAGE: {sys.argv[0]} [path to CSV file] [threshold 0..1 <0 is very strict, 1 is very loose>]")
    print("    - format of CSV file is: original_text, (source_language), (target_language), translation_a, translation_b, known_good")
    exit(42)

def _validate_threshold(threshold):
    message = 'threshold must be a number > 0 and < 1'
    if threshold < 0:
        raise ValueError(message)
    if threshold >= 1:
        raise ValueError(message)

class Results:
    def __init__(self) -> None:
        self.a = 0
        self.b = 0
        self.neither = 0

    @staticmethod
    def _percent(num, den):
        return round((num * 100.0) / den, 2)

    def __str__(self) -> str:
        total = self.a + self.b + self.neither
        return f"A: {Results._percent(self.a, total)}, B: {Results._percent(self.b, total)} of {total} total texts."

def evaluate_from_csv(path_to_csv_file, threshold):
    lines = util_file.read_lines_from_file(path_to_csv_file, True)
    results = Results()
    for line in lines:
        # original_text, source_language, target_language, translation_a, translation_b, known_good
        parts = line.split(",")
        original_text = parts[0]
        translation_a = parts[3]
        translation_b = parts[4]
        known_good = parts[5]
        aOrB = evaluate_a_or_b(translation_a, translation_b, known_good, threshold)
        best = None
        if aOrB is None:
            print(f"'{original_text}' -> '(both A and B are poor quality)")
            results.neither += 1
            continue
        elif aOrB == "A":
            best = translation_a
            results.a += 1
        elif aOrB == "B":
            best = translation_b
            results.b += 1
        else:
            raise ValueError(f"Expected A or B or None - but got {aOrB}")
        print(f"'{original_text}' -> '{best}' [{aOrB} is best] [known good = '{parts[3]}']")
    return results

if __name__ == '__main__':
    len_args = len(sys.argv)
    if len_args == 3:
        path_to_csv_file = sys.argv[1]
        threshold = float(sys.argv[2])
        _validate_threshold(threshold)
        results = evaluate_from_csv(path_to_csv_file, threshold)
        print(results)
    else:
        _print_usage_and_exit()
