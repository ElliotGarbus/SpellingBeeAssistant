from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import NumericProperty, OptionProperty

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
RootLayout:
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
            values: ['All', 'popular.txt', 'sowpods.txt', 'words_alpha.txt', 'word.list.txt']
            on_text: root.load_dictionary()
    Seperator:
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
        UniqueLettersInput:
            id: center_letter_ti
            size_hint_x: None
            width: center_letter_label.width
            on_text: root.get_words()
        Label:
            text: 'Surrounding Letters: '
            size_hint_x: None
            width: self.texture_size[0]
        UniqueLettersInput:
            id: surrounding_letters_ti
            max_characters: 6
            hint_text: 'Enter the 6 other letters'
            size_hint_x: None
            width: 6 * 30
            on_text: root.get_words()
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
        CharLimitedAlphaInput:
            id: starts_with
            size_hint_x: None
            width: 30 * 2
        Label:
            text: 'Length: '
            text_size: self.size
            halign: 'right'
            valign: 'middle'
        MaxValueInput:
            id: length
            size_hint_x: None
            width: 30 * 2
        Button:
            text: 'Enter'
            on_release: root.filter_candidates()
        Button:
            text: 'Clear'
            on_release: root.clear()
    Seperator:
    ScrollView:
        GridLayout:
            cols: 4
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


class UniqueLettersInput(TextInput):
    max_characters = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = self.unique_letters
        self.write_tab = False

    def unique_letters(self, c, undo):
        if not c.isalpha() or c.upper() in self.text or len(self.text) >= self.max_characters:
            return ''
        else:
            return c.upper()


class MaxValueInput(TextInput):
    max_value = NumericProperty(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = self.numbers_only
        self.write_tab = False

    def numbers_only(self, c, undo):
        if not c.isdecimal() or int(self.text + c) > self.max_value:
            return ''
        else:
            return c

class CharLimitedAlphaInput(TextInput):
    max_characters = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = self.limit_len
        self.write_tab = False

    def limit_len(self, c, undo):
        if not c.isalpha() or len(self.text) >= self.max_characters:
            return ''
        else:
            return c.upper()


class RootLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.words = None # the list of words
        self.candidates = None # possible answers

    def load_dictionary(self):
        dictionary = self.ids.spinner.text
        if dictionary == 'All':
            self.load_all()
        else:
            with open(dictionary) as f:
                self.words = f.read().lower().splitlines()
        self.get_words()

    def load_all(self):
        dictionaries = self.ids.spinner.values[1:]
        all_words = []
        for dictionary in dictionaries:
            with open(dictionary) as f:
                all_words.extend(f.read().lower().splitlines())
        self.words = list(set(all_words)) # remove duplicates

    def get_words(self):
        center = self.ids.center_letter_ti.text.lower()
        surrounding = self.ids.surrounding_letters_ti.text.lower()
        if len(center + surrounding) == 7:
            four_or_more = '{4,}'
            p = re.compile(f'^[{center + surrounding}]{four_or_more}$')
            self.candidates = [word.upper() for word in self.words if center in word and p.match(word)]
            self.show_words(self.candidates)

    def show_words(self, words):
        self.ids.grid.clear_widgets()
        for word in words:
            self.ids.grid.add_widget(Label(text=word))

    def filter_candidates(self):
        starts_with = self.ids.starts_with.text
        length = 0 if not self.ids.length.text else int(self.ids.length.text)

        if not starts_with and not length:
            return
        words = self.candidates[::]
        if starts_with:
            words = [word for word in words if word.startswith(starts_with)]
        if length:
            words = [word for word in words if len(word) == length]
        self.show_words(words)

    def clear(self):
        self.ids.starts_with.text = ''
        self.ids.length.text = ''
        self.show_words(self.candidates)





class SpellingBeeAssistantApp(App):
    def build(self):
        return Builder.load_string(kv)

    def on_start(self):
        self.root.load_dictionary()




SpellingBeeAssistantApp().run()