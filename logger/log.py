from ordered_enum import OrderedEnum


class LogLevels(OrderedEnum):
    """Inherits from OrderedEnum to order the Loglevels 
    from lowest to highest precedence

    Order is:
    - debug
    - info
    - warning
    - error
    """
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


class Log:
    """Logger class to print messages based off the log level set
    Will print if Log is active

    Calling Log at a log level will also log messages from log levels exceeding the set one. 

    For example: logging debug would log debug, info, warning and error. While, logging warning would only log warning and error. 

    """
    log_level = LogLevels.INFO
    is_active = False

    @classmethod
    def print_console(cls, msg: str) -> None:
        """print message in the console if log is active

        Args:
            msg (str): the message to print
        """
        if cls.is_active:
            print(msg)

    @classmethod
    def debug(cls, msg: str) -> None:
        """print debug messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.DEBUG:
            cls.print_console(f'[DEBUG] {msg}')

    @classmethod
    def info(cls, msg: str) -> None:
        """print info messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.INFO:
            cls.print_console(f'[INFO] {msg}')

    @classmethod
    def warning(cls, msg: str) -> None:
        """print warning messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.WARNING:
            cls.print_console(f'[WARNING] {msg}')

    @classmethod
    def error(cls, msg: str) -> None:
        """print debug messages is the log level is equal or lower to itself 

        Args:
            msg (str): the message to print
        """
        if cls.log_level <= LogLevels.ERROR:
            cls.print_console(f'[ERROR] {msg}')
