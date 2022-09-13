from typing import Type

from msaSDK.admin.frontend.components import PageSchema
from msaSDK.admin import AdminApp, ModelAdmin
from msaSDK.db.crud.utils import schema_create_by_schema
from msaSDK.admin.utils.translation import i18n as _
from starlette.requests import Request

from .admin import UserLoginFormAdmin, GroupAdmin, PermissionAdmin, UserAdmin, \
    UserRegFormAdmin, RoleAdmin, UserInfoFormAdmin  # noqa F401
from .auth import AuthRouter


class UserAuthApp(AdminApp, AuthRouter):
    page_schema = PageSchema(label=_('User Authentication'), icon='fa fa-lock', sort=99)
    router_prefix = '/auth'
    # default admin
    UserLoginFormAdmin: Type[UserLoginFormAdmin] = UserLoginFormAdmin
    UserRegFormAdmin: Type[UserRegFormAdmin] = UserRegFormAdmin
    UserInfoFormAdmin: Type[UserInfoFormAdmin] = UserInfoFormAdmin
    UserAdmin: Type[UserAdmin] = UserAdmin
    RoleAdmin: Type[ModelAdmin] = RoleAdmin
    GroupAdmin: Type[ModelAdmin] = GroupAdmin
    PermissionAdmin: Type[ModelAdmin] = PermissionAdmin

    def __init__(self, app: "AdminApp", msa_app=None):
        """User Auth App

            Note:
                The app parameter for the Auth App is normaly provided by the AuthAdminSite Class.
                This class shouldn't be instantiated directly.

            Args:
                app: The admin app instance
                msa_app: The MSAApp instance [Optional]
        """
        self.msa_app = msa_app
        AdminApp.__init__(self, app, msa_app)
        AuthRouter.__init__(self)
        self.UserAdmin.model = self.UserAdmin.model or self.auth.user_model
        self.UserLoginFormAdmin.schema = self.UserLoginFormAdmin.schema or schema_create_by_schema(
            self.auth.user_model, 'UserLoginIn', include={'username', 'password'}
        )
        self.UserLoginFormAdmin.schema_submit_out = self.UserLoginFormAdmin.schema_submit_out or self.schema_user_login_out
        self.UserRegFormAdmin.schema = self.UserRegFormAdmin.schema or schema_create_by_schema(
            self.auth.user_model, 'UserRegIn', include={'username', 'password', 'email'}
        )
        self.UserRegFormAdmin.schema_submit_out = self.UserRegFormAdmin.schema_submit_out or self.schema_user_login_out
        self.UserInfoFormAdmin.schema = self.UserInfoFormAdmin.schema or schema_create_by_schema(
            self.auth.user_model, 'UserInfoForm',
            exclude={'id', 'username', 'password', 'is_active', 'parent_id', 'point', 'create_time'}
        )
        self.UserInfoFormAdmin.schema_submit_out = self.UserInfoFormAdmin.schema_submit_out or self.schema_user_info
        # register admin
        self.register_admin(
            self.UserLoginFormAdmin,
            self.UserRegFormAdmin,
            self.UserInfoFormAdmin,
            self.UserAdmin,
            self.RoleAdmin,
            self.GroupAdmin,
            self.PermissionAdmin
        )

    async def has_page_permission(self, request: Request) -> bool:
        """check the page permission for the request

            Args:
                request: the request object

            Returns: True or False

        """
        return (await super().has_page_permission(request)
                and await request.auth.requires(roles='admin', response=False)(request))
