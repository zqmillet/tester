class TestStepQueue(set):
    def pop(self):
        teststeps = {teststep for teststep in self if teststep.start()}
        self.difference_update(teststeps)
        return teststeps
