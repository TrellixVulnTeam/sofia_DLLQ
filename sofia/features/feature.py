from collections import defaultdict
from operator import and_
from sofia.entity import Entity
from sofia.error_manager import ERROR_MANAGER

class Feature(object):
    """ A feature that can be calculated from resources and other features. """
    
    IN = []
    OUT = []
    
    def __init__(self, resources=None, dependencies=None, param={}, ins=None, outs=None, converters={}):
        self.changed = True
        self.calculated = False
        self.resources = set() if resources is None else resources
        self.dependencies = {} if dependencies is None else dependencies
        self.param = param
        self.ins = {in_: in_ for in_ in self.IN} if ins is None else ins
        self.outs = {out: Entity(out) for out in self.OUT} if outs is None else outs
        self.name = self._getName()
        self.converters = converters
    
    def __str__(self):
        """ Return the name of the feature based on it's resources and
        arguments. """
        return self.name
    
    def init(self):
        """ Initialise the feature.

        When overridden, this function can be passed arguments that are parsed
        from the command line.
        """
        pass
    
    def calculate(self, **kwargs):
        """Calculate this feature
        
        Assumes dependencies are already resolved. This function must be
        overridden when implementing new features.
        
        :param dict entities: currently calculated entities. The target is at
            entities['target'].
        """
        raise NotImplementedError('You must override this function')

    def format(self, entity):
        """Convert entity produced by this feature to a string
        
        :param object entity: convert this entity
        """
        return str(entity)
    
    def generate(self, entities, features):
        """Generate a feature
        
        This function resolves all dependencies and then calculates the
        feature.
        
        :param dict entities: currently calculated entities
        :param features: available features
        :type features: dict of features
        """
        name = self.name
        if self.calculated:
            return entities[name]
        
        dependencies_changed = False
        for feature in self.dependencies.itervalues():
            features[feature].generate(entities, features)
            if features[feature].changed:
                dependencies_changed = True
        if not dependencies_changed and name in entities:
            self.calculated = True
            self.changed = False
            return entities[name]
        
        local_entities = {}
        for dependency_name, feature in self.dependencies.iteritems():
            local_entities[dependency_name] = entities[feature]
        for edge, converter in self.converters.iteritems():
            converter.convert(local_entities)
        res = self.calculate(**local_entities)
        self.calculated = True
        self.changed = not (name in entities and entities[name] is res)
        entities[name] = res
        return res
    
    def reset(self, features):
        """ Resets the calculation status of this feature and all dependencies 
        to False.
        """
        self.calculated = False
        for feature in self.dependencies.itervalues():
            features[feature].reset(features)
    
    def getAttributes(self):
        res = {}
        for out in self.outs.itervalues():
            res.update(out.attr)
        return res
    
    def _getName(self):
        """ Return the name of the feature based on it's resources and
        arguments. """
        name = [type(self).__name__]
        if len(self.resources) != 0:
            tmp = ','.join(resource.name for resource in self.resources\
                if resource.name != 'target')
            if len(tmp) > 0:
                name.append('-r ' + tmp)
        if len(self.param) != 0:
            tmp = ','.join('%s=%s'%e for e in self.param.iteritems())
            name.append('-p ' + tmp)
        if len(self.outs) != 0:
            tmp = []
            for entity in self.outs.itervalues():
                tmp.extend((k, v) for k, v in entity.attr.iteritems()\
                    if v is not None)
            tmp = ','.join('%s=%s'%e for e in tmp)
            if len(tmp) > 0:
                name.append('-a ' + tmp)
        return '\\n'.join(name)
    
    @classmethod
    def getOutput(cls, ins={}, outs={}, requested_attr={}):
        """ Determine the attributes of the outputs

        Given the provided and requested attributes, determine the output
        attributes.
        """
        #TODO use the entity graph to return proper entities with attributes
        # Check that input entity attributes match
        common_attr_names = set.intersection(*[set(entity.attr) for entity in ins.itervalues()])
        for name in common_attr_names:
            common_attr = set()
            for entity in ins.itervalues():
                common_attr.add(entity.attr[name])
            if len(common_attr) > 1:
                ERROR_MANAGER.addError('%s could not match %s attributes: %s'%\
                    (cls.__name__, name, ', '.join('(%s: %s)'%(k, v.attr[name]) for k, v in ins.iteritems())))
                return None
        
        # Yield the output entities
        out_attr = {}
        for entity in ins.itervalues():
            out_attr.update(entity.attr)
        outs = {out: Entity(out, out_attr) for out in outs}
        return outs
        #return {out: ENTITY_FACTORY.makeEntity(out, attr) for out in outs}
