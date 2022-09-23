# -*- coding: utf-8 -*-

import html
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel


class WDCPosition(BaseModel):  # Used for entity
    id: int = 0
    pageid: int = -1
    paraid: int = -1  #
    senid: int = -1
    s: int = -1
    e: int = -1


class WDCWord(BaseModel):
    id: int = -1
    text: str = ""
    lemma: str = ""
    misc: Optional[str] = None
    pos: str = ""
    type: Optional[str] = ""
    morph: str = ""
    head: int = -1
    label: str = ""
    deps: str = ""
    role: str = ""


class WDCToken(BaseModel):
    id: int = -1
    position: WDCPosition = WDCPosition()
    nwords: int = 0
    text: str = ""
    misc: Dict = {}
    ner: str = ""
    density: float = 0.0
    words: List[WDCWord] = []

    def addWord(self, wrd: WDCWord):
        if wrd:
            wrd.id = len(self.words)
            self.words.append(wrd)
            self.nwords = len(self.words)


class WDCTriple(BaseModel):
    id: int = -1
    position: WDCPosition = WDCPosition()
    score: float = 0.0
    subject: Dict = {}
    predicate: Dict = {}
    object: Dict = {}
    utterance: str = ""
    perspective: Dict = {}


class WDCItem(BaseModel):
    id: int = -1
    score: float = 0.0
    text: str = ""
    type: str = ""
    pos: List[Tuple] = []
    pos_text: List[str] = []


class WDCMeaning(BaseModel):  # Used for entity
    id: int = -1
    positions: List[WDCPosition] = []
    description: str = ""
    type: str = ""
    synset: str = ""
    offset: int = 0
    ssid: str = ""
    lexname: str = ""
    tree: List[str] = []
    tree_names: List[str] = []
    root_tree: List[str] = []
    root_tree_names: List[str] = []
    domains: List[str] = []
    frames: List[str] = []
    frames_id: List[int] = []
    frames_set: List[str] = []
    frames_set_id: List[int] = []
    root: str = ""
    lemmas: List[str] = []
    sees: List[str] = []
    hypernyms: List[str] = []
    hyponyms: List[str] = []
    holonyms: List[str] = []
    meronyms: List[str] = []
    similar: List[str] = []
    entailments: List[str] = []
    name: str = ""
    misc: Dict = {}
    hits: int = 1
    token: str = ""
    pos: str = ""
    context: List[str] = []

    def addPosition(self, pos: WDCPosition):
        if pos:
            self.positions.append(pos)

    def processSynset(self, syn, type: str):
        if not syn:
            return
        self.type = type
        # print("processSynset", self.token, syn)

        self.pos = syn.pos()
        self.synset = syn.name()
        self.offset = syn.offset()
        self.ssid = str(self.offset).zfill(8) + "-" + syn.pos()
        # lemmas
        self.lemmas = syn.lemma_names()
        # lexname
        ln = str(syn.lexname()).split(".")
        if len(ln) > 0:
            self.lexname = ln[1]
        else:
            self.lexname = str(syn.lexname())

        # similar
        lst = syn.similar_tos()
        self.similar = [entry.name() for entry in lst]
        # hypernyms
        lst = syn.hypernyms()
        self.hypernyms = [entry.name() for entry in lst]
        # hyponyms
        lst = syn.hyponyms()
        self.hyponyms = [entry.name() for entry in lst]
        # holonyms
        lst = syn.part_holonyms()
        self.holonyms = [entry.name() for entry in lst]
        # meronyms
        lst = syn.part_meronyms()
        self.meronyms = [entry.name() for entry in lst]
        # entailments
        lst = syn.entailments()
        self.entailments = [entry.name() for entry in lst]
        # sees
        lst = syn.also_sees()
        self.sees = [entry.name() for entry in lst]
        # domains
        lst = syn.topic_domains()
        self.domains = [
            entry.name() for entry in lst if entry.name() not in self.domains
        ]
        # root
        rn = syn.root_hypernyms()
        if len(rn) > 0:
            for rentry in rn:
                if len(self.root) > 1:
                    self.root += "/"
                self.root += str(rentry.name()).split(".")[0]
        # full tree
        lstm = syn.hypernym_paths()
        for li, lst in enumerate(lstm):
            rtxt = "root#" + str(li)
            rtxtn = "root#" + str(li)
            for entry in lst:
                if len(rtxt) > 1:
                    rtxt += "."
                    rtxtn += "."
                rtxt += entry.name()
                rtxtn += str(entry.name()).split(".")[0]
            self.root_tree.append(rtxt)
            self.root_tree_names.append(rtxtn)
        else:
            self.type = "WOE"
            meta: Dict = syn.metadata()
            self.pos = syn.pos
            if "description" in meta.keys():
                self.description = meta["description"]
            # print("Metadata", syn.metadata())
            # print("Sense", syn.senses())

            self.name = syn.senses()[0].word().lemma().replace(" ", "_")
            for sense in syn.get_related("domain_topic"):
                if len(sense.words()) > 0:
                    self.domains.append(sense.words()[0].lemma())

            self.offset = 0
            if len(self.synset) < 1:
                sid: str = str(syn.id)
                sids = sid.split("-")
                if len(sids) > 0:
                    sid = sids[1]
                else:
                    sid = sid.replace("odenet-", "")
                    sid = sid.replace("oewn-", "")
                    sid = sid.replace("-n", "")
                self.synset = self.name + "." + syn.pos + "." + sid

            self.ssid = str(syn.id)
            # lemmas
            self.lemmas = syn.lemmas()

            # hypernyms
            lst = syn.get_related("hypernym")
            self.hypernyms.extend(
                [nentry.lemmas()[0] for nentry in lst if len(nentry.lemmas()) > 0]
            )
            self.hypernyms.extend(
                [nentry.words()[0].lemma() for nentry in lst if len(nentry.words()) > 0]
            )

            # hyponyms
            lst = syn.get_related("hyponym")
            self.hyponyms.extend(
                [nentry.lemmas()[0] for nentry in lst if len(nentry.lemmas()) > 0]
            )
            self.hyponyms.extend(
                [nentry.words()[0].lemma() for nentry in lst if len(nentry.words()) > 0]
            )

            # holonyms
            lst = syn.get_related("holo_member")
            self.holonyms.extend(
                [nentry.lemmas()[0] for nentry in lst if len(nentry.lemmas()) > 0]
            )
            self.holonyms.extend(
                [nentry.words()[0].lemma() for nentry in lst if len(nentry.words()) > 0]
            )

            # meronyms
            lst = syn.get_related("mero_member")
            self.meronyms.extend(
                [nentry.lemmas()[0] for nentry in lst if len(nentry.lemmas()) > 0]
            )
            self.meronyms.extend(
                [nentry.words()[0].lemma() for nentry in lst if len(nentry.words()) > 0]
            )

            # entailments
            lst = syn.get_related("entails")
            self.entailments.extend(
                [nentry.lemmas()[0] for nentry in lst if len(nentry.lemmas()) > 0]
            )
            self.entailments.extend(
                [nentry.words()[0].lemma() for nentry in lst if len(nentry.words()) > 0]
            )

            # root
            rn = syn.hypernyms()
            if len(rn) > 0:
                for nentry in rn:
                    if len(self.root) > 1:
                        self.root += "/"
                    self.root += str(nentry.id)
            # full tree
            lstm = syn.hypernym_paths()
            for li, lst in enumerate(lstm):
                if li > 5:
                    break
                rtxt = "root#" + str(li)
                rtxtn = "root#" + str(li)
                for nentry in lst:
                    if len(rtxt) > 1:
                        if not rtxt.endswith("."):
                            rtxt += "."
                            rtxtn += "."
                    rtxt += nentry.id
                    if len(nentry.lemmas()) > 0:
                        rtxtn += str(nentry.lemmas()[0])
                    elif len(nentry.words()) > 0:
                        rtxtn += str(nentry.words()[0].lemma())
                self.root_tree.append(rtxt)
                self.root_tree_names.append(rtxtn)

        if len(self.description) < 1:
            self.description = syn.definition()

        # name
        ns = self.synset.split(".")
        if len(ns) > 0 and len(self.name) < 1:
            self.name = ns[0]
        elif len(self.name) < 1:
            self.name = self.synset

        if len(self.lexname) < 1:
            self.lexname = "generic"

        self.tree.append(self.lexname)
        self.tree.append(self.root)
        self.tree.extend(self.domains)
        self.tree.extend(self.hypernyms)

        self.synset = self.synset.upper()
        if not self.description:
            self.description = self.name.capitalize() + " > " + self.token.capitalize()

    def get_tree(self) -> str:
        ret: str = self.get_synset_list_names(self.tree, sep=".")
        return ret

    def get_root_tree_names(self) -> str:
        ret: str = ""
        for entry in self.root_tree_names:
            if len(ret) > 1:
                ret += "\n"
            ret += entry
        return ret

    def get_root_tree(self) -> str:
        ret: str = ""
        for entry in self.root_tree:
            if len(ret) > 1:
                ret += "\n"
            ret += entry
        return ret

    def get_frames(self) -> str:
        ret: str = self.get_synset_list_names(self.frames)
        return ret

    def get_frames_set(self) -> str:
        ret: str = self.get_synset_list_names(self.frames_set)
        return ret

    def get_domains(self) -> str:
        ret: str = self.get_synset_list_names(self.domains)
        return ret

    def get_lemmas(self) -> str:
        ret: str = self.get_synset_list_names(self.lemmas)
        return ret

    def get_sees(self) -> str:
        ret: str = self.get_synset_list_names(self.sees)
        return ret

    def get_similar(self) -> str:
        ret: str = self.get_synset_list_names(self.similar)
        return ret

    def get_hyponyms(self) -> str:
        ret: str = self.get_synset_list_names(self.hyponyms)
        return ret

    def get_hypernyms(self) -> str:
        ret: str = self.get_synset_list_names(self.hypernyms)
        return ret

    def get_holonyms(self) -> str:
        ret: str = self.get_synset_list_names(self.holonyms)
        return ret

    def get_meronyms(self) -> str:
        ret: str = self.get_synset_list_names(self.meronyms)
        return ret

    def get_entailments(self) -> str:
        ret: str = self.get_synset_list_names(self.entailments)
        return ret

    def get_synset_list_names(self, lst_syn: List, sep: str = ", ") -> str:
        ret: str = ""
        entry: str
        for entry in lst_syn:
            ln = entry.split(".")
            if len(ln) > 0:
                if len(ret) > 1:
                    ret += sep
                ret += ln[0].replace("_", " ")
            else:
                if len(ret) > 1:
                    ret += sep
                ret += entry.replace("_", " ")
        return ret

    def get_tooltip(self) -> str:
        ret = (
            "<span><i><small><strong>"
            + html.escape(self.type.upper() + "." + self.synset.upper())
            + "</strong> / "
            + html.escape(self.ssid.upper())
            + "</small></i><hr></span>"
        )  # <p>{{ entry[3] }}</p>
        ret += (
            "<p><h5><b><strong>"
            + html.escape(self.name.capitalize())
            + "</strong></b> > "
            + html.escape(self.token.capitalize())
            + "</h5></p>"
        )  # <p>{{ entry[3] }}</p>
        # ret += "<hr>"
        ret += (
            "<span><i><small><strong>Description</strong></small></i><hr><i><h6>"
            + html.escape(self.description.capitalize())
            + "<h6></i></span>"
        )
        # ret += "<hr>"
        ret += (
            "<span><i><small><strong>Node</strong></small></i><hr><h6>"
            + html.escape(self.get_tree())
            + "</h6></span>"
        )
        ret += (
            "<span><i><small><strong>Tree</strong></small></i><hr><h6>"
            + html.escape(self.get_root_tree_names()).replace("\n", "<br><br>")
            + "</h6></span>"
        )
        # ret += "<hr>"
        if len(self.sees) > 0:
            ret += (
                "<span><i><small><strong>Sees</strong></small></i><hr><h6>"
                + html.escape(self.get_sees())
                + "</h6></span>"
            )
        if len(self.similar) > 0:
            ret += (
                "<span><i><small><strong>Similar</strong></small></i><hr><h6>"
                + html.escape(self.get_similar())
                + "</h6></span>"
            )
        # ret += "<hr>"
        if len(self.hyponyms) > 0:
            ret += (
                "<span><i><small><strong>Specifics</strong></small></i><hr><h6>"
                + html.escape(self.get_hyponyms())
                + "</h6></span>"
            )
        if len(self.hypernyms) > 0:
            ret += (
                "<span><i><small><strong>Generalized</strong></small></i><hr><h6>"
                + html.escape(self.get_hypernyms())
                + "</h6></span>"
            )
        if len(self.holonyms) > 0:
            ret += (
                "<span><i><small><strong>Whole</strong></small></i><hr><h6>"
                + html.escape(self.get_holonyms())
                + "</h6></span>"
            )
        if len(self.meronyms) > 0:
            ret += (
                "<span><i><small><strong>Part</strong></small></i><hr><h6>"
                + html.escape(self.get_meronyms())
                + "</h6></span>"
            )
        # ret += "<hr>"
        if len(self.entailments) > 0:
            ret += (
                "<span><i><small><strong>Entailments</strong></small></i><hr><h6>"
                + html.escape(self.get_entailments())
                + "</h6></span>"
            )
        # ret += "<hr>"
        if len(self.domains) > 0:
            ret += (
                "<span><i><small><strong>Topic/Domain</strong></small></i><hr><h6>"
                + html.escape(self.get_domains())
                + "</h6></span>"
            )
        if len(self.frames) > 0:
            ret += (
                "<span><i><small><strong>Frames</strong></small></i><hr><h6>"
                + html.escape(self.get_frames())
                + "</h6></span>"
            )
        if len(self.frames_set) > 0:
            ret += (
                "<span><i><small><strong>FramesSet</strong></small></i><hr><h6>"
                + html.escape(self.get_frames_set())
                + "</h6></span>"
            )
        ret += (
            "<span><i><small><strong>Usual Words</strong></small></i><hr><h6><em>"
            + html.escape(self.get_lemmas())
            + "</h6></span>"
        )
        # ret = ret.replace("'", "\"")
        return ret


class WDCSpan(BaseModel):  # Used for entity
    id: int = -1
    text: str = ""
    ntokens: int = 0
    npos: int = 0
    type: str = ""
    misc: Dict = {}
    tokens: List[WDCToken] = []
    positions: List[WDCPosition] = []

    def addPosition(self, pos: WDCPosition):
        if pos:
            pos.id = len(self.positions)
            self.positions.append(pos)
            self.npos = len(self.positions)
            self.positions.sort(key=lambda x: (x.pageid, x.paraid, x.senid, x.s, x.e))
            for xi, pos in enumerate(self.positions):
                pos.id = xi


class WDCMLEntry(BaseModel):
    id: int = -1  #
    text: str = ""  #
    text_en: str = ""  #
    sentiment: str = ""
    density: float = 0.0

    en_xpos: List[str] = []
    en_upos: List[str] = []
    en_tokens: List[str] = []

    lng_xpos: List[str] = []
    lng_upos: List[str] = []
    lng_tokens: List[str] = []

    misc: Dict = {}

    nentities: int = 0
    nmeanings: int = 0

    entities: List[WDCSpan] = []
    meanings: List[WDCMeaning] = []

    def addEntity(self, entity: WDCSpan):
        if entity:
            self.entities.append(entity)
            self.nentities = len(self.entities)

    def addMeaning(self, meaning: WDCMeaning, pos: WDCPosition):
        if meaning:
            for mentry in self.meanings:
                if mentry.synset.__eq__(meaning.synset):
                    mentry.hits += 1
                    if pos not in mentry.positions:
                        mentry.positions.append(pos)
                    return

            self.nmeanings = len(self.meanings)
            meaning.id = self.nmeanings - 1
            meaning.positions.append(pos)
            self.meanings.append(meaning)


class WDCSentence(BaseModel):
    id: int = -1  #
    text: str = ""  #
    text_en: str = ""  #
    sentiment: str = ""
    density: float = 0.0
    ntokens: int = 0
    nwords: int = 0
    nentities: int = 0
    ndepends: int = 0
    ntriples: int = 0

    en_xpos: List[str] = []
    en_upos: List[str] = []
    en_tokens: List[str] = []

    lng_xpos: List[str] = []
    lng_upos: List[str] = []
    lng_tokens: List[str] = []

    tokens: List[WDCToken] = []
    triples: List[WDCTriple] = []
    dependencies: List = []
    misc: Dict = {}
    position: WDCPosition = WDCPosition()

    def addPosition(self, pos: WDCPosition):
        if pos:
            pos.senid = self.id
            self.position = pos

    def addToken(self, tok: WDCToken):
        if tok:
            tok.position.senid = self.id
            self.tokens.append(tok)
            self.ntokens = len(self.tokens)
            tok.id = self.ntokens - 1
            if self.density == 0.0:
                self.density = tok.density
            self.density = round(((self.density + tok.density) / 2.0), 2)

    def addTriple(self, triple: WDCTriple):
        if triple:
            triple.position.senid = self.id
            self.triples.append(triple)
            self.ntriples = len(self.triples)
            triple.id = self.ntriples - 1


class WDCParagraph(BaseModel):
    id: int = -1
    content: str = ""
    semantic: str = ""
    nsentences: int = 0
    ntokens: int = 0
    nwords: int = 0
    nentities: int = 0
    ndepends: int = 0

    lang: Optional[str] = None
    sentences: List[WDCSentence] = []
    position: WDCPosition = WDCPosition()

    def addPosition(self, pos: WDCPosition):
        if pos:
            pos.paraid = self.id
            self.position = pos

    def addSentence(self, sentence: WDCSentence):
        if sentence:
            sentence.position.paraid = self.id
            self.sentences.append(sentence)
            self.nsentences = len(self.sentences)
            sentence.id = self.nsentences - 1

    def getTextNoLF(self):
        ret = ""

        for sen in self.sentences:
            ret += sen.text + " "
        return ret


class WDCPage(BaseModel):
    id: int = -1
    content: str = ""
    nparagraphs: int = 0
    paragraphs: List[WDCParagraph] = []
    s: int = -1
    e: int = -1

    def addParagraph(self, paragraph: WDCParagraph):
        if paragraph:
            paragraph.position.pageid = self.id
            self.paragraphs.append(paragraph)
            self.nparagraphs = len(self.paragraphs)


class WDCMLDocument(BaseModel):
    content: str = ""
    nentries: int = 0
    targetsList: List = []
    trainList: List = []
    entries: List[WDCMLEntry] = []  #
    raw_json: List[Dict] = []
    df_data: List = []
    profile_html: str = ""
    profile_learn_html: str = ""
    prediction_html: str = ""
    leaderboard_html: str = ""

    def set_leaderboard_html(self, strHTML: str):
        if len(strHTML) > 0:
            self.leaderboard_html = html.escape(strHTML)

    def get_leaderboard_html(self) -> str:
        ret: str = ""
        if len(self.leaderboard_html) > 0:
            ret = html.unescape(self.leaderboard_html)
        return ret

    def set_profile_learn_html(self, strHTML: str):
        if len(strHTML) > 0:
            self.profile_learn_html = html.escape(strHTML)

    def get_profile_learn_html(self) -> str:
        ret: str = ""
        if len(self.profile_learn_html) > 0:
            ret = html.unescape(self.profile_learn_html)
        return ret

    def set_profile_html(self, strHTML: str):
        if len(strHTML) > 0:
            self.profile_html = html.escape(strHTML)

    def get_profile_html(self) -> str:
        ret: str = ""
        if len(self.profile_html) > 0:
            ret = html.unescape(self.profile_html)
        return ret

    def set_prediction_html(self, strHTML: str):
        if len(strHTML) > 0:
            self.prediction_html = html.escape(strHTML)

    def get_prediction_html(self) -> str:
        ret: str = ""
        if len(self.prediction_html) > 0:
            ret = html.unescape(self.prediction_html)
        return ret

    def addEntry(self, entry: WDCMLEntry):
        if entry:
            self.entries.append(entry)
            self.nentries = len(self.entries)


class WDCDocument(BaseModel):
    content: str = ""
    npages: int = 0  #
    nparagraphs: int = 0
    nsentences: int = 0
    ntokens: int = 0
    nwords: int = 0
    nentities: int = 0
    ndepends: int = 0
    ntriples: int = 0
    nmeanings: int = 0

    pages: List[WDCPage] = []  #
    entities: List[WDCSpan] = []
    meanings: List[WDCMeaning] = []

    def getCurrentPageID(self):
        ret = -1
        ix = len(self.pages)
        if ix > 0:
            ret = self.pages[ix - 1].id
        return ret

    def addPage(self, page: WDCPage):
        if page:
            self.pages.append(page)
            self.npages = len(self.pages)
            page.id = self.npages - 1

    def addEntity(self, entity: WDCSpan):
        if entity:
            self.entities.append(entity)
            self.nentities = len(self.entities)

    def addMeaning(self, meaning: WDCMeaning, pos: WDCPosition):
        if meaning:
            for mentry in self.meanings:
                if mentry.synset.__eq__(meaning.synset):
                    mentry.hits += 1
                    if pos not in mentry.positions:
                        mentry.positions.append(pos)
                    return

            self.nmeanings = len(self.meanings)
            meaning.id = self.nmeanings - 1
            meaning.positions.append(pos)
            self.meanings.append(meaning)
