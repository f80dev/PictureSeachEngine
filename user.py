class User(object):
    def __init__(self, obj:dict):
        self.id = obj["id"]
        self.username = obj["username"]
        self.password = obj["password"]

    def __str__(self):
        return "User(id='%s')" % self.id
