#!/usr/bin/python3
"""
Script to control progress of HSK vocabulary learning
"""

import sys


def load_hsk_vocabulary(filename):
    """
    Loads HSK vocabulary from the given file.
    """
    result = []

    with open(filename) as input_file:
        for line in input_file:
            hyeroglyph = ""
            reading = ""
            meaning = ""
            vocabulary_line = line.split('\t')
            hyeroglyph = vocabulary_line[0].strip()
            reading = vocabulary_line[1].strip()
            meaning = vocabulary_line[2].strip()
            result.append((hyeroglyph, reading + "\t\t" + meaning))

    return result


def known_dict_to_vocabulary(known_dict, vocabulary):
    """
    Creates known HSK vocabulary from the given known words list
    and full HSK vocabulary.
    """
    result = []

    for word in vocabulary:
        if known_dict.get(word[0], False):
            result.append(word)

    return result


def load_known_words(filename):
    """
    Loads known words from the given filename.
    """
    result = {}
    with open(filename) as input_file:
        for line in input_file:
            result[line.strip()] = True
    return result


def print_vocabulary(print_array, exclusions=None):
    """
    Prints the given vocabulary to stdout
    """
    if exclusions is None:
        exclusions = {}

    counter = 0
    for word in print_array:
        if len(exclusions) > 0:
            if exclusions.get(word[0], False):
                continue
        counter += 1
        if len(word[0]) < 3:
            print(counter, "\t", word[0], "\t", word[1])
        else:
            print(counter, "\t", word[0], word[1])


def print_progress(learn_words, known_words):
    """
    Prints the learning words progress to stdout.
    """
    need_to_learn_count = len(learn_words)
    for word in learn_words:
        if len(known_words) > 0:
            if known_words.get(word[0], False):
                need_to_learn_count = need_to_learn_count - 1

    print("\nLearned:")
    print('*' * len(known_words))
    print("\nNeed to learn:")
    print("*" * need_to_learn_count)
    print("")


def get_args():
    """
    Returns the args dictionary based on args passed to the script.
    """

    result = {
        'hsk-vocabulary-file': 'hsk-vocab.txt',
        'known-words-file': 'known-words.txt',
        'print-full-hsk': False,
        'print-remaining-hsk': False,
        'print-known-hsk': False,
        'print-progress': False
    }

    usage_message = """
    Usage: python3 check_hsk_vocab.py

    Parameters:
        print-full-hsk          Print full HSK vocabulary from the appropriate file.
        print-remaining-hsk     Print HSK vocabulary words those are unknown yet.
        print-known-hsk         Print only known HSK words with meanings from HSK vocabulary.
        print-progress          Print graphics "I know this count - I need to learn this count"
    """

    if len(sys.argv) == 1:
        print(usage_message)
    else:
        for arg in sys.argv[1:]:
            if arg == 'print-full-hsk':
                result['print-full-hsk'] = True
            elif arg == 'print-remaining-hsk':
                result['print-remaining-hsk'] = True
            elif arg == 'print-known-hsk':
                result['print-known-hsk'] = True
            elif arg == 'print-progress':
                result['print-progress'] = True

    return result


def main():
    """
    Main function
    """
    start_args = get_args()

    known_words = load_known_words(start_args['known-words-file'])
    hsk_vocabulary = load_hsk_vocabulary(start_args['hsk-vocabulary-file'])

    if start_args['print-known-hsk']:
        print("\nYou do know this words:\n")
        print_vocabulary(known_dict_to_vocabulary(known_words, hsk_vocabulary))

    if start_args['print-remaining-hsk']:
        print("\nYou should learn these words:\n")
        print_vocabulary(hsk_vocabulary, exclusions=known_words)

    if start_args['print-full-hsk']:
        print("\nHSK Vocabulary:\n")
        print_vocabulary(hsk_vocabulary, exclusions={})

    if start_args['print-progress']:
        print_progress(hsk_vocabulary, known_words)


if __name__ == "__main__":
    main()
