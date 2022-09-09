#


## WDCPosition
```python 
WDCPosition()
```



----


## WDCWord
```python 
WDCWord()
```



----


## WDCToken
```python 
WDCToken()
```




**Methods:**


### .addWord
```python
.addWord(
   wrd: WDCWord
)
```


----


## WDCTriple
```python 
WDCTriple()
```



----


## WDCItem
```python 
WDCItem()
```



----


## WDCMeaning
```python 
WDCMeaning()
```




**Methods:**


### .addPosition
```python
.addPosition(
   pos: WDCPosition
)
```


### .processSynset
```python
.processSynset(
   syn, type: str
)
```


### .get_tree
```python
.get_tree()
```


### .get_root_tree_names
```python
.get_root_tree_names()
```


### .get_root_tree
```python
.get_root_tree()
```


### .get_frames
```python
.get_frames()
```


### .get_frames_set
```python
.get_frames_set()
```


### .get_domains
```python
.get_domains()
```


### .get_lemmas
```python
.get_lemmas()
```


### .get_sees
```python
.get_sees()
```


### .get_similar
```python
.get_similar()
```


### .get_hyponyms
```python
.get_hyponyms()
```


### .get_hypernyms
```python
.get_hypernyms()
```


### .get_holonyms
```python
.get_holonyms()
```


### .get_meronyms
```python
.get_meronyms()
```


### .get_entailments
```python
.get_entailments()
```


### .get_synset_list_names
```python
.get_synset_list_names(
   lst_syn: List, sep: str = ', '
)
```


### .get_tooltip
```python
.get_tooltip()
```


----


## WDCSpan
```python 
WDCSpan()
```




**Methods:**


### .addPosition
```python
.addPosition(
   pos: WDCPosition
)
```


----


## WDCMLEntry
```python 
WDCMLEntry()
```




**Methods:**


### .addEntity
```python
.addEntity(
   entity: WDCSpan
)
```


### .addMeaning
```python
.addMeaning(
   meaning: WDCMeaning, pos: WDCPosition
)
```


----


## WDCSentence
```python 
WDCSentence()
```




**Methods:**


### .addPosition
```python
.addPosition(
   pos: WDCPosition
)
```


### .addToken
```python
.addToken(
   tok: WDCToken
)
```


### .addTriple
```python
.addTriple(
   triple: WDCTriple
)
```


----


## WDCParagraph
```python 
WDCParagraph()
```




**Methods:**


### .addPosition
```python
.addPosition(
   pos: WDCPosition
)
```


### .addSentence
```python
.addSentence(
   sentence: WDCSentence
)
```


### .getTextNoLF
```python
.getTextNoLF()
```


----


## WDCPage
```python 
WDCPage()
```




**Methods:**


### .addParagraph
```python
.addParagraph(
   paragraph: WDCParagraph
)
```


----


## WDCMLDocument
```python 
WDCMLDocument()
```




**Methods:**


### .set_leaderboard_html
```python
.set_leaderboard_html(
   strHTML: str
)
```


### .get_leaderboard_html
```python
.get_leaderboard_html()
```


### .set_profile_learn_html
```python
.set_profile_learn_html(
   strHTML: str
)
```


### .get_profile_learn_html
```python
.get_profile_learn_html()
```


### .set_profile_html
```python
.set_profile_html(
   strHTML: str
)
```


### .get_profile_html
```python
.get_profile_html()
```


### .set_prediction_html
```python
.set_prediction_html(
   strHTML: str
)
```


### .get_prediction_html
```python
.get_prediction_html()
```


### .addEntry
```python
.addEntry(
   entry: WDCMLEntry
)
```


----


## WDCDocument
```python 
WDCDocument()
```




**Methods:**


### .getCurrentPageID
```python
.getCurrentPageID()
```


### .addPage
```python
.addPage(
   page: WDCPage
)
```


### .addEntity
```python
.addEntity(
   entity: WDCSpan
)
```


### .addMeaning
```python
.addMeaning(
   meaning: WDCMeaning, pos: WDCPosition
)
```

