# TODO: for now assert that this statement return without errors

# test output of SentencesToAnki
from sentences_to_anki import SentencesToAnki
SentencesToAnki(input='input/test_sentences.txt',output='output/test_sentences.txt')

# test conversions of Dictionary class to ChineseWord
from dictionary import Dictionary
word = '㧯'
a = Dictionary.get(Dictionary.traditional==word)
cn = a.to_cn_word()
vars(cn)