#


### findSystemFonts
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
