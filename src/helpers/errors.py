class RedisConnectionError(Exception):
    def __init__(self, host, port, error):
        super().__init__(f"Failed to connect to redis at host: {host}, port: {port}. {error}")
        self.host = host
        self.port = port


class QueryGeneratorError(Exception):
    def __init__(self, error):
        super().__init__(f"An unexpected error occurred: {error}.")
