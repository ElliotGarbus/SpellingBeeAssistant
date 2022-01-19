from kivy.app import App
from kivy.lang import Builder

import re

kv = """

<Seperator@BoxLayout>:
    padding: 10
    size_hint_y: None
    height: 30
    Widget:
        canvas:
            Color:
                rgb: 1, 1, 1
            Line:
                points: self.x, self.center_y, self.right, self.center_y

BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'SpellingBee Assistant'
        size_hint_y: None
        height: 48
    BoxLayout:
        size_hint_y: None
        height: 48
        Label:
            text: 'Dictionary: '
            size_hint_x: None
            width: self.texture_size[0] + 10
            
        Spinner:
            id: spinner
            text: 'popular.txt'
            values: ['All', 'popular.txt', 'sowpods.txt', 'words_alpha.txt', 'words.list.txt']
    BoxLayout:
        spacing: 10
        size_hint_y: None
        height: 30
        Label:
        Label:
            id: center_letter_label
            text: 'Center'
            size_hint_x: None
            width: 30
        Label:
            text: 'Surrounding Letters'
        Label:
    BoxLayout:
        spacing: 10
        size_hint_y: None
        height: 30
        Label:
        TextInput:
            id: center_letter_ti
            size_hint_x: None
            width: center_letter_label.width
        TextInput:
            id: surrounding_letters_ti
            hint_text: 'Enter the 6 other letters'
            size_hint_x: None
            width: 6 * 30
        Label:
    Seperator:
    BoxLayout:
        padding: 10, 0  # [padding_horizontal, padding_vertical]
        size_hint_y: None
        height: 30
        Label:
            text: 'Starts with: '
            text_size: self.size
            halign: 'right'
            valign: 'middle'
        TextInput:
            size_hint_x: None
            width: 30 * 2
        Label:
            text: 'Length: '
            text_size: self.size
            halign: 'right'
            valign: 'middle'
        TextInput:
            size_hint_x: None
            width: 30 * 2
        Button:
            text: 'Enter'
        Button:
            text: 'Clear'
    Seperator:
    ScrollView:
        GridLayout:
            cols: 5
            id: grid
            row_default_height: 30
            size_hint_y: None
            height: self.minimum_height
"""




# words_alpha.txt file from: https://github.com/dwyl/english-words/blob/master/words_alpha.txt
# words_alpha contains many words not in the SpellingBee dictionary

# popular.txt from https://github.com/dolph/dictionary/blob/master/popular.txt
# too restrictive

# word.list.txt from https://norvig.com/ngrams/word.list
# In between the 2 lists above, still contains many words not used in SpellingBee

# sowpods.txt from https://norvig.com/ngrams/



with open('popular.txt') as f:
    words = f.read().lower().splitlines()

# center = input('Enter Center Character: ').lower()
# surrounding = input('Enter the Surrounding Characters: ').lower()
center = 'e'
surrounding = 'imzgna'

four_or_more = '{4,}'
p = re.compile(f'^[{center + surrounding}]{four_or_more}$')
words = [word for word in words if center in word and p.match(word)]
print(words)
print(f'There are {len(words)} words in the list')
words = [word for word in words if word.startswith('lo')]
print(words)


class SpellingBeeAssistantApp(App):
    def build(self):
        return Builder.load_string(kv)


SpellingBeeAssistantApp().run()