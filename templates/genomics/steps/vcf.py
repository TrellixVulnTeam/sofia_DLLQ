import gzip

from lhc.collections.inorder_access_set import InOrderAccessSet
from lhc.io.vcf.iterator import VcfEntryIterator
from lhc.io.vcf.tools.split_alt import _split_variant

from sofia.step import Resource, Target


class VcfIterator(Target):
    
    EXT = {'.vcf', '.vcf.gz'}
    FORMAT = 'vcf_file'
    OUT = ['variant']
    
    def get_interface(self, filename):
        self.variants = []
        fileobj = gzip.open(filename) if filename.endswith('.gz') else open(filename)
        return iter(VcfEntryIterator(fileobj))

    def calculate(self):
        if len(self.variants) == 0:
            self.variants = _split_variant(self.interface.next())
        return self.variants.pop()


class VcfSet(Resource):
    """A set of variants parsed from a .vcf file
    """
    
    EXT = {'.vcf', '.vcf.gz'}
    FORMAT = 'vcf_file'
    OUT = ['variant_set']
    
    def get_interface(self, filename):
        fileobj = gzip.open(filename) if filename.endswith('.gz') else open(filename)
        return InOrderAccessSet(VcfEntryIterator(fileobj))
