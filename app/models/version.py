class Version(object):
    def __init__(self,name="None", version="0.0"):
        self.name=name
        self.version=version
        
    @staticmethod
    def from_dict(source):
        return Version(name=source["name"],version=source["version"])
    
    def to_dict(self):
        return {"name" : self.name, "version" : self.version}