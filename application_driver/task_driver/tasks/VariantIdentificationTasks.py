from application_driver.helper_modules import shortestSuperstring

class VariantIdentificationTasks:

    def __init__(self):
        self.state = 'ACTIVE'

    def execute(self, dataStructure, metadata):
        variantLabels = metadata['known_variant_labels']
        responseObject = {
            'MAXIMUM_MATCHES': len(dataStructure)
        }
        counter = 0
        for label in variantLabels:
            responseSubObject = {
                'variant': label,
                'matches': 0
            }
            responseObject[counter] = responseSubObject
            counter += 1

        for contigList in dataStructure:
            matchedVariantIndex = self._identifyAmongVariants(contigList[0], metadata)
            if (matchedVariantIndex > -1):
                responseObject[matchedVariantIndex]['matches'] += 1

        return self._formatFinalResponseObject(responseObject, counter)

    def _identifyAmongVariants(self, unkownContig, metadata):
        variantReads = metadata['known_variant_reads']
        responseIndex = -1
        counter = 0
        for variant in variantReads:
            if (shortestSuperstring.overlap_length(unkownContig, variant) == len(variant)):
                responseIndex = counter
                break
            counter += 1
            
        return responseIndex

    def _formatFinalResponseObject(self, responseObject, counter):
        finalResponseObject = {
            'MAXIMUM_MATCHES': responseObject['MAXIMUM_MATCHES']
        }
        for index in range(counter):
            curIndexVariant = responseObject[index]['variant']
            curIndexMatches = responseObject[index]['matches']

            finalResponseObject[curIndexVariant] = {
                'Variant_Matches': curIndexMatches
            }

        return finalResponseObject