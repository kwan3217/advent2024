"""
--- Day 5: Print Queue ---
Satisfied with their search on Ceres, the squadron of
scholars suggests subsequently scanning the stationery
stacks of sub-basement 17.

The North Pole printing department is busier than ever
this close to Christmas, and while The Historians continue
their search of this historically significant facility, an
Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time
explaining that the new sleigh launch safety manual updates
won't print correctly. Failure to update the safety manuals
would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the
safety manuals must be printed in a very specific order.
The notation X|Y means that if both page number X and page
number Y are to be produced as part of an update, page
number X must be printed at some point before page number
Y.

The Elf has for you both the page ordering rules and the
pages to produce in each update (your puzzle input), but
can't figure out whether each update has the pages in the
right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47

The first section specifies the page ordering rules, one per line.
The first rule, 47|53, means that if an update includes both page
number 47 and page number 53, then page number 47 must be printed
at some point before page number 53. (47 doesn't necessarily need
to be immediately before 53; other pages are allowed to be
between them.)

The second section specifies the page numbers of each update.
Because most safety manuals are different, the pages needed in the
updates are different too. The first update, 75,47,61,53,29, means
that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying
which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the
right order:

75 is correctly first because there are rules that put each other
   page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and
   every other page must be after it according to 47|61, 47|53,
   and 47|29.
61 is correctly in the middle because 75 and 47 are before it
   (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.

Because the first update does not include some page numbers, the
ordering rules involving those missing page numbers are ignored.

The second and third updates are also in the correct order according
to the rules. Like the first update, they also do not include
every page number, and so only some of the ordering rules apply -
within each update, the ordering rules that involve missing page
numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it
would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order,
since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due
to breaking several rules.

For some reason, the Elves also need to know the middle page number
of each update being printed. Because you are currently only printing
the correctly-ordered updates, you will need to find the middle page
number of each correctly-ordered update. In the above example, the
correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13

These have middle page numbers of 61, 53, and 29 respectively. Adding
these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering
rules is bigger and more complicated than the above example.

Determine which updates are already in the correct order. What do you
get if you add up the middle page number from those correctly-ordered
updates?

Created: 12/5/24
"""


def is_correct(rules:list[tuple[int,int]],update:list[int])->bool:
    """
    Return True if the given update follows the rules, and False otherwise
    :param rules: list of rule tuples
    :param update:
    :return:
    """
    obeys_rules = True
    for prior, posterior in rules:
        if prior not in update:
            continue
        if posterior not in update:
            continue
        if update.index(prior) > update.index(posterior):
            obeys_rules = False
            break
    return obeys_rules


def dec05a(rules:list[tuple[int,int]],updates:list[list[int]])->int:
    """
    Return the sum of the middle page numbers for the updates that
    follow the rules
    :param rules: List of rule tuples
    :param updates: List of updates
    :return: sum of middle page numbers for updates that follow the rules
    """
    result=0
    for update in updates:
        if is_correct(rules,update):
            assert len(update)%2==1,"Even-length update found. What's the middle number for this?"
            result+=update[len(update)//2]
    return result


def fix_update(rules:list[tuple[int,int]],update:list[int])->list[int]:
    """
    Fix an update.
    :param rules:
    :param update:
    :return:
    """
    # Do this by a bogo-sort like mechanism. If a pair of pages in the update
    # violates the rules, swap them then go back to the beginning of the rule
    # list.
    done=False
    update=update[:]
    while not done:
        done=True
        for prior,posterior in rules:
            if prior in update and posterior in update and update.index(prior)>update.index(posterior):
                done=False
                update[update.index(prior)]=posterior
                update[update.index(posterior)]=prior
                break
    return update


def dec05b(rules:list[tuple[int,int]],updates:list[list[int]])->int:
    """
    Fix the updates that don't follow the rules and return the sum of the middle numbers of
    only the updates that needed to be fixed.
    :param rules:
    :param updates:
    :return:
    """
    result=0
    for update in updates:
        if not is_correct(rules,update):
            update=fix_update(rules,update)
            assert len(update)%2==1,"Even-length update found. What's the middle number for this?"
            result+=update[len(update)//2]
    return result


def test_dec05a():
    rules=[(47,53),
           (97,13),
           (97,61),
           (97,47),
           (75,29),
           (61,13),
           (75,53),
           (29,13),
           (97,29),
           (53,29),
           (61,53),
           (97,53),
           (61,29),
           (47,13),
           (75,47),
           (97,75),
           (47,61),
           (75,61),
           (47,29),
           (75,13),
           (53,13)]
    updates=[[75,47,61,53,29],
             [97,61,53,29,13],
             [75,29,13],
             [75,97,47,61,53],
             [61,13,29],
             [97,13,75,29,47]]
    assert dec05a(rules,updates)==143


def test_dec05b():
    rules=[(47,53),
           (97,13),
           (97,61),
           (97,47),
           (75,29),
           (61,13),
           (75,53),
           (29,13),
           (97,29),
           (53,29),
           (61,53),
           (97,53),
           (61,29),
           (47,13),
           (75,47),
           (97,75),
           (47,61),
           (75,61),
           (47,29),
           (75,13),
           (53,13)]
    updates=[[75,47,61,53,29],
             [97,61,53,29,13],
             [75,29,13],
             [75,97,47,61,53],
             [61,13,29],
             [97,13,75,29,47]]
    assert dec05b(rules,updates)==123


def read_dec05()->tuple[list[tuple[int,int]],list[list[int]]]:
    rules=[]
    updates=[]
    with open("data/dec05.txt","rt") as inf:
        for line in inf:
            line=line.strip()
            if line=="":
                break
            rules.append(tuple([int(part.strip()) for part in line.split("|")]))
        for line in inf:
            line=line.strip()
            updates.append([int(part.strip()) for part in line.split(",")])
    return rules,updates


def main():
    test_dec05a()
    test_dec05b()
    rules,updates=read_dec05()
    print(dec05a(rules,updates))
    print(dec05b(rules,updates))


if __name__ == "__main__":
    main()
