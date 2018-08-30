from Response import ResponseBase


class EeveeResponse(ResponseBase):
    def __init__(self, eevee, connection, cooldown=10):
        super(EeveeResponse, self).__init__(cooldown)
        self.eevee = eevee
        self.connection = connection
        return

    def respond(self, message):
        self.eevee.ChangeHappiness(20)
        s = r"I'm so happy " + str(self.eevee.Happiness)
        self.connection.send_message(s)
        return
