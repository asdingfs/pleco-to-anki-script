from opencc import OpenCC
from pypinyin import pinyin, lazy_pinyin, Style
from pypinyin_dict.phrase_pinyin_data import cc_cedict
from pypinyin_dict.pinyin_data import kxhc1983
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
kxhc1983.load()

# initialise converter methods
to_simplified = OpenCC('tw2s').convert
def to_pinyin(*args, **kwargs):
  return lazy_pinyin(*args, **kwargs, style=Style.TONE, tone_sandhi=True)
to_segments = jieba.cut

# initialise database
dict_db = SqliteExtDatabase(DICT_DB)
dict_db.connect()