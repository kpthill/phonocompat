from collections import defaultdict
import json

most_spoken_lang_codes = ["cmn", "spa", "eng", "hin", "arb", "por", "ben", "rus", "jpn", "pan", "deu", "jav", "wuu", "ind", "zsm", "tel", "vie", "kor", "fra", "mar", "tam"]

weird_chars = {
    "g": "\u0261", # LATIN SMALL LETTER SCRIPT G
    "!": "\u01C3", # LATIN LETTER RETROFLEX CLICK
    "|": "\u01C0", # LATIN LETTER DENTAL CLICK
    "'": "\u02BC", # MODIFIER LETTER APOSTROPHE
    ":": "\u02D0", # MODIFIER LETTER TRIANGULAR COLON
}

def phoibleify(chars):
    def replace_char(c):
        if c in weird_chars.keys():
            return weird_chars[c]
        return c
    return list(map(replace_char, chars))

# import phoible data, yielding languages that are in the list
def import_phoible(phoible_file_loc, langs_to_keep):
    res = defaultdict(list)
    count = 0
    with open(phoible_file_loc, 'r') as file:
        for line in file:
            count+=1
            fields = line.split(',')
            lang_code = fields[2].strip('"')
            if lang_code in langs_to_keep:
                res[lang_code].append(fields)
    print("%d lines processed" % count)
    return res

def cleanup_lang(data):
    assert(len(data) >= 1)
    assert(len(data[0]) >= 10)

    res = {}
    res["iso_code"] = data[0][2]
    res["name"] = data[0][3]
    res["phonemes"] = defaultdict(set)

    for datum in data:
        if " " in datum[3]:
            continue

        phoneme = datum[6].strip('"')
        allophones = datum[7].strip('"')
        segment_class = datum[9].strip('"')

        if not segment_class == "consonant":
            continue

        print("%s: %s, %s" % (phoneme, allophones, segment_class))
        res["phonemes"][phoneme].update(allophones.strip("\"").split(" "))

    res["phonemes"] = {k: list(v) for k, v in res["phonemes"].items()}

    return res

def pretty_print_language(lang):
    print("%s (\"%s\"):" % (lang["name"], lang["iso_code"]))

    for (phoneme, allophones) in lang["phonemes"].items():
        print("%s: %s" % (phoneme, ", ".join(list(allophones))))


def unmatched_phonemes(phoneme_set, lang):
    print(lang["phonemes"].keys())
    return [p for p in phoneme_set if p not in lang["phonemes"].keys()]

def clean_langs(data, lang_list):
    res = {}
    for lang_code in lang_list:
        res[lang_code] = cleanup_lang(data[lang_code])
    return res

def __main__():
    print("seeking languages:")
    print(most_spoken_lang_codes)

    data = import_phoible("../phoible/data/phoible.csv", most_spoken_lang_codes)

    print("Languages found:")
    print(data.keys())

    print("Missing:")
    print(set(most_spoken_lang_codes) - set(data.keys()))

    english = cleanup_lang(data["eng"])
    print("parsed for english:")
    print(pretty_print_language(english))

    trial_phonemes = phoibleify(list("bcdfgt")+["t̠ʃ", "tʃ"])
    print("unmatched phonemes for english from [%s]:" % trial_phonemes)
    print(unmatched_phonemes(trial_phonemes, english))

    print(json.dumps(clean_langs(data, most_spoken_lang_codes)))

__main__()
