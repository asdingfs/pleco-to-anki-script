import re

from constants import TONE_COLORS
from constants import to_simplified, transliterate, transcriptions
from dictionary import Dictionary
from zhon import hanzi

class ChineseWord:
  def __init__(self, traditional='', simplified='', pinyin='', english=''):
    self.traditional = traditional
    self.simplified = simplified
    self.pinyin = pinyin
    self.english = english

  def is_valid_word(self):
    return bool(
      self.traditional and self.simplified and
      self.pinyin and self.english
    )

  def dashed_simplified(self):
    return ChineseWord.dash_equal_characters(self.traditional, self.simplified)

  def dashed_traditional(self):
    return ChineseWord.dash_equal_characters(self.simplified, self.traditional)

  def standardise_pinyin(self):
    accented_pinyin = transcriptions.numbered_to_accented(self.pinyin)
    self.pinyin = re.sub(re.compile(r'\s+'), '', accented_pinyin)

  def set_simplified_from_traditional(self):
    self.simplified = to_simplified(self.traditional)

  def set_pinyin_from_simplified(self):
    self.pinyin = ''.join(transliterate(self.simplified))

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
      self.set_english_from_simplified()
    else:
      self.set_simplified_from_traditional() if bool(self.simplified) is False else None
      self.set_pinyin_from_simplified() if bool(self.pinyin) is False else None
      self.set_english_from_simplified() if bool(self.english) is False else None

  def deconstructed_hanzi(self):
    return re.findall('[{}]'.format(hanzi.characters), self.traditional)

  @classmethod
  def dash_equal_characters(klass, reference, comparison):
    dash_form = ["" for i in range(len(reference))]
    for i in range(len(reference)):
      if reference[i] == comparison[i]:
        dash_form[i] = '—'
      else:
        dash_form[i] = comparison[i]
    return ''.join(dash_form).strip()

  @classmethod
  def from_dictionary(self, entry):
    cn_word = ChineseWord(
      traditional=entry.traditional,
      simplified=entry.simplified,
      pinyin=entry.pinyin,
      english=entry.english
    )
    cn_word.standardise_pinyin()
    return cn_word
