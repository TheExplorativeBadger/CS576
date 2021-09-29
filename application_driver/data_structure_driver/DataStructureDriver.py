from application_driver.data_structure_driver.data_structures.GreedyHamiltonianPathDirectedGraph import GreedyHamiltonianPathDirectedGraph

class DataStructureDriver():

    GREEDY_HAMILTONIAN_PATH = 'GREEDY_HAMILTONIAN_PATH'

    def __init__(self):
        self._state = 'ACTIVE'

    def buildApplicationDataStructure(self, applicationType, sourceData):
        if (applicationType == self.GREEDY_HAMILTONIAN_PATH):
            return self._buildGreedyHamiltonianPathGraph(sourceData)
        else:
            return "INVALID_APPLICATION_TYPE"

    def _buildGreedyHamiltonianPathGraph(self, sourceData):
        reads = sourceData['reads']
        min_overlap = sourceData['min_overlap']
        return GreedyHamiltonianPathDirectedGraph(reads, min_overlap)