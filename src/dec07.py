"""
Brute force and Ignorance! O(2**n) here we go!

Created: 12/7/24
"""
from functools import partial
from itertools import combinations_with_replacement, permutations, product
from typing import Iterable, Callable
from multiprocessing import Pool

StrEqns=list[str]
Terms=list[int]
Eqn=tuple[int,Terms]
Eqns=list[Eqn]


def format_eqns(str_eqns:StrEqns)->Eqns:
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


def permutations_with_replacement(items:Iterable,n:int):
    for combo in combinations_with_replacement(items,n):
        for perm in permutations(combo):
            yield perm


Operator=Callable[[int,int],int]
Operators=Iterable[Operator]

def check_one_eqn(*args,operators:Operators)->bool:
    i_eqn, eqn=args[0]
    answer,terms=eqn
    print(f"{i_eqn} - {answer}: {terms}")
    print(f"Number of possibilities: {len(operators)**(len(terms)-1)}")
    for i_perm,perm_operators in enumerate(product(operators,repeat=len(terms[1:]))):
        this_result = terms[0]
        for term,operator in zip(terms[1:],perm_operators):
            this_result=operator(this_result,term)
        if this_result==answer:
            return True


operators_a = [lambda a, b: a + b, lambda a, b: a * b]


def dec07(eqns:Eqns,operators:Operators)->int:
    result=0
    numbered_eqns = list(enumerate(eqns))
    map_results=[check_one_eqn(numbered_eqn,operators=operators) for numbered_eqn in numbered_eqns]
    for map_result,(answer,terms) in zip(map_results,eqns):
        if map_result:
            result+=answer
    return result


def test_dec07a():
    assert dec07(test_eqns,operators_a)==3749


def read_dec07()->Eqns:
    with open("data/dec07.txt","rt") as inf:
        result=[line for line in inf if line!=""]
    return format_eqns(result)


operators_b = [lambda a, b: a + b, lambda a, b: a * b, lambda a,b:int(str(a)+str(b))]


def test_dec07b():
    assert dec07(test_eqns,operators_b)==11387


def main():
    test_dec07a()
    eqns=read_dec07()
    print(dec07(eqns,operators_a))
    test_dec07b()
    print(dec07(eqns,operators_b))


if __name__ == "__main__":
    main()
