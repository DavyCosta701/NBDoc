import nltk


class StopWords:
    def __init__(self):
        self.stopwords = {
            'pt': nltk.corpus.stopwords.words('portuguese'),
            'en': nltk.corpus.stopwords.words('english')
        }
