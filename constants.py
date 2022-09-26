from opencc import OpenCC
from pypinyin import pinyin
from pypinyin_dict.phrase_pinyin_data import cc_cedict
from pypinyin_dict.pinyin_data import kxhc1983
import jieba

TONE_COLORS = [
  "#93ceff", # TONE 1
  "#89ffca", # TONE 2
  "#b489ff", # TONE 3
  "#ff8080", # TONE 4
  "#c6c6c6"  # TONE 5
]

cc_cedict.load()
kxhc1983.load()

to_simplified = OpenCC('tw2s').convert
to_pinyin = pinyin
to_segments = jieba.cut
