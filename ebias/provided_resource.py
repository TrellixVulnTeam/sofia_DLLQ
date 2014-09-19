import os

class ProvidedResource(object):
    def __init__(self, fname, type, name=None):
        self.fname = fname
        self.type = type
        self.name = os.path.basename(fname) if name is None else name

    def __str__(self):
        return '%s;type=%s;%s'%(self.fname, self.type, self.name)
