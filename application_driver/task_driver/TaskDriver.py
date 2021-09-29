from application_driver.task_driver.tasks.VariantIdentificationTasks import VariantIdentificationTasks
from application_driver.task_driver.tasks.GreedyHamiltonianPathTasks import GreedyHamiltonianPathTasks

class TaskDriver():

    GREEDY_HAMILTONIAN_PATH = 'GREEDY_HAMILTONIAN_PATH'
    VARIANT_IDENTIFICATION = 'VARIANT_IDENTIFICATION'

    def __init__(self):
        self._state = 'ACTIVE'

    def execute(self, applicationType, dataStructure, metadata = None):
        if (applicationType == self.GREEDY_HAMILTONIAN_PATH):
            return self._executeGreedyHamiltonianPathTasks(dataStructure)
        elif (applicationType == self.VARIANT_IDENTIFICATION):
            return self._executeVariantIdentificationTasks(dataStructure, metadata)
        else:
            return "INVALID_APPLICATION_TYPE"

    def _executeGreedyHamiltonianPathTasks(self, dataStructure):
        greedyHamiltonianPathTasks = GreedyHamiltonianPathTasks()
        return greedyHamiltonianPathTasks.execute(dataStructure)

    def _executeVariantIdentificationTasks(self, dataStructure, metadata):
        variantIdentificationTasks = VariantIdentificationTasks()
        return variantIdentificationTasks.execute(dataStructure, metadata)