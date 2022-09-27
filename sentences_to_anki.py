# see input test_sentences for sample format
from dictionary import Dictionary
from chinese_word import ChineseWord
from constants import to_simplified
from anki_formatting import *

class SentencesToAnki:
  def __init__(self, input, output, tags=''):
    self.input_file = open(input, 'rt', encoding='utf-8-sig')
    self.output_file = open(output, 'wt', encoding='utf-8-sig')
    self.tags = tags
    self.parse()
    self.input_file.close()
    self.output_file.close()

  def parse(self):
    count = 0
    for line in self.input_file:
      sentences, words = line.strip().split(';')
      field_sequence = [
        self.format_sentences(sentences, words),
        '', # audio (using other plugin to generate)
        '', # TODO: pinyin,
        '', # TODO: meaning,
        self.format_words(words), # formatted words
        '' # TODO: context
      ]
      self.output_file.write(';'.join(field_sequence) + "\n")
      count += 1
    print("Parsed %s entries successfully!" % (count))

  def format_sentences(self, sentences, words):
    bolded_sentences = sentences.replace("&", "\n")
    for word in words.split('&'):
      bolded_sentences = bold_word_in_sentence(bolded_sentences, word)
    return escape(bolded_sentences)

  def format_words(self, words):
    arr = list(map(self.format_word, words.split('&')))
    return '<hr>'.join(arr)

  def format_word(self, word):
    cn_word = self.translate(word)
    return "<ruby>%s%s</ruby>"%(
      get_rubi_element(
        cn_word.traditional,
        cn_word.zhuyin
      ),
      get_rubi_element(
        cn_word.english,
        ''
      )
    )

  def translate(self, tw_word):
    tl_word = Dictionary.get_or_none(Dictionary.simplified==to_simplified(tw_word))
    cn_word = ChineseWord(traditional=tw_word)
    if tl_word: # if not None
      cn_word = ChineseWord.from_dictionary(tl_word)
    else:
      cn_word.fill_fields_from_traditional() # autofill as much as possible
      print("Word: 「%s」 cannot be found in the dictionary"%(tw_word))
    return cn_word
