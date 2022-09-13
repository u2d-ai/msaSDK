# -*- coding: utf-8 -*-
import sys
import traceback
from functools import lru_cache
from loguru import logger


class MSABaseExceptionHandler:

    def __init__(self) -> None:
        super().__init__()
        self.stack_trace = list()

    def handle(self, ex: Exception, *args):
        """handle Exception

            Get the current system exception, extract unformatter stack traces as tuples.

            ```mermaid
            flowchart LR
                 system_exception -. n:m .-> Exceptions
                 Exceptions -. m:m .-> Extract
                 Extract -. m:m .-> Formatted
            ```

            Formats stacktrace to: File : %s , Line : %d, Func.Name : %s, Message : %s

            Logs the information with logger.error() str, args, type, value, stack_trace

            Raises:
                TypeError: Exception: ... Arguments: ... Message: ... Stack trace: ...
        """
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        self.stack_trace = [ "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2],
                                                                                      trace[3]) for trace in trace_back]


        logger.error("Exception: %s " % ex.__str__(), args)
        logger.error("Exception type : %s " % ex_type.__name__)
        logger.error("Exception message : %s" % ex_value)
        logger.error("Stack trace : %s" % self.stack_trace)
        raise TypeError("Exception: %s " % ex.__str__() + " Arguments:" + str(args) + " Message:" + str(ex_value)
                        + " Stack trace : " + str(self.stack_trace))


@lru_cache()
def getMSABaseExceptionHandler() -> MSABaseExceptionHandler:
    """
    This function returns a cached instance of the MSABaseExceptionHandler object.
    Note:
        Caching is used to prevent re-reading the environment every time the MSABaseExceptionHandler is used.
    """
    return MSABaseExceptionHandler()
