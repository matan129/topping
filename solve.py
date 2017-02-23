from ortools.linear_solver import pywraplp as ps

from main import *


def solve():
    data = Data('example')
    solver = ps.Solver('SHA7', ps.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    y = {}
    t = {}
    for v in data.videos:
        for c in v.caches.keys():
            y[(v, c)] = solver.IntVar(0.0, 1.0, 'y {0} {1}'.format(str(v), str(c)))

        for e in v.endpoints:
            for c in e.caches.keys():
                t[(v, c, e)] = solver.IntVar(0.0, 1.0, 't {0} {1} {2}'.format(str(v), str(c), str(e)))
            t[(v, e)] = solver.IntVar(0.0, 1.0, 't {0} {1} D'.format(str(v), str(e)))

    constraints = {}
    # for c in data.caches.keys():
    #     constraints[c] = solver.Constraint(0.0, data.max_cache_capacity)

    for v in data.videos:
        for c in v.caches.keys():
            if c not in constraints.keys():
                constraints[c] = solver.Constraint(0.0, data.max_cache_capacity)
            constraints[c].SetCoefficient(y[(v, c)], v.size + 0.0)
        
        for e in v.endpoints:
            constraints[(e, v)] = solver.Constraint(1.0, 1.0)
            constraints[(e, v)].SetCoefficient(t[(v, e)], 1)

            for c in e.caches.keys():
                constraints[(e, v)].SetCoefficient(t[(v, c, e)], 1)
                constraints[(v, c, e)] = solver.Constraint(-solver.infinity(), 0.0)
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
        objective.SetCoefficient(t[(v, e)], (r.num_requests * e.latency_to_data_center) / N)

    objective.SetMinimization()
    assert solver.Solve() == ps.Solver.OPTIMAL

    from collections import defaultdict
    final_caches = defaultdict(list)
    for (v, c), value in y.iteritems():
        if value.solution_value() == 1:
            final_caches[c].append(v.id)

    lines = [str(len(final_caches.keys()))]
    for cache_id, videos in final_caches.iteritems():
        lines.append(' '.join(map(str, [cache_id] + videos)))

    print '\n'.join(lines)
    
if __name__ == '__main__':
    solve()
