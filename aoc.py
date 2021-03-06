import collections
import itertools
import os


def day1(digits, part2=False):
    ret = 0
    for x in range(len(digits)):
        d1 = digits[x]
        if not part2:
            d2 = digits[(x + 1) % len(digits)]
        else:
            d2 = digits[int((x + (len(digits) / 2))) % len(digits)]
        if d1 == d2:
            ret += int(d1)
    return ret


def day2(spreadsheet, part2=False):
    ret = 0
    for line in spreadsheet.split("\n"):
        if not part2:
            l = list(map(int, line.split()))
            ret += max(l) - min(l)
        else:
            l = map(int, line.split())
            for a in itertools.permutations(l, 2):
                div = a[0] / a[1]
                if div == int(div):
                    ret += int(div)
                    break
    return ret


def day3(input, part2=False):
    def right(x, y):
        return x + 1, y

    def up(x, y):
        return x, y + 1

    def left(x, y):
        return x - 1, y

    def down(x, y):
        return x, y - 1

    def manhattan_distance(x, y):
        return sum(abs(a - b) for a, b in zip(x, y))

    def nearby(x, y):
        n = 0
        around = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x - 1, y), (x + 1, y), (x - 1, y - 1), (x, y - 1),
                  (x + 1, y - 1)]
        for pos in around:
            if pos in other_grid:
                n += other_grid[pos]
        return n

    order = itertools.cycle([right, up, left, down])
    x = 0
    y = 0
    g = {1: (0, 0)}
    other_grid = {(0, 0): 1}
    times_to_move = 1
    n = 1
    while True:
        for _ in range(2):
            move = next(order)
            for _ in range(times_to_move):
                if n > int(input):
                    break
                x, y = move(x, y)
                n += 1
                g[n] = (x, y)
                near = nearby(x, y)
                other_grid[(x, y)] = near
                if near > int(input) and part2:
                    return near
                # print(n,x,y)
        times_to_move += 1
        if n > int(input):
            break
    return manhattan_distance((0, 0), g[int(input)])


def day4(passwords, part2=False):
    def isvalid(s, part2):
        uniq = set()
        uniqs = set()
        words = s.split()
        for w in words:
            sortw = ''.join(sorted(w))
            if w in uniq:
                return False
            if sortw in uniqs and part2:
                return False
            uniq.add(w)
            uniqs.add(sortw)
        return True

    valid = 0
    for p in passwords.split('\n'):
        if isvalid(p, part2):
            valid += 1
    return valid


def day5(maze, part2=False):
    maze = list(map(int, maze.split()))
    steps = 0
    n = 0
    try:
        while True:
            old_n = n
            n += maze[n]
            if maze[old_n] >= 3 and part2:
                maze[old_n] += -1
            else:
                maze[old_n] += 1
            steps += 1
    except IndexError:
        return steps


def day6(blocks, part2=False):
    blocks = list(map(int, blocks.split()))
    states = set(tuple(blocks))
    loops = 0
    wanted = False
    old_loops = 0
    while True:
        num = max(blocks)
        start = blocks.index(num)
        blocks[start] = 0
        for x in range(start + 1, start + num + 1):
            blocks[x % len(blocks)] += 1
        loops += 1
        if tuple(blocks) in states:
            if not part2:
                return loops
            else:
                if not wanted:
                    wanted = list(blocks)
                    old_loops = loops
                else:
                    if blocks == wanted:
                        return loops - old_loops
        states.add(tuple(blocks))


def day7(input, part2=False):
    ends = {}
    tower = {}
    reverse_tower = {}
    weights = {}
    for line in input.split('\n'):
        line = line.split(' ')
        n = line[0]
        weights[n] = int(line[1][1:-1])
        if len(line) > 2:
            c = ''.join(line[3:]).split(',')
            tower[n] = c
            for cn in c:
                reverse_tower[cn] = n
        else:
            ends[n] = []
    for program in ends:
        step = program
        while step in reverse_tower:
            step = reverse_tower[step]
            ends[program].append(step)
        if not part2:
            return step
    # noinspection PyUnboundLocalVariable
    bottom = step
    total_weights = {}

    def get_weight(node):
        weight = 0
        weight += weights[node]
        if node in tower:
            for child in tower[node]:
                weight += get_weight(child)
        return weight

    for w in weights:
        total_weights[w] = get_weight(w)
    smallest = bottom
    smallest_w = total_weights[smallest]
    for t in tower:
        t_weights = [total_weights[x] for x in tower[t]]
        if t_weights != [t_weights[0]] * len(t_weights):
            if total_weights[t] < smallest_w:
                smallest = t
                smallest_w = total_weights[t]
    ws = [[child, weights[child], total_weights[child]] for child in tower[smallest]]
    # noinspection PyArgumentList
    b = collections.Counter([x[2] for x in ws])
    good = b.most_common()[0][0]
    bad = b.most_common()[-1][0]
    for x in ws:
        if x[2] == bad:
            return x[1] + (good - bad)


def day8(input, part2=False):
    registers = collections.defaultdict(int)
    max_reg = 0

    def do_test(a, check, b):
        if check == '>':
            return a > b
        elif check == '<':
            return a < b
        elif check == '>=':
            return a >= b
        elif check == '==':
            return a == b
        elif check == '<=':
            return a <= b
        elif check == '!=':
            return a != b
        else:
            print(check)
            raise Exception('unknown check')

    for line in input.split('\n'):
        reg, op, dif, _, test, cmp, val = line.split(' ')
        dif = int(dif)
        val = int(val)
        if do_test(registers[test], cmp, val):
            if op == 'inc':
                registers[reg] += dif
            elif op == 'dec':
                registers[reg] -= dif
        max_reg = max(max_reg, max(registers.values()))
    if not part2:
        return max(registers.values())
    else:
        return max_reg


def day9(input, part2=False):
    def process(s, part2):
        ignore_next = False
        discard = False
        for char in s:
            if ignore_next:
                ignore_next = False
                continue
            if char == '!':
                ignore_next = True
                continue

            if char == '<' and not discard:
                discard = True
                continue

            if char == '>' and discard:
                discard = False
                continue

            if not discard and not part2:
                yield char
            if discard and part2:
                yield char

    depth = 0
    score = 0
    discarded = []
    for c in process(input, part2):
        discarded.append(c)
        if c == '{':
            depth += 1
            score += depth
        elif c == '}':
            depth -= 1

    if not part2:
        return score
    return len(discarded)


def run():
    tests = {
        # day1: (
        #     {'1122': 3, '1111': 4, '1234': 0, '91212129': 9},
        #     {'1212': 6, '1221': 0, '123425': 4, '123123': 12, '12131415': 4}
        # ),
        # day2: (
        #     {"5 1 9 5\n7 5 3\n2 4 6 8": 18},
        #     {"5 9 2 8\n9 4 7 3\n3 8 6 5": 9},
        # ),
        # day3: (
        #     {'1': 0, '12': 3, '23': 2, '1024': 31},
        #     {}
        # ),
        # day4: (
        #     {'aa bb cc dd ee\naa bb cc dd aa\naa bb cc dd aaa': 2},
        #     {'abcde fghij\nabcde xyz ecdab\na ab abc abd abf abj\niiii oiii ooii oooi oooo\noiii ioii iioi iiio': 3}
        # ),
        # day5: (
        #     {'0 3 0 1 -3': 5},
        #     {'0 3 0 1 -3': 10}
        # ),
        # day6: (
        #     {'0 2 7 0': 5},
        #     {'0 2 7 0': 4}
        # ),
        # day7: (
        #     {'pbga (66)\nxhth (57)\nebii (61)\nhavc (66)\nktlj (57)\nfwft (72) -> ktlj, cntj, xhth\nqoyq (66)\npadx ('
        #      '45) -> pbga, havc, qoyq\ntknk (41) -> ugml, padx, fwft\njptl (61)\nugml (68) -> gyxo, ebii, jptl\ngyxo '
        #      '(61)\ncntj (57)': 'tknk'},
        #     {'pbga (66)\nxhth (57)\nebii (61)\nhavc (66)\nktlj (57)\nfwft (72) -> ktlj, cntj, xhth\nqoyq (66)\npadx ('
        #      '45) -> pbga, havc, qoyq\ntknk (41) -> ugml, padx, fwft\njptl (61)\nugml (68) -> gyxo, ebii, jptl\ngyxo '
        #      '(61)\ncntj (57)': 60}
        # ),
        # day8: (
        #     {'b inc 5 if a > 1\na inc 1 if b < 5\nc dec -10 if a >= 1\nc inc -20 if c == 10': 1},
        #     {'b inc 5 if a > 1\na inc 1 if b < 5\nc dec -10 if a >= 1\nc inc -20 if c == 10': 10}
        # )
        day9: (
            {
                '{}': 1,
                '{{{}}}': 6,
                '{{},{}}': 5,
                '{{{},{},{{}}}}': 16,
                '{<a>,<a>,<a>,<a>}': 1,
                '{{<ab>},{<ab>},{<ab>},{<ab>}}': 9,
                '{{<!!>},{<!!>},{<!!>},{<!!>}}': 9,
                '{{<a!>},{<a!>},{<a!>},{<ab>}}': 3
            },
            {
                '<>': 0,
                '<random characters>': 17,
                '<<<<>': 3,
                '<{!>}>': 2,
                '<!!>': 0,
                '<!!!>>': 0,
                '<{o"i!a,<{i<a>': 10
            }
        )
    }

    for day in tests:
        day_name = day.__name__
        for part in [0, 1]:
            for test, output in tests[day][part].items():
                answer = day(test, part)
                same = answer == output
                print("%s %s(%s, %s) = %s == %s" % (same, day_name, test.__repr__(), part, answer, output))
                if not same:
                    raise ValueError
        day_file = 'data/%s.txt' % day_name
        if os.path.exists(day_file):
            data = open(day_file).read().strip()
            print("%s(%s) = %s" % (day_name, day_file, day(data)))
            print("%s(%s, 1) = %s" % (day_name, day_file, day(data, 1)))


if __name__ == '__main__':
    run()
