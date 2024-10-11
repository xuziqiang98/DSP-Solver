from src.solver import SolverFactory

envs = ['DSP', 'RDP', 'IRDP','RDRDP']

def make(id, adj):
    
    if id in envs:
        env = SolverFactory.get(id, adj)
    else:
        raise NotImplementedError()

    return env