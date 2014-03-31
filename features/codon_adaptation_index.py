from modules.feature import Feature
from modules.resource import Resource
from codon_usage_table import CodonUsageTable

class CodonAdaptationIndex(Feature):
    
    NAME = 'cai'
    RESOURCES = ['cut', 'seq', 'mdl']
    DEPENDENCIES = [
        {'name': 'cut1',
         'feature': Resource,
         'resource_map': {'name': 'cut'}
        },
        {'name': 'cut2',
         'feature': CodonUsageTable,
         'resource_map': {'seq': 'seq', 'mdl': 'mdl'}
        }
    ]
    
    def calculate(self, cut1, cut2):
        return cai(cut1, cut2)
