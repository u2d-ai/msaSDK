#


### getResultSentences
```python
.getResultSentences(
   doc: WDCDocument
)
```


----


### getResultDependencies
```python
.getResultDependencies(
   doc: WDCDocument
)
```


----


### getResultTriples
```python
.getResultTriples(
   doc: WDCDocument
)
```


----


### getResultEntities
```python
.getResultEntities(
   doc: WDCDocument
)
```


----


### getResultEntitiesGroups
```python
.getResultEntitiesGroups(
   doc: WDCDocument
)
```


----


### getResultTokens
```python
.getResultTokens(
   doc: WDCDocument
)
```


----


### getResultWords
```python
.getResultWords(
   doc: WDCDocument
)
```


----


### getResultParagraphs
```python
.getResultParagraphs(
   doc: WDCDocument
)
```


----


### getResultPages
```python
.getResultPages(
   doc: WDCDocument
)
```


----


### createEntityOnly
```python
.createEntityOnly(
   text: str, type: str, start: int, end: int, pageid: int = -1, paraid: int = -1,
   senid: int = -1, misc = None
)
```


----


### createEntitySimple
```python
.createEntitySimple(
   paragraph: WDCParagraph, text, type, start, end, misc, x, senx
)
```


----


### createEntity
```python
.createEntity(
   paragraph: WDCParagraph, ent, optionCountry: bool, optionOrg: bool,
   optionDensity: bool, optionNatural: bool, langcode: str
)
```


----


### createToken
```python
.createToken(
   tok, optionDensity: bool, optionNatural: bool, langcode: str
)
```


----


### createWord
```python
.createWord(
   wrd
)
```


----


### getCompleteRoleFromDep
```python
.getCompleteRoleFromDep(
   dep
)
```


----


### createTriple
```python
.createTriple(
   triple: Dict, x
)
```


----


### createParagraph
```python
.createParagraph(
   par, x
)
```


----


### createNewDoc
```python
.createNewDoc(
   inputText: str, langcode: str = 'en'
)
```


----


### createNewMLDoc
```python
.createNewMLDoc(
   data: dict, langcode: str = 'en', optionTargetFields: str = 'IMPULSKATEGORIE,
   IMPULSART', optionTrainFields: str = 'SACHVERHALT'
)
```


----


### createNewParagraphs
```python
.createNewParagraphs(
   page: WDCPage, sdu_page: SDUPage, parmove: int, optionSentiment: bool,
   langcode: str
)
```

