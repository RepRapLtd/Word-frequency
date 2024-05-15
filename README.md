# Word-frequency

Simple word-frequency text analysis program

 This takes text and removes all the punctuation from it reducing it to a list or words.
Then it works out the frequency of each word in the text (so 1,000 words containing the word "is" four
times would give "is" 0.004). Then it divides that frequency by the frequency of the same word
in English in general, so values bigger than 1.0 mean the text contains the word more often than general English
and less than 1.0 means the text contains them less.

It then saves the result to a file in the following form:

```

frock 286.979537
  .
  .
told 0.627716
  .
  .
sarasate (1.62e-08)
  .
  .
world (0.000776)
  .
  .
cleanthat (possibly misspelled or unknown)

```

The words in the document that are much more heavily used than they are in general English are listed
first, followed by the number giving how much more frequent they are than in general English.

Words with a frequency in brackets appear after that list. They each only appear once in the text
and the number in brackets is their frequency in English. This list is ordered rarest word first.

Finally there is a list of words that don't appear in English at all. These are usually things like foreign words
or typos.

If I get a chance I'll add a bit that allows you to detect rare words that are used close together, so if 
you've used "frock" twice in thirty lines, it'll tell you.

This needs the Python 3 wordfreq package from here: https://github.com/rspeer/wordfreq

'The Red Headed League' (including a few typos) is included as a test text. To run the program:

$ python3 wordUsage.py the-red-headed-league.txt rhl.op

This will put the output in the file rhl.op.

If someone wants to write a simple GUI for this and hit me with a pull request, that would be great!

This program was written by GPT4 under instruction from me (Adrian Bowyer).

Licence: GPL


