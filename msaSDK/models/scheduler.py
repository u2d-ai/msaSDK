import datetime
from typing import Any, List, Optional, Union
from pydantic import BaseModel


class MSASchedulerRepoLogRecord(BaseModel):
    """**MSASchedulerRepoLogRecord** Pydantic Response Class"""

    task_name: str
    action: str
    created: Optional[datetime.datetime]
    name: str
    msg: str
    levelname: Any
    levelno: int
    pathname: str
    filename: str
    module: str
    exc_text: Any
    lineno: int
    funcName: str
    msecs: float
    relativeCreated: Optional[datetime.datetime]
    thread: int
    threadName: str
    processName: str
    process: int
    message: Any
    formatted_message: Any


class MSASchedulerTaskDetail(BaseModel):
    """**MSASchedulerTaskDetail** Pydantic Response Class"""

    permanent_task: bool
    fmt_log_message: str
    daemon: Any
    name: str
    description: Any
    logger_name: str
    execution: Any
    priority: int
    disabled: bool
    force_run: bool
    force_termination: bool
    status: str
    timeout: Optional[Union[str, int, datetime.timedelta]]
    parameters: Any
    start_cond: Any
    end_cond: Any
    on_startup: bool
    on_shutdown: bool
    last_run: Optional[datetime.datetime]
    last_success: Optional[datetime.datetime]
    last_fail: Optional[datetime.datetime]
    last_terminate: Optional[datetime.datetime]
    last_inaction: Optional[datetime.datetime]
    last_crash: Optional[datetime.datetime]
    func: Any
    path: Any
    func_name: str
    cache: bool
    sys_paths: List


class MSASchedulerTaskStatus(BaseModel):
    """**MSASchedulerTaskStatus** Pydantic Response Class"""

    name: Optional[str] = None
    """Task Name."""
    detail: Optional[MSASchedulerTaskDetail] = None
    """Task detail."""


class MSASchedulerStatus(BaseModel):
    """
    **MSASchedulerStatus** Pydantic Response Class
    """

    name: Optional[str] = "msaSDK Service"
    """Service Name."""
    tasks: Optional[List[MSASchedulerTaskStatus]] = []
    """Optional MSASchedulerTaskStatus List"""
    message: Optional[str] = "None"
    """Optional Message Text"""


class MSASchedulerLog(BaseModel):
    """
    **MSASchedulerStatus** Pydantic Response Class
    """

    name: Optional[str] = "msaSDK Service"
    """Service Name."""
    log: Optional[List[MSASchedulerRepoLogRecord]] = []
    """Optional MSASchedulerRepoLogRecord List"""
    message: Optional[str] = "None"
    """Optional Message Text"""
