import os
from datetime import datetime

logfile = os.path.join(os.path.dirname(__file__), "MultiLog.log")
class LoggerClass:
    def __init__(self, level=2, visual=True):
        if not isinstance(level,int):
            self.visual = True
            self.Fatal("Logger passed level of type {}, not {}".format(type(level), int), TypeError)
        if not isinstance(visual, bool):
            self.visual = True
            self.Fatal("Logger passed level of type {}, not {}".format(type(level), int), TypeError)

        self.file = open(logfile,"a")
        self.level = level
        self.visual = visual
        self.Trace("Initializing Logger")

    def __del__(self):
        self.file.close()

    def _log(self,level,message):
        if level == 1:
            status = "ERROR "
        elif level==2:
            status = "WARN "
        elif level==3:
            status = "LOG"
        elif level==4:
            status = "TRACE "
        else:
            self.Fatal("Received invalid log level {}".format(level), ValueError)

        date_string = str(datetime.now())

        self.file.write(" ".join([date_string, status, message,"\n"]))

    def Trace(self,message):
        if self.level>=4:
            if self.visual:
                print(message)
            self._log(4,message)

    def Log(self, message):
        if self.level>=3:
            if self.visual:
                print(message)
            self._log(3,message)

    def Warn(self, warning):
        if self.level>=2:
            if self.visual:
                print(warning)
            self._log(2,warning)

    def Fatal(self, error, exception=Exception):
        if self.visual:
            print(error)
        self._log(1,error)
        raise exception(error)


Logger = LoggerClass(visual=True)
