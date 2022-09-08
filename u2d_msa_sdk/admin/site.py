import os.path
import platform
import time
import uuid

import aiofiles
from fastapi import UploadFile, File, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from u2d_msa_sdk import admin
from u2d_msa_sdk.db.crud.schema import MSACRUDOut
from .admin import AdminApp, IframeAdmin, PageAdmin, BaseAdminSite, RouterAdmin
from .frontend.components import PageSchema, Page, Property, Divider
from .settings import AdminSettings
from .utils.translation import i18n as _
from ..utils.sysinfo import get_sysinfo


class DocsAdmin(IframeAdmin):
    group_schema = PageSchema(label='API Docs', icon='fa fa-book', sort=-100)
    page_schema = PageSchema(label='OpenAPI', icon='fa fa-book')

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.docs_url


class ReDocsAdmin(IframeAdmin):
    group_schema = PageSchema(label='API Docs', icon='fa fa-book', sort=-100)
    page_schema = PageSchema(label='Redocs', icon='fa fa-book')

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.redoc_url


class HomeAdmin(PageAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('Home'), icon='fa fa-home', url='/home', isDefaultPage=True, sort=100)
    page_path = '/home'

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        sysinfo = get_sysinfo()
        page.body = [
            Property(
                title='Service Info',
                column=4,
                items=[
                    Property.Item(label='Title', content=self.site.fastapi.title),
                    Property.Item(label='Version', content=self.site.fastapi.version),
                    Property.Item(label='Language', content=self.site.settings.language),
                    Property.Item(label='Debug', content=str(self.site.fastapi.debug)),
                ]
            ),
            Divider(),
            Property(
                title='MSA SDK',
                column=4,
                items=[
                    Property.Item(label='System', content=platform.system()),
                    Property.Item(label='Python', content=platform.python_version()),
                    Property.Item(label='Version', content=admin.__version__),
                    Property.Item(label='License', content='MIT'),
                ]
            ),
            Divider(),
            Property(
                title='System',
                column=4,
                items=[
                    Property.Item(label='Booted', content=sysinfo.System_Boot),
                    Property.Item(label='IP', content=sysinfo.IP_Address),
                    Property.Item(label='MAC Address', content=sysinfo.MAC_Address),
                    Property.Item(label='Host Name', content=sysinfo.Host_Name),
                    Property.Item(label='CPU Physical', content=sysinfo.CPU_Physical),
                    Property.Item(label='CPU Logical', content=sysinfo.CPU_Logical),
                    Property.Item(label='CPU in Use', content=sysinfo.CPU_Current),
                    Property.Item(label='CPU Affinity', content=sysinfo.CPU_Affinity),
                    Property.Item(label='Mem Total', content=sysinfo.Memory_Physical),
                    Property.Item(label='Mem Usage', content=str(sysinfo.Memory_Usage.percent) + "%"),
                    Property.Item(label='Mem Free', content=sysinfo.Memory_Available),
                    Property.Item(label='PID', content=sysinfo.PID),
                    Property.Item(label='OS Name', content=sysinfo.OS_Name),
                    Property.Item(label='OS Version', content=sysinfo.OS_Version),
                    Property.Item(label='OS Release', content=sysinfo.OS_Release),
                    Property.Item(label='Status', content=sysinfo.Runtime_Status),
                ]
            ),
        ]
        return page


class FileAdmin(RouterAdmin):
    # todo perfect: Limit file size/suffixes/content_type
    file_directory: str = 'upload'
    file_path: str = '/upload'
    file_max_size: int = 2 * 1024 * 1024
    router_prefix = '/file'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.file_directory = self.file_directory or self.file_path
        self.static_path = self.mount_staticfile()

    def get_filename(self, file: UploadFile):
        filename = str(uuid.uuid4()).replace('-', '') + os.path.splitext(file.filename)[1]
        return os.path.join(time.strftime("%Y%m"), filename)

    def mount_staticfile(self) -> str:
        os.path.exists(self.file_directory) or os.makedirs(self.file_directory)
        self.app.site.fastapi.mount(self.file_path, StaticFiles(directory=self.file_directory), self.file_directory)
        return self.app.site.router_path + self.file_path

    def register_router(self):

        @self.router.post(self.file_path, response_model=MSACRUDOut[self.UploadOutSchema])
        async def file_upload(file: UploadFile = File(...)):
            filename = self.get_filename(file)
            file_path = os.path.join(self.file_directory, filename)
            file_dir = os.path.dirname(file_path)
            os.path.exists(file_dir) or os.makedirs(file_dir)
            try:
                res = await file.read()
                if self.file_max_size and len(res) > self.file_max_size:
                    return MSACRUDOut(status=-2, msg='The file size exceeds the limit')
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(res)
                return MSACRUDOut(
                    data=self.UploadOutSchema(filename=filename, url=f'{self.static_path}/{filename}'),
                )

            except Exception as e:
                return MSACRUDOut(status=-1, msg=str(e))

    class UploadOutSchema(BaseModel):
        filename: str = None
        url: str = None


class AdminSite(BaseAdminSite):

    def __init__(self, settings: AdminSettings, fastapi: FastAPI = None, engine: AsyncEngine = None):
        super().__init__(settings, fastapi, engine)
        self.register_admin(HomeAdmin, DocsAdmin, ReDocsAdmin, FileAdmin)
