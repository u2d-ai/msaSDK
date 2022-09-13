# -*- coding: utf-8 -*-

import html
import json
from typing import Dict, List

import pandas as pd

from msaSDK.utils.errorhandling import getMSABaseExceptionHandler
from msaSDK.models.sdu import SDUPage, SDUSentence
from msaSDK.models.wdc import WDCDocument, WDCSentence, WDCPage, WDCParagraph, WDCSpan, WDCPosition, WDCToken, \
    WDCWord, WDCTriple, WDCMLDocument

if __name__ == '__main__':
    pass

async def getResultSentences(doc: WDCDocument):
    ret = []
    pages = doc.pages
    for page in pages:
        for para in page.paragraphs:
            ret += para.sentences
            # for sen in para.sentences:
            # sen = seno.copy(exclude={'tokens', 'words', 'positions', 'entities'})
            # ret.append(sen)
    return ret


async def getResultDependencies(doc: WDCDocument):
    ret = []
    pages = doc.pages
    for page in pages:

        for para in page.paragraphs:
            for seno in para.sentences:
                deps: List = [dep for dep in seno.dependencies]
                res: Dict = {"pageid": page.id, "paraid": para.id, "senid": seno.id, "sentence": seno.text,
                             "deps": deps}
                ret.append(res)
    return ret


async def getResultTriples(doc: WDCDocument):
    ret = []
    pages = doc.pages
    for page in pages:
        for para in page.paragraphs:
            for seno in para.sentences:
                ret += seno.triples
    return ret


async def getResultEntities(doc: WDCDocument):
    ret = []

    # for ent in doc.entities:
    # ent = ento.copy(exclude={'tokens', 'words', 'positions'})
    # ret.append(ent)
    return doc.entities


async def getResultEntitiesGroups(doc: WDCDocument):
    ret = {}
    lst: List[WDCSpan] = doc.entities.copy()
    lst.sort(key=lambda x: (x.type, x.text.lower(), x.text))

    for ent in lst:
        # ent = ento.copy(exclude={'tokens', 'words'})
        if ent.type in ret.keys():
            ret[ent.type] = list(ret[ent.type]) + [ent]
        else:
            ret[ent.type] = [ent]
    return ret


async def getResultTokens(doc: WDCDocument):
    ret = []
    pages = doc.pages
    for page in pages:
        for para in page.paragraphs:
            for sen in para.sentences:
                ret += sen.tokens

    return ret


async def getResultWords(doc: WDCDocument):
    ret = []
    pages = doc.pages
    for page in pages:
        for para in page.paragraphs:
            for sen in para.sentences:
                for tok in sen.tokens:
                    ret += tok.words
    return ret


async def getResultParagraphs(doc: WDCDocument):
    ret = []
    pages = doc.pages
    for page in pages:
        ret += page.paragraphs
        # for para in page.paragraphs:
        # para = parao.copy(exclude={'sentences', 'entities'})
        # ret.append(para)
    return ret


async def getResultPages(doc: WDCDocument):
    ret = []
    pages = doc.pages
    for pageo in pages:
        ret.append({"id": pageo.id, "nparagraphs": pageo.nparagraphs, "content": pageo.content})
    return ret


async def createEntityOnly(text: str, type: str, start: int, end: int, pageid: int = -1, paraid: int = -1,
                           senid: int = -1, misc=None):
    if misc is None:
        misc = {}
    if len(text) < 1:
        return None

    nent = WDCSpan()
    try:
        nent.id = -1
        nent.text = text
        nent.type = type
        nent.misc = misc
        npos = WDCPosition()
        npos.senid = senid
        npos.pageid = pageid
        npos.paraid = paraid
        npos.s = start  # + headmove
        npos.e = end  # + headmove
        nent.addPosition(npos)

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: createEntitySimple:")

    return nent


async def createEntitySimple(paragraph: WDCParagraph, text, type, start, end, misc, x, senx):
    if len(text) < 1:
        return None
    nent = WDCSpan()
    try:
        nent.id = x
        nent.text = text
        nent.type = type
        nent.misc = misc
        npos = WDCPosition()
        npos.senid = senx
        npos.pageid = paragraph.position.pageid
        npos.paraid = paragraph.id
        npos.s = start  # + headmove
        npos.e = end  # + headmove
        nent.addPosition(npos)
        paragraph.nentities += 1

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: createEntitySimple:")

    return nent


async def createEntity(paragraph: WDCParagraph, ent,
                       optionCountry: bool, optionOrg: bool, optionDensity: bool,
                       optionNatural: bool, langcode: str):
    if not paragraph and not ent:
        return None

    nent = WDCSpan()
    try:
        nent.text = ent.text
        nent.type = ent.type
        paragraph.nentities += 1
        npos = WDCPosition()
        npos.pageid = paragraph.position.pageid
        npos.senid = ent.sent.index
        npos.paraid = paragraph.id
        npos.s = ent.start_char
        npos.e = ent.end_char
        nent.addPosition(npos)
        nent.ntokens = len(ent.tokens)

        for ti, tok in enumerate(ent.tokens):
            ntok = await createToken(tok, optionDensity=optionDensity, optionNatural=optionNatural, langcode=langcode)
            ntok.position.senid = ent.sent.index
            ntok.position.paraid = paragraph.id
            ntok.position.pageid = paragraph.position.pageid
            if len(ent.words) > ti:
                nwrd = await createWord(ent.words[ti])
                ntok.words.append(nwrd)

            nent.tokens.append(ntok)

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: createEntity:")

    return nent


async def createToken(tok, optionDensity: bool,
                      optionNatural: bool, langcode: str):
    if not tok:
        return None

    ntok = WDCToken()
    ntok.id = tok.id[0]
    ntok.text = tok.text
    ntok.misc["nlp"] = tok.misc
    ntok.position.s = tok.start_char
    ntok.position.e = tok.end_char
    if tok.ner:
        ntok.ner = tok.ner
    for wrd in tok.words:
        nwrd = await createWord(wrd)
        ntok.words.append(nwrd)

    return ntok


async def createWord(wrd):
    if not wrd:
        return None

    nwrd = WDCWord()
    nwrd.id = wrd.id
    nwrd.text = wrd.text
    nwrd.misc = wrd.misc

    nwrd.lemma = wrd.lemma
    nwrd.pos = wrd.upos
    nwrd.type = wrd.xpos
    nwrd.morph = wrd.feats
    if nwrd.morph is None:
        nwrd.morph = ""
    if wrd.head:
        nwrd.head = wrd.head
    if wrd.deprel:
        nwrd.label = wrd.deprel
    if wrd.deps:
        nwrd.deps = wrd.deps
        nwrd.role = await getCompleteRoleFromDep(nwrd.deps)

    return nwrd


async def getCompleteRoleFromDep(dep) -> str:
    if dep == 'nsubj':
        return 'agent'
    if dep == 'iobj':
        return 'recipient'
    if dep == 'dobj':
        return 'undergoer'
    if dep == 'mod':
        return 'oblique'
    if dep == 'nmod':
        return 'oblique'
    if dep == 'nmod_prep':
        return 'oblique'
    if dep == 'nsubjpass':
        return 'undergoer'
    if dep == 'advcl':
        return 'oblique'
    if dep == 'nmod:agent':
        return 'agent'
    if dep == 'ccomp':
        return 'eventuality'
    if dep == 'xcomp':
        return 'eventuality'
    if dep == 'acl_prep':
        return 'eventuality'
    if dep == 'advcl_prep':
        return 'eventuality'
    if dep == 'advcl':
        return 'eventuality'
    if dep == 'acl':
        return 'eventuality'
    if dep == 'acl_prep':
        return 'eventuality'
    if dep == 'parataxis':
        return 'eventuality'
    if dep == 'tmod':
        return 'oblique'
    if dep == 'nmod:tmod':
        return 'oblique'
    if dep == 'agent':
        return 'agent'
    if dep == 'vmod':
        return 'undergoer'
    if dep == 'nsubj':
        return 'not(undergoer),not(recipient),not(oblique)'
    if dep == 'iobj':
        return 'not(undergoer),not(agent),not(oblique)'
    if dep == 'dobj':
        return 'not(agent),not(recipient),not(oblique)'
    if dep == 'nmod_prep':
        return 'not(undergoer),not(recipient),not(agent)'
    return ""


async def createTriple(triple: Dict, x):
    if triple is None:
        return None
    ntriple = WDCTriple()
    try:
        if "subject" in triple.keys():
            ntriple.subject = triple["subject"]
        if "relation" in triple.keys():
            ntriple.predicate = triple["relation"]
        if "object" in triple.keys():
            ntriple.object = triple["object"]
        if "perspective" in triple.keys():
            ntriple.object = triple["perspective"]
        if "utterance type" in triple.keys():
            ntriple.object = triple["utterance type"]
        ntriple.id = x
    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: createTriple:")

    return ntriple


async def createParagraph(par, x):
    if par is None:
        return None
    npar = WDCParagraph()
    npar.id = x

    return npar


async def createNewDoc(inputText: str, langcode: str = "en"):
    newdoc = WDCDocument()
    return newdoc


async def createNewMLDoc(data: dict, langcode: str = "en",
                         optionTargetFields: str = "IMPULSKATEGORIE, IMPULSART",
                         optionTrainFields: str = "SACHVERHALT"):
    newdoc = WDCMLDocument()
    sheet_value: str
    sheet_key: str
    value: dict
    key: str
    targetsList = optionTargetFields.split(",")
    trainList = optionTrainFields.split(",")

    newdoc.targetsList = [entry.strip() for entry in targetsList]
    newdoc.trainList = [entry.strip() for entry in trainList]

    for sheet_key, sheet_value in data.items():
        data = json.loads(sheet_value)
        newdoc.raw_json.append(data)
        sheet_df: pd.DataFrame
        final_df: pd.DataFrame = pd.DataFrame()

        sheet_df = pd.read_json(sheet_value)
        final_df.index = sheet_df.index

        col_list: List = newdoc.targetsList + newdoc.trainList
        final_df[col_list] = sheet_df[col_list]

        newdoc.df_data.append(final_df.to_dict())
        newdoc.content += html.escape(final_df.to_html(notebook=True))

    newdoc.content = newdoc.content.replace("\n ", "").replace("\n", "")
    return newdoc


async def createNewParagraphs(page: WDCPage, sdu_page: SDUPage,
                              parmove: int, optionSentiment: bool, langcode: str):
    try:

        for xp, parT in enumerate(sdu_page.text.paragraphs):
            npar = await createParagraph(parT, xp)
            npar.semantic = parT.semantic_type
            npos = WDCPosition()
            npos.s = parmove
            if langcode == "en":
                if len(parT.sentences_en) < 1:
                    parT.sentences_en = parT.sentences.copy()
            for si, sen in enumerate(parT.sentences):

                sen_en: SDUSentence = parT.sentences_en[si]
                nsen = WDCSentence()
                nsenpos = WDCPosition()
                nsenpos.s = parmove
                nsenpos.pageid = page.id
                nsenpos.senid = sen.id
                nsen.text = sen.text
                if len(nsen.text_en) < 1 and len(sen_en.text) > 0:
                    nsen.text_en = sen_en.text
                if len(nsen.en_tokens) < 1 and len(sen_en.tokens) > 0:
                    nsen.en_tokens = sen_en.tokens.copy()

                if len(nsen.en_upos) < 1 and len(sen_en.upos) > 0:
                    nsen.en_upos = sen_en.upos.copy()
                if len(nsen.en_xpos) < 1 and len(sen_en.xpos) > 0:
                    nsen.en_xpos = sen_en.xpos.copy()

                if len(nsen.lng_tokens) < 1 and len(sen.tokens) > 0:
                    nsen.lng_tokens = sen.tokens.copy()

                if len(nsen.lng_upos) < 1 and len(sen.upos) > 0:
                    nsen.lng_upos = sen.upos.copy()
                if len(nsen.lng_xpos) < 1 and len(sen.xpos) > 0:
                    nsen.lng_xpos = sen.xpos.copy()

                nsen.id = sen.id
                npar.nsentences += 1
                parmove += len(sen.text) + 1
                nsenpos.e = parmove
                nsen.addPosition(nsenpos)
                npar.addSentence(nsen)

            npos.e = parmove
            npos.pageid = page.id
            npos.senid = -1
            npar.addPosition(npos)
            page.addParagraph(npar)

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: createNewParagraphs:")

    return parmove
