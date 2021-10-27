from application_driver.task_driver.tasks.VariantIdentificationTasks import VariantIdentificationTasks
from application_driver.task_driver.tasks.GreedyHamiltonianPathTasks import GreedyHamiltonianPathTasks
from application_driver.task_driver.tasks.ReadToGenomeDynamicAlignmentTasks import ReadToGenomeDynamicAlignmentTasks
from application_driver.task_driver.tasks.SubgenomicRNAVariantIdentificationTasks import SubgenomicRNAVariantIdentificationTasks

class TaskDriver():

    GREEDY_HAMILTONIAN_PATH = 'GREEDY_HAMILTONIAN_PATH'
    VARIANT_IDENTIFICATION = 'VARIANT_IDENTIFICATION'
    READ_TO_GENOME_DYNAMIC_ALIGNMENT_SKIPS = 'READ_TO_GENOME_DYNAMIC_ALIGNMENT_SKIPS'
    SUBGENOMIC_RNA_VARIANT_IDENTIFICATION = 'SUBGENOMIC_RNA_VARIANT_IDENTIFICATION'

    def __init__(self):
        self._state = 'ACTIVE'

    def getTestString(self):
        return 'Hello from Task Driver'

    def execute(self, applicationType, dataStructure, metadata = None):
        if (applicationType == self.GREEDY_HAMILTONIAN_PATH):
            return self._executeGreedyHamiltonianPathTasks(dataStructure, metadata)
        elif (applicationType == self.VARIANT_IDENTIFICATION):
            return self._executeVariantIdentificationTasks(dataStructure, metadata)
        elif (applicationType == self.READ_TO_GENOME_DYNAMIC_ALIGNMENT_SKIPS):
            return self._executeReadToGenomeDynamicAlignmentTasks(dataStructure, metadata)
        elif (applicationType == self.SUBGENOMIC_RNA_VARIANT_IDENTIFICATION):
            return self._executeSubgenomicRNAVariantIdentificationTasks(dataStructure, metadata)
        else:
            return 'INVALID_APPLICATION_TYPE'

    def _executeGreedyHamiltonianPathTasks(self, dataStructure, metadata = None):
        greedyHamiltonianPathTasks = GreedyHamiltonianPathTasks()
        return greedyHamiltonianPathTasks.execute(dataStructure)

    def _executeVariantIdentificationTasks(self, dataStructure, metadata = None):
        variantIdentificationTasks = VariantIdentificationTasks()
        return variantIdentificationTasks.execute(dataStructure, metadata)

    def _executeReadToGenomeDynamicAlignmentTasks(self, dataStructure, metadata = None):
        readToGenomeDynamicAlignmentTasks = ReadToGenomeDynamicAlignmentTasks()
        return readToGenomeDynamicAlignmentTasks.execute(dataStructure, metadata)

    def _executeSubgenomicRNAVariantIdentificationTasks(self, dataStructure, metadata = None):
        subgenomicRNAVariantIdentificationTasks = SubgenomicRNAVariantIdentificationTasks()
        return subgenomicRNAVariantIdentificationTasks.execute(dataStructure, metadata)