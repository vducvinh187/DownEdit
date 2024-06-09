import datetime
import logging
import time

from rich.logging import RichHandler
from rich.traceback import install
from rich.console import Console

from .singleton import Singleton

install()

class Formatter(logging.Formatter):
    msg_color = {
        "DEBUG"     : "cyan",
        "INFO"      : "green",
        "WARNING"   : "yellow",
        "ERROR"     : "red",
        "CRITICAL"  : "bold red",
        "FILE"      : "magenta",
    }

    def __init__(self, fmt="{message}", style='{', datefmt="[%X]"):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        """
        Format the message with color based on the log level
        """
        # Retrieve the original message
        message = record.getMessage()
        # color = self.msg_color.get(record.levelname, 'white')
        # message = f"[{color}]{message}[/]"
        record.msg = message
        return super().format(record)
    

class Logger(logging.Logger, metaclass=Singleton):
    def __init__(self, name, level=logging.DEBUG):
        # Prevent re-initialization of the logger
        if hasattr(self, '_ready'):
            return
        
        super().__init__(name, level)
        self.console = Console()
        self._ready = True

    def config_log(self, log_level=logging.DEBUG):
        """
        Set new log level and configure 
        """
        self.setLevel(log_level)

        console_handler = RichHandler(
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
            omit_repeated_times=False
        )
        console_handler.setFormatter(Formatter())
        self.addHandler(console_handler)
    
    def pause(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.console.input(f"[cyan][{current_time}][/] [green]Press any key to continue ...[/]")

    def close(self):
        # Properly close and remove all handlers
        for handler in self.handlers:
            handler.close()
            self.removeHandler(handler)
        self.handlers.clear()
        # Ensure all logs are processed before exit
        time.sleep(0.5)

# Set the custom logger class as the default
logging.setLoggerClass(Logger)

# Adding custom log level method
FILE_LEVEL_NUM = 25
logging.addLevelName(FILE_LEVEL_NUM, "FILE")

def file(self, message, *args, **kwargs):
    if self.isEnabledFor(FILE_LEVEL_NUM):
        self._log(FILE_LEVEL_NUM, message, args, **kwargs)

logging.Logger.file = file

def init_logging():
    logger = logging.getLogger("DownEdit")
    if not logger.handlers:
        logger.config_log()
    return logger

# Initialize the logger
logger = init_logging()