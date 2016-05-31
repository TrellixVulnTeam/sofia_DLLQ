from sofia.error_manager import ERROR_MANAGER
from sofia.workflow.entity_node import EntityNode
from sofia.entity_type import EntityType


class EntityResolver(object):
    def __init__(self, entity_type, template, provided_entities, maps={}, requested_resources=set(), visited=None):
        self.entity_type = entity_type
        self.template = template
        self.provided_entities = provided_entities
        self.maps = maps
        self.requested_resources = requested_resources

        self.visited = set() if visited is None else visited

    def __str__(self):
        return self.entity_type
    
    def __iter__(self):
        is_not_provided = True
        for provided_entity in self.provided_entities:
            if provided_entity.name == self.entity_type:
                is_not_provided = False
                yield EntityNode(provided_entity)

        step_names = self.template.get_children(self.entity_type)
        if len(step_names) == 0 and is_not_provided:
            ERROR_MANAGER.add_error('No steps produce {}'.format(self.entity_type))

        from step_resolver import StepResolver
        for step_name in step_names:
            if step_name in self.visited:
                continue
            step = self.template.steps[step_name]
            it = StepResolver(step,
                              self.template,
                              self.provided_entities,
                              self.maps,
                              self.requested_resources,
                              set(self.visited))
            for step_node in it:
                entity_type = EntityType(self.entity_type)
                entity_type.attributes = step_node.out_attributes[self.entity_type]
                entity_node = EntityNode(entity_type)
                entity_node.add_step_node(step_node)
                yield entity_node
