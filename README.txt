setup:

pip3 install these things:
- dragonmapper, for pinyin <-> zhuyin
- zhon, for common chinese constants
- opencc, for most accurate traditional <-> simplified conversion
- jieba, for most accurate segmentation of chinese characters (works better in simplified chinese)
- pypinyin, to convert sentences to pinyin (simplified character inputs produces better results)
- pypinyin-dict, for more accurate pinyin dictionaries for pypinyin library
- cedict_utils, for parsing cedict dictionaries automatically
- sqlite3, for cedict lookups
- peewee, ORM for sqlite3

found some weaknesses in some package, e.g.:
- in pinyin_jyutping_sentence: does not seem to support multiple pronounciations of a hanzi characters
- this application uses three different libraries to utilise the strengths of each package

errors:
- Some unique pronounciation (e.g. yō, ō) raises an error, current limitations of dragonmapper library

usage:
run python in the main directory, then copy paste the following script according to your needs :)

A. to convert Pleco flashcards to Anki, run the following, and change as necessary:

from pleco_to_anki import PlecoToAnki
PlecoToAnki(
  input='input/pleco-immersion.txt',
  output='output/anki-immersion.txt',
  tags='Vocabulary Incomplete Immersion'
)

B. to convert sentences card to Anki, run the following and change as necessary

from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/test_sentences.txt',
  output='output/test_sentences.txt',
  tags='Test Tags Test_Tags'
)

thanks, and have fun!