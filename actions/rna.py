from sofia_.action import Resource, Target


class RnaIterator(Target):

    EXT = ['.rna']
    TYPE = 'rna_structure'
    OUT = ['rna_structure_iterator']

    def init(self):
        self.parser = None


class RnaSet(Target):

    EXT = ['.rna']
    TYPE = 'rna_structure'
    OUT = ['rna_structure_set']

    def init(self):
        self.parser = None