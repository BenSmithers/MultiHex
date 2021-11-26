import os, sys
from datetime import datetime

# duplicate from the utils file so we don't have recursive imports 
def get_base_dir():
    # set up the save directory
    if sys.platform=='linux':
        basedir = os.path.join(os.path.expandvars('$HOME'),'.local','MultiHex')
    elif sys.platform=='darwin': #macOS
        basedir = os.path.join(os.path.expandvars('$HOME'),'MultiHex')
    elif sys.platform=='win32' or sys.platform=='cygwin': # Windows and/or cygwin. Not actually sure if this works on cygwin
        basedir = os.path.join(os.path.expandvars('%AppData%'),'MultiHex')
    else:
        Logger.Fatal("{} is not a supported OS".format(sys.platform), NotImplementedError)

    return(basedir)

logfile = os.path.join(get_base_dir(), "MultiLog.log")
class LoggerClass:
    def __init__(self, level=2, visual=True):
        if not isinstance(level,int):
            self.visual = True
            self.Fatal("Logger passed level of type {}, not {}".format(type(level), int), TypeError)
        if not isinstance(visual, bool):
            self.visual = True
            self.Fatal("Logger passed level of type {}, not {}".format(type(level), int), TypeError)

        self.file = open(logfile,mode='wt', buffering=1)
        self.level = level
        self.visual = visual
        self.Trace("Initializing Logger")

        self.pipe = None

    def connect(self, target):
        """
        This way we can connect some other object to this logger, and potentially display the log output in some gui (or whatever)
        """
        if not hasattr(target, "__call__"):
            self.Fatal("Cannot pipe to a non-callable", TypeError)

        self.pipe = target

    #def __del__(self):
        #self.file.close()

    def _log(self,level,message):
        if level == 1:
            status = "ERROR "
        elif level==2:
            status = "WARN  "
        elif level==3:
            status = "LOG   "
        elif level==4:
            status = "TRACE "
        else:
            self.Fatal("Received invalid log level {}".format(level), ValueError)

        date_string = str(datetime.now())

        self.file.write(" ".join([date_string, status, message,"\n"]))

        if self.pipe is not None:
            self.pipe(" ".join([date_string, status, message,"\n"]))

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


Logger = LoggerClass(level=3,visual=True)

