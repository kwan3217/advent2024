"""
Brute force and Ignorance! O(2**n) here we go!

Created: 12/7/24
"""


def format_eqns(str_eqns:list[str])->list[tuple[int,list[int]]]:
    result=[]
    for str_eqn in [str_eqn for str_eqn in str_eqns if str_eqn.strip()!=""]:
        l,r=[x.strip() for x in str_eqn.split(":")]
        terms=[int(term.strip()) for term in r.split(" ") if term.strip()!=""]
        result.append((int(l.strip()),terms))
    return result


test_eqns=format_eqns([
"190: 10 19",
"3267: 81 40 27",
"83: 17 5",
"156: 15 6",
"7290: 6 8 6 15",
"161011: 16 10 13",
"192: 17 8 14",
"21037: 9 7 18 13",
"292: 11 6 16 20",
])


def test_dec07a():
    assert dec07a(test_eqns)==3749


def main():
    test_dec07a()
    test_dec07b()


if __name__ == "__main__":
    main()
