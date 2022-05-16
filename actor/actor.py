class ActorExample:

    def __init__(self):
        self.param1 = None
        self.param2 = None

def get(actor):
    return actor

def update(actor, param1=None, param2=None):
    if param1 is not None:
        actor.param1 = param1
    if param2 is not None:
        actor.param2 = param2
    return actor
