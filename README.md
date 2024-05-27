# Word-frequency

Simple word-frequency text analysis program

We should probably ignore Victorian ideas about elegant variation when writing. But, if you're a writer, you
do probably want to know if you've used the word "gargantuan" twice within three pages. This
program attempts to analyse that sort of thing for you. (Yes. The "probably" was deliberate...)

This takes text and removes all the punctuation from it reducing it to a list of words.
Then it works out the frequency of each word in the text (so 1,000 words containing the word "is" four
times would give "is" 0.004). Then it divides that frequency by the frequency of the same word
in English in general, so values bigger than 1.0 mean the text contains the word more often than general English
and less than 1.0 means the text contains them less.

It then saves the result to a CSV file in the following form:

frock,286.979537,5615,2
  .
  .
told,0.627716,279,2
  .
  .
sarasate,1.62e-08,,1
  .
  .
world,0.000776,,1
  .
  .
cleanthat,possibly misspelled or unknown,,

The words in the text that are more heavily used than they are in general English are listed
first, followed by the number giving how much more frequent they are than in general English, followed by
the shortest gap between two instances of the word in the text, followed by the number of times
the word appears. The gap is the number of other words in between.

Words with a count of 1 appear after that list. The number in brackets is their frequency in English. This list
is ordered rarest word first.

Finally there is a list of words that don't appear in English at all. These are usually things like foreign words
or typos.

This needs the Python 3 wordfreq package from here: https://github.com/rspeer/wordfreq

'The Red Headed League' (including a few typos) is included as a test text. To run the program:

$ python3 wordUsage.py the-red-headed-league.txt rhl.csv

This will put the output in the file rhl.csv that you can ten read in to a spreadsheet.

If someone wants to write a simple GUI for this and hit me with a pull request, that would be great!

It should also be quite simple to make it work for languages other than English. The 
wordfreq package has multilingual support.

This program was written by GPT4 under instruction from me, Adrian Bowyer.

Licence: GPL


