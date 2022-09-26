import re
from dragonmapper import transcriptions
from chinese_word import ChineseWord

class PlecoFlashcardEntry:
  def __init__(self, entry, separator="\t"):
    self.chinese_word = ChineseWord()
    self.separator = separator
    self.parse_line(entry)
    self.dashed_traditional = PlecoFlashcardEntry.dash_equal_characters(self.simplified, self.traditional)
    self.dashed_simplified = PlecoFlashcardEntry.dash_equal_characters(self.traditional, self.simplified)
    return

  def parse_line(self,line):
    array = line.split(self.separator)
    self.parse_hanzi(array[0])
    raw_pinyin = re.sub('\W+', '', array[1])
    self.parse_pinyin(raw_pinyin)
    self.parse_zhuyin(raw_pinyin)
    self.parse_meaning(array[2])
    return self.chinese_word

  def parse_hanzi(self, raw_hanzi):
    simplified_hanzi, traditional_hanzi = raw_hanzi.replace("]", '').split("[")
    self.chinese_word.simplified = simplified_hanzi
    self.chinese_word.traditional = traditional_hanzi

  def parse_pinyin(self, raw_pinyin):
    dragonmapper_pinyin = transcriptions.zhuyin_to_pinyin(transcriptions.pinyin_to_zhuyin(raw_pinyin))
    self.chinese_word.pinyin = dragonmapper_pinyin

  def parse_zhuyin(self, raw_pinyin):
    dragonmapper_zhuyin = transcriptions.pinyin_to_zhuyin(raw_pinyin)
    self.chinese_word.zhuyin = dragonmapper_zhuyin

  def parse_meaning(self, raw_meaning):
    parsed_meaning = raw_meaning.strip().replace(';', ',')
    self.chinese_word.meaning = parsed_meaning
