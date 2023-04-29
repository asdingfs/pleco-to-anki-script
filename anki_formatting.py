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