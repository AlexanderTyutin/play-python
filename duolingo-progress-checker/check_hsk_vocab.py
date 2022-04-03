#!/usr/bin/python3
"""
Script to control progress of HSK vocabulary learning
"""

import sys
import random


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
            if ';' in line:
                result[line.strip().split(';')[0]] = True
            elif '\t' in line:
                result[line.strip().split('\t')[0]] = True
            else:
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

    start_learn_count = len(learn_words)

    print("\nLearned " + str(start_learn_count - need_to_learn_count) + ":")
    print('*' * (start_learn_count - need_to_learn_count))
    print("\nNeed to learn " + str(need_to_learn_count) + "/" + str(start_learn_count) + ":")
    print("*" * need_to_learn_count)
    print("")


def get_args():
    """
    Returns the args dictionary based on args passed to the script.
    """

    result = {
        'hsk-vocabulary-file': 'hsk-vocab.txt',
        'known-words-file': 'words.duo',
        'print-full-hsk': False,
        'print-remaining-hsk': False,
        'print-known-hsk': False,
        'print-progress': False,
        'play-game': False
    }

    usage_message = """
    Usage: python3 check_hsk_vocab.py

    Parameters:
        print-full-hsk          Print full HSK vocabulary from the appropriate file.
        print-remaining-hsk     Print HSK vocabulary words those are unknown yet.
        print-known-hsk         Print only known HSK words with meanings from HSK vocabulary.
        print-progress          Print graphics "I know this count - I need to learn this count".
        print-non-hsk           Print non HSK words from the known wordlist file.
        play-game               Run simple question game to check known words.
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
            elif arg == 'play-game':
                result['play-game'] = True

    return result


def game_get_question_data(vocabulary):
    """
    Returns question entities
    """
    max_number = len(vocabulary) - 1
    result_answer_word = random.randint(0, max_number)
    result_choises = [result_answer_word, -1, -1, -1]
    answers_count = 4

    for index in range(1, answers_count):
        while True:
            answer_number = random.randint(0, max_number)
            if answer_number not in result_choises:
                result_choises[index] = answer_number
                break

    random.shuffle(result_choises)

    return result_answer_word, result_choises


def game_print_question(vocabulary, shown_word_number, shown_choices):
    """
    Prints question to stdout
    """
    print("\n\t\t\t", vocabulary[shown_word_number][0], "\n")
    index = 0
    for choise in shown_choices:
        index += 1
        print(str(index) + ")", vocabulary[choise][1])


def play_game(known_vocabulary):
    """
    Runs game to refresh knowledge
    """
    user_choise = -1

    while int(user_choise) != 0:
        word_number, choises = game_get_question_data(known_vocabulary)

        game_print_question(known_vocabulary, word_number, choises)

        user_choise = input("\nEnter your choice (0 for exit): ")

        try:
            if int(user_choise) == 0:
                print("\n\t\t\tGood bye!\n")
            elif int(user_choise) == choises.index(word_number) + 1:
                print("\n\t\t\tRight!\n")
            else:
                print("\n\t\t\tWrong! Right answer:",
                      choises.index(word_number) + 1, "\n")
        except Exception as ex:
            print(
                "\n\t\t\tYour choice is not acceptable! Type only numbers from 1 to 4!\n")
            print("\t\t\t", str(ex))
            user_choise = -1


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
        print_vocabulary(hsk_vocabulary)

    if start_args['print-progress']:
        print_progress(hsk_vocabulary, known_words)

    if start_args['play-game']:
        play_game(known_dict_to_vocabulary(known_words, hsk_vocabulary))


if __name__ == "__main__":
    main()
