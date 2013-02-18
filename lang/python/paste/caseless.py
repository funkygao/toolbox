class Caseless:

    def __init__(self, global_config):
        self.config = global_config

    def __call__(self, app):
        return app
    
