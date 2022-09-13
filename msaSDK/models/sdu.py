# -*- coding: utf-8 -*-

"""Module for the Semantic Document Understanding - Content

"""


from sqlmodel import SQLModel

"""str: Module Version"""
import html
import os
from typing import Optional, List, Dict, Tuple
from msaSDK.utils.htmlutils import sanitize


def getCRLF() -> str:
    """ get's the OS Environment Variable for ``CR_LF``.
         Default: ``\\n``
    """
    ret: str = os.getenv("CR_LF", "\n")
    return ret


def getSentenceSeperator() -> str:
    """ get's the OS Environment Variable for ``SENTENCE_SEPARATOR``.
         Default: `` `` (Space/Blank)
    """
    ret: str = os.getenv("SENTENCE_SEPARATOR", " ")
    return ret


def getCRParagraph() -> str:
    # CR_PARAGRAPH
    """ get's the OS Environment Variable for ``CR_PARAGRAPH``.
         Default: ``\\n\\n``
    """
    ret: str = os.getenv("CR_PARAGRAPH", "\n\n")
    return ret


class SDUPageImage(SQLModel):
    """Page Image Pydantic Model.

        Storing the information about the Image representation of a Page.
    """
    id: int = -1  # ID = Page Index.
    filepath_name: str = ""  # Filepath to the image on filesystem storage.
    height: float = 0.  # Image Height.
    width: float = 0.  # Image Width.
    dpi: float = 0.  # Picture DPI Resolution.
    format: str = ""  # Image Format (png, jpg etc.).
    mode: str = ""  # Image Mode.
    layout: List = []  # Image Layout Information."""

    class Config:
        orm_mode = False


class SDUEmail(SQLModel):
    """Parsed EMail Pydantic Model."""
    msg_id: str = ""
    msg_from: str = ""
    msg_to: str = ""
    msg_cc: str = ""
    msg_bcc: str = ""
    msg_subject: str = ""
    msg_sent_date: str = ""
    msg_body: str = ""
    seg_body: str = ""  # Segmented Body (Signature, etc.)
    seg_sign: str = ""
    msg_sender_ip: str = ""
    msg_to_domains: str = ""
    msg_received: List = []
    msg_reply_to: str = ""
    msg_timezone: str = ""
    msg_headers: Dict = {}

    class Config:
        orm_mode = False


class SDULanguage(SQLModel):
    """Detected Language Pydantic Model."""
    code: str = 'unknown'  # Short de, en etc.
    lang: str = 'unknown'  # Language name like german.
    reliable: bool = False  # is the detected result reliable.
    proportion: int = -1  # Proportion of the text in this language.
    bytes: int = -1  # Bytes of the text in this language.
    confidence: float = -1  # Confidence from 0.01 to 1.0.
    winner: Optional[str] = None  # Selected overall Winner
    details: Optional[Tuple] = tuple()  # Details of the top 3 detected languages.

    class Config:
        orm_mode = False


class SDUStatistic(SQLModel):
    """Text Statistics Pydantic Model."""
    avg_character_per_word: float = 0
    avg_letter_per_word: float = 0
    avg_sentence_length: float = 0
    avg_syllables_per_word: float = 0
    avg_sentence_per_word: float = 0
    difficult_words: int = 0
    lexicon_count: int = 0
    long_word_count: int = 0
    reading_time_s: float = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    reading_ease_score: float = 0
    reading_ease: str = ""
    grade: float = 0
    smog: float = 0
    coleman: float = 0
    reading_index: float = 0
    reading_score: float = 0
    write_formula: float = 0
    fog: float = 0
    standard: str = ""
    crawford: float = 0
    gulpease_index: float = 0
    osman: float = 0

    class Config:
        orm_mode = False


class SDUSentence(SQLModel):
    id: int = -1
    text: str = ""
    xpos: List[str] = []
    upos: List[str] = []
    tokens: List[str] = []

    class Config:
        orm_mode = False


class SDUPDFElement(SQLModel):
    line_id: int = -1
    span_id: int = -1
    flags: int = 0
    bold: bool = False
    italic: bool = False
    font: str = ""
    fontsize: float = 0.
    color: int = 0


class SDUParagraph(SQLModel):
    id: int = -1
    sort: int = -1
    nsen: int = 0
    semantic_type: str = "text"
    section: str = "body"
    size_type: str = "body"
    sentences: List[SDUSentence] = []
    sentences_en: List[SDUSentence] = []
    clean: str = ""
    lang: SDULanguage = SDULanguage()
    elements: List[SDUPDFElement] = []

    class Config:
        orm_mode = False

    def hasText(self) -> bool:
        return len(self.sentences) > 0

    def getText(self) -> str:
        return self.getTextNoLF()

    def getTextNoLF(self) -> str:
        ret = ""
        for sen in self.sentences:
            ret += sen.text + " "
        return ret

    def getTextLF(self) -> str:
        ret = ""
        for sen in self.sentences:
            ret += sen.text + getCRLF()
        return ret


class SDUText(SQLModel):
    raw: str = ""
    clean: str = ""
    html_content: str = ""
    structured_content: Dict = {}
    lang: SDULanguage = SDULanguage()
    paragraphs: List[SDUParagraph] = []

    class Config:
        orm_mode = False


class SDUPage(SQLModel):
    page: int = -1
    npar: int = 0
    input: str = ""
    has_en: bool = False
    text: SDUText = SDUText()

    class Config:
        orm_mode = False

    def hasText(self):
        return len(self.text.paragraphs) > 0

    def getTextDefault(self):
        return self.getTextNoLF()

    def getTextNoLF(self):
        ret = ""
        for par in self.text.paragraphs:
            for sen in par.sentences:
                ret += sen.text + " "
        return ret

    def getTextNoLF_EN(self):
        ret = ""
        for par in self.text.paragraphs:
            for sen in par.sentences_en:
                ret += sen.text + " "
        return ret

    def getTextNoLF_Paragraph(self):
        ret = ""
        for par in self.text.paragraphs:
            for sen in par.sentences:
                ret += sen.text + getSentenceSeperator()
            ret += getCRParagraph()
        return ret

    def getTextLF(self, space_before_lf: bool = False):
        ret = ""
        for par in self.text.paragraphs:
            for sen in par.sentences:
                ret += sen.text
                if space_before_lf:
                    ret += getSentenceSeperator()
                ret += getCRLF()
        return ret

    def getTextLF_Paragraph(self, space_before_lf: bool = False):
        ret = ""
        for par in self.text.paragraphs:
            for sen in par.sentences:
                ret += sen.text
                if space_before_lf:
                    ret += getSentenceSeperator()
                ret += getSentenceSeperator()
            ret += getCRParagraph()
        return ret

    def getAllSentencesTextListLF(self):
        ret = []
        for par in self.text.paragraphs:
            for i, sen in enumerate(par.sentences):
                txt = sen.text
                if i == len(par.sentences) - 1:
                    txt = txt + getCRParagraph()
                else:
                    txt = txt + getCRLF()
                ret.append(txt)
        return ret

    def getTextForNLP(self):
        ret = []

        for par in self.text.paragraphs:
            txt = ""
            for sen in par.sentences:
                txt += sen.text.replace("\n", "") + "\n\n"
            if len(txt) > 1:
                ret.append(txt)
        return ret

    def getTextForDisplay(self):
        ret = ""
        for par in self.text.paragraphs:
            txt: str
            if par.semantic_type.__contains__("list"):
                txt = par.getText()
                ret += txt + getCRLF()
            else:
                txt = par.getText()
                if par.semantic_type.__contains__("head") or par.semantic_type.__contains__("title"):
                    ret += getCRLF() + txt + getCRLF()
                elif len(par.sentences) > 1:
                    ret += txt + getCRParagraph()
                else:
                    ret += txt + getCRLF()
        ret = ret.replace(getCRParagraph() + getCRLF(), getCRParagraph())
        return ret

    def getAllSentencesTextList(self):
        ret = []

        for par in self.text.paragraphs:
            txt = ""
            if par.semantic_type.__contains__("list"):
                txt = par.getTextLF()
            else:
                txt = par.getText()
            ret.append(txt)
        return ret

    def getAllSentencesTextListNoTableAndLists(self):
        ret = []

        for par in self.text.paragraphs:
            txt = ""
            if par.semantic_type.__contains__("table"):
                pass
            elif par.semantic_type.__contains__("list"):
                pass
            elif par.semantic_type.__contains__("image_text"):
                pass
            elif par.semantic_type.__contains__("imagetext"):
                pass
            elif par.semantic_type.__contains__("image"):
                pass
            elif par.semantic_type.__contains__("figure"):
                pass
            elif par.section.__contains__("footer"):
                pass
            elif par.semantic_type.__contains__("title"):
                pass
            elif par.semantic_type.__contains__("headline"):
                pass
            else:
                for i, sen in enumerate(par.sentences):
                    if len(txt) > 0:
                        txt += " "
                    txt = txt + sen.text  # getCRParagraph()
                ret.append(txt)
        return ret

    def getAllSentencesTextList_en(self):
        ret = []
        for par in self.text.paragraphs:
            for i, sen in enumerate(par.sentences_en):
                txt = sen.text
                if i == len(par.sentences_en) - 1:
                    txt = txt + getCRParagraph()
                else:
                    txt = txt + getSentenceSeperator()
                ret.append(txt)
        return ret

    def setInput(self, inputText: str):
        self.input = inputText


class SDUVersion(SQLModel):
    version: str = ""
    creation_date: str = ""

    class Config:
        orm_mode = False


class SDULearnset(SQLModel):
    # dict entry is the class, list are the train entrys for this class
    version: str = ""
    text: Dict = {}
    nlu: Dict = {}
    nlp: Dict = {}
    emb: Dict = {}
    vec_words: Dict = {}
    vec_sent: Dict = {}

    def set_version(self, version: str):
        self.version = version

    def reset(self):
        self.text.clear()
        self.nlu.clear()
        self.nlp.clear()
        self.emb.clear()
        self.vec_words.clear()
        self.vec_sent.clear()

    class Config:
        orm_mode = False


class SDUData(SQLModel):
    npages: int = 0  #
    stats: SDUStatistic = SDUStatistic()  #
    pages: List[SDUPage] = []
    converter: List[str] = []
    email: SDUEmail = SDUEmail()  # email header
    text: SDUText = SDUText()  # parsed/body only
    images: List[SDUPageImage] = []

    class Config:
        orm_mode = False

    def addPagePreProcessing(self, pagepre: SDUPage):
        if pagepre:
            self.pages.append(pagepre)
            self.npages = len(self.pages)
            pagepre.page = self.npages

    def escaped(self):
        return html.escape(self.text.html_content)

    async def sanitized(self):
        return await sanitize(self.text.html_content)


class SDUBBox(SQLModel):
    x0: float = -1
    y0: float = -1
    x1: float = -1
    y1: float = -1

    class Config:
        orm_mode = False


class SDUElement(SQLModel):
    id: int
    start: int = -1
    end: int = -1

    class Config:
        orm_mode = False


class SDUAttachment(SQLModel):
    id: str = ""
    name: str = ""
    path: str = ""
    metadata: Dict = {}
    text: SDUText = SDUText()
    charset: str = ""
    encoding: str = ""
    disposition: str = ""
    content_type: str = ""
    binary: bool = False
    payload: str = ""
    status: str = ""

    class Config:
        orm_mode = False


class SDUDimensions(SQLModel):
    id: int = -1
    height: float = 0.
    width: float = 0.
    factor_x: float = 0.
    factor_y: float = 0.
    rotation: int = 0

    class Config:
        orm_mode = False


class SDUFonts(SQLModel):
    id: int = -1
    fontsizes: Dict = {}
    fonts: List = []
    avg_fontsize: int = 14
    small_fontsize: int = 10000

    class Config:
        orm_mode = False


class SDULayout(SQLModel):
    id: int = -1
    dimensions: SDUDimensions = SDUDimensions()
    fonts: SDUFonts = SDUFonts()
    texttrace: List = []
    images: List = []
    drawings: List = []
    blocks: List[tuple] = []
    bjson: Dict = {}
    columns: List[SDUBBox] = []
    rows: List[SDUBBox] = []
    layouts: List = []
    header: SDUBBox = SDUBBox()
    body: SDUBBox = SDUBBox()
    footer: SDUBBox = SDUBBox()
    margin_left: SDUBBox = SDUBBox()
    margin_right: SDUBBox = SDUBBox()

    class Config:
        orm_mode = False


class SDUContent(SQLModel):
    attachments: List[SDUAttachment] = []
    layouts: List[SDULayout] = []

    class Config:
        orm_mode = False
