# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime
from enum import Enum
from queue import Queue
from time import time

import pytz
from loguru import logger
from pydantic import typing
from starlette.concurrency import run_in_threadpool


class MSATimerEnum(str, Enum):
    """Enum for the different timer Types"""
    every_poll = 'every poll'
    every_second = 'every second'
    on_the_5_second = 'on the 5 second'
    on_the_15_second = 'on the 15 second'
    on_the_30_second = 'on the 30 second'
    every_minute = 'every minute'
    on_the_5_minute = 'on the 5 minute'
    on_the_15_minute = 'on the 15 minute'
    on_the_30_minute = 'on the 30 minute'
    every_hour = 'every hour'
    schedule = 'schedule'


class MSATimers:
    """
        Class to create dictionary of timers for use in MSAScheduler.
    """

    def __init__(self):
        """
        self.timer_jobs is the primary resource in MSATimers
        This is filled by MSATimers
        It is then accessed by the source
        and served to MSAScheduler
        """
        #### timer job lists
        self.timer_jobs = {
            MSATimerEnum.every_poll: [],
            MSATimerEnum.every_second: [],
            MSATimerEnum.on_the_5_second: [],
            MSATimerEnum.on_the_15_second: [],
            MSATimerEnum.on_the_30_second: [],
            MSATimerEnum.every_minute: [],
            MSATimerEnum.on_the_5_minute: [],
            MSATimerEnum.on_the_15_minute: [],
            MSATimerEnum.on_the_30_minute: [],
            MSATimerEnum.every_hour: [],
            MSATimerEnum.schedule: [],  # (function, 'HH:MM')
        }

    def create_timer(self, T_mode: MSATimerEnum, func: typing.Callable, mark_HH_MM: str = None):

        """ Create a Timer

        Args:
            T_mode: MSATimerEnum
            func: the call handler for this timer
            mark_HH_MM: If scheduler type then this is the time for execution.

        """

        # is a string
        if not isinstance(T_mode, MSATimerEnum):
            raise ValueError(f'Timer mode must be from MSATimerEnum')

        timer_mode = T_mode

        # check if timer is in timer_jobs
        if timer_mode not in list(self.timer_jobs.keys()):
            raise ValueError(
                f'Attempted to use non-timer: "{T_mode}", available timers are: {list(self.timer_jobs.keys())}')

        #### validate function
        # if not isinstance(func, types.FunctionType):
        if not hasattr(func, '__call__'):
            raise ValueError(
                f'Timer\'s function must be a function object, it should not have () on the end. e.g. myfunction, not myfunction()')

        if timer_mode[:2] == 'on' or timer_mode[:5] == 'every':
            #### on and every can be directly placed in timer_jobs
            self.timer_jobs[timer_mode].append(func)

        elif timer_mode == 'schedule':
            #### check format of the schedule time
            # is 24 hour format string
            if not isinstance(mark_HH_MM, str) or len(mark_HH_MM) != 5:
                raise ValueError(f'Schedule time ({mark_HH_MM}) must be a string in 24 hour format. e.g. "07:02"')

            # validate timer hours and minutes are formatted correctly
            try:
                # validate hours
                int(mark_HH_MM[:2])
            except ValueError:
                raise ValueError(f'Schedule time format issue, are hours in 24 hour format? e.g. "07:02"')
            try:
                # validate minutes
                int(mark_HH_MM[-2:])
            except ValueError:
                raise ValueError(f'Schedule time ({mark_HH_MM}) format issue, are minutes two digits? e.g. 17:02')

            #### add schedule timer to timer_jobs
            if 0 <= int(mark_HH_MM[:2]) < 24 and 0 <= int(mark_HH_MM[-2:]) < 60:
                self.timer_jobs[MSATimerEnum.schedule].append((func, mark_HH_MM))
            else:
                # error caused by hours or minutes not within range
                raise ValueError(f'Scheduled time ({mark_HH_MM}) not in 24 hour format HH:MM')

        else:
            # error for not being on, every, or schedule (this should never happen)
            raise ValueError(f'Attempted to use non-timer: {T_mode}')


class MSAScheduler:
    def __init__(self, jobs: dict, local_time_zone: str = 'UTC', poll_millis: float = 1000, debug: bool = False,
                 parent_logger=None):
        """ MSAScheduler object runs timers

        Standard Polling is 1 second

        Args:
            jobs: timer_jobs: dict[MSATimerEnum, list] = {...
            local_time_zone: str = 'UTC'
            poll_millis: float = 1000
            debug: bool = False
            parent_logger: logger instance to use, if empty it creates a local loguru logger
        """

        # self.jobs are all of the timers
        # it is a dictionary created by the MSATimers class
        self.jobs = jobs
        """dictionary MSATimers instances"""
        self.debug = debug
        """Debug mode True/False"""
        self.logger = parent_logger if parent_logger else logger

        self._poll_queue = Queue(maxsize=10)
        self._seconds_queue = Queue(maxsize=10)
        self._general_queue = Queue(maxsize=10)

        # polling time in milliseconds
        self._POLL_MILLIS = poll_millis
        self.local_time_zone = local_time_zone
        self.enabled: bool = False
        self.is_running: bool = False

    async def _run_job(self, job: typing.Callable):
        is_coroutine = asyncio.iscoroutinefunction(job)
        if self.debug:
            self.logger.info("Scheduler.run_job is_coroutine: " + str(is_coroutine) + " Job: " + str(job))
        if is_coroutine:
            await job.__call__()  # type: ignore
        else:
            await run_in_threadpool(job.__call__)

    async def stop_timers(self):
        """Stop all timers"""
        while self.is_running:
            self.enabled = False
            await asyncio.sleep(self._POLL_MILLIS / 1000)

    async def run_timers(self, poll_adjuster=.99, debug=False):
        '''runs timers as follows:

        * Step 1: run every poll jobs
        * Step 2: load timer queues for next poll
        * Step 3: delay function which runs previous poll queues

        poll_adjustor allows time for other timing
        '''
        if debug == True: print('\n\n run_timer with debug=True')

        #### set up last varables
        (last_hour, last_minute, last_second) = get_time(self.local_time_zone)
        last_milli = 0
        start_milli = time() * 1000
        self.enabled = True
        self.is_running = True
        while self.enabled:
            if not self.enabled:
                break
            await asyncio.sleep(0.1)
            milli = (time() * 1000) - start_milli

            #### deal with millis rolling
            # this should never happen
            if milli < 0:
                milli = (time() * 1000)
                last_milli = 0

            if (milli - last_milli) >= self._POLL_MILLIS:
                HHMMSS = get_time(self.local_time_zone)

                #### polling mark_HH_MMer
                last_milli = milli

                #### Run Every poll jobs ####
                if self.jobs['every poll'] != []:
                    for job in self.jobs['every poll']:
                        # print(f'poll: {job.__name__}')
                        await self._run_job(job)

                #### Second ####
                if last_second != HHMMSS[2]:
                    #### Every second jobs ####
                    for job in self.jobs['every second']:
                        self._seconds_queue.put(job)

                    last_second = HHMMSS[2]

                    #### On second jobs ####
                    if int(HHMMSS[2]) % 5 == 0 or int(HHMMSS[2]) == 0:
                        for job in self.jobs['on the 5 second']:
                            self._general_queue.put(job)

                    if int(HHMMSS[2]) % 15 == 0 or int(HHMMSS[2]) == 0:
                        for job in self.jobs['on the 15 second']:
                            self._general_queue.put(job)

                    if int(HHMMSS[2]) % 30 == 0 or int(HHMMSS[2]) == 0:
                        for job in self.jobs['on the 30 second']:
                            self._general_queue.put(job)

                    #### Minute ####
                    if last_minute != HHMMSS[1]:
                        #### Every minute jobs ####
                        for job in self.jobs['every minute']:
                            self._general_queue.put(job)
                        last_minute = HHMMSS[1]

                        #### On minute jobs ####
                        if int(HHMMSS[1]) % 5 == 0 or int(HHMMSS[1]) == 0:
                            for job in self.jobs['on the 5 minute']:
                                self._general_queue.put(job)

                        if int(HHMMSS[1]) % 15 == 0 or int(HHMMSS[1]) == 0:
                            for job in self.jobs['on the 15 minute']:
                                self._general_queue.put(job)

                        if int(HHMMSS[1]) % 30 == 0 or int(HHMMSS[1]) == 0:
                            for job in self.jobs['on the 30 minute']:
                                self._general_queue.put(job)

                        #### schedule jobs
                        if self.jobs['schedule'] != []:
                            for details in self.jobs['schedule']:
                                if details[1][:2] == HHMMSS[0] and details[1][-2:] == HHMMSS[1]:
                                    self._general_queue.put(details[0])

                        #### Hour ####
                        if last_hour != HHMMSS[0]:
                            #### Every hour jobs ####
                            for job in self.jobs['every hour']:
                                self._general_queue.put(job)
                            last_hour = HHMMSS[0]

            #### Delay function
            # runs queue jobs while waiting for poll time
            # poll_adjustor must take into account longest poll job
            while (milli - last_milli) < (poll_adjuster * self._POLL_MILLIS):
                #### run queues
                if self._seconds_queue.empty() == False:
                    job = self._seconds_queue.get()
                    # run job
                    await self._run_job(job)

                else:
                    if self._general_queue.empty() == False:
                        job = self._general_queue.get()
                        # run job
                        await self._run_job(job)
                    else:
                        await asyncio.sleep(self._POLL_MILLIS / 1000)  # all queues empty

                #### update milli
                milli = (time() * 1000) - start_milli

        self.is_running = False


def get_time_stamp(local_time_zone='UTC', time_format='HMS'):
    now_local = datetime.now(pytz.timezone(local_time_zone))
    if time_format == 'YMD:HM':
        return now_local.strftime('%Y-%m-%d' + '-' + '%H:%M')
    else:
        return now_local.strftime('%H:%M:%S')


def get_time(local_time_zone='UTC'):
    now_local = datetime.now(pytz.timezone(local_time_zone))
    HH = now_local.strftime('%H')
    MM = now_local.strftime('%M')
    SS = now_local.strftime('%S')
    return (HH, MM, SS)
