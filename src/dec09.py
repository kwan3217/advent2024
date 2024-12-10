"""
Trying a different way of documenting things -- typing out my thoughts in the code.

First, we create the test cases which will fail

Now read the problem. Amphipods! Oh no! The test data is there, so grab it.



Created: 12/9/24
"""

test_disk_map="2333133121414131402"
ref_expanded_map=[None if char=='.' else int(char) for char in "00...111...2...333.44.5555.6666.777.888899"]
ref_defrag_map  =[None if char=='.' else int(char) for char in "0099811188827773336446555566.............."]


def expand_disk_map(disk_map:str)->list[int]:
    result=[]
    for i_file,(used_blocks,free_blocks) in enumerate(zip(disk_map[::2],disk_map[1::2])):
        result+=[i_file]*int(used_blocks)+[None]*int(free_blocks)
    result+=[i_file+1]*int(disk_map[-1])
    return result


def defrag(expanded_map:list[int])->list[int]:
    result=[item for item in expanded_map]
    done=False
    while not done:
        # Find the first open block
        i_open=result.index(None)
        # Find the last used block
        for i_check in range(len(result)-1,-1,-1):
            if result[i_check] is not None:
                i_last=i_check
                break
        # Check for done. We are done if the last used block is before the first open block.
        if i_last<i_open:
            done=True
            break
        # Move the last used block into the first open slot
        result[i_open]=result[i_last]
        result[i_last]=None
    return result


def cksum(defrag_map:list[int])->int:
    result=0
    for blockid,fileid in enumerate(defrag_map):
        if fileid is not None:
            result+=blockid*fileid
    return result


def dec09a(expanded_map:list[int])->int:
    return cksum(defrag(expanded_map))


def test_dec09a():
    expanded_map=expand_disk_map(test_disk_map)
    print(expanded_map)
    print(ref_expanded_map)
    for test,ref in zip(expanded_map,ref_expanded_map):
        assert test==ref
    defrag_map=defrag(expanded_map)
    print(defrag_map)
    print(ref_defrag_map)
    for test,ref in zip(defrag_map,ref_defrag_map):
        assert test==ref
    assert dec09a(expanded_map)==1928


def test_dec09b():
    assert dec09b(test_disk_map)==None


def main():
    test_dec09a()
    print()
    test_dec09b()


if __name__ == "__main__":
    main()
