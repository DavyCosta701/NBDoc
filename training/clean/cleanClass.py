from PyPDF2 import PdfReader
from docx import Document
from training.languages.langStop import StopWords


class _CleanInterface(StopWords):
    def __init__(self, archive):
        super().__init__()
        self.archive = archive
        self.characters = "\n" \
                          "#-*`.[]'():/${}1234567890\"?=<>,;_~" \
                          ""
        self.content = ''

    def _extract(self):
        with open(self.archive, 'r', encoding='utf-8') as arch:
            content: str = arch.read()
        self.content = content

    def clean(self, language: str = None) -> list[str]:
        self._extract()

        for char in self.characters:
            self.content = self.content.replace(char, ' ')

        self.content = self.content.split(' ')

        if language:
            swlist = self.stopwords[language.lower()]
            self.content = (w.lower() for w in self.content if w not in swlist)

        true_wordlist = filter(lambda x: x != '', self.content)

        return list(true_wordlist)


class _CleanPDF(_CleanInterface):

    def _extract(self):
        with open(self.archive, 'rb') as arch:
            pdf = PdfReader(arch)
            content: str = ""
            for page in pdf.pages:
                content += page.extract_text()

        self.content = content


class _CleanDocx(_CleanInterface):

    def _extract(self):

        docx = Document(self.archive)
        content: str = ""

        for paragraph in docx.paragraphs:
            content += paragraph.text

        self.content = content
