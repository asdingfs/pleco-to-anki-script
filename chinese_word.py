import re

from constants import TONE_COLORS
from constants import to_simplified, transliterate, to_segments
from dictionary import Dictionary
from zhon import zhuyin, hanzi

class ChineseWord:
  def __init__(self, traditional='', simplified='', pinyin='', zhuyin='', english=''):
    self.traditional = traditional
    self.simplified = simplified
    self.pinyin = pinyin
    self.zhuyin = zhuyin
    self.english = english

  def is_valid_word(self):
    return bool(
      self.traditional and self.simplified and
      self.pinyin and self.zhuyin and
      self.english
    )

  def dashed_simplified(self):
    return ChineseWord.dash_equal_characters(self.traditional, self.simplified)

  def dashed_traditional(self):
    return ChineseWord.dash_equal_characters(self.simplified, self.traditional)

  def set_simplified_from_traditional(self):
    self.simplified = to_simplified(self.traditional)

  def set_pinyin_from_simplified(self):
    self.pinyin = ''.join(transliterate(self.simplified, zhuyin=False))

  # NOTE: expected value for zhuyin encoding is a string which every syllable is separated by space
  def set_zhuyin_from_simplified(self):
    self.zhuyin = ' '.join(transliterate(self.simplified, zhuyin=True))

  def set_english_from_simplified(self):
    entry = Dictionary.get_or_none(Dictionary.simplified==self.simplified)
    if entry is None:
      self.english = 'N/A'
    else:
      self.english = entry.english

  def fill_fields_from_traditional(self, overwrite=False):
    if overwrite:
      self.set_simplified_from_traditional()
      self.set_pinyin_from_simplified()
      self.set_zhuyin_from_simplified()
      self.set_english_from_simplified()
    else:
      self.set_simplified_from_traditional() if bool(self.simplified) is False else None
      self.set_pinyin_from_simplified() if bool(self.pinyin) is False else None
      self.set_zhuyin_from_simplified() if bool(self.zhuyin) is False else None
      self.set_english_from_simplified() if bool(self.english) is False else None

  def deconstructed_zhuyin(self):
    return re.findall(zhuyin.syllable, self.zhuyin)

  def hanzi_zhuyin_pairs(self):
    pairs = { 'hanzi': [], 'zhuyin': [] }
    deconstructed_zhuyin = self.deconstructed_zhuyin()
    if bool(deconstructed_zhuyin):
      offset = 0
      for idx, char in enumerate(self.traditional):
        pairs['hanzi'].append(char)
        if bool(re.findall('[{}]'.format(hanzi.stops + hanzi.non_stops), char)): # if a punctuation
          pairs['zhuyin'].append(char)
          offset += 1
        else:
          pairs['zhuyin'].append(deconstructed_zhuyin[idx-offset])
    return pairs

  @classmethod
  def dash_equal_characters(klass, reference, comparison):
    dash_form = ["" for i in range(len(reference))]
    for i in range(len(reference)):
      if reference[i] == comparison[i]:
        dash_form[i] = '—'
      else:
        dash_form[i] = comparison[i]
    return ' '.join(dash_form).strip()

  @classmethod
  def from_dictionary(self, dictionary):
    cn_word = ChineseWord(
      traditional=dictionary.traditional,
      simplified=dictionary.simplified,
      pinyin=dictionary.pinyin,
      english=dictionary.english
    )
    # transliterate and standardise zhuyin and pinyin format according to the one defined in-class
    cn_word.set_zhuyin_from_simplified()
    cn_word.set_pinyin_from_simplified()
    return cn_word
