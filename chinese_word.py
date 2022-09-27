from constants import TONE_COLORS
from constants import to_simplified, to_pinyin, to_segments
from dictionary import Dictionary
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

  def set_simplified_from_traditional(self):
    self.simplified = to_simplified(self.traditional)

  def set_pinyin_from_simplified(self):
    arr = [item for sublist in to_pinyin(self.simplified) for item in sublist]
    self.pinyin = ''.join(arr)

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
      self.set_zhuyin_from_pinyin()
      self.set_english_from_simplified()
    else:
      self.set_simplified_from_traditional() if bool(self.simplified) is False else None
      self.set_pinyin_from_simplified() if bool(self.pinyin) is False else None
      self.set_zhuyin_from_pinyin() if bool(self.zhuyin) is False else None
      self.set_english_from_simplified() if bool(self.english) is False else None

  @classmethod
  def dash_equal_characters(reference, comparison):
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
    cn_word.set_zhuyin_from_pinyin()
    cn_word.set_pinyin_from_zhuyin()
    return cn_word
