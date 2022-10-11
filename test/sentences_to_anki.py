# TODO: for now assert that this statement return without errors

# test output of SentencesToAnki
from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/test_sentences.txt',
  output='output/test_sentences.txt',
  tags='Test Tags Test_Tags'
)

# test output of SentencesToAnki
from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/sentences_female.txt',
  output='output/sentences_female.txt',
  tags='CCC_B2L11 Sentences Incomplete Female_Audio Dialogue'
)

# test output of SentencesToAnki
from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/sentences_male.txt',
  output='output/sentences_male.txt',
  tags='CCC_B2L11 Sentences Incomplete Male_Audio Dialogue'
)

# test output of SentencesToAnki
from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/sentences_readings.txt',
  output='output/sentences_readings.txt',
  tags='CCC_B2L10 Sentences Incomplete Male_Audio Readings'
)

from sentences_to_anki import SentencesToAnki
SentencesToAnki(
  input='input/sentences_short.txt',
  output='output/sentences_short.txt',
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
