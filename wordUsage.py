#
# Simple word-frequency text analysis program
#
# This takes text and removes all the punctuation from it reducing it to a list or words.
# Then it works out the frequency of each word in the text (so 1,000 words containing the word "is" four
# times would give "is" 0.004). Then it divides that frequency by the frequency of the same word
# in English in general, so values bigger than 1.0 mean the text contains the word more often than general English
# and less than 1.0 means the text contains them less.
#
# It then saves the result to a file in the following form:
#
# frock 286.979537
#   .
#   .
# told 0.627716
#   .
#   .
# sarasate (1.62e-08)
#   .
#   .
# world (0.000776)
#   .
#   .
# cleanthat (possibly misspelled or unknown)
#
# The words in the document that are much more heavily used than they are in general English are listed
# first, followed by the number giving how much more frequent they are than in general English.
#
# Words with a frequency in brackets appear after that list. They each only appear once in the text
# and the number in brackets is their frequency in English. This list is ordered rarest word first.
#
# Finally there is a list of words that don't appear in English at all. These are usually things like foreign words
# or typos.
#
# This needs the Python 3 wordfreq package from here: https://github.com/rspeer/wordfreq
#
# 'The Red Headed League' (including a few typos) is included as a test text. To run the program:
#
# $ python3 wordUsage.py the-red-headed-league.txt rhl.op
#
# This will put the output in the file rhl.op.
#
# If someone wants to write a simple GUI for this and hit me with a pull request, that would be great!
#
# This program was written by GPT4 under instruction from me (Adrian Bowyer).
#
# Licence: GPL
#

import sys
import re
from wordfreq import word_frequency

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Replace hyphens with a space before removing non-alphabetic characters
        content = content.replace('-', ' ')
        # Remove possessives and general apostrophe s by stripping any "'s" from words
        content = re.sub(r"['’]s\b", "", content)
        # Remove all characters that are not letters or spaces
        cleaned_content = re.sub('[^a-zA-Z\s]', '', content)
        cleaned_content = cleaned_content.lower()
        words = cleaned_content.split()
        return words


def count_and_sort_words_by_relative_frequency(words_list):
    word_count = {}
    for word in words_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    total_words = len(words_list)
    word_frequencies = []
    single_occurrence_words = []
    zero_english_frequency_words = []

    for word, count in word_count.items():
        general_freq = word_frequency(word, 'en')
        if general_freq == 0:  # Treat as a spelling mistake or unknown word
            zero_english_frequency_words.append((word, 0, 0))
        elif count == 1:
            # Handle single occurrence words separately, set flag as 1
            single_occurrence_words.append((word, general_freq, 1))
        else:
            doc_freq = count / total_words
            relative_frequency = doc_freq / general_freq
            # Normal word that appears multiple times, flag as 2
            word_frequencies.append((word, relative_frequency, 2))

    # Sort normal frequencies by relative frequency in descending order
    sorted_word_frequencies = sorted(word_frequencies, key=lambda x: (-x[1], x[0]))

    # Sort single occurrence words by their general English frequency, rarest first
    sorted_single_occurrences = sorted(single_occurrence_words, key=lambda x: x[1])

    # Add single occurrence words and zero frequency words at the end
    sorted_word_frequencies.extend(sorted_single_occurrences)
    sorted_word_frequencies.extend(zero_english_frequency_words)

    return sorted_word_frequencies

def write_results_to_file(results, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, freq, flag in results:
            if flag == 0:  # Spelling mistakes or unknown words
                file.write(f"{word} (possibly misspelled or unknown)\n")
            elif flag == 1:  # Single occurrence with English frequency
                file.write(f"{word} ({freq})\n")
            else:  # Word appears multiple times
                file.write(f"{word} {freq:.6f}\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python wordUsage.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    words = process_text_file(input_file)
    word_frequencies = count_and_sort_words_by_relative_frequency(words)
    write_results_to_file(word_frequencies, output_file)
    print("Processing completed. Output written to:", output_file)

if __name__ == "__main__":
    main()
