class State(object):

    __slots__ = ('is_done', 'step', 'inputs', 'outputs', 'index')

    def __init__(self, step, inputs, outputs, index):
        self.is_done = False

        self.step = step
        self.inputs = inputs
        self.outputs = outputs
        self.index = index

    def run(self):
        self.is_done = self.step.run(self.inputs, self.outputs)

    def can_run(self):
        return not self.has_ended() and (not self.is_done or all(in_.is_readable() for in_ in self.inputs.itervalues()))

    def has_ended(self):
        return all(out.has_ended for out in self.outputs.itervalues())

    def get_user_warnings(self):
        return self.step.get_user_warnings()

    def __getstate__(self):
        return self.is_done, self.step, self.inputs, self.outputs, self.index

    def __setstate__(self, state):
        self.is_done, self.step, self.inputs, self.outputs, self.index = state
