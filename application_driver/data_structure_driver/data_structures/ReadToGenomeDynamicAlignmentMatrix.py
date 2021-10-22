from application_driver.data_structure_driver.data_structures.base_data_structures.SequenceAlignment2DMatrix import SequenceAlignment2DMatrix

class ReadToGenomeDynamicAlignmentMatrix(SequenceAlignment2DMatrix):

    def __init__(self, sequenceOne, sequenceTwo, metadata):
        super().__init__(sequenceOne, sequenceTwo, metadata)
        
    def _initialize(self, metadata = None):
        
        ''' 
            ∀ i > 0, M(i,0) = s × i
            ∀ j ≥ 0, M(0,j) = 0 
        '''
        
        self.tracebackPointers = [ [ [ None ] ] * self.numColumns for i in range(self.numRows)]
        space_score = metadata['space_score']
        for i in range(1, self.numRows):
            self.matrix[i][0] = i * space_score
            self.tracebackPointers[i][0] = [tuple(i-1, 0)]
        for j in range(self.numColumns):
            self.matrix[0][j] = 0
            self.tracebackPointers[0][j] = [tuple(0, j-1)]

    def _recur(self, metadata = None):
        
        '''
            The dynamic programming recurrence for this task is:

            M(i,j) = max {
                
                M(i−1,j−1) + S(xi,yj)
                M(i−1,j) + s
                M(i,j−1) + s
                max { (k,ℓ) ∈ R : ℓ = j } M(i,k−1) + r

            }
 
            where the  max  in the fourth case (the "skip" case) is taken 
            over all skip intervals in R that have end position equal to j.
            This fourth case is not considered for positions in the genome that 
            are not the end of any skip interval in R .
        '''

        substitution_matrix = metadata['substitution_matrix']
        space_score = metadata['space_score']
        skip_score = metadata['skip_score']
        skip_intervals = metadata['skip_intervals']

        for i in range(1, self.numRows):
            rowCharacter = self.rowSequence[i-1]

            for j in range(1, self.numColumns):
                columnCharacter = self.columnSequence[j-1]

                auntValue = self.matrix[i-1][j-1] + substitution_matrix[(rowCharacter, columnCharacter)]
                parentValue = self.matrix[i-1][j] + space_score
                siblingValue = self.matrix[i][j-1] + space_score

                maxSkipIntervalScore = -999999999999
                maxSkipIntervalIndex = -1
                for skipInterval in skip_intervals:
                    if skipInterval[1] == j:
                        curIndex = skipInterval[0] - 1
                        curScore = self.matrix[i][curIndex] + skip_score
                        if curScore > maxSkipIntervalScore:
                            maxSkipIntervalScore = curScore
                            maxSkipIntervalIndex = curIndex

                maximumValue = auntValue
                tracebackPositionList = [tuple(i-1, j-1)]

                if parentValue > maximumValue:
                    maximumValue = parentValue
                    traceBackPositionList = [tuple(i-1, j)]
                elif parentValue == maximumValue:
                    tracebackPositionList.append(tuple(i-1, j))

                if siblingValue > maximumValue:
                    maximumValue = siblingValue
                    traceBackPositionList = [tuple(i, j-1)]
                elif siblingValue == maximumValue:
                    tracebackPositionList.append(tuple(i, j-1))

                if maxSkipIntervalScore > maximumValue:
                    maximumValue = maxSkipIntervalScore
                    traceBackPositionList = [tuple(i, maxSkipIntervalIndex)]
                elif maxSkipIntervalScore == maximumValue:
                    tracebackPositionList.append(tupule(i, maxSkipIntervalIndex))

                self.tracebackPointers[i][j] = tracebackPositionList

    def getScoreMatrix(self):
        return self.matrix

    def getTracebackPointerMatrix(self):
        return self.tracebackPointers