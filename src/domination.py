import scripts.path_setup

class Domination:
    
    domis = {'independent Roman domination': 'IRD'}

    def getAbbreviation(self, dom_type) -> str:
        return self.domis[dom_type]
