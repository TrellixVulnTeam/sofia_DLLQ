from lhc.indices.index import Index


class KeyIndex(Index):
    
    RETURN = 'single'
    TYPE = 'exact'
    
    def __init__(self):
        self.index = {}
    
    def __contains__(self, key):
        return key in self.index
    
    def __getitem__(self, key):
        return self.index[key]
    
    def __setitem__(self, key, value):
        self.index[key] = value