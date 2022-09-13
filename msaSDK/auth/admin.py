from abc import ABC
from typing import Dict, Any, Type, Callable, List, Optional

from fastapi import Depends, HTTPException
from msaSDK.admin.admin import FormAdmin, ModelAdmin
from msaSDK.admin.frontend.components import ActionType, Action, ButtonToolbar, Form, Html, Grid, Page, Horizontal, \
    PageSchema
from msaSDK.admin.frontend.constants import LevelEnum, DisplayModeEnum
from msaSDK.db.crud.schema import MSACRUDOut
from msaSDK.admin.utils.translation import i18n as _
from .auth import Auth
from .auth.models import BaseUser, User, Group, Permission, Role
from .auth.schemas import UserLoginOut
from pydantic import BaseModel
from sqlalchemy import insert, update, select
from starlette import status
from starlette.requests import Request
from starlette.responses import Response


def attach_page_head(page: Page) -> Page:
    page.body = [Html(
        html=f'<div style="display: flex; justify-content: center; align-items: center; margin: 96px 0px 8px;"><img src="/msastatic/img/msa_logo_big.png" alt="logo" style="margin-right: 8px; width: 160px;"></div><div style="display: flex; justify-content: center; align-items: center; margin: 10px 0px 8px;font-size: 32px; font-weight: bold;">Login</div><div style="width: 100%; text-align: center; color: rgba(0, 0, 0, 0.45); margin-bottom: 40px;">{_("msaSDK Admin - Login")}</div>'
    ),
        Grid(
            columns=[{"body": [page.body], "lg": 2, "md": 4, "valign": "middle"}],
            align='center',
            valign='middle'
        )]
    return page


class UserLoginFormAdmin(FormAdmin, ABC):
    """The default User Login Form from the AuthAdminSite"""
    page = Page(title=_('User Login'))
    page_path = '/login'
    page_parser_mode = 'html'
    schema: Type[BaseModel] = None
    schema_submit_out: Type[UserLoginOut] = None
    page_schema = None
    page_route_kwargs = {'name': 'login'}

    async def handle(
            self,
            request: Request,
            data: BaseModel,  # self.schema
            **kwargs
    ) -> MSACRUDOut[BaseModel]:  # self.schema_submit_out
        if request.user:
            return MSACRUDOut(code=1, msg=_('User logged in!'), data=self.schema_submit_out.parse_obj(request.user))
        user = await request.auth.authenticate_user(username=data.username, password=data.password)  # type:ignore
        if not user:
            return MSACRUDOut(status=-1, msg=_('Incorrect username or password!'))
        if not user.is_active:
            return MSACRUDOut(status=-2, msg=_('Inactive user status!'))

        token_info = self.schema_submit_out.parse_obj(user)
        auth: Auth = request.auth
        token_info.access_token = await auth.backend.token_store.write_token(user.dict())
        return MSACRUDOut(code=0, data=token_info)

    @property
    def route_submit(self):
        async def route(response: Response, result: MSACRUDOut = Depends(super().route_submit)):
            if result.status == 0 and result.code == 0:  # 登录成功,设置用户信息
                response.set_cookie('Authorization', f'bearer {result.data.access_token}')
            return result

        return route

    async def get_form(self, request: Request) -> Form:
        form = await super().get_form(request)
        form.update_from_kwargs(
            title='',
            mode=DisplayModeEnum.horizontal,
            submitText=_("Sign in"),
            actionsClassName="no-border m-none p-none",
            panelClassName="",
            wrapWithPanel=True,
            horizontal=Horizontal(left=3, right=9),
            actions=[
                ButtonToolbar(
                    buttons=[
                        ActionType.Link(
                            actionType='link',
                            link=f'{self.router_path}/reg',
                            label=_('Sign up')
                        ),
                        Action(actionType='submit', label=_("Sign in"), level=LevelEnum.primary),
                    ]
                )
            ]
        )
        form.redirect = request.query_params.get('redirect') or '/'
        return form

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        return attach_page_head(page)

    @property
    def route_page(self) -> Callable:
        async def route(request: Request, result=Depends(super().route_page)):
            if request.user:
                raise HTTPException(
                    status_code=status.HTTP_307_TEMPORARY_REDIRECT, detail='already logged in',
                    headers={'location': request.query_params.get('redirect') or '/'}
                )
            return result

        return route

    async def has_page_permission(self, request: Request) -> bool:
        return True


class UserRegFormAdmin(FormAdmin, ABC):
    """The default User Registration Form from the AuthAdminSite"""
    user_model: Type[BaseUser] = User
    page = Page(title=_('User Register'))
    page_path = '/reg'
    page_parser_mode = 'html'
    schema: Type[BaseModel] = None
    schema_submit_out: Type[UserLoginOut] = None
    page_schema = None
    page_route_kwargs = {'name': 'reg'}

    async def handle(
            self,
            request: Request,
            data: BaseModel,  # self.schema
            **kwargs
    ) -> MSACRUDOut[BaseModel]:  # self.schema_submit_out
        auth: Auth = request.auth
        user = await auth.db.scalar(select(self.user_model).where(self.user_model.username == data.username))
        if user:
            return MSACRUDOut(status=-1, msg=_('Username has been registered!'), data=None)
        user = await auth.db.scalar(select(self.user_model).where(self.user_model.email == data.email))
        if user:
            return MSACRUDOut(status=-2, msg=_('Email has been registered!'), data=None)
        user = self.user_model.parse_obj(data)
        values = user.dict(exclude={'id', 'password'})
        values['password'] = auth.pwd_context.hash(user.password.get_secret_value())  # 密码hash保存
        stmt = insert(self.user_model).values(values)
        try:
            user.id = await auth.db.async_execute(
                stmt,
                on_close_pre=lambda r: getattr(r, "lastrowid", None)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error Execute SQL：{e}",
            ) from e
        # 注册成功,设置用户信息
        token_info = self.schema_submit_out.parse_obj(user)
        token_info.access_token = await auth.backend.token_store.write_token(user.dict())
        return MSACRUDOut(code=0, msg=_('Registered successfully!'), data=token_info)

    @property
    def route_submit(self):
        async def route(response: Response, result: MSACRUDOut = Depends(super().route_submit)):
            if result.status == 0 and result.code == 0:  # 登录成功,设置用户信息
                response.set_cookie('Authorization', f'bearer {result.data.access_token}')
            return result

        return route

    async def get_form(self, request: Request) -> Form:
        form = await super().get_form(request)
        form.redirect = request.query_params.get('redirect') or '/'
        form.update_from_kwargs(
            title='',
            mode=DisplayModeEnum.horizontal,
            submitText=_('Sign up'),
            actionsClassName="no-border m-none p-none",
            panelClassName="",
            wrapWithPanel=True,
            horizontal=Horizontal(left=3, right=9),
            actions=[
                ButtonToolbar(
                    buttons=[
                        ActionType.Link(
                            actionType='link',
                            link=f'{self.router_path}/login',
                            label=_('Sign in'),
                        ),
                        Action(actionType='submit', label=_('Sign up'), level=LevelEnum.primary),
                    ]
                )
            ]
        )

        return form

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        return attach_page_head(page)

    async def has_page_permission(self, request: Request) -> bool:
        return True


class UserInfoFormAdmin(FormAdmin):
    """The default User Info Form from the AuthAdminSite"""
    page_schema = None
    group_schema = None
    user_model: Type[BaseUser] = User
    page = Page(title=_('User Profile'))
    page_path = '/userinfo'
    schema: Type[BaseModel] = None
    schema_submit_out: Type[BaseUser] = None
    form_init = True
    form = Form(mode=DisplayModeEnum.horizontal)
    page_route_kwargs = {'name': 'userinfo'}

    async def get_init_data(self, request: Request, **kwargs) -> MSACRUDOut[Any]:
        return MSACRUDOut(data=request.user.dict(exclude={'password'}))

    async def get_form(self, request: Request) -> Form:
        form = await super().get_form(request)
        formitems = [
            await self.get_form_item(request, modelfield)
            for k, modelfield in self.user_model.__fields__.items()
            if k not in self.schema.__fields__ and k != 'password'
        ]
        form.body.extend(
            formitem.update_from_kwargs(disabled=True)
            for formitem in formitems
            if formitem
        )
        return form

    async def handle(self, request: Request, data: BaseModel, **kwargs) -> MSACRUDOut[Any]:
        stmt = update(self.user_model).where(self.user_model.username == request.user.username).values(data.dict())
        await self.site.db.async_execute(stmt)
        return MSACRUDOut(data={**request.user.dict(), **data.dict()})

    async def has_page_permission(self, request: Request) -> bool:
        return await self.site.auth.requires(response=False)(request)


class UserAdmin(ModelAdmin):
    """The User Admin object from the AuthAdminSite"""
    group_schema = None
    page_schema = PageSchema(label=_('User'), icon='fa fa-user')
    model: Type[BaseUser] = None
    exclude = ['password']
    link_model_fields = [User.roles, User.groups]
    search_fields = [User.username]

    async def on_create_pre(self, request: Request, obj, **kwargs) -> Dict[str, Any]:
        data = await super(UserAdmin, self).on_create_pre(request, obj, **kwargs)
        data['password'] = request.auth.pwd_context.hash(data['password'])  # 密码hash保存
        return data

    async def on_update_pre(self, request: Request, obj, item_id: List[int], **kwargs) -> Dict[str, Any]:
        data = await super(UserAdmin, self).on_update_pre(request, obj, item_id, **kwargs)
        password = data.get('password')
        if password:
            data['password'] = request.auth.pwd_context.hash(data['password'])  # 密码hash保存
        return data


class RoleAdmin(ModelAdmin):
    """Admin Role object"""
    group_schema = None
    page_schema = PageSchema(label=_('Role'), icon='fa fa-group')
    model = Role
    link_model_fields = [Role.permissions]
    readonly_fields = ['key']


class GroupAdmin(ModelAdmin):
    """Admin Group object"""
    group_schema = None
    page_schema = PageSchema(label=_('Group'), icon='fa fa-group')
    model = Group
    link_model_fields = [Group.roles]
    readonly_fields = ['key']


class PermissionAdmin(ModelAdmin):
    """Admin Permission object"""
    group_schema = None
    page_schema = PageSchema(label=_('Permission'), icon='fa fa-lock')
    model = Permission
    readonly_fields = ['key']
