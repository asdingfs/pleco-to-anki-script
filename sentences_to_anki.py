import re

# see input test_sentences for sample format
from dictionary import Dictionary
from chinese_word import ChineseWord
from constants import to_simplified, to_pinyin, to_segments
from zhon import pinyin
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
    self.output_file.write('tags:' + self.tags + "\n")
    count = 0
    for line in self.input_file:
      sentences, words, meaning, context = line.strip().split(';')
      field_sequence = [
        self.format_sentences(sentences, words),
        '', # audio (using other plugin to generate)
        '', # picture comprehension test field (manually uploaded later)
        '', # supporting picture for reading/listening context (manually uploaded later)
        self.format_pinyin(sentences, words), # format pinyin by using jieba segmentation
        escape(meaning.strip()), # meaning
        self.format_words(words), # formatted words
        escape(context.strip()) # context
      ]
      self.output_file.write(';'.join(field_sequence) + "\n")
      count += 1
    print("Parsed %s entries successfully!" % (count))

  def format_sentences(self, sentences, words):
    bolded_sentences = sentences.replace("&", "<br>")
    for word in words.split('&'):
      bolded_sentences = emphasize_word_in_sentence(bolded_sentences, word)
    return escape(bolded_sentences)

  def format_pinyin(self, sentences, words):
    emphasized_words = list(map(to_simplified, words.split('&')))
    arr = []
    for segment in to_segments(to_simplified(sentences)):
      word = ChineseWord(simplified = segment)
      word.set_pinyin_from_simplified()
      emphasis = self.find_emphasis(word.simplified, emphasized_words)
      if word.simplified == '&':
        word = "<br>"
      elif bool(emphasis):
        idx = word.simplified.find(emphasis)
        length = len(emphasis)
        pinyin_arr = re.findall(pinyin.syllable, word.pinyin, re.I)
        word = ''.join(pinyin_arr[:idx]) +\
          emphasize(''.join(pinyin_arr[idx:idx+length])) +\
          ''.join(pinyin_arr[idx+length:])
      else:
        word = word.pinyin
      arr.append(word)
    return escape(' '.join(arr))

  # TODO: refactor for optimisation later
  def find_emphasis(self, word, emphasized_words):
    for emphasis in emphasized_words:
      if emphasis in word:
        return emphasis
    return ''

  def format_words(self, words):
    arr = list(map(self.format_word, words.split('&')))
    return escape("<table>%s</table>"%(''.join(arr)))

  def format_word(self, word):
    cn_word = self.translate(word)
    deconstructed = cn_word.hanzi_zhuyin_pairs()
    length = len(cn_word.traditional)
    rubi_text = ''
    for i in range(length):
      hanzi, zhuyin = deconstructed['hanzi'][i], deconstructed['zhuyin'][i]
      furigana = '' if hanzi == zhuyin else zhuyin
      rubi_text += get_rubi_element(hanzi, furigana)
    return "<tr><td><ruby>%s</ruby></td><td>%s</td></tr>"%(
      rubi_text,
      cn_word.english.replace("\n", "<br>")
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
