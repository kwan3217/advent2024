"""
Describe purpose of this script here

Created: 12/8/24
"""
from itertools import combinations

test_input=["............",
            "........0...",
            ".....0......",
            ".......0....",
            "....0.......",
            "......A.....",
            "............",
            "............",
            "........A...",
            ".........A..",
            "............",
            "............"]


test_input0=["..........",
             "..........",
             "..........",
             "....a.....",
             "..........",
             ".....a....",
             "..........",
             "..........",
             "..........",
             ".........."]


test_input1=["..........",
             "..........",
             "..........",
             "....a.....",
             "........a.",
             ".....a....",
             "..........",
             "..........",
             "..........",
             ".........."]


AntennaMap=list[str]
AntinodeMap=list[list[str]]
AntennaCoords=tuple[int,int]
AntennaList=list[AntennaCoords]


def enumerate_frequencies(map:AntennaMap)->str:
    result=""
    for row in map:
        for char in row:
            if char not in result and char!=".":
                result+=char
    return result


def find_antennas(map:AntennaMap,freq:str)->AntennaList:
    result=[]
    for i_row,row in enumerate(map):
        for i_col,char in enumerate(row):
            if char==freq:
                result.append((i_row,i_col))
    return result


def count_antinodes(an_map:AntinodeMap)->int:
    result=0
    for row in an_map:
        for col in row:
            if col!='.':
                result+=1
    return result


def dec08a(map:AntennaMap):
    freqs=enumerate_frequencies(map)
    print(freqs)
    an_map=[["."]*len(row) for row in map]
    n_rows=len(map)
    n_cols=len(map[0])
    for freq in freqs:
        pairs=find_antennas(map,freq)
        combos=combinations(pairs,2)
        for (i_row0,i_col0),(i_row1,i_col1) in combos:
            drow=i_row1-i_row0
            dcol=i_col1-i_col0
            i_rowAN0=i_row0-drow
            i_colAN0=i_col0-dcol
            i_rowAN1=i_row1+drow
            i_colAN1=i_col1+dcol
            if 0<=i_rowAN0<n_rows and 0<=i_colAN0<n_cols:
                an_map[i_rowAN0][i_colAN0]=freq
            if 0<=i_rowAN1<n_rows and 0<=i_colAN1<n_cols:
                an_map[i_rowAN1][i_colAN1]=freq
    print_an_map(an_map)
    return count_antinodes(an_map)


def dec08b(map:AntennaMap):
    freqs=enumerate_frequencies(map)
    print(freqs)
    an_map=[["."]*len(row) for row in map]
    n_rows=len(map)
    n_cols=len(map[0])
    for freq in freqs:
        pairs=find_antennas(map,freq)
        combos=combinations(pairs,2)
        for (i_row0,i_col0),(i_row1,i_col1) in combos:
            drow=i_row1-i_row0
            dcol=i_col1-i_col0
            # Find common factors and divide them out
            # Any common factors must be less than the number of rows so only check up to there
            # Start high and work down
            for factor in range(n_rows,1,-1): #count down to but not including 1
                if abs(drow)%factor==0 and abs(dcol)%factor==0:
                    drow//=factor
                    dcol//=factor
                    break
            done=False
            for i in range(-n_rows,n_rows+1):
                i_rowAN0=i_row0+i*drow
                i_colAN0=i_col0+i*dcol
                if 0<=i_rowAN0<n_rows and 0<=i_colAN0<n_cols:
                    an_map[i_rowAN0][i_colAN0]=freq
    print_an_map(an_map)
    return count_antinodes(an_map)


def print_an_map(an_map:AntinodeMap):
    for row in an_map:
        for col in row:
            print(col,end='')
        print()


def test_dec08a():
    assert dec08a(test_input0)==2
    assert dec08a(test_input1)==4
    assert dec08a(test_input)==14


def test_dec08b():
    assert dec08b(test_input)==34


def read_dec08()->AntennaMap:
    with open("data/dec08.txt","rt") as inf:
        result=[line.strip() for line in inf if line.strip()!=""]
    return result


def main():
    test_dec08a()
    map=read_dec08()
    print(dec08a(map))
    test_dec08b()
    print(dec08b(map))


if __name__ == "__main__":
    main()
