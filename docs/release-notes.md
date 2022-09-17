# Release Notes
## Possible future features:
* Add examples for Amins Pages and additional features of the Admin and auth module
* versioning? FastAPI versioning
* camel case support FastAPI-CamelCase
* FastAPI Future Flags?
* fastapi_socketio?
* Events lib? FastApi Events or FastAPI Websocket Pub/Sub fastapi-cloudevents? Webhook receive? Seems we need a combination of some

## 0.1.5
* Cleaned Static Files
* Optimized logging as the * import from justpy and rocketry overrides the logging with INFO
* Fixed some typo in Docs
* Added more examples docu
* Added Web UI Examples

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

