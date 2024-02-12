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
    print(f"USAGE: {sys.argv[0]} [path to CSV file]")
    print("    - format of CSV file is: original_text, translation_a, translation_b, known_good")
    exit(42)

def _validate_threshold(threshold):
    message = 'threshold must be a number > 0 and < 1'
    if threshold < 0:
        raise ValueError(message)
    if threshold >= 1:
        raise ValueError(message)

def evaluate_from_csv(path_to_csv_file, threshold):
    lines = util_file.read_lines_from_file(path_to_csv_file, True)
    for line in lines:
        # original_text, translation_a, translation_b, known_good
        parts = line.split(",")
        original_text = parts[0]
        translation_a = parts[1]
        translation_b = parts[2]
        known_good = parts[3]
        aOrB = evaluate_a_or_b(translation_a, translation_b, known_good, threshold)
        best = None
        if aOrB is None:
            print(f"'{original_text}' -> '(both A and B are poor quality)")
            continue
        elif aOrB == "A":
            best = translation_a
        elif aOrB == "B":
            best = translation_b
        else:
            raise ValueError(f"Expected A or B or None - but got {aOrB}")
        print(f"'{original_text}' -> '{best}' [{aOrB} is best] [known good = '{parts[3]}']")

if __name__ == '__main__':
    len_args = len(sys.argv)
    if len_args == 3:
        path_to_csv_file = sys.argv[1]
        threshold = float(sys.argv[2])
        _validate_threshold(threshold)
        evaluate_from_csv(path_to_csv_file, threshold)
    else:
        _print_usage_and_exit()
