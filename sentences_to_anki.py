import re

# see input test_sentences for sample format
from dictionary import Dictionary
from chinese_word import ChineseWord
from constants import to_simplified, to_segments
from zhon import pinyin
from anki_formatting import *

class SentencesToAnki:
  def __init__(self, input, output, tags='', context=''):
    self.input_file = open(input, 'rt', encoding='utf-8-sig')
    self.output_file = open(output, 'wt', encoding='utf-8-sig')
    self.tags = tags
    self.context = context
    self.parse()
    self.input_file.close()
    self.output_file.close()

  def parse(self):
    self.output_file.write('tags:' + self.tags + "\n")
    count = 0
    for line in self.input_file:
      try:
        input_segments = line.strip().split(';')
        # sanitising input line, and provide helpful error messages
        if any(input_segments): # check if there are any valuable inputs
          if len(input_segments) == 3: # if there are 3 segments
            sentences, words, meaning = line.strip().split(';')
            words = words.replace("＆", "&") # sanitise easily-mistaken input UTF-8, e.g. '＆' and '&'
          else:
            message = f"Error on line: {count + 1} with content: \"{line}\" in file: {self.input_file.name}\n"
            message += "Message: Please make sure that there are three line segments in the line separated by ';'"
            raise ValueError(message)
        else:
          continue # if all of the elements are empty, ignore and skip to next line

        field_sequence = [
          self.format_sentences(sentences, words),
          '', # audio (using other plugin to generate)
          '', # picture comprehension test field (manually uploaded later)
          '', # supporting picture for reading/listening context (manually uploaded later)
          self.format_pinyin(sentences, words), # format pinyin by using jieba segmentation
          escape(meaning.strip()), # meaning
          self.format_words(words), # formatted words
          escape(self.context.strip()) # context
        ]
      except ValueError as e:
        e.args += (f"on input line: {count + 1} with content: \"{line}\" in file: {self.input_file.name}\n",)
        raise

      self.output_file.write(';'.join(field_sequence) + "\n")
      count += 1
    print("Parsed %s entries successfully!" % (count))

  def format_sentences(self, sentences, words):
    bolded_sentences = sentences.replace("&", "<br>")
    for word in split_and_filter(words, '&'):
      bolded_sentences = emphasize_word_in_sentence(bolded_sentences, word)
    return escape(bolded_sentences)

  def format_pinyin(self, sentences, words):
    # helper functions to merge intervals
    def merge_intervals(intervals):
      # Sort intervals based on start times
      intervals.sort(key=lambda x: x[0])
      merged = []
      for interval in intervals:
        # If the merged list is empty or no overlap, append the interval
        if not merged or merged[-1][1] < interval[0]:
          merged.append(interval)
        # If there is an overlap, merge the intervals
        else:
          merged[-1][1] = max(merged[-1][1], interval[1])
      return merged

    emphasized_words = list(map(to_simplified, split_and_filter(words, '&')))
    arr = []
    for segment in to_segments(to_simplified(sentences)):
      word = ChineseWord(simplified = segment)
      word.set_pinyin_from_simplified()
      emphases = self.find_emphasis(word.simplified, emphasized_words)
      if word.simplified == '&':
        word = "<br>"
      elif bool(emphases):
        pinyin_arr = re.findall(pinyin.syllable, word.pinyin, re.I)
        intervals = []
        for emphasis in emphases:
          idx = word.simplified.find(emphasis)
          intervals += [[idx, idx+len(emphasis)]]
        word = ''
        idx = 0
        for interval in merge_intervals(intervals):
          word += ''.join(pinyin_arr[idx:interval[0]])
          word += emphasize(''.join(pinyin_arr[interval[0]:interval[1]]))
          idx = interval[1]
        word += ''.join(pinyin_arr[idx:])
      else:
        word = word.pinyin
      arr.append(word)
    return escape(' '.join(arr))

  # TODO: refactor for optimisation later
  def find_emphasis(self, word, emphasized_words):
    emphases = [] # note emphases is plural
    for emphasis in emphasized_words:
      if emphasis in word:
        emphases += [emphasis]
    return emphases

  def format_words(self, words):
    arr = list(map(self.format_word, split_and_filter(words, '&')))
    return escape("<table>%s</table>"%(''.join(arr)))

  # a 'word' may contain multiple pronounciation, hence different dictionary entries
  # this method will display them as separate row
  def format_word(self, word):
    entries = self.translate(word)
    first_entry = True
    result = ''
    for entry in entries:
      if first_entry:
        result += "<tr><td rowspan=%s>%s<br>(%s)</td><td>%s</td><td>%s</td></tr>"%(
          len(entries),
          entry.traditional,
          entry.dashed_simplified(),
          entry.pinyin,
          entry.english.replace("\n", "<br>")
        )
        first_entry = False
      else:
        result += "<tr><td>%s</td><td>%s</td></tr>"%(
          entry.pinyin,
          entry.english.replace("\n", "<br>")
        )
    return result

  # return a list of potential translations that matches tw_word
  def translate(self, tw_word):
    tl_words = Dictionary.select().where(Dictionary.traditional==tw_word)
    if len(tl_words): # if at least one definition exists
      return list(map(ChineseWord.from_dictionary, tl_words)) 
    else:
      print("Word: 「%s」 cannot be found in the dictionary"%(tw_word))
      cn_word = ChineseWord(traditional=tw_word)
      cn_word.fill_fields_from_traditional() # autofill as much as possible
      return [cn_word]
