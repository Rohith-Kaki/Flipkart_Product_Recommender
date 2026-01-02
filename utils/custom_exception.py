import sys

class CustomException(Exception):
    def __init__(self, message:str, error_detail:Exception = None):
        self.error_message = self.get_error_message(message=message, error_detail=error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_error_message(self, message, error_detail):
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "UnKnow"
        line_number = exc_tb.tb_frame.f_lineno if exc_tb else "UnKnow"
        return f"{message} | Error: {error_detail} | File: {file_name} | line: {line_number}"
    
    def __str__(self):
        return self.error_message