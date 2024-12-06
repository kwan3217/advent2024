"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you
all away to the North Pole prototype suit manufacturing lab... in
the year 1518! It turns out that having direct access to history is
very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be
important to avoid anyone from 1518 while The Historians search for
the Chief. Unfortunately, a single guard is patrolling this part of
the lab.

Maybe you can work out where the guard will go ahead of time so
that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For
example:

   ....#.....
   .........#
   ..........
   ..#.......
   .......#..
   ..........
   .#..^.....
   ........#.
   #.........
   ......#...

The map shows the current position of the guard with ^ (to indicate
the guard is currently facing up from the perspective of the map).
Any obstructions - crates, desks, alchemical reactors, etc. - are
shown as #.

Lab guards in 1518 follow a very strict patrol protocol which
involves repeatedly following these steps:

If there is something directly in front of you, turn right 90
degrees.
Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until
she reaches an obstacle (in this case, a pile of failed suit
prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns
right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers),
she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves
the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific
positions in the lab will be in the patrol path. Including the
guard's starting position, the positions visited by the guard
before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your
map.

Predict the path of the guard. How many distinct positions will the
guard visit before leaving the mapped area?

Created: 12/5/24
"""
from copy import deepcopy
from enum import Flag

import matplotlib.pyplot as plt
import numpy as np


class Cell(Flag):
    NONE=0
    N=1
    E=2
    S=4
    W=8
    HASH=16
    O=32
    START=64
    OBSTACLE=HASH|O
    PATH=N|E|S|W

Map=list[list[Cell]]
StrMap=list[str]

char_to_cell={"#":Cell.HASH,".":Cell.NONE,"^":Cell.START|Cell.N}
cell_to_char={Cell.NONE:".",
              Cell.N:"^",#"↑",
              Cell.S:"v",#"↓",
              Cell.E:">",#"→",
              Cell.W:"<",#"←"
              Cell.N|Cell.S:"|",#"↕",
              Cell.N|Cell.E:"+",#"↱",
              Cell.N|Cell.E|Cell.W:"+",#"↱",
              Cell.N|Cell.S|Cell.W:"+",#"↕",
              Cell.E|Cell.S|Cell.W:"+",#"↕",
              Cell.N|Cell.W:"+",#"↰",
              Cell.E|Cell.W:"-",#"↔",
              Cell.S|Cell.E:"+",#"↳",
              Cell.S|Cell.W:"+",#"↲",
              Cell.HASH:"#",
              Cell.O:"O",
              Cell.N|Cell.START:"!",
              Cell.N|Cell.W|Cell.START:"!",
              Cell.N|Cell.E|Cell.W|Cell.START:"+",
              Cell.N|Cell.S|Cell.START:"|",#"↕",
              Cell.N|Cell.S|Cell.W|Cell.START:"+",#"↕",
              }

turn_right={
    Cell.N:Cell.E,
    Cell.E:Cell.S,
    Cell.S:Cell.W,
    Cell.W:Cell.N
}


dir_vector={
    Cell.N:( 0,-1),
    Cell.E:( 1, 0),
    Cell.S:( 0, 1),
    Cell.W:(-1, 0)
}


def print_map(map:Map):
    for row in map:
        print("".join([cell_to_char[cell] for cell in row]))


def count_map(map:Map):
    result=0
    for i_row,row in enumerate(map):
        for i_col,cell in enumerate(row):
            if (cell&Cell.PATH)!=Cell.NONE:
                result+=1
    return result


def plot_map(map:Map):
    count=count_map(map)
    map=np.array([[cell.value for cell in row] for row in map])
    plt.figure("map")
    plt.clf()
    plt.imshow(map)
    plt.title(f"Positions: {count}")
    plt.pause(0.01)


def dec06a(map:Map)->int:
    map=deepcopy(map)
    # First find the guard (marked by "^")
    dir=Cell.N
    dx,dy=dir_vector[dir]
    steps=0
    n_rows=len(map)
    n_cols=len(map[0])
    for i_row,row in enumerate(map):
        for i_col,cell in enumerate(row):
            if Cell.START in cell:
                guard_row=i_row
                guard_col=i_col
    done=False
    while not done:
        # Mark current point as visited:
        #if steps%10==0:
        #    plot_map(map)
        steps+=1
        map[guard_row][guard_col]|=dir
        # check what's ahead:
        try:
            while map[guard_row+dy][guard_col+dx]!=Cell.NONE and map[guard_row+dy][guard_col+dx] in Cell.OBSTACLE:
                dir=turn_right[dir]
                dx,dy=dir_vector[dir]
            if dir in map[guard_row+dy][guard_col+dx]:
                # We've reached this cell and have traversed it in this direction before, so we have looped
                raise ValueError("Loop found")
            guard_row+=dy
            guard_col+=dx
            if guard_row==0 or guard_col==0:
                map[guard_row][guard_col]|=dir
                done=True # Will step out next time
        except IndexError:
            # IndexError only happens when we are about to step off the map
            done=True
    # Now that the guard has left the map, count how many # are on the map.
    return count_map(map)


def format_map(str_map:StrMap)->Map:
    """
    Convert a map in the form of a list of strings into one in the
    form of a list of lists of chars. This way the map is mutable.
    :param test_map:
    :return:
    """
    return [[char_to_cell[char] for char in row] for row in str_map]


def has_loop(map:Map)->bool:
    try:
        dec06a(map)
        return False
    except ValueError:
        return True


def dec06b(map:Map)->int:
    map=deepcopy(map)
    result=0
    n_rows=len(map)
    n_cols=len(map[0])
    for i_row,row in enumerate(map):
        for i_col,cell in enumerate(row):
            if cell==Cell.NONE:
                this_map=deepcopy(map)
                this_map[i_row][i_col]=Cell.O
                if has_loop(this_map):
                    print("~~~")
                    print_map(this_map)
                    result+=1
    return result


test_map=format_map([
          "....#.....",
          ".........#",
          "..........",
          "..#.......",
          ".......#..",
          "..........",
          ".#..^.....",
          "........#.",
          "#.........",
          "......#..."])


def test_dec06a():
    assert dec06a(test_map)==41


def test_dec06b():
    assert dec06b(test_map)==6


def read_dec06():
    with open("data/dec06.txt") as inf:
        result=[line.strip() for line in inf if line.strip()!=""]
    return format_map(result)


def main():
    print_map(test_map)
    test_dec06a()
    map=read_dec06()
    print(dec06a(map))
    test_dec06b()
    print(dec06b(map))


if __name__ == "__main__":
    main()
