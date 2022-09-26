from constants import Simplifier, Segmenter, Converter
from constants import TONE_COLORS

class ChineseWord:
  def __init__(self, traditional='', simplified='', pinyin='', zhuyin='', meaning=''):
    self.traditional = traditional
    self.simplified = simplified
    self.pinyin = pinyin
    self.zhuyin = zhuyin
    self.meaning = meaning

  def is_valid_word(self):
    return bool(
      self.traditional and self.simplified and
      self.pinyin and self.zhuyin and
      self.meaning
    )

  def dashed_simplified(self):
    return ChineseWord.dash_equal_characters(self.traditional, self.simplified)

  def dashed_traditional(self):
    return ChineseWord.dash_equal_characters(self.simplified, self.traditional)

  # TODO: return HTML text containing interleaved phonetics called ruby-style texts
  def get_rubi_element(self):
    return "<rb>%s</rb><rp>(</rp><rt>%s</rt><rp>)</rp>"%(
      self.traditional,
      self.zhuyin
    )

  @classmethod
  def dash_equal_characters(reference, comparison)
    dash_form = ["" for i in range(len(reference))]
    for i in range(len(reference)):
      if reference[i] == comparison[i]:
        dash_form[i] = '—'
      else:
        dash_form[i] = comparison[i]

    return ' '.join(dash_form).strip()