# TODO: for now assert that this statement return without errors

# test output of SentencesToAnki
from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/test_sentences.txt',
  output='output/test_sentences.txt',
  tags='CCC_B2L9 Sentences Incomplete_Audio Incomplete_Meaning Incomplete_Source'
)

from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/test_sentences_short.txt',
  output='output/test_sentences_short.txt',
  tags='Immersion Sentences Incomplete'
)

# test conversions of Dictionary class to ChineseWord
from dictionary import Dictionary
word = '㧯'
a = Dictionary.get(Dictionary.traditional==word)
cn = a.to_cn_word()
vars(cn)


# test hanzi_zhuyin_pairs
from chinese_word import ChineseWord
a = ChineseWord('是。泰國到處都是廟，就像法國有很多教堂一樣。')
a.fill_fields_from_traditional()
a.hanzi_zhuyin_pairs()
