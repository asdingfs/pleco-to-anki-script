from opencc import OpenCC
from pypinyin import pinyin
from pypinyin_dict.phrase_pinyin_data import cc_cedict
from pypinyin_dict.pinyin_data import kxhc1983
import jieba

TONE_COLORS = [
  "#93ceff",
  "#89ffca",
  "#b489ff",
  "#ff8080",
  "#c6c6c6"
]

cc_cedict.load()
kxhc1983.load()

Simplifier = OpenCC('tw2s')
Converter = pinyin
Segmenter = jieba
