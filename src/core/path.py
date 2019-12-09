#TODO check if path exist

class Path(object):
    def __init__(self, server="None", local=None):
        self.local = None
        self._local = local
        self.server = server
        

    def __setattr__(self, name, value):
        if name == "local":
            object.__setattr__(self, "_local", value)
        else:
            object.__setattr__(self, name, value)


    def __getattribute__(self, name):
        if name == "local":
            if self._local == None:
                return object.__getattribute__(self, "server")
            else:
                return object.__getattribute__(self, "_local")
        else:
            return object.__getattribute__(self, name)

