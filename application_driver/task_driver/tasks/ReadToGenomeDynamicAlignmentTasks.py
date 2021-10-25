class ReadToGenomeDynamicAlignmentTasks():

    def __init__(self):
        self.state = 'ACTIVE'

    def execute(self, readToGenomeDynamicAlignmentMatrix, metadata):
        startPosition = self._findTracebackStartIndex(readToGenomeDynamicAlignmentMatrix)
        return self._tracebackToOriginColumnFromStartIndex(readToGenomeDynamicAlignmentMatrix, startPosition)

    def _findTracebackStartIndex(self, readToGenomeDynamicAlignmentMatrix)
        scoreMatrix = readToGenomeDynamicAlignmentMatrix.getScoreMatrix()
        finalRowIndex = readToGenomeDynamicAlignmentMatrix.getNumberRows
        
        maxValue = -999999999999
        maxValueIndices = []
        for j in range(readToGenomeDynamicAlignmentMatrix.getNumbercolumns()):
            if scoreMatrix[finalRowIndex][j] > maxValue:
                maxValuue = scoreMatrix[finalRowIndex][j]
                maxValueIndices = [tuple(finalRowIndex, j)]
            elif scoreMatrix[finalRowIndex][j] == maxValue:
                maxValueIndices.append(tuple(finalRowIndex, j))

        if len(maxValueIndices) > 1:
            highestLexicographicalIndex = maxValueIndices[0]
            for indexTupleIndex in range(1, len(maxValueIndices)):
                if maxValueIndices[indexTupleIndex] > highestLexicographicalIndex:
                    highestLexicographicalIndex = maxValueIndices[indexTupleIndex]
        
        return highestLexicographicalIndex

    def _tracebackToOriginColumnFromStartIndex(self, readToGenomeDynamicAlignmentMatrix, startPosition)
        scoreMatrix = readToGenomeDynamicAlignmentMatrix.getScoreMatrix()
        tracebackPointerMatrix = readToGenomeDynamicAlignmentMatrix.getTracebackPointerMatrix()
        finalScore = scoreMatrix[startPosition[0]][startPosition[1]]

        readString = readToGenomeDynamicAlignmentMatrix.getRowSequence()
        genomeString = readToGenomeDynamicAlignmentMatrix.getColumnSequence()

        currentRowIndex = startPosition[0]
        currentColumnIndex = startPosition[1]
        readTracebackString = ''
        genomeTracebackString = ''

        continueLooping = True
        while continueLooping:
            nextPositionList = tracebackPointerMatrix[currentRowIndex][currentColumnIndex]

            nextPosition = nextPositionList[0]
            if len(nextPositionList) > 1:
                for position in nextPositionList:
                    if position > nextPosition:
                        nextPosition = position

            if currentRowIndex - nextPosition[0] == 1
                if currentColumnIndex - nextPosition[1] == 1:
                    readTracebackString = readTracebackString + readString[currentRowIndex-1]
                    genomeTracebackString = genomeTracebackString + genomeString[currentColumnIndex-1]

                else:
                    readTracebackString = readTracebackString + readString[currentRowIndex-1]
                    genomeTracebackString = genomeTracebackString + '-'

            else:
                if currentColumnIndex - nextPosition == 1:
                    readTracebackString = readTracebackString + '-'
                    genomeTracebackString = genomeTracebackString + genomeString[currentColumnIndex-1]
                else:
                    numberSkipCharacters = currentColumnIndex - nextPosition
                    readTracebackString = readTracebackString + ('=' * numberSkipCharacters)
                    genomeTracebackString = genomeTracebackString + genomeString[nextPosition-1:currentColumnIndex]
            
            currentRowIndex = nextPosition[0]
            currentColumnIndex = nextPosition[1]

            if currentRowIndex == 0:
                continueLooping = False

        return tuple([readTracebackString[::-1], genomeTracebackString[::-1]], finalScore, startPosition[1])
