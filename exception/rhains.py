import traceback
import sys




class RhainsExceptionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
        self.exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)[-1]
        
        self.filename = tb.filename
        self.lineno = tb.lineno
        self.name = tb.name
        self.text = tb.line
    
    def __str__(self) -> str:
        return f"""
            ====== Rhains Exception Error ======
            ====================================
            
            file:       {self.filename}
            function:   {self.name}
            line:       {self.lineno}
            
            Error: {self.exc_type.__name__}
            ------------------------------------
            {self.text}
        """
