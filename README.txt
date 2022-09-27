pip3 install these things:

opencc, for most accurate traditional <-> simplified conversion
jieba, for most accurate segmentation of chinese characters
pypinyin, to convert sentences to pinyin (simplified character inputs produces better results)
pypinyin-dict, for more accurate pinyin dictionaries for pypinyin library
cedict_utils, for parsing cedict dictionaries automatically
sqlite3, for cedict lookups
peewee, ORM for sqlite3


found some weaknesses in some package, e.g.:
- in pinyin_jyutping_sentence: does not seem to support multiple pronounciations of a hanzi characters
- dragonmapper, for pinyin <-> zhuyin

that's why this package uses three different libraries to utilise the strengths of each package
