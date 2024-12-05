"""
"Looks like the Chief's not here. Next!" One of The Historians pulls
out a device and pushes the only button on it. After a brief flash,
you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the
station tugs on your shirt; she'd like to know if you could help her
with her word search (your puzzle input). She only has to find one
word: XMAS.

This word search allows words to be horizontal, vertical, diagonal,
written backwards, or even overlapping other words. It's a little
unusual, though, as you don't merely need to find one instance of
XMAS - you need to find all of them. Here are a few ways XMAS might
appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word
search again, but where letters not involved in any XMAS have been replaced
with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?


--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that
this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're
supposed to find two MAS in the shape of an X. One way to achieve that
is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram.
Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have
been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side
and try again. How many times does an X-MAS appear?


Created: 12/4/24
"""


def search(word_search:list[str],word:str="XMAS")->int:
    """
    Count the number of times the word appears from left-to-right
    :param word_search: Grid to search
    :param word: Word to search for
    :return: Number of times the word appears
    """
    result=0
    for line in word_search:
        for i in range(len(line)-len(word)+1):
            if line[i:i+len(word)]==word:
                result+=1
    return result


def search_pat(word_search:list[str],pat:list[list[str]]=None)->int:
    """
    Find a 2D pattern in a word search
    :param word_search:
    :param pat: Pattern to search for. Must be rectangular IE
                all rows the same length. Use NONE for the
                don't care condition
    :return: Number of times the pattern hits
    """
    if pat is None:
        pat=[["M",None,"S"],
             [None,"A",None],
             ["M",None,"S"]]
    n_rows=len(word_search)
    n_cols=len(word_search[0])
    n_rows_pat=len(pat)
    n_cols_pat=len(pat[0])
    result=0
    for i_row in range(n_rows-n_rows_pat+1):
        for i_col in range(n_cols-n_cols_pat+1):
            found=True
            for i_row_pat in range(n_rows_pat):
                for i_col_pat in range(n_cols_pat):
                    if pat[i_row_pat][i_col_pat] is not None and pat[i_row_pat][i_col_pat]!=word_search[i_row+i_row_pat][i_col+i_col_pat]:
                        found=False
            if found:
                result+=1
    return result



def flip_lr(word_search:list[str])->list[str]:
    """
    Flip a word search grid left-to-right. This will allow for searching for
    the target word from right-to-left, but doesn't perform any searching
    itself.
    :param word_search:
    :return:
    """
    return [line[::-1] for line in word_search]


def transpose(word_search:list[str])->list[str]:
    """
    Transpose the word search grid.

    Assume the grid is rectangular with m rows and n columns, represented
    by a list with m elements, each of which is a string with n characters.
    Return a list of n elements where each element is a string with m characters.
    :param word_search:
    :return:
    """
    n_rows=len(word_search)
    n_cols=len(word_search[0])
    result=[[None]*n_rows for i in range(n_cols)] #Make sure the lists are separate
    for i_row in range(n_rows):
        for i_col in range(n_cols):
            result[i_col][i_row]=word_search[i_row][i_col]
    result=["".join(row) for row in result]
    return result


def rotate(word_search:list[str])->list[str]:
    """
    Rotate a word search grid 90deg, such that the right column becomes
    the top row.

    :param word_search:
    :return:
    """
    n_rows=len(word_search)
    n_cols=len(word_search[0])
    result=[[None]*n_rows for i in range(n_cols)] #Make sure the lists are separate
    for i_old_row in range(n_rows):
        for i_old_col in range(n_cols):
            i_new_row=n_cols-i_old_col-1
            i_new_col=i_old_row
            result[i_new_row][i_new_col]=word_search[i_old_row][i_old_col]
    result=["".join(row) for row in result]
    return result


def searchdiag(word_search:list[str],word:str="XMAS")->int:
    """
    Search for words diagonally from upper left to lower right
    :param word_search:
    :param word:
    :return:
    """
    n_rows=len(word_search)
    n_cols=len(word_search[0])
    result=0
    for i_row in range(n_rows-len(word)+1):
        for i_col in range(n_cols-len(word)+1):
            diag_word=""
            for i_let in range(len(word)):
                diag_word+=word_search[i_row+i_let][i_col+i_let]
            if word==diag_word:
                result+=1
    return result



def dec04a(word_search:list[str],word:str="XMAS")->int:
    # Search left-to-right
    result=search(word_search,word)
    # Search right-to-left
    result+=search(rotate(word_search),word)
    # Search top-to-bottom
    result+=search(rotate(rotate(word_search)),word)
    # Search bottom-to-top
    result+=search(rotate(rotate(rotate(word_search))),word)
    # Search UL-BR
    result+=searchdiag(word_search,word)
    # Search right-to-left
    result+=searchdiag(rotate(word_search),word)
    # Search top-to-bottom
    result+=searchdiag(rotate(rotate(word_search)),word)
    # Search bottom-to-top
    result+=searchdiag(rotate(rotate(rotate(word_search))),word)
    return result


def dec04b(word_search:list[str],pat:list[list[str]]=None)->int:
    result=search_pat(word_search,pat)
    result+=search_pat(rotate(word_search),pat)
    result+=search_pat(rotate(rotate(word_search)),pat)
    result+=search_pat(rotate(rotate(rotate(word_search))),pat)
    return result


def test_dec04a():
    word_search=["MMMSXXMASM",
                 "MSAMXMSMSA",
                 "AMXSXMAAMM",
                 "MSAMASMSMX",
                 "XMASAMXAMM",
                 "XXAMMXXAMA",
                 "SMSMSASXSS",
                 "SAXAMASAAA",
                 "MAMMMXMMMM",
                 "MXMXAXMASX"]
    assert dec04a(word_search)==18


def test_dec04b():
    word_search=["MMMSXXMASM",
                 "MSAMXMSMSA",
                 "AMXSXMAAMM",
                 "MSAMASMSMX",
                 "XMASAMXAMM",
                 "XXAMMXXAMA",
                 "SMSMSASXSS",
                 "SAXAMASAAA",
                 "MAMMMXMMMM",
                 "MXMXAXMASX"]
    assert dec04b(word_search)==9


def read_dec04()->list[str]:
    with open("data/dec04.txt","rt") as inf:
        result=[line.strip() for line in inf if line.strip()!=""]
    return result


def main():
    test_dec04a()
    test_dec04b()
    word_search=read_dec04()
    print(dec04a(word_search))
    print(dec04b(word_search))


if __name__ == "__main__":
    main()
