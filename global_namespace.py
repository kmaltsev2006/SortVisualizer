class Status:
    
    def __init__(self):
        self.interrupted = False
        self.completed = False
        self.interrupt_time = -1
        self.reset_time = 0


sessions = [Status()]
session_number = 0
mode = None