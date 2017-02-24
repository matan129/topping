from ortools.linear_solver import pywraplp as ps
from tqdm import trange, tqdm
from main import *


def output(name, data):
    with open(os.path.join('res', name + '.out'), 'wb') as f:
        f.write(data)


def solve(name):
    data = Data(name)
    solver = ps.Solver('SHA7', ps.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    y = {}
    t = {}
    for v in tqdm(data.videos, desc='video vars'):
        for c in tqdm(v.caches.iterkeys()):
            y[(v, c)] = solver.IntVar(0.0, 1.0, 'y_{0}_{1}'.format(str(v.id), str(c)))

        for e in tqdm(v.endpoints, desc='video endpoints vars'):
            for c in tqdm(e.caches.iterkeys(), desc='endpoint caches vars'):
                if (v, c, e) not in t:
                    t[(v, c, e)] = solver.IntVar(0.0, 1.0, 't_{0}_{1}_{2}'.format(str(v.id), str(c), str(id(e))))

            if (v, e) not in t:
                t[(v, e)] = solver.IntVar(0.0, 1.0, 't_{0}_{1}_D'.format(str(v.id), str(id(e))))

    constraints = {}
    print
    print

    for v in tqdm(data.videos, desc='video constraints'):
        for c in tqdm(v.caches.iterkeys(), desc='video caches constraints'):
            if c not in constraints.iterkeys():
                constraints[c] = solver.Constraint(0.0, data.max_cache_capacity)
            constraints[c].SetCoefficient(y[(v, c)], v.size + 0.0)

        for e in tqdm(v.endpoints, desc='video endpoint constraints'):
            constraints[(e, v)] = solver.Constraint(1.0, 1.0)
            constraints[(e, v)].SetCoefficient(t[(v, e)], 1)

            for c in tqdm(e.caches.iterkeys(), desc='endpoint caches constraints'):
                constraints[(e, v)].SetCoefficient(t[(v, c, e)], 1)
                constraints[(v, c, e)] = solver.Constraint(-solver.infinity(), 0.0)
                constraints[(v, c, e)].SetCoefficient(t[(v, c, e)], 1)
                constraints[(v, c, e)].SetCoefficient(y[(v, c)], -1)
    print
    print
    print 'objective'
    objective = solver.Objective()

    N = 0
    for r in data.requests:
        N += r.num_requests

    for r in tqdm(data.requests, desc='requests'):
        v = data.videos[r.video_id]
        e = data.endpoints[r.endpoint_id]
        for c in tqdm(e.caches.iterkeys(), desc='endpoint cache'):
            objective.SetCoefficient(t[(v, c, e)], (r.num_requests * e.caches[c]) / N)
        objective.SetCoefficient(t[(v, e)], (r.num_requests * e.latency_to_data_center) / N)

    print
    print 
    print 'solve'
    objective.SetMinimization()
    print solver.Solve() == ps.Solver.OPTIMAL

    from collections import defaultdict
    final_caches = defaultdict(list)
    for (v, c), value in y.iteritems():
        if value.solution_value() == 1:
            final_caches[c].append(v.id)

    lines = [str(len(final_caches.keys()))]
    for cache_id, videos in final_caches.iteritems():
        lines.append(' '.join(map(str, [cache_id] + videos)))

    output(name, '\n'.join(lines))


import sys
if __name__ == '__main__':
    solve(sys.argv[1])
