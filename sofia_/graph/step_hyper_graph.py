from lhc.graph import HyperGraph


class StepHyperGraph(HyperGraph):
    """ A hyper graph of all the possible step calculation pathways. """
    def __init__(self, entity_graph):
        super(StepHyperGraph, self).__init__()
        self.steps = dict()
        self.entity_graph = entity_graph

    @property
    def entities(self):
        return self.vs

    def registed_entity(self, entity):
        self.add_vertex(entity)

    def register_step(self, step):
        """ Add an step to the hyper graph.

        :param step: The step to add to the graph.
        """
        self.steps[step.name] = step

        for in_ in step.ins:
            self.add_outward_edge(in_, step.name)

        for out in step.outs:
            self.add_inward_edge(out, step.name)