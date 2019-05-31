class EventHandler:

    def __init__(self, stream):
        self.stream = stream
        pass

    def terminate_program:
        if self.stream.is_active():
            self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        QtCore.QCoreApplication.quit()



