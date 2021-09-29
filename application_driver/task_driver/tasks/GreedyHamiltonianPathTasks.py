from application_driver.helper_modules import shortestSuperstring

class GreedyHamiltonianPathTasks():

    def __init__(self):
        self.state = 'ACTIVE'

    def execute(self, greedyHamiltonianGraph):
        return self._findGraphContigs(greedyHamiltonianGraph)

    def _findGraphContigs(greedyHamiltonianGraph):
        connectedReadComponentList = greedyHamiltonianGraph.getConnectedComponents()
        responseContigsList = []
        for component in connectedReadComponentList:
            curContig = shortestSuperstring.merge_ordered_reads(component)
            responseContigsList.append(curContig)
        return responseContigsList