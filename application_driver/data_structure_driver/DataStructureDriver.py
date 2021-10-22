from application_driver.data_structure_driver.data_structures.GreedyHamiltonianPathDirectedGraph import GreedyHamiltonianPathDirectedGraph
from application_driver.data_structure_driver.data_structures.ReadToGenomeDynamicAlignmentMatrix import ReadToGenomeDynamicAlignmentMatrix

class DataStructureDriver():

    GREEDY_HAMILTONIAN_PATH = 'GREEDY_HAMILTONIAN_PATH'
    READ_TO_GENOME_DYNAMIC_ALIGNMENT_SKIPS = 'READ_TO_GENOME_DYNAMIC_ALIGNMENT_SKIPS'

    def __init__(self):
        self._state = 'ACTIVE'

    def getTestString(self):
        return 'Hello from Data Structure Driver'

    def buildApplicationDataStructure(self, applicationType, sourceData):
        if (applicationType == self.GREEDY_HAMILTONIAN_PATH):
            return self._buildGreedyHamiltonianPathGraph(sourceData)
        elif (applicationType == self.READ_TO_GENOME_DYNAMIC_ALIGNMENT_SKIPS):
            return self._buildReadToGenomeDynamicAlignmentMatrix(sourceData)
        else:
            return 'INVALID_APPLICATION_TYPE'

    def _buildGreedyHamiltonianPathGraph(self, sourceData):
        reads = sourceData['reads']
        min_overlap = sourceData['min_overlap']
        return GreedyHamiltonianPathDirectedGraph(reads, min_overlap)

    def _buildReadToGenomeDynamicAlignmentMatrix(self, sourceData):
        read_sequence = sourceData['read_sequence']
        genome_sequence = sourceData['genome_sequence']

        metadata = {
            'substitution_matrix': sourceData['substitution_matrix'],
            'skip_intervals': sourceData['skip_intervals'],
            'space_score': sourceData['space_score'],
            'skip_score': sourceData['skip_score']
        }

        return ReadToGenomeDynamicAlignmentMatrix(read_sequence, genome_sequence, metadata)