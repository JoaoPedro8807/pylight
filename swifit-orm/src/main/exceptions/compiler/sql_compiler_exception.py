class SqlCompilerException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    
    #implmentar o rollback ou algo do tipo

    def __str__(self):
        return self.message