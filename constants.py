from opencc import OpenCC
from dragonmapper import transcriptions
from pypinyin import pinyin, lazy_pinyin, Style
from pypinyin_dict.phrase_pinyin_data import cc_cedict
from playhouse.sqlite_ext import SqliteExtDatabase
import jieba

DICT_DB = 'data/cedict.db'
TONE_COLORS = [
  "#93ceff", # TONE 1
  "#89ffca", # TONE 2
  "#b489ff", # TONE 3
  "#ff8080", # TONE 4
  "#c6c6c6"  # TONE 5
]

# initialise settings for converters
cc_cedict.load()
jieba.set_dictionary('data/dict.txt.big')
jieba.initialize()

# initialise converter methods
to_simplified = OpenCC('tw2s').convert
def transliterate(*args):
  return lazy_pinyin(*args, tone_sandhi=True, style=Style.TONE)
to_segments = jieba.cut
standardise_pinyin = transcriptions.numbered_to_accented

# initialise database
dict_db = SqliteExtDatabase(DICT_DB)
dict_db.connect()