"""
Advent of Code 2024-12-02

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain
no sign of the Chief Historian, the engineers there run up to you as soon as
they see you. Apparently, they still talk about the time Rudolph was saved
through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really
appreciate your help analyzing some unusual data from the Red-Nosed reactor.
You turn to check if The Historians are waiting for you, but they seem to
have already divided into groups that are currently searching every corner
of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report
per line. Each report is a list of numbers called levels that are separated
by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed
reactor safety systems can only tolerate levels that are either gradually
increasing or gradually decreasing. So, a report only counts as safe if both
of the following are true:

* The levels are either all increasing or all decreasing.
* Any two adjacent levels differ by at least one and at most three.

In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

Created: 12/1/24
"""

def read_dec02(infn:str="data/dec02.txt")->list[list[int]]:
    """
    Read the unusual data.

    :param infn:
    :return:  List of reports. Each report is a list of integers.
    """
    with open(infn,"rt") as inf:
        reports=[[int(part) for part in line.strip().split(" ")] for line in inf]
    return reports


def first_problem(report:list[int])->int:
    """
    Find the index of the first problem in a report
    :param report: List of levels
    :return: index of first problem, or None if no problems
    """
    last_level = report[0]
    increasing = None
    for i_level,level in enumerate(report[1:]):
        i_level+=1
        if increasing is not None:
            if increasing:
                if level < last_level:
                    return i_level
            else:
                if level > last_level:
                    return i_level
        else:
            increasing = level > last_level
        if not (1 <= abs(level - last_level) <= 3):
            return i_level
        last_level = level
    return None


def dec02a(reports:list[list[int]])->int:
    """
    Calculate the number of safe reports
    :param reports:
    :return: Number of safe reports.
    """
    safe_count=0
    for report in reports:
        if first_problem(report) is None:
            safe_count+=1
    return safe_count


def dec02b(reports:list[list[int]])->int:
    """
    Calculate the number of safe reports
    :param reports:
    :return: Number of safe reports.

    The engineers are surprised by the low number of safe reports until
    they realize they forgot to tell you about the Problem Dampener.

    The Problem Dampener is a reactor-mounted module that lets the
    reactor safety systems tolerate a single bad level in what would
    otherwise be a safe report. It's like the bad level never happened!

    Now, the same rules apply as before, except if removing a single
    level from an unsafe report would make it safe, the report instead
    counts as safe.

    More of the above example's reports are now safe:

    7 6 4 2 1: Safe without removing any level.
    1 2 7 8 9: Unsafe regardless of which level is removed.
    9 7 6 2 1: Unsafe regardless of which level is removed.
    1 3 2 4 5: Safe by removing the second level, 3.
    8 6 4 4 1: Safe by removing the third level, 4.
    1 3 6 7 9: Safe without removing any level.
    Thanks to the Problem Dampener, 4 reports are actually safe!

    Update your analysis by handling situations where the Problem
    Dampener can remove a single level from unsafe reports. How many
    reports are now safe?
    """
    safe_count=0
    for report in reports:
        if (i_problem:=first_problem(report)) is None:
            safe_count+=1
        else:
            # Implement the Problem Dampener by dropping each level and seeing if that makes
            # the report safe. We can stop after we find one that works, but this does make
            # this an N**2 solution to the problem.
            for i_drop in range(len(report)):
                patched_report=[level for i_level,level in enumerate(report) if i_level!=i_drop]
                if first_problem(patched_report) is None:
                    safe_count+=1
                    break
    return safe_count


def test_dec02a():
    reports=[[7,6,4,2,1],
             [1,2,7,8,9],
             [9,7,6,2,1],
             [1,3,2,4,5],
             [8,6,4,4,1],
             [1,3,6,7,9]]
    assert dec02a(reports)==2


def test_dec02b():
    reports=[[7,6,4,2,1],
             [1,2,7,8,9],
             [9,7,6,2,1],
             [1,3,2,4,5],
             [8,6,4,4,1],
             [1,3,6,7,9]]
    assert dec02b(reports)==4


def main():
    test_dec02a()
    test_dec02b()
    reports=read_dec02("data/dec02.txt")
    print(dec02a(reports))
    print(dec02b(reports))


if __name__ == "__main__":
    main()
