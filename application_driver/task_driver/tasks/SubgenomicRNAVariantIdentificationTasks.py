class SubgenomicRNAVariantIdentificationTasks():

    def __init__(self):
        self.state = 'ACTIVE'

    def execute(self, readAlignmentDict, metadata):
        variantSkipLengths = metadata['variant_length_dict']
        responseObject = {
            'MAXIMUM_MATCHES': len(readAlignmentDict)
        }
 
        for key in variantSkipLengths:
            responseSubObject = {
                'variant': key,
                'matches': 0
            }
            responseObject[key] = responseSubObject
        
        for key in readAlignmentDict:
            currentReadAlignment = readAlignmentDict[key][0][0]
            matchedVariant = self._identifyAmongVariants(currentReadAlignment, variantSkipLengths)
            if (matchedVariant):
                responseObject[matchedVariant]['matches'] += 1

        return self._formatFinalResponseObject(responseObject)

    def _identifyAmongVariants(self, alignedRead, variantSkipLengths):
        curNumSkipChars = self._countNumberSkipCharacters(alignedRead)
        for key in variantSkipLengths:
            if variantSkipLengths[key] == curNumSkipChars:
                return key
        return None
    
    def _countNumberSkipCharacters(self, alignedRead):
        counter = 0
        for char in alignedRead:
            if char == '=':
                counter += 1
        return counter
    
    def _formatFinalResponseObject(self, responseObject):
        finalResponseObject = {
            'MAXIMUM_MATCHES': responseObject['MAXIMUM_MATCHES']
        }

        for key in responseObject:
            if key == 'MAXIMUM_MATCHES':
                pass
            else:
                finalResponseObject[key] = {
                    'Variant_Matches': responseObject[key]['matches']
                }
        finalResponseObject['MOST_PREVELANT_VARIANT'] = self._findMostPrevelantVariant(finalResponseObject)
        return finalResponseObject
    
    def _findMostPrevelantVariant(self, responseObject):
        maxMatches = 0
        maxMatchVariant = ''
        for key in responseObject:
            if key == 'MAXIMUM_MATCHES':
                pass
            else:
                curMatches = responseObject[key]['Variant_Matches']
                if curMatches > maxMatches:
                    maxMatches = curMatches
                    maxMatchVariant = key
                    
        returnObject = {
            'Variant': maxMatchVariant,
            'Matches': maxMatches
        }
        return returnObject
