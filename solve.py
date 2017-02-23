from ortools.linear_solver import pywraplp as ps

from main import *


def solve():
    data = Data('example')
    solver = ps.Solver('SHA7', ps.Solver.GLOP_LINEAR_PROGRAMMING)

    y = {}
    t = {}
    for v in data.videos:
        for c in v.caches.keys():
            y[(v, c)] = solver.IntVar(0.0, 1.0, 'y {0} {1}'.format(str(v), str(c)))

        for e in v.endpoints:
            for c in e.caches.keys():
                t[(v, c, e)] = solver.IntVar(0.0, 1.0, 't {0} {1} {2}'.format(str(v), str(c), str(e)))

    constraints = {}
    # for c in data.caches.keys():
    #     constraints[c] = solver.Constraint(0.0, data.max_cache_capacity)

    for v in data.videos:
        for c in v.caches.keys():
            if c not in constraints.keys():
                constraints[c] = solver.Constraint(0.0, data.max_cache_capacity)
            constraints[c].SetCoefficient(y[(v, c)], v.size + 0.0)
        
        for e in v.endpoints:
            constraints[(e, v)] = solver.Constraint(0.0, 1.0)

            for c in e.caches.keys():
                constraints[(e, v)].SetCoefficient(t[(v, c, e)], 1)
                constraints[(v, c, e)] = solver.Constraint(0.0, solver.infinity())
                constraints[(v, c, e)].SetCoefficient(t[(v, c, e)], 1)
                constraints[(v, c, e)].SetCoefficient(y[(v, c)], -1)
        
    objective = solver.Objective()

    N = 0
    for r in data.requests:
        N += r.num_requests

    for r in data.requests:
        v = data.videos[r.video_id]
        e = data.endpoints[r.endpoint_id]
        for c in e.caches.keys():
            objective.SetCoefficient(t[(v, c, e)], (r.num_requests * e.caches[c]) / N)

    objective.SetMinimization()
    solver.Solve()

    
    
if __name__ == '__main__':
    solve()
