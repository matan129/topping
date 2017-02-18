class Slice(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.score = (x2 - x1) * (y2 - y1)

    def __repr__(self):
        return '({0}, {1})=>({2}, {3})'.format(self.x1, self.y1, self.x2, self.y2)


class Pizza(object):
    def __init__(self, rows, cols, min_toppings, max_for_slice, toppings):
        self.rows = int(rows)
        self.cols = int(cols)
        self.min_toppings = int(min_toppings)
        self.max_for_slice = int(max_for_slice)
        self.toppings = [list(t) for t in toppings]
        self.toppings_cache = {}

    def is_valid_slice(self, ):
        pass

    def __repr__(self):
        s = ' '.join(map(str, [self.rows, self.cols, self.min_toppings, self.max_for_slice]))
        return s + '\n' + '\n'.join(map(str, self.toppings))

    @staticmethod
    def count_toppings(pizza_clone, x1, x2, y1, y2):
        t, m = 0, 0
        for i in xrange(x1, x2):
            for j in xrange(y1, y2):
                topping = pizza_clone[j][i]
                if topping == 'X':
                    return None
                elif topping == 'T':
                    t += 1
                else:
                    m += 1
        return t, m

    def draw_on_pizza(self, pizza, slice):
        for i in xrange(slice.x1, slice.x2):
            for j in xrange(slice.y1, slice.y2):
                pizza[j][i] = 'X'

    def split_greedy(self, x, y, pizza_clone):
        for i in xrange(x + 1, min(x + self.max_for_slice, self.cols)):
            max_y = min(y + self.max_for_slice / (i - x), self.rows)
            for j in xrange(y + 1, max_y + 1):
                res = self.count_toppings(pizza_clone, x, i, y, j)
                if res is None:
                    break
                t, m = res
                if t >= self.min_toppings and m >= self.min_toppings:
                    return Slice(x, y, i, j)

    def split_all_pizza_greedy(self):
        lines_to_first_untaken = {}
        pizza_clone = [line[:] for line in self.toppings]
        slices = []
        y = 0
        while lines_to_first_untaken.get(y, 0) < self.cols:
            x = lines_to_first_untaken.get(y, 0)
            slice = self.split_greedy(x, y, pizza_clone)
            if slice is None:
                lines_to_first_untaken[y] = lines_to_first_untaken.get(y, 0) + 1
                y += 1
            else:
                self.draw_on_pizza(pizza_clone, slice)
                slices.append(slice)
                for k in xrange(y, slice.y2):
                    lines_to_first_untaken[k] = slice.x2
                y = slice.y2
            if y >= self.rows:
                min_val = None
                min_key = None
                for key, val in lines_to_first_untaken.iteritems():
                    if min_val is None or val < min_val:
                        min_val = val
                        min_key = key
                y = min_key
        return slices


def main(pizza):
    print pizza
    slices = pizza.split_all_pizza_greedy()
    print sum(map(lambda s: s.score, slices))
    print slices
    print 'Done'


def get_pizza(name):
    with open(r'Pizzas\\' + name) as f:
        data = f.read()
    data = data.splitlines()
    return Pizza(*data[0].split(), toppings=data[1:])


if __name__ == '__main__':
    main(get_pizza('big.in'))
