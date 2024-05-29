from . import *

class Links(BaseModel):
    id = PrimaryKeyField()
    website_links = CharField(max_length=500)
    documents = CharField(max_length=500)
    examples = CharField(max_length=500)
    area_specific = CharField(max_length=500)
    containers = CharField(max_length=500)
    rp_documents = CharField(max_length=500)
