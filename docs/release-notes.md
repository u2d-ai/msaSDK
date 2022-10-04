# Release Notes
## Next release:
* New msaAdmin integration, with Admin, AuthAdmin and new Scheduler which supports Dashboard

## 0.2.5
* Switched from local packages to msa* packages
* Updated dashboard template, switched to amis version 2.3.0 from 1.10.2 and from local js/css to unpkg.com cdn
* BugFix: Solved language issues for the sdk based message popup's

## 0.1.6
* bug fixed with profiler
* bug fixed within sdk.js = was wrong version
* added script folder
* renamed docs dist folder
* added docs_src (todo move all sources there)
* fixed bug in features and deleted mappings as we don't want to define our models twice

## 0.1.5
* Cleaned Static Files
* Optimized logging as the * import from justpy and rocketry overrides the logging with INFO
* Fixed some typo in Docs
* Added more examples docu
* Added Web UI Examples
* Fully integrated JustPy 0.9.2 into msaSDK as the original JustPy is just not build for full integration in FastAPI, makes things easier
* Added signal module, as decorator and middleware plus the option to mount middleware in MSAApp via settings
* Added storagedict: Dicts who can sync themself to data storage backends, like redis, zookeeper.
* Added dynaconf: Can be used as a second option for own Settings handling.
* BUG: in logger fixed, uvicorn handler wasnt empty list, corrected this (Some log messages were duplicated)

## 0.1.4
* Integrated PyFilesystem2 as Abstract Filesystem for the Service
* Integrated msaSDk and FastAPI Docs in Admin API Docs as IFrame Pages
* Integrated justpy WEB UI Framework into MSAAPI Class

## 0.1.3
* merged fileupload and fileutils modules into refactored file module
* added TinyDB as JSON Storage into MSApp
* changed Scheduler from own implementation to https://rocketry.readthedocs.io/en/stable/index.html
* added some more docstrings
* changed readme.md links for images
* reduced size of logo_big
* automation of doc for requirements now also documents required packages from the ones installed by requirements.txt file

## 0.1.2

This is the first public release of msaSDK, former releases are all stages of development and internal releases

