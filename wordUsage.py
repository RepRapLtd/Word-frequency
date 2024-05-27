#
# Simple word-frequency text analysis program
#
# We should probably ignore Victorian ideas about elegant variation when writing. But, if you're a writer, you
# do probably want to know if you've used the word "gargantuan" twice within three pages. This
# program attempts to analyse that sort of thing for you. (Yes. The "probably" was deliberate...)
#
# This takes text and removes all the punctuation from it reducing it to a list of words.
# Then it works out the frequency of each word in the text (so 1,000 words containing the word "is" four
# times would give "is" 0.004). Then it divides that frequency by the frequency of the same word
# in English in general, so values bigger than 1.0 mean the text contains the word more often than general English
# and less than 1.0 means the text contains them less.
#
# It then saves the result to a CSV file in the following form:
#
# frock,286.979537,5615,2
#   .
#   .
# told,0.627716,279,2
#   .
#   .
# sarasate,1.62e-08,,1
#   .
#   .
# world,0.000776,,1
#   .
#   .
# cleanthat,possibly misspelled or unknown,,
#
# The words in the text that are more heavily used than they are in general English are listed
# first, followed by the number giving how much more frequent they are than in general English, followed by
# the shortest gap between two instances of the word in the text, followed by the number of times
# the word appears. The gap is the number of other words in between.
#
# Words with a count of 1 appear after that list. The number in brackets is their frequency in English. This list
# is ordered rarest word first.
#
# Finally there is a list of words that don't appear in English at all. These are usually things like foreign words
# or typos.
#
# This needs the Python 3 wordfreq package from here: https://github.com/rspeer/wordfreq
#
# 'The Red Headed League' (including a few typos) is included as a test text. To run the program:
#
# $ python3 wordUsage.py the-red-headed-league.txt rhl.csv
#
# This will put the output in the file rhl.csv that you can ten read in to a spreadsheet.
#
# If someone wants to write a simple GUI for this and hit me with a pull request, that would be great!
#
# It should also be quite simple to make it work for languages other than English. The
# wordfreq package has multilingual support.
#
# This program was written by GPT4 under instruction from me, Adrian Bowyer.
#
# Licence: GPL
#

import sys
import re
from wordfreq import word_frequency
import csv
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
    word_positions = {}

    # First pass: Count the occurrences and record positions of each word
    for index, word in enumerate(words_list):
        if word in word_count:
            word_count[word] += 1
            word_positions[word].append(index)
        else:
            word_count[word] = 1
            word_positions[word] = [index]

    total_words = len(words_list)
    word_frequencies = []
    single_occurrence_words = []
    zero_english_frequency_words = []
    min_gaps = {}  # To store the minimum gap for each word

    # Second pass: Calculate relative frequencies and find minimum gaps
    for word, count in word_count.items():
        general_freq = word_frequency(word, 'en')
        if general_freq == 0:  # Treat as a spelling mistake or unknown word
            zero_english_frequency_words.append((word, 0, 0))
        elif count == 1:
            single_occurrence_words.append((word, general_freq, 1))
        else:
            # Calculate document frequency
            doc_freq = count / total_words
            relative_frequency = doc_freq / general_freq if general_freq != 0 else doc_freq
            word_frequencies.append((word, relative_frequency, count))

            # Calculate minimum gap
            positions = word_positions[word]
            min_gap = min(positions[i] - positions[i - 1] for i in range(1, len(positions)))
            min_gaps[word] = min_gap

    # Sort the list of tuples by relative frequency in descending order for normal words
    sorted_word_frequencies = sorted(word_frequencies, key=lambda x: (-x[1], x[0]))

    # Sort single occurrence words by their general English frequency, rarest first
    sorted_single_occurrences = sorted(single_occurrence_words, key=lambda x: x[1])

    # Combine and return the results
    sorted_word_frequencies.extend(sorted_single_occurrences)
    sorted_word_frequencies.extend(zero_english_frequency_words)

    return sorted_word_frequencies, min_gaps




def write_results_to_file(results, min_gaps, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Word", "Relative Frequency", "Minimum Gap", "Count"])

        for word, freq, count in results:
            if count == 0:  # Spelling mistakes or unknown words
                writer.writerow([word, "possibly misspelled or unknown", "", ""])
            elif count == 1:  # Single occurrence with English frequency
                writer.writerow([word, freq, "", 1])
            else:  # Word appears multiple times
                min_gap = min_gaps.get(word, 'N/A')
                writer.writerow([word, f"{freq:.6f}", min_gap, count])

# Example of how to use the modified function:
# Assuming you have a list of (word, frequency, flag) tuples called 'results' and a dictionary 'min_gaps':
# results, min_gaps = count_and_sort_words_by_relative_frequency(words)
# write_results_to_file(results, min_gaps, 'output.csv')


'''
def main():
    if len(sys.argv) != 3:
        print("Usage: python wordUsage.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    words = process_text_file(input_file)
    word_frequencies, min_gaps = count_and_sort_words_by_relative_frequency(words)
    write_results_to_file(word_frequencies, min_gaps, output_file)
    print("Processing completed. Output written to:", output_file)

if __name__ == "__main__":
    main()
'''
words = process_text_file("the-red-headed-league.txt")
word_frequencies, min_gaps = count_and_sort_words_by_relative_frequency(words)
write_results_to_file(word_frequencies, min_gaps, "rhl.csv")
