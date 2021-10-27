class ReadToGenomeDynamicAlignmentTasks():

    def __init__(self):
        self.state = 'ACTIVE'

    def execute(self, readToGenomeDynamicAlignmentMatrix, metadata):
        startPosition = self._findTracebackStartIndex(readToGenomeDynamicAlignmentMatrix)
        return self._tracebackToOriginColumnFromStartIndex(readToGenomeDynamicAlignmentMatrix, startPosition)

    def _findTracebackStartIndex(self, readToGenomeDynamicAlignmentMatrix):
        scoreMatrix = readToGenomeDynamicAlignmentMatrix.getScoreMatrix()
        finalRowIndex = readToGenomeDynamicAlignmentMatrix.getNumberRows() - 1
        maxValue = -999999999999
        maxValueIndices = []
        for j in range(readToGenomeDynamicAlignmentMatrix.getNumberColumns()):
            if scoreMatrix[finalRowIndex][j] > maxValue:
                maxValue = scoreMatrix[finalRowIndex][j]
                maxValueIndices = [(finalRowIndex, j)]
            elif scoreMatrix[finalRowIndex][j] == maxValue:
                maxValueIndices.append((finalRowIndex, j))

        highestLexicographicalIndex = maxValueIndices[0]
        if len(maxValueIndices) > 1:
            for indexTupleIndex in range(1, len(maxValueIndices)):
                if maxValueIndices[indexTupleIndex] > highestLexicographicalIndex:
                    highestLexicographicalIndex = maxValueIndices[indexTupleIndex]
        return highestLexicographicalIndex

    def _tracebackToOriginColumnFromStartIndex(self, readToGenomeDynamicAlignmentMatrix, startPosition):
        
        # print("Start Position: ", startPosition)
        scoreMatrix = readToGenomeDynamicAlignmentMatrix.getScoreMatrix()
        # print("Score Matrix: ", scoreMatrix)
        
        tracebackPointerMatrix = readToGenomeDynamicAlignmentMatrix.getTracebackPointerMatrix()
        # print("Traceback Matrix: ",tracebackPointerMatrix)
        finalScore = scoreMatrix[startPosition[0]][startPosition[1]]

        # print("Final Score: ", finalScore)
        readString = readToGenomeDynamicAlignmentMatrix.getRowSequence()
        genomeString = readToGenomeDynamicAlignmentMatrix.getColumnSequence()

        currentRowIndex = startPosition[0]
        currentColumnIndex = startPosition[1]
        
        finalColumnIndex = currentColumnIndex
        readTracebackString = ''
        genomeTracebackString = ''
        # print()
        continueLooping = True

        while continueLooping:

            if currentRowIndex == 0:
                continueLooping = False
                print("Recursion Ending")
                break

            # print("Current Row: ", currentRowIndex)
            # print("Current Column: ", currentColumnIndex)
            nextPositionList = tracebackPointerMatrix[currentRowIndex][currentColumnIndex]
            # print("Next Position List: ", nextPositionList)
            nextPosition = nextPositionList[0]
            if len(nextPositionList) > 1:
                for position in nextPositionList:
                    if position > nextPosition:
                        nextPosition = position

            # print("Next Chosen Position: ", nextPosition)

            if currentRowIndex - nextPosition[0] == 1:
                if currentColumnIndex - nextPosition[1] == 1:
                    readTracebackString = readTracebackString + readString[currentRowIndex-1]
                    genomeTracebackString = genomeTracebackString + genomeString[currentColumnIndex-1]

                else:
                    readTracebackString = readTracebackString + readString[currentRowIndex-1]
                    genomeTracebackString = genomeTracebackString + '-'

            else:
                if currentColumnIndex - nextPosition[1] == 1:
                    readTracebackString = readTracebackString + '-'
                    genomeTracebackString = genomeTracebackString + genomeString[currentColumnIndex-1]

                else:
                    numberSkipCharacters = currentColumnIndex - nextPosition[1]
                    readTracebackString = readTracebackString + ('=' * numberSkipCharacters)
                    addonString = genomeString[nextPosition[1]:currentColumnIndex]
                    genomeTracebackString = genomeTracebackString + addonString[::-1]
            
            currentRowIndex = nextPosition[0]
            currentColumnIndex = nextPosition[1]
        
        return ([readTracebackString[::-1], genomeTracebackString[::-1]], finalScore, currentColumnIndex + 1)