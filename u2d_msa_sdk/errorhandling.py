import sys
import traceback
from functools import lru_cache


class MSABaseExceptionHandler:

    def __init__(self) -> None:
        super().__init__()
        self.stack_trace = list()

    def handle(self, ex: Exception, *args):
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        for trace in trace_back:
            self.stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception: %s " % ex.__str__(), args)
        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" % ex_value)
        print("Stack trace : %s" % self.stack_trace)
        print("Stack trace : %s" % self.stack_trace)
        raise TypeError("Exception: %s " % ex.__str__() + " Arguments:" + str(args) + " Message:" + str(ex_value))


@lru_cache()
def getMSABaseExceptionHandler() -> MSABaseExceptionHandler:
    yield MSABaseExceptionHandler()
