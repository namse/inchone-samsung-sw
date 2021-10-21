from typing import Generator, List

# 백준시는 N개의 구역으로 나누어져 있다.
# 구역은 1번부터 N번까지 번호가 매겨져 있다.

# 각 구역은 두 선거구 중 하나에 포함되어야 한다.


# 구역 A에서 인접한 구역을 통해서 구역 B로 갈 수 있을 때 두 구역은 연결되어 있다고 한다.

# 중간에 통하는 인접한 구역은 0개 이상이어야 한다.
# 중간에 통하는 인접한 구역은 모두 같은 선거구에 포함된 구역이어야 한다.

# 공평하게 선거구를 나누기 위해 두 선거구에 포함된 인구의 차이를 최소로 하려고 한다.
# 백준시의 정보가 주어졌을 때, 인구 차이의 최솟값을 구해보자.

# 1. 구역을 두개의 선거구로 나누는 모든 경우의 수를 구하고

class Section:
    def __init__(self, population: int) -> None:
        self.population = population
        self.connectedSections: set[Section] = set([])

class ElectionDistrict:
    def __init__(self, sections: List[Section]) -> None:
        self.sections = sections
    
    def getPopulation(self) -> int:
        return sum([s.population for s in self.sections])

def divideSectionsToTwo(sections: List[Section]) -> Generator[List[List[Section]], None, None]:
    if len(sections) == 0:
        yield ([], [])
        return
    sections = sections.copy()
    last = sections[len(sections) - 1]
    rest = sections[:-1]
    for (sectionsA, sectionsB) in divideSectionsToTwo(rest):
        yield (sectionsA, [last] + sectionsB)
        yield ([last] + sectionsA, sectionsB)

def isSectionsConnected(sections: List[Section]) -> bool:
    if len(sections) <= 1:
        return True
    
    connectedSections = set([])
    
    for section in sections:
        for connectedSection in section.connectedSections:
            connectedSections.add(connectedSection)
    
    for section in sections:
        if section not in connectedSections:
            return False
    
    return True
    

def getAllElectionDistrictsCases(sections: List[Section]) -> Generator[List[ElectionDistrict], None, None]:
    
    # 구역을 두 개의 선거구로 나눠야 한다.
    for (sectionsA, sectionsB) in divideSectionsToTwo(sections):

        # 선거구는 구역을 적어도 하나 포함해야 한다.
        if len(sectionsA) == 0 or len(sectionsB) == 0:
            continue

        # 한 선거구에 포함되어 있는 구역은 모두 연결되어 있어야 한다.
        if not isSectionsConnected(sectionsA) or not isSectionsConnected(sectionsB):
            continue
        
        yield (ElectionDistrict(sectionsA), ElectionDistrict(sectionsB))

def getSectionsFromInput() -> List[Section]:
    int(input()) # ignore it
    
    populations = map(int, input().split())

    sections = [Section(population) for population in populations]
    
    for section in sections:
        indexInputWithoutCount = list(map(int, input().split()))[1:]

        connectedSectionIndexes = [oneBaseIndex - 1 for oneBaseIndex in indexInputWithoutCount]
        for connectedSectionIndex in connectedSectionIndexes:
            connectedSection = sections[connectedSectionIndex]

            section.connectedSections.add(connectedSection)
            connectedSection.connectedSections.add(section)

    return sections

    # 이렇게 짜면 복잡해.
    #     
    # for sectionIndex in range(sectionCount):
    #     connectedSectionCount = int(input())
    #     for _ in range(connectedSectionCount):
    #         connectedSectionIndex = int(input()) - 1
    #         sections[connectedSectionIndex].connectedSections.add(sections[sectionIndex])




sections = getSectionsFromInput()

minimumPopulationDifference = -1

# 2. 각 경우의 수의 인구 차이를 구하고
for (electionDistrictA, electionDistrictB) in getAllElectionDistrictsCases(sections):

    populationA = electionDistrictA.getPopulation()
    populationB = electionDistrictB.getPopulation()
    populationDifference = abs(populationA - populationB)

    # 3. 가장 인구 차이가 적은 경우를 구하고
    if minimumPopulationDifference == -1 or populationDifference < minimumPopulationDifference:
        minimumPopulationDifference = populationDifference

# 4. 그것을 출력한다.
print(minimumPopulationDifference)