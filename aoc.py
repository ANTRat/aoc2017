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


def run():
    tests = {
        day1: (
            {'1122': 3, '1111': 4, '1234': 0, '91212129': 9},
            {'1212': 6, '1221': 0, '123425': 4, '123123': 12, '12131415': 4}
        ),
        day2: (
            {"5 1 9 5\n7 5 3\n2 4 6 8": 18},
            {"5 9 2 8\n9 4 7 3\n3 8 6 5": 9},
        ),
        day3: (
            {'1': 0, '12': 3, '23': 2, '1024': 31},
            {}
        ),
        day4: (
            {'aa bb cc dd ee\naa bb cc dd aa\naa bb cc dd aaa': 2},
            {'abcde fghij\nabcde xyz ecdab\na ab abc abd abf abj\niiii oiii ooii oooi oooo\noiii ioii iioi iiio': 3}
        ),
        day5: (
            {'0 3 0 1 -3': 5},
            {'0 3 0 1 -3': 10}
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
