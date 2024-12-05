"""
Created: 12/3/24
--- Day 3: Mull It Over ---
"Our computers are having issues, so I have no idea if we have any Chief
Historians in stock! You're welcome to check the warehouse, though," says
the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop.
The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are
having issues again?"

The computer appears to be trying to run a program, but its memory (your
puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It
does that with instructions like mul(X,Y), where X and Y are each 1-3
digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a
result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many
invalid characters that should be ignored, even if they look like part of a
mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 )
do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
 ^^^^^^^^                    ^^^^^^^^                ^^^^^^^^^!!!!!!!!
Only the four highlighted sections are real mul instructions. Adding up
the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you
get if you add up all of the results of the multiplications?

"""
from re import finditer


def dec03a(memory:str)->int:
    """
    https://xkcd.com/208/
    :param memory: String containing contents of memory
    :return: Sum of all valid mul([0-9]{1,3},[0-9]{1,3}) instructions
    """
    result=0
    for match in finditer(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)",memory):
        a=int(match.group(1))
        b=int(match.group(2))
        result+=a*b
    return result


def dec03b(memory:str)->int:
    """
    https://xkcd.com/208/
    :param memory: String containing contents of memory
    :return: Sum of all valid mul([0-9]{1,3},[0-9]{1,3}) instructions
    """
    result=0
    do=True
    for match in finditer(r"(?:mul\(([0-9]{1,3}),([0-9]{1,3})\))|(do\(\))|(don't\(\))",memory):
        if match.group(0)=="do()":
            do=True
        elif match.group(0)=="don't()":
            do=False
        else:
            a=int(match.group(1))
            b=int(match.group(2))
            result+=((a*b) if do else 0)
    return result


def test_dec03a():
    memory="xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    assert dec03a(memory)==161


def test_dec03b():
    memory="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert dec03b(memory)==48


def read_dec03(infn:str="data/dec03.txt")->str:
    result=""
    with open(infn,"rt") as inf:
        for line in inf:
            result+=line.strip()
    return result
        

def main():
    test_dec03a()
    test_dec03b()
    memory=read_dec03()
    print(dec03a(memory))
    print(dec03b(memory))


if __name__ == "__main__":
    main()
