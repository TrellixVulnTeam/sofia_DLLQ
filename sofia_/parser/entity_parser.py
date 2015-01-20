import re

from requested_entity import RequestedEntity


class EntityParser(object):
    """ A parser for entity requests.
        
    The entity request takes the form of:
        <entity_request> ::= <entity>[:<attribute>[:<attribute>]*]
        <attribute> ::= <key>=<value>[,<value>]*

    where
        <entity>
            is the name of an entity
        <key>
            is the name of an attribute
        <value>
            is the value of an attribute

    Command line examples:
        -e chromosome_id position
        -e gene_id:resource=gencode.gtf,gene_id=ensemble
    """

    REGX = re.compile(r'(?P<entity>[^:]+)(?P<attributes>.+)?')
    
    def __init__(self, provided_resources):
        """ Initialise the ActionParser with a list of resources that the user
        has provided. """
        self.provided_resources = provided_resources

    def parse_entity_requests(self, entity_requests):
        """ Parse all entity requests in a list.

        :param entity_requests: a list of entity request strings
        :return: a list of RequestedEntities
        """
        return [self.parse_entity_request(entity_request) for entity_request in
                entity_requests if entity_request.strip() != '']
    
    def parse_entity_request(self, entity_request):
        """ Parse a single entity request.

        :param entity_request: an entity request string
        :return: a RequestedEntity
        """
        match = self.REGX.match(entity_request)
        if match is None:
            raise ValueError('Unrecognised entity request.')
        entity = match.group('entity')
        attributes = {} if match.group('attributes') is None else\
            {k: sorted(v.split(',')) for k, v in
             (part.split('=', 1) for part in match.group('attributes').split(':'))}
        resources = self._get_resource(attributes['resources']) if 'resources' in attributes else\
            frozenset()
        return RequestedEntity(entity, attributes, resources)
    
    def _get_resources(self, resources, entity):
        """ Parse a resource from the action string and check if any requested
        resources have been provided by the user. """
        try:
            return frozenset(self.provided_resources[r] for r in resources)
        except KeyError, e:
            raise KeyError('Resource "{}" requested by action "{}" not provided.'.format(e.args[0], entity))