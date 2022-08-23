import uvicorn


class MSAServerUvicorn:

    def __init__(self, app: str, app_dir: str, host: str, port: int, reload: bool = False, log_level: str = "info",
                 workers: int = 1) -> None:
        super().__init__()
        self.app: str = app
        self.app_dir: str = app_dir
        self.port: int = port
        self.host: str = host
        self.reload: bool = reload
        self.log_level: str = log_level
        self.workers: int = workers

    def run(self):
        uvicorn.run(app=self.app, app_dir=self.app_dir, host=self.host, port=self.port, reload=self.reload,
                    log_level=self.log_level, workers=self.workers)
