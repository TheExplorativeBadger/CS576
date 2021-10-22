class SequenceAlignment2DMatrix:

    def __init__(self, sequenceOne, sequenceTwo, metadata = None):
        self.rowSequence = sequenceOne
        self.columnSequence = sequenceTwo
        self.numRows = len(sequenceOne) + 1
        self.numColumns = len(sequenceTwo) + 1
        self.matrix = [[None] * self.numColumns for i in range(self.numRows)]

        self._build(metadata)

    def _build(self, metadata = None):
        self._initialize(metadata)
        self._recur(metadata)
        
    def _initialize(self, metadata = None):
        ''' Provides a default initialization of 0s in first row and column'''
        for i in range(self.numRows):
            self.matrix[i][0] = 0
        for j in range(self.numColumns):
            self.matrix[0][j] = 0
    
    def _recur(self, metadata = None):
        ''' Provides a default single pass to fill the matrix with 0s'''
        for i in range(1, self.numRows):
            for j in range(1, self.numColumns):
                self.matrix[i][j] = 0