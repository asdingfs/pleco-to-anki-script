import re
from dragonmapper import transcriptions

class PlecoFlashcardEntry:
  def __init__(self, entry, transcriptions_spaced=True):
    self.traditional = ''
    self.simplified = ''
    self.pinyin = ''
    self.zhuyin = ''
    self.transcriptions_spaced = transcriptions_spaced
    self.parse_line(entry)
    self.dashed_traditional = PlecoFlashcardEntry.dash_equal_characters(self.simplified, self.traditional)
    self.dashed_simplified = PlecoFlashcardEntry.dash_equal_characters(self.traditional, self.simplified)
    return

  def parse_line(self,line):
    array = line.split("\t")
    self.traditional, self.simplified = PlecoFlashcardEntry.parse_hanzi(array[0])
    raw_pinyin = re.sub('\W+', '', array[1])
    self.pinyin = PlecoFlashcardEntry.parse_pinyin(raw_pinyin, spaced=self.transcriptions_spaced)
    self.zhuyin = PlecoFlashcardEntry.parse_zhuyin(raw_pinyin, spaced=self.transcriptions_spaced)
    self.meaning = array[2].strip()
    return

  # static methods
  @staticmethod
  def parse_hanzi(mixed_hanzi):
    simplified_hanzi, traditional_hanzi = mixed_hanzi.replace("]", '').split("[")
    return [traditional_hanzi, simplified_hanzi]

  @staticmethod
  def parse_pinyin(raw_pinyin, spaced=True):
    # with the following method it's guaranteed that the pinyin will return spaced
    dragonmapper_pinyin = transcriptions.zhuyin_to_pinyin(transcriptions.pinyin_to_zhuyin(raw_pinyin))
    return dragonmapper_pinyin if spaced else dragonmapper_pinyin.replace(' ', '')

  @staticmethod
  def parse_zhuyin(raw_pinyin, spaced=True):
    zhuyin_accent_tones = [" ", "ˊ", "ˇ", "ˋ", "˙"]
    string_zhuyin = transcriptions.pinyin_to_zhuyin(raw_pinyin)
    grouped_zhuyin = []
    grouped_bopomofo = ''
    # NOTE: the following is  NOT standard zhuyin, 
    #       but very useful to mark separation in anki cards
    first_tone_replacement = "ˉ"  
    for bopomofo in string_zhuyin:
      grouped_bopomofo += bopomofo if (bopomofo != " ") else first_tone_replacement
      if bopomofo in zhuyin_accent_tones:
        grouped_zhuyin += [grouped_bopomofo]
        grouped_bopomofo = ''
    separator = ' ' if spaced else ''
    return separator.join(grouped_zhuyin)

  @staticmethod
  def dash_equal_characters(reference, comparison, spaced=True):
    dash_form = ["" for i in range(len(reference))]

    for i in range(len(reference)):
      if reference[i] == comparison[i]:
        dash_form[i] = '—'
      else:
        dash_form[i] = comparison[i]

    return (' ' if spaced else '').join(dash_form).strip()
