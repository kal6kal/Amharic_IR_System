import sys
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices
from PySide6.QtWidgets import QApplication, QMainWindow
from SideBar_ui import Ui_MainWindow

import os
from spacy.lang.am import Amharic
from collections import Counter
import pandas as pd
import numpy as np
import hm  # ወንበሮቻችን

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

data_path = r'C:\Users\user\Documents\Data_science\IR real\Demo_data\Updated_Demo'
books = os.listdir(data_path)
base_url = "https://allaboutethio.com/"


class Data():
    def __init__(self, text):
        self.text = text
        self.book_norm = {}
        self.Ifile = None
        self.query_df = None
        self.QI_df = None
        self.vsm_result = {}
        self.tokens = []

    def prepare_index(self):
        self.Ifile = pd.read_csv('IDF_ized.csv')
        self.Ifile.drop('Unnamed: 0', axis=1, inplace=True)
        self.book_norm = {}
        for book in books:
            book_value = self.Ifile[book].values
            vector_length = np.round(np.linalg.norm(book_value), 3)
            self.book_norm[book] = vector_length

    def query(self, text):
        nlp = Amharic()
        nlp.max_length = 20000000
        text = text.strip()
        doc = nlp(text)
        self.tokens.extend([token.text for token in doc if not token.is_punct])

        Doc_freq = []
        IDF = []

        for token in self.tokens:
            word_freq = {}
            for book in books:
                document = os.path.join(data_path, book)
                with open(document, 'r', encoding='utf-8') as file:
                    content = file.read()
                    word_count = Counter(content.split())
                    word_freq[book] = word_count[token]
            idf = float(self.Ifile['IDF'].loc[self.Ifile['Term'] == token])
            IDF.append(idf)
            Doc_freq.append(word_freq)

        self.query_df = pd.DataFrame({'Term': self.tokens, "Doc_freq": Doc_freq, "IDF": IDF})
        return self.query_df

    def compile(self):
        self.query_df['Q'] = self.query_df['Doc_freq'].apply(lambda x: np.sum(list(x.values())))
        self.query_df['Q'] = self.query_df['Q'] * self.query_df['IDF']
        self.query_df.drop(['Doc_freq', 'IDF'], axis=1, inplace=True)

    def merge(self):
        self.Ifile = self.Ifile.loc[self.Ifile['Term'].isin(self.tokens)]
        self.Ifile = self.Ifile[['Term'] + books]
        self.QI_df = self.query_df.merge(self.Ifile, on='Term')
        for book in books:
            self.QI_df[book] = self.QI_df[book] * self.QI_df['Q']

    def VSM(self):
        for book in books:
            result = self.QI_df[book].sum()
            self.vsm_result[book] = result
        self.vsm_result = pd.Series(self.vsm_result, name='result')
        self.vsm_result = pd.DataFrame(self.vsm_result)
        self.vsm_result.sort_values(by='result', ascending=False, inplace=True)

    def process(self):
        self.prepare_index()
        self.query(self.text)
        self.compile()
        self.merge()
        self.VSM()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.burger_button.setChecked(True)

        # --- Minor UI Improvements ---
        self.ui.search_lineEdit.setToolTip("Enter your Amharic query here")
        self.ui.Tokenize_button.setText("Tokenize Text")
        self.ui.stemer_Button.setText("Stem Words")
        self.ui.Normalize_Button.setText("Normalize Text")
        font = QFont("Arial", 10)
        self.ui.result_listWidget.setFont(font)
        self.ui.swords_listWidget.setFont(font)
        self.ui.normalized_listWidget.setFont(font)
        self.ui.tokenize_listWidget.setFont(font)

        self.show()

        # --- Connect buttons ---
        self.ui.home_button.clicked.connect(self.onHome_buttonClicked)
        self.ui.home_button_2.clicked.connect(self.onHome_buttonClicked2)
        self.ui.Tokenize_button.clicked.connect(self.onTokenize_buttonClicked)
        self.ui.Tokenize_button_2.clicked.connect(self.onTokenize_buttonClicked2)
        self.ui.stem_button.clicked.connect(self.onStopWord_buttonClicked)
        self.ui.stem_button_2.clicked.connect(self.onStopWord_buttonClicked2)
        self.ui.normalize_button.clicked.connect(self.onNormalize_buttonClicked)
        self.ui.normalize_button_2.clicked.connect(self.onNormalize_buttonClicked2)
        self.ui.search_button.clicked.connect(lambda: self.perform_search(self.ui.search_lineEdit.text()))
        self.ui.result_listWidget.itemClicked.connect(self.open_link)
        self.ui.stemer_Button.clicked.connect(lambda: self.stemmer(self.ui.search_lineEdit.text()))
        self.ui.Normalize_Button.clicked.connect(lambda: self.Normalization(self.ui.search_lineEdit.text()))
        self.ui.tokenize_Button.clicked.connect(lambda: self.Tokenization(self.ui.search_lineEdit.text()))

    # --- Button Handlers ---
    def onHome_buttonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def onHome_buttonClicked2(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def onTokenize_buttonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def onTokenize_buttonClicked2(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def onStopWord_buttonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def onStopWord_buttonClicked2(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def onNormalize_buttonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def onNormalize_buttonClicked2(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def perform_search(self, query):
        VSM = Data(query)
        VSM.process()
        query_result = list(VSM.vsm_result.index)
        query_links = []
        for item in query_result:
            parts = item.split('.')
            query_link = base_url + parts[0] + '.html'
            query_links.append(query_link)
        self.ui.result_listWidget.clear()
        self.ui.result_listWidget.addItems(query_links)

    def open_link(self, item):
        url = QUrl(item.text())
        QDesktopServices.openUrl(url)

    def stemmer(self, word):
        try:
            result = hm.anal('a', word)[0]['lemma']
            print(result)
            self.ui.swords_listWidget.addItem(result)
            return result
        except:
            self.ui.swords_listWidget.addItem(word)
            print(result)
            return word

    def Normalization(self, word):
        dict1 = {"ሐ": "ሀ", "ሑ": "ሁ", "ሒ": "ሂ", "ሓ": "ሃ", "ሔ": "ሄ", "ሕ": "ህ", "ሖ": "ሆ",
                 "ኀ": "ሀ", "ኁ": "ሁ", "ኂ": "ሂ", "ኃ": "ሃ", "ኄ": "ሄ", "ኅ": "ህ", "ኆ": "ሆ"}
        dict2 = {"ሠ": "ሰ", "ሡ": "ሱ", "ሢ": "ሲ", "ሣ": "ሳ", "ሤ": "ሴ", "ሥ": "ስ", "ሦ": "ሶ", "ሧ": "ሷ"}
        dict3 = {"ዐ": "አ", "ዑ": "ኡ", "ዒ": "ኢ", "ዓ": "ኣ", "ዔ": "ኤ", "ዕ": "እ", "ዖ": "ኦ"}
        dict4 = {"ጸ": "ፀ", "ጹ": "ፁ", "ጺ": "ፂ", "ጻ": "ፃ", "ጼ": "ፄ", "ጽ": "ፅ", "ጾ": "ፆ"}
        dict5 = {'ዉ': 'ው'}
        merged_dict = {}
        merged_dict.update(dict1)
        merged_dict.update(dict2)
        merged_dict.update(dict3)
        merged_dict.update(dict4)
        merged_dict.update(dict5)
        for char, value in merged_dict.items():
            word = word.replace(char, value)
        print(word)
        self.ui.normalized_listWidget.addItem(word)
        return word

    def Tokenization(self, text):
        Tokens = []
        nlp = Amharic()
        nlp.max_length = 20000000
        text = text.strip()
        doc = nlp(text)
        Tokens.extend([token.text for token in doc if not token.is_punct])
        print(Tokens)
        self.ui.tokenize_listWidget.addItems(Tokens)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
