from modules.feature import Feature
from resource import DynamicResource

class Position(Feature):
    
    NAME = 'pos'
    RESOURCES = ['locus']
    DEPENDENCIES = [
        {'name': 'locus',
         'feature': DynamicResource,
         'resource_map': {'name': 'locus'}
        }
    ]
    
    def calculate(self, locus):
        if hasattr(locus, 'pos'):
            return locus.pos
        elif hasattr(locus, 'start'):
            return locus.start
        msg = 'Can not extract position feature from type: {type}'
        raise TypeError(msg.format(type=type(locus)))