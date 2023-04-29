import re
from chinese_word import ChineseWord

class PlecoFlashcardEntry:
  def __init__(self, entry, separator="\t"):
    self.chinese_word = ChineseWord()
    self.separator = separator
    self.parse_line(entry)
    return

  def parse_line(self,line):
    array = line.split(self.separator)
    if len(array) < 3:
      array += ['' for i in range(max(0, 3 - len(array)))]
    self.parse_hanzi(array[0].strip())
    raw_pinyin = re.sub('\W+', '', array[1].strip())
    raw_pinyin = raw_pinyin.replace("u:", "ü")
    self.parse_pinyin(raw_pinyin)
    self.parse_meaning(array[2].strip())
    return self.chinese_word

  def parse_hanzi(self, raw_hanzi):
    split_hanzi = raw_hanzi.replace("]", '').split("[")
    if len(split_hanzi) != 2:
      raise ValueError('The chinese characters in flashcard export is incorrect, it should be in 「繁體字[簡體字]」format. Please re-check your export settings')
    simplified_hanzi, traditional_hanzi = split_hanzi
    self.chinese_word.simplified = simplified_hanzi
    self.chinese_word.traditional = traditional_hanzi

  def parse_pinyin(self, raw_pinyin):
    self.chinese_word.pinyin = raw_pinyin

  def parse_meaning(self, raw_meaning):
    parsed_meaning = raw_meaning.strip().replace(';', ',')
    self.chinese_word.english = parsed_meaning
