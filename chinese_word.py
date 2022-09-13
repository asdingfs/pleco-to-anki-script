from opencc import OpenCC
from pypinyin import pinyin, Style

class ChineseWord:
  def __init__(self, traditional):
    self.converter = OpenCC('tw2sp.json')
    self.transcriber = pinyin
    self.traditional = traditional
    self.simplified = ""
    self.pinyin = ""
    self.zhuyin = ""
    self.__init_attributes()

  def __init_attributes(self):
    self.simplified = self.__dash_simplified()
    self.pinyin = self.__pinyin()
    self.zhuyin = self.__zhuyin()

  def __full_simplified(self):
    return self.converter.convert(self.traditional)

  def __dash_simplified(self):
    full_traditional = self.traditional
    full_simplified = self.__full_simplified()
    dash_simplified = ["" for i in range(len(self.traditional))]

    for i in range(len(full_traditional)):
      if full_traditional[i] == full_simplified[i]:
        dash_simplified[i] = ' — '
      else:
        dash_simplified[i] = full_simplified[i]

    return ''.join(dash_simplified).strip()

  def __pinyin(self):
    # space_separated_hanzi = ' '.join(list(self.traditional.replace(' ', '')))
    standard_pinyin = self.transcriber(self.traditional, style=Style.TONE)
    my_pinyin = []
    
    for each_pinyin in standard_pinyin:
      my_pinyin += each_pinyin
      
    return ' '.join(my_pinyin)

  def __zhuyin(self):    
    zhuyin_accent_tones = ["ˉ", "ˊ", "ˇ", "ˋ", "˙"]
    standard_zhuyin = self.transcriber(self.traditional, style=Style.BOPOMOFO)
    my_zhuyin = []

    # NOTE: the following is  NOT standard zhuyin, 
    #       but very useful to read anki cards
    for each_zhuyin in standard_zhuyin:
      tone = each_zhuyin[-1][-1]
      if tone in zhuyin_accent_tones:
        my_zhuyin += each_zhuyin[-1]
      else:
        my_zhuyin += each_zhuyin[-1] + zhuyin_accent_tones[0]

    return ''.join(my_zhuyin)



