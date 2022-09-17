# WEB UI

<h2 align="center">
  msaSDK justpy - WEB UI Integration
</h2>

---
<p align="center">
    <em>Initialized by the MSAApp Class</em>
</p>

---

## Simple Example

Required MSAApp Service Definition (Settings):

    ui_justpy: bool = True
    
    # Optional to get the demos router mounted
    ui_justpy_demos: bool = True

Create the app object first
```python

from msaSDK.models.service import get_msa_app_settings
from msaSDK.service import MSAApp


settings = get_msa_app_settings()
settings.title = "Your Microservice Titel"
settings.version = "0.0.1"
settings.debug = True

# Enable the ui and demo
settings.ui_justpy = True
settings.ui_justpy_demos = True # will mount them all automatically

app = MSAApp(settings=settings)
```

If you want to mount them manually, or your custom UI Code

## Integrated Demo's
### Black Jack - Cards Demo
```python
from msaSDK.utils.ui_demos.card import cards_demo
app.add_jproute("/ui/cards", cards_demo)
```
![UI_Demo_Cards](images/msa_ui_demos_cards.png)

### Click Event Demo
```python
from msaSDK.utils.ui_demos.click import click_demo
app.add_jproute("/ui/click", click_demo)
```
![UI_Demo_Click](images/msa_ui_demos_click.png)

### Dogs App Demo
```python
from msaSDK.utils.ui_demos.dogs import dogs_demo
app.add_jproute("/ui/dogs", dogs_demo)
```
![UI_Demo_Dogs](images/msa_ui_demos_dogs.png)

### Happiness Dataset Demo - World Happiness Ranking
```python
from msaSDK.utils.ui_demos.happiness import happiness_demo, corr_stag_test, corr_test
app.add_jproute("/ui/happiness", happiness_demo)
# the sub routes in the happiness demo
app.add_jproute("/corr_staggered", corr_stag_test)
app.add_jproute("/corr", corr_test)
```
![UI_Demo_Happiness](images/msa_ui_demos_happiness.png)

### Iris Dataset Demo
```python
from msaSDK.utils.ui_demos.iris import iris_demo
app.add_jproute("/ui/iris", iris_demo)
```
![UI_Demo_Iris](images/msa_ui_demos_iris.png)

### Quasar Demo
```python
from msaSDK.utils.ui_demos.quasar import quasar_demo
app.add_jproute("/ui/quasar", quasar_demo)
```
![UI_Demo_Quasar](images/msa_ui_demos_quasar.png)

### Notification Demo
```python
from msaSDK.utils.ui_demos.after import after_click_demo
app.add_jproute("/ui/after", after_click_demo)
```
![UI_Demo_After](images/msa_ui_demos_after.png)

### Drag & Drop Demo
```python
from msaSDK.utils.ui_demos.drag import drag_demo
app.add_jproute("/ui/drag", drag_demo)
```
![UI_Demo_Drag](images/msa_ui_demos_drag.png)

### Multiple Uploads Demo
```python
from msaSDK.utils.ui_demos.uploads import upload_demo
app.add_jproute("/ui/upload", upload_demo)
```
![UI_Demo_Upload](images/msa_ui_demos_upload.png)
