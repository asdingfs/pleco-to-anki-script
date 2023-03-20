# collection of pure functions
def escape(text):
  return "\"%s\""%(text.replace("\"", "\"\""))

def emphasize(text):
  return "<b><u>%s</u></b>"%(text)

def split_and_filter(text, delimiter):
  return list(filter(None, text.split(delimiter)))

def emphasize_word_in_sentence(sentence, word):
  arr = sentence.split(word)
  return emphasize(word).join(arr)

# return HTML text containing interleaved phonetics called ruby-style texts
def get_rubi_element(word, furigana = ''):
  if furigana: # is not empty
    return "<rb>%s</rb><rp>(</rp><rt>%s</rt><rp>)</rp>"%(
      word,
      furigana
    )
  else:
    return "<rb>%s</rb>"%(
      word
    )