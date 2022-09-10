#



## findSystemFonts
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fonts.py/#L11"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.findSystemFonts(
   fontpaths = None, fontext = 'ttf'
)
```

---
Search for fonts in the specified font paths.  If no paths are
given, will use a standard set of system paths, as well as the
list of fonts tracked by fontconfig if fontconfig is installed and
available.  A list of TrueType fonts are returned by default with
AFM fonts as an option.
