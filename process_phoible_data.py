from collections import defaultdict
import json

# most_spoken_lang_codes = ["cmn", "spa", "eng", "hin", "arb", "por", "ben", "rus", "jpn", "pan", "deu", "jav", "wuu", "ind", "zsm", "tel", "vie", "kor", "fra", "mar", "tam"]

BILLION = 1000 * 1000 * 1000
MILLION = 1000 * 1000

# NOTES: "Lahnda" / "Western Punjabi", rank 20 on the wikipedia list with 82.8 million speakers, was
# left off because Phoible doesn't have an entry for it (only for some smaller language
# subgroupings).

most_spoken_langs = [
    { "rank":  1, "name": "English"                                   , "code": "eng" , "speakers": 1.268 * BILLION },
    { "rank":  2, "name": "Mandarin Chinese (incl. Standard Chinese)" , "code": "cmn" , "speakers": 1.120 * BILLION },
    { "rank":  3, "name": "Hindi"                                     , "code": "hin" , "speakers": 637.3 * MILLION },
    { "rank":  4, "name": "Spanish"                                   , "code": "spa" , "speakers": 537.9 * MILLION },
    { "rank":  5, "name": "French"                                    , "code": "fra" , "speakers": 276.6 * MILLION },
    { "rank":  6, "name": "Standard Arabic"                           , "code": "arb" , "speakers": 274.0 * MILLION },
    { "rank":  7, "name": "Bengali"                                   , "code": "ben" , "speakers": 265.2 * MILLION },
    { "rank":  8, "name": "Russian"                                   , "code": "rus" , "speakers": 258.0 * MILLION },
    { "rank":  9, "name": "Portuguese"                                , "code": "por" , "speakers": 252.2 * MILLION },
    { "rank": 10, "name": "Indonesian"                                , "code": "ind" , "speakers": 199.0 * MILLION },
    { "rank": 11, "name": "Urdu"                                      , "code": "urd" , "speakers": 170.6 * MILLION },
    { "rank": 12, "name": "German"                                    , "code": "deu" , "speakers": 131.6 * MILLION },
    { "rank": 13, "name": "Japanese"                                  , "code": "jpn" , "speakers": 126.4 * MILLION },
    { "rank": 14, "name": "Swahili"                                   , "code": "swh" , "speakers":  98.5 * MILLION },
    { "rank": 15, "name": "Marathi"                                   , "code": "mar" , "speakers":  95.3 * MILLION },
    { "rank": 16, "name": "Telugu"                                    , "code": "tel" , "speakers":  93.0 * MILLION },
    { "rank": 17, "name": "Turkish"                                   , "code": "tur" , "speakers":  85.2 * MILLION },
    { "rank": 18, "name": "Yue Chinese (incl. Cantonese)"             , "code": "yue" , "speakers":  84.9 * MILLION },
    { "rank": 19, "name": "Tamil"                                     , "code": "tam" , "speakers":  83.8 * MILLION },
    { "rank": 20, "name": "Western Punjabi (Lahnda)"                  , "code": "lah" , "speakers":  82.8 * MILLION },
    { "rank": 21, "name": "Wu Chinese (incl. Shanghainese)"           , "code": "wuu" , "speakers":  81.8 * MILLION },
    { "rank": 22, "name": "Korean"                                    , "code": "kor" , "speakers":  79.4 * MILLION },
    { "rank": 23, "name": "Vietnamese"                                , "code": "vie" , "speakers":  77.0 * MILLION },
    { "rank": 24, "name": "Hausa"                                     , "code": "hau" , "speakers":  72.7 * MILLION },
    { "rank": 25, "name": "Javanese"                                  , "code": "jav" , "speakers":  68.3 * MILLION },
    { "rank": 26, "name": "Egyptian Arabic"                           , "code": "arz" , "speakers":  67.8 * MILLION },
    { "rank": 27, "name": "Italian"                                   , "code": "ita" , "speakers":  67.7 * MILLION },
    { "rank": 28, "name": "Thai"                                      , "code": "tha" , "speakers":  60.7 * MILLION },
    { "rank": 29, "name": "Gujarati"                                  , "code": "guj" , "speakers":  60.7 * MILLION },
    { "rank": 30, "name": "Kannada"                                   , "code": "kan" , "speakers":  56.5 * MILLION },
]

weird_chars = {
    "g": "\u0261", # LATIN SMALL LETTER SCRIPT G
    "!": "\u01C3", # LATIN LETTER RETROFLEX CLICK
    "|": "\u01C0", # LATIN LETTER DENTAL CLICK
    "'": "\u02BC", # MODIFIER LETTER APOSTROPHE
    ":": "\u02D0", # MODIFIER LETTER TRIANGULAR COLON
}

all_base_ipa_symbols = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ɑ', 'ɐ', 'ɒ', 'æ',
    'ɓ', 'ʙ', 'β', 'ɔ', 'ɕ', 'ç', 'ɗ', 'ɖ', 'ð', 'ʤ', 'ə', 'ɘ', 'ɚ', 'ɛ', 'ɜ',
    'ɝ', 'ɞ', 'ɟ', 'ʄ', 'ɡ', 'ɠ', 'ɢ', 'ʛ', 'ɦ', 'ɧ', 'ħ', 'ɥ', 'ʜ', 'ɨ', 'ɪ',
    'ʝ', 'ɭ', 'ɬ', 'ɫ', 'ɮ', 'ʟ', 'ɱ', 'ɯ', 'ɰ', 'ŋ', 'ɳ', 'ɲ', 'ɴ', 'ø', 'ɵ',
    'ɸ', 'θ', 'œ', 'ɶ', 'ʘ', 'ɹ', 'ɺ', 'ɾ', 'ɻ', 'ʀ', 'ʁ', 'ɽ', 'ʂ', 'ʃ', 'ʈ',
    'ʧ', 'ʉ', 'ʊ', 'ʋ', 'ⱱ', 'ʌ', 'ɣ', 'ɤ', 'ʍ', 'χ', 'ʎ', 'ʏ', 'ʑ', 'ʐ', 'ʒ',
    'ʔ', 'ʡ', 'ʕ', 'ʢ', 'ǀ', 'ǁ', 'ǂ', 'ǃ',
]

def normalize_consonant(consonant):
    "Toss all diacritics, return None if it's an affricate"
    res = ""
    for c in consonant:
        if c in ['\u0660', '\u0665']:
            return None
        if c in all_base_ipa_symbols:
            res += c

    if len(res) is not 1:
        return None

    return res

    # return len(res) == 1 : res ? None;

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

        consonant = normalize_consonant(phoneme)

        if consonant is None or consonant is "":
            continue

        # print("%s: %s, %s" % (consonant, allophones, segment_class))
        res["phonemes"][consonant].update(allophones.strip("\"").split(" "))

    # Turn allophones back into a list
    res["phonemes"] = {k: list(v) for k, v in res["phonemes"].items()}

    return res

def pretty_print_language(lang):
    print("%s (\"%s\"):" % (lang["name"], lang["iso_code"]))

    for (phoneme, allophones) in lang["phonemes"].items():
        print("%s: %s" % (phoneme, ", ".join(list(allophones))))


def unmatched_phonemes(phoneme_set, lang):
    # print(lang["phonemes"].keys())
    return [p for p in phoneme_set if p not in lang["phonemes"].keys()]

def clean_langs(data, lang_list):
    res = {}
    for lang in lang_list:
        lang_code = lang["code"]
        if len(data[lang_code]) == 0:
            continue
        # merge dicts for result
        res[lang_code] = {**cleanup_lang(data[lang_code]), **lang}
    return res

def __main__():
    most_spoken_lang_codes = [lang["code"] for lang in most_spoken_langs]
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

    json_res = json.dumps(clean_langs(data, most_spoken_langs))

    # print(json_res)

    # NEXT_STEP: Figure out why the cleanup from normalize_consonant isn't making it through to the
    # website.

    with open("site/most_spoken.json", "w") as f:
        f.write(json_res)

    print("json written to file")

__main__()
