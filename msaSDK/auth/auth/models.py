from datetime import datetime
from typing import Optional, List, Any, Union, Sequence

from msaSDK.admin.frontend.components import InputImage, ColumnImage
from msaSDK.admin.utils.fields import Field
from msaSDK.admin.utils.translation import i18n as _
from pydantic import EmailStr, SecretStr
from sqlalchemy import Column, String, and_
from sqlalchemy.orm import backref, Session
from sqlalchemy.sql.selectable import Exists
from sqlmodel import SQLModel, Relationship, select
from sqlmodel.sql.expression import SelectOfScalar

SelectOfScalar.inherit_cache = True


class PkMixin(SQLModel):
    id: int = Field(default=None, primary_key=True, nullable=False)


class CreateTimeMixin(SQLModel):
    create_time: datetime = Field(default_factory=datetime.now, title=_('Create Time'))


class UsernameMixin(SQLModel):
    username: str = Field(
        title=_('Username'), max_length=32,
        sa_column=Column(String(32), unique=True, index=True, nullable=False)
    )


class PasswordStr(SecretStr, str):
    pass


class PasswordMixin(SQLModel):
    password: PasswordStr = Field(
        title=_('Password'), max_length=128,
        sa_column=Column(String(128), nullable=False),
        msa_ui_form_item='input-password'
    )


class EmailMixin(SQLModel):
    email: EmailStr = Field(
        None,
        title=_('Email'),
        sa_column=Column(String(50), unique=True, index=True, nullable=True),
        msa_ui_form_item='input-email'
    )


class UserRoleLink(SQLModel, table=True):
    __tablename__ = 'auth_user_roles'
    __table_args__ = {'extend_existing': True}
    user_id: Optional[int] = Field(
        default=None, foreign_key="auth_user.id", primary_key=True, nullable=False
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="auth_role.id", primary_key=True, nullable=False
    )


class UserGroupLink(SQLModel, table=True):
    __tablename__ = 'auth_user_groups'
    __table_args__ = {'extend_existing': True}
    user_id: Optional[int] = Field(
        default=None, foreign_key="auth_user.id", primary_key=True, nullable=False
    )
    group_id: Optional[int] = Field(
        default=None, foreign_key="auth_group.id", primary_key=True, nullable=False
    )


class GroupRoleLink(SQLModel, table=True):
    __tablename__ = 'auth_group_roles'
    __table_args__ = {'extend_existing': True}
    group_id: Optional[int] = Field(
        default=None, foreign_key="auth_group.id", primary_key=True, nullable=False
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="auth_role.id", primary_key=True, nullable=False
    )


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = 'auth_role_permissions'
    __table_args__ = {'extend_existing': True}
    role_id: Optional[int] = Field(
        default=None, foreign_key="auth_role.id", primary_key=True, nullable=False
    )
    permission_id: Optional[int] = Field(
        default=None, foreign_key="auth_permission.id", primary_key=True, nullable=False
    )


class BaseUser(PkMixin, UsernameMixin, PasswordMixin, EmailMixin, CreateTimeMixin):
    __tablename__ = 'auth_user'
    __table_args__ = {'extend_existing': True}
    is_active: bool = Field(default=True, title=_('Is Active'))
    nickname: str = Field(None, title=_('Nickname'), max_length=32)
    avatar: str = Field(
        None, title=_('Avatar'), max_length=100,
        msa_ui_form_item=InputImage(
            maxLength=1, maxSize=2 * 1024 * 1024,
            receiver='post:/admin/file/upload'
        ),
        msa_ui_table_column=ColumnImage(width=50, height=50, enlargeAble=True)
    )

    class Config:
        use_enum_values = True

    @property
    def is_authenticated(self) -> bool:
        return self.is_active

    @property
    def display_name(self) -> str:
        return self.nickname or self.username

    @property
    def identity(self) -> str:
        return self.username

    def _exists_role(self, *role_whereclause: Any) -> Exists:
        # check user role
        user_role_ids = select(Role.id).join(
            UserRoleLink, (UserRoleLink.user_id == self.id) & (UserRoleLink.role_id == Role.id)
        ).where(*role_whereclause)
        # check user group
        role_group_ids = select(GroupRoleLink.group_id).join(
            Role, and_(*role_whereclause, Role.id == GroupRoleLink.role_id)
        )
        group_user_ids = select(UserGroupLink.user_id).where(UserGroupLink.user_id == self.id).where(
            UserGroupLink.group_id.in_(role_group_ids)
        )
        return user_role_ids.exists() | group_user_ids.exists()

    def _exists_roles(self, roles: List[str]) -> Exists:
        """
        Check if the user belongs to the specified user role, or to a user group that contains the specified user role

        Args:
            roles:

        Returns:
            Exists
        """
        return self._exists_role(Role.key.in_(roles))

    def _exists_groups(self, groups: List[str]) -> Exists:
        """
        Check if the user belongs to the specified user group

        Args:
            groups:

        Returns:
            Exists
        """
        group_ids = select(Group.id).join(
            UserGroupLink, (UserGroupLink.user_id == self.id) & (UserGroupLink.group_id == Group.id)
        ).where(Group.key.in_(groups))
        return group_ids.exists()

    def _exists_permissions(self, permissions: List[str]) -> Exists:
        """
        Check if the user belongs to the user role with the specified privileges

        Args:
            permissions:

        Returns:
            Exists
        """
        role_ids = select(RolePermissionLink.role_id).join(
            Permission, Permission.key.in_(permissions) & (Permission.id == RolePermissionLink.permission_id)
        )
        return self._exists_role(Role.id.in_(role_ids))

    def has_requires(
            self,
            session: Session,
            *,
            roles: Union[str, Sequence[str]] = None,
            groups: Union[str, Sequence[str]] = None,
            permissions: Union[str, Sequence[str]] = None,
    ) -> bool:
        """
        Check if the user has the specified RBAC privileges

        Args:
            session: sqlalchemy `Session`; asynchronous `AsyncSession`, please use `run_sync` method.
            roles: list of roles
            groups: list of user groups
            permissions: list of permissions

        Returns:
            Return `True` for successful detection.
        """
        stmt = select(1)
        if groups:
            groups_list = [groups] if isinstance(groups, str) else list(groups)
            stmt = stmt.where(self._exists_groups(groups_list))
        if roles:
            roles_list = [roles] if isinstance(roles, str) else list(roles)
            stmt = stmt.where(self._exists_roles(roles_list))
        if permissions:
            permissions_list = [permissions] if isinstance(permissions, str) else list(permissions)
            stmt = stmt.where(self._exists_permissions(permissions_list))
        return bool(session.scalar(stmt))


class User(BaseUser, table=True):
    __tablename__ = 'auth_user'
    __table_args__ = {'extend_existing': True}
    roles: List["Role"] = Relationship(link_model=UserRoleLink)
    groups: List["Group"] = Relationship(link_model=UserGroupLink)


class BaseRBAC(PkMixin):
    __table_args__ = {'extend_existing': True}
    key: str = Field(
        ..., title=_('Identify'), max_length=20,
        sa_column=Column(String(20), unique=True, index=True, nullable=False)
    )
    name: str = Field(..., title=_('Name'), max_length=20)
    desc: str = Field(default='', title=_('Description'), max_length=400, msa_ui_form_item='textarea')


class Role(BaseRBAC, table=True):
    """Roles"""
    __tablename__ = 'auth_role'
    groups: List["Group"] = Relationship(back_populates="roles", link_model=GroupRoleLink)
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermissionLink)


class BaseGroup(BaseRBAC):
    __tablename__ = 'auth_group'
    parent_id: int = Field(None, title=_('Parent'), foreign_key="auth_group.id")


class Group(BaseGroup, table=True):
    """Group"""
    roles: List["Role"] = Relationship(back_populates="groups", link_model=GroupRoleLink)


class Permission(BaseRBAC, table=True):
    """Permisson"""
    __tablename__ = 'auth_permission'
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermissionLink)
