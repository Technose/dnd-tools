class Logger:
    def __init__(self, isVerbose) -> None:
        self.isVerbose = isVerbose
        

    def Write(self, message):
        print(message)

    def Debug(self, message):
        if self.isVerbose:
            print(f"Debug: {message}")

    def Error(self, message):
        print(f"Error: {message}")