from msaSDK.models.service import get_msa_app_settings
from msaSDK.service import MSAApp

settings = get_msa_app_settings()
settings.title = "Your Microservice Titel"
settings.version = "0.0.1"
settings.debug = True

app = MSAApp(settings=settings)

app.logger.info("Initialized " + settings.title + " " + settings.version)


@app.get("/my_service_url")
def my_service():
    return {"message": "hello world"}


if __name__ == "__main__":
    pass
