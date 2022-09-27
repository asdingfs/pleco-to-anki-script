from pleco_flashcard_entry import PlecoFlashcardEntry

class PlecoToAnki:
  def __init__(self, input, output, tags=''):
    self.input_file = open(input, 'rt', encoding='utf-8-sig')
    self.output_file = open(output, 'wt', encoding='utf-8-sig')
    self.tags = tags
    self.parse()
    self.input_file.close()
    self.output_file.close()

  def parse(self):
    self.output_file.write('tags:' + self.tags + "\n")
    count = 0
    for line in self.input_file:
      word = PlecoFlashcardEntry(line).chinese_word
      sequence = [
        word.traditional,
        word.english,
        "『" + word.dashed_simplified + "』",
        word.zhuyin,
        word.pinyin,
        word.english,
        '',
        'Pleco Flashcards'
      ]
      self.output_file.write(';'.join(sequence) + "\n")
      del word
      count += 1
    print("Parsed %s entries successfully!" % (count))


  
