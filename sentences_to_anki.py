# see input test_sentences for sample format
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
      bolded_sentences = sentences.replace("&", "\n")
      for word in words.split('&'):
        bolded_sentences = bold_word_in_sentence(bolded_sentences, word)
      field_sequence = [
        escape(bolded_sentences),
        '', # audio (using other plugin to generate)
        '', # TODO: pinyin,
        '', # TODO: meaning,
        '', # TODO: words
        '' # TODO: context
      ]
      self.output_file.write(';'.join(field_sequence) + "\n")
      count += 1
    print("Parsed %s entries successfully!" % (count))

