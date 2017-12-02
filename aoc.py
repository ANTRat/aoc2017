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


def run():
    tests = {
        day1: (
            {'1122': 3, '1111': 4, '1234': 0, '91212129': 9},
            {'1212': 6, '1221': 0, '123425': 4, '123123': 12, '12131415': 4}
        )
    }

    for day in tests:
        day_name = day.__name__
        for part in [0, 1]:
            for test, output in tests[day][part].items():
                answer = day(test, part)
                same = answer == output
                print("%s %s(%s, %s) = %s == %s" % (same, day_name, test, part, answer, output))
                if not same:
                    raise ValueError
        day_file = 'data/%s.txt' % day_name
        if os.path.exists(day_file):
            data = open(day_file).read().strip()
            print("%s(%s) = %s" % (day_name, day_file, day(data)))
            print("%s(%s, 1) = %s" % (day_name, day_file, day(data, 1)))


if __name__ == '__main__':
    run()
