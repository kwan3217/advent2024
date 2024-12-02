"""
Given two lists of numbers: Match up the two smallest and calculate the distance
between them. Then match up the next smallest, etc and get a total distance
between the lists. For instance, the example list is:

3   4
4   3
2   5
1   3
3   9
3   3

In the example list above, the pairs and distances would be as follows:

The smallest number in the left list is 1, and the smallest number in the right list is 3. The distance between them is 2.
The second-smallest number in the left list is 2, and the second-smallest number in the right list is another 3. The distance between them is 1.
The third-smallest number in both lists is 3, so the distance between them is 0.
The next numbers to pair up are 3 and 4, a distance of 1.
The fifth-smallest numbers in each list are 3 and 5, a distance of 2.
Finally, the largest number in the left list is 4, while the largest number in the right list is 9; these are a distance 5 apart.
To find the total distance between the left list and the right list, add up the distances between all of the pairs you found. In the example above, this is 2 + 1 + 0 + 1 + 2 + 5, a total distance of 11!

Your actual left and right lists contain many location IDs. What is the total distance between your lists?



Created: 12/1/24
"""

def dec01a(list1:list,list2:list):
    result=0
    for a,b in zip(sorted(list1),sorted(list2)):
        result+=abs(b-a)
    return result


def test_dec01a():
    list1=[3,4,2,1,3,3]
    list2=[4,3,5,3,9,3]
    assert dec01a(list1,list2)==11


def read_dec01a(infn:str)->tuple[list,list]:
    list1=[]
    list2=[]
    with open(infn,"rt") as inf:
        for line in inf:
            parts=line.split(" ")
            list1.append(int(parts[ 0]))
            list2.append(int(parts[-1]))
    return list1,list2


def test_dec01b():
    list1=[3,4,2,1,3,3]
    list2=[4,3,5,3,9,3]
    assert dec01b(list1,list2)==31


def dec01b(list1:list,list2:list)->int:
    result=0
    for a in list1:
        for b in list2:
            if a==b:
                result+=b
    return result

def main():
    test_dec01a()
    test_dec01b()
    print(dec01a(*read_dec01a("data/dec01a.txt")))
    print(dec01b(*read_dec01a("data/dec01a.txt")))


if __name__ == "__main__":
    main()
