from . import *

class SoftwareName(BaseModel):
    id = PrimaryKeyField()
    software_name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    description = TextField()
    software_type = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    software_class = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    research_area = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    research_discipline = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    