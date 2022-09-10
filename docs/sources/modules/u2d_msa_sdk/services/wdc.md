#



## getResultSentences
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L18"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultSentences(
   doc: WDCDocument
)
```


----



## getResultDependencies
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L30"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultDependencies(
   doc: WDCDocument
)
```


----



## getResultTriples
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L47"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultTriples(
   doc: WDCDocument
)
```


----



## getResultEntities
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L57"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultEntities(
   doc: WDCDocument
)
```


----



## getResultEntitiesGroups
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L66"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultEntitiesGroups(
   doc: WDCDocument
)
```


----



## getResultTokens
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L80"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultTokens(
   doc: WDCDocument
)
```


----



## getResultWords
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L91"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultWords(
   doc: WDCDocument
)
```


----



## getResultParagraphs
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L102"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultParagraphs(
   doc: WDCDocument
)
```


----



## getResultPages
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L113"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getResultPages(
   doc: WDCDocument
)
```


----



## createEntityOnly
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L121"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createEntityOnly(
   text: str, type: str, start: int, end: int, pageid: int = -1, paraid: int = -1,
   senid: int = -1, misc = None
)
```


----



## createEntitySimple
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L148"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createEntitySimple(
   paragraph: WDCParagraph, text, type, start, end, misc, x, senx
)
```


----



## createEntity
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L172"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createEntity(
   paragraph: WDCParagraph, ent, optionCountry: bool, optionOrg: bool,
   optionDensity: bool, optionNatural: bool, langcode: str
)
```


----



## createToken
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L209"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createToken(
   tok, optionDensity: bool, optionNatural: bool, langcode: str
)
```


----



## createWord
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L229"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createWord(
   wrd
)
```


----



## getCompleteRoleFromDep
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L255"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getCompleteRoleFromDep(
   dep
)
```


----



## createTriple
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L309"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createTriple(
   triple: Dict, x
)
```


----



## createParagraph
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L331"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createParagraph(
   par, x
)
```


----



## createNewDoc
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L340"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createNewDoc(
   inputText: str, langcode: str = 'en'
)
```


----



## createNewMLDoc
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L345"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createNewMLDoc(
   data: dict, langcode: str = 'en', optionTargetFields: str = 'IMPULSKATEGORIE,
   IMPULSART', optionTrainFields: str = 'SACHVERHALT'
)
```


----



## createNewParagraphs
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/services/wdc.py/#L379"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createNewParagraphs(
   page: WDCPage, sdu_page: SDUPage, parmove: int, optionSentiment: bool,
   langcode: str
)
```

