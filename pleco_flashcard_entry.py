import re
from dragonmapper import transcriptions

class PlecoFlashcardEntry:
  def __init__(self, entry, separator="\t", transcriptions_spaced=True):
    self.traditional = ''
    self.simplified = ''
    self.pinyin = ''
    self.zhuyin = ''
    self.separator = separator
    self.transcriptions_spaced = transcriptions_spaced
    self.parse_line(entry)
    self.dashed_traditional = PlecoFlashcardEntry.dash_equal_characters(self.simplified, self.traditional)
    self.dashed_simplified = PlecoFlashcardEntry.dash_equal_characters(self.traditional, self.simplified)
    return

  def parse_line(self,line):
    array = line.split(self.separator)
    self.traditional, self.simplified = PlecoFlashcardEntry.parse_hanzi(array[0])
    raw_pinyin = re.sub('\W+', '', array[1])
    self.pinyin = PlecoFlashcardEntry.parse_pinyin(raw_pinyin, spaced=self.transcriptions_spaced)
    self.zhuyin = PlecoFlashcardEntry.parse_zhuyin(raw_pinyin, spaced=self.transcriptions_spaced)
    self.meaning = array[2].strip().replace(';',',')
    return

  # static methods
  @staticmethod
  def parse_hanzi(mixed_hanzi):
    simplified_hanzi, traditional_hanzi = mixed_hanzi.replace("]", '').split("[")
    return [traditional_hanzi.strip(), simplified_hanzi.strip()]

  @staticmethod
  def parse_pinyin(raw_pinyin, spaced=True):
    # with the following method it's guaranteed that the pinyin will return spaced
    dragonmapper_pinyin = transcriptions.zhuyin_to_pinyin(transcriptions.pinyin_to_zhuyin(raw_pinyin))
    return dragonmapper_pinyin if spaced else dragonmapper_pinyin.replace(' ', '')

  @staticmethod
  def parse_zhuyin(raw_pinyin, spaced=True):
    zhuyin_accent_tones = [" ", "ˊ", "ˇ", "ˋ", "˙"]
    standard_zhuyin = transcriptions.pinyin_to_zhuyin(raw_pinyin).split(' ')
    # NOTE: the following is  NOT standard zhuyin, 
    #       but very useful to mark separation in anki cards
    grouped_zhuyin = []
    for each_zhuyin in standard_zhuyin:
      first_tone_addition = '' if each_zhuyin[-1] in zhuyin_accent_tones else "ˉ"
      grouped_zhuyin += [each_zhuyin + first_tone_addition]

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
