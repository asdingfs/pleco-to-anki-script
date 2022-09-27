from peewee import *
from constants import dict_db
from playhouse.sqlite_ext import SqliteExtDatabase
from cedict_utils.cedict import CedictParser
from chinese_word import ChineseWord

sqlite_db = SqliteExtDatabase('data/cedict.db')

class Dictionary(Model):
  traditional = CharField()
  simplified = CharField()
  pinyin = CharField()
  english = TextField()
  raw_line = TextField()

  def to_cn_word(self):
    cn_word = ChineseWord(
      traditional=self.traditional,
      simplified=self.simplified,
      pinyin=self.pinyin,
      english=self.english
    )
    # transliterate and standardise zhuyin and pinyin format according to the one defined in-class
    cn_word.set_zhuyin_from_pinyin()
    cn_word.set_pinyin_from_zhuyin()
    return cn_word

  class Meta:
    database = dict_db

def db_entry(raw_entry):
  entry = vars(raw_entry)
  # format 'meanings' to be have more meaningful separation
  arr = ["[%s] %s"%(idx + 1, e) for idx, e in enumerate(entry['meanings'])]
  entry['english'] = '\n'.join(arr)
  entry.pop('meanings', None)
  return entry

def rebuild(dict_file = 'data/cedict_ts.u8'):
  # delete current tables & recreate
  with dict_db.atomic() as _:
    dict_db.drop_tables([Dictionary], safe=True)
    dict_db.create_tables([Dictionary], safe=True)

  # freshly read dictionary file
  parser = CedictParser()
  parser.read_file(dict_file)
  entries = parser.parse()
  with dict_db.atomic() as _:
    count = 0
    source = list(map(db_entry, entries))
    for batch in chunked(source, 500):
      count = Dictionary.insert_many(batch).execute()
    print("TOTAL: Processed %s entries successfully!"%(count))

    
