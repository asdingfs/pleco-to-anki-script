from constants import TONE_COLORS
from constants import to_simplified, to_pinyin, to_segments
from dragonmapper import transcriptions

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

  def set_zhuyin_from_pinyin(self):
    self.zhuyin = transcriptions.pinyin_to_zhuyin(self.pinyin)

  def set_pinyin_from_zhuyin(self):
    self.pinyin = transcriptions.zhuyin_to_pinyin(self.zhuyin)

  @classmethod
  def dash_equal_characters(reference, comparison):
    dash_form = ["" for i in range(len(reference))]
    for i in range(len(reference)):
      if reference[i] == comparison[i]:
        dash_form[i] = '—'
      else:
        dash_form[i] = comparison[i]

    return ' '.join(dash_form).strip()