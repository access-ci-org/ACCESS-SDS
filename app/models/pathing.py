from . import *

class Pathing(BaseModel):
    id = PrimaryKeyField()
    pathing = CharField(max_length=500)