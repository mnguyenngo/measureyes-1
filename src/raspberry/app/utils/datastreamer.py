

class DataReader():
    def init(self, api_url=None):
        if api_url is None:
            self.api_url = """
                https://hidden-lowlands-41791.herokuapp.com/responses/1"""
