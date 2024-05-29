from . import *

class SoftwareName(BaseModel):
    id = PrimaryKeyField()
    software_name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    rp_software = CharField(constraints=[SQL('COLLATE NOCASE')])
    description = TextField()
    software_type = CharField(constraints=[SQL('COLLATE NOCASE')])
    software_class = CharField(constraints=[SQL('COLLATE NOCASE')])
    research_area = CharField(constraints=[SQL('COLLATE NOCASE')])
    research_discipline = CharField(constraints=[SQL('COLLATE NOCASE')])
     