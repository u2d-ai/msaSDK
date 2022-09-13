from typing import Type

from starlette.requests import Request

from msaSDK.admin.frontend.components import Flex, App, Service, ActionType, Dialog
from msaSDK.admin.frontend.constants import SizeEnum
from msaSDK.admin.frontend.types import MSAUIAPI
from msaSDK.admin.site import AdminSite
from msaSDK.admin.utils.translation import i18n as _
from msaSDK.auth.app import UserAuthApp
from msaSDK.auth.auth import Auth
from msaSDK.service import MSAApp


class AuthAdminSite(AdminSite):
    auth: Auth = None
    UserAuthApp: Type[UserAuthApp] = UserAuthApp

    def __init__(
            self,
            msa_app: MSAApp = None,
            auth: Auth = None
    ):
        super().__init__(msa_app)
        self.auth = auth or self.auth or Auth(db=self.db)
        self.UserAuthApp.msa_app = msa_app
        self.UserAuthApp.auth = self.auth
        self.register_admin(self.UserAuthApp)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        user_auth_app = self.get_admin_or_create(self.UserAuthApp)
        app.header = Flex(
            className="w-full", justify='flex-end', alignItems='flex-end', items=[app.header, {
                "type": "dropdown-button",
                "label": f"{request.user.username}",
                "trigger": "hover",
                "icon": "fa fa-user",
                "buttons": [
                    ActionType.Dialog(
                        label=_('User Profile'),
                        dialog=Dialog(
                            title=_('User Profile'),
                            actions=[],
                            size=SizeEnum.lg,
                            body=Service(
                                schemaApi=MSAUIAPI(
                                    method='post',
                                    url=f"{user_auth_app.router_path}/form/userinfo",
                                    cache=600000,
                                    responseData={'&': '${body}'}
                                )
                            )
                        )
                    ),
                    ActionType.Url(
                        label=_('Sign out'),
                        url=f"{user_auth_app.router_path}/logout"
                    ),
                ]
            }]
        )
        return app

    async def has_page_permission(self, request: Request) -> bool:
        return await self.auth.requires(response=False)(request)
