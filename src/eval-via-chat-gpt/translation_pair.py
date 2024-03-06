class TranslationPair:
    def __init__(self, csv_line, line_num):
        # source_text, source_language, target_language, translation_a, translation_b
        parts = csv_line.split(",")
        self.source_text = parts[0]
        self.source_language = parts[1]
        self.target_language = parts[2]
        self.translation_a = parts[3]
        self.translation_b = parts[4]
        self.line_num = line_num
