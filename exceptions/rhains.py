# import traceback
# import platform
# import datetime
# import sys


class RhainsBaseException(Exception):
    def __init__(self, message="An error occurred"):
        super().__init__(message)
    #     self.message = message
    #     self.timestamp = datetime.datetime.now()
    #     self.timezone = datetime.datetime.now().astimezone().tzinfo
    #     self.system_info = platform.system()
    #     self.details = self._get_error_details()

    # def _get_error_details(self):
    #     exc_type, exc_value, exc_traceback = sys.exc_info()
    #     tb = traceback.extract_tb(exc_traceback)[-1]
    #     filename = tb.filename
    #     line_number = tb.lineno
    #     function_name = tb.name
    #     format_exc = ''.join(
    #         traceback.format_exception(exc_type, exc_value, exc_traceback)
    #     ).splitlines()[2:-1]
    #     return {
    #         "filename": filename,
    #         "line_number": line_number,
    #         "function_name": function_name,
    #         "exc_type": exc_type.__name__,
    #         "exc_value": str(exc_value),
    #         'traceback': '\n' + '\n'.join(format_exc),
    #     }

    # def __str__(self):
    #     line = "=" * (len(self.__class__.__name__) + 8)
    #     return (f"\n=== {self.__class__.__name__} ===\n"
    #             f"{line}\n"
    #             f"Exception occurred:\n"
    #             f"Message: {self.message}\n"
    #             f"File: {self.details['filename']}\n"
    #             f"Line: {self.details['line_number']}\n"
    #             f"Function: {self.details['function_name']}\n"
    #             # f"Error Type: {self.details['exc_type']}\n"
    #             f"Error Value: {self.details['exc_value']}\n"
    #             f"Timestamp: {self.timestamp} {self.timezone}\n"
    #             f"Traceback: {self.details['traceback']}\n"
    #             f"System: {self.system_info}\n"
    #             f"{line}\n"
    #             )
