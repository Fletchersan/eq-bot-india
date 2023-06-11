class GenericError(Exception):
    "Something went wrong"
    def __init__(self, msg="Uh oh something went wrong!"):
        self.message = msg
        super().__init__(self.message)