from application_driver.helper_modules import fasta

class FileUtils:

    def __init__(self):
        self._state = 'ACTIVE'

    def readFastaFile(self, filePath):
        return fasta.read_sequences_from_fasta_file(filePath)

    def getReadsFromFastaFileContentsAsList(self, fileContents):
        readList = []
        for line in fileContents:
            readList.append(line[1])
        return readList

    def getLabelsFromFastaFileContentsAsList(self, fileContents):
        labelList = []
        for line in fileContents:
            labelList.append(line[0])
        return labelList