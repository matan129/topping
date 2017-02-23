from ortools.linear_solver import pywraplp as ps

from main import *



def output(name, data):
    with open(os.path.join('res', name + '.out'), 'wb') as f:
        f.write(data)

def solve_with_subset(data, videos, final_caches):
    solver = ps.Solver('SHA7', ps.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    y = {}
    t = {}
    for v in videos:
        for c in v.caches.keys():
            y[(v, c)] = solver.IntVar(0.0, 1.0, 'y_{0}_{1}'.format(str(v.id), str(c)))

        for e in v.endpoints:
            for c in e.caches.keys():
                if (v, c, e) not in t:
                    t[(v, c, e)] = solver.IntVar(0.0, 1.0, 't_{0}_{1}_{2}'.format(str(v.id), str(c), str(id(e))))

            if (v, e) not in t:
                t[(v, e)] = solver.IntVar(0.0, 1.0, 't_{0}_{1}_D'.format(str(v.id), str(id(e))))

    constraints = {}

    for v in videos:
        for c in v.caches.keys():
            if c not in constraints.keys():
                constraints[c] = solver.Constraint(0.0, data.caches[c])
            constraints[c].SetCoefficient(y[(v, c)], v.size + 0.0)

        for e in v.endpoints:
            constraints[(e, v)] = solver.Constraint(1.0, 1.0)
            constraints[(e, v)].SetCoefficient(t[(v, e)], 1)

            for c in e.caches.keys():
                constraints[(e, v)].SetCoefficient(t[(v, c, e)], 1)
                constraints[(v, c, e)] = solver.Constraint(-solver.infinity(), 0.0)
                constraints[(v, c, e)].SetCoefficient(t[(v, c, e)], 1)
                constraints[(v, c, e)].SetCoefficient(y[(v, c)], -1)

    print 'objective'
    objective = solver.Objective()

    N = 0
    for r in data.requests:
        if r.video_id in videos:
            N += r.num_requests

    for r in data.requests:
        if r.video_id in videos:
            v = videos[r.video_id]
        e = data.endpoints[r.endpoint_id]
        for c in e.caches.keys():
            objective.SetCoefficient(t[(v, c, e)], (r.num_requests * e.caches[c]) / N)
        objective.SetCoefficient(t[(v, e)], (r.num_requests * e.latency_to_data_center) / N)

    objective.SetMinimization()

    for (v, c), value in y.iteritems():
        if value.solution_value() == 1:
            final_caches[c].append(v.id)
            data.caches[c] = data.caches[c] - v.size



def solve(name):
    from collections import defaultdict
    data = Data(name)
    final_caches = defaultdict(list)
    for i in xrange(0, len(data.videos) - 64, 64):
        final_caches = solve_with_subset(data, data.videos[i:i+64], final_caches)

    lines = [str(len(final_caches.keys()))]
    for cache_id, videos in final_caches.iteritems():
        lines.append(' '.join(map(str, [cache_id] + videos)))
    output(name, '\n'.join(lines))


import sys
if __name__ == '__main__':
    solve(sys.argv[1])
