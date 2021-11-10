import math
from collections import deque

addresses = [4, 8, 20, 24, 28, 36, 44, 20, 24, 28, 36, 40, 44, 68, 72, 92, 96, 100]
address_size = 16
instruction_size = 32
block_size = 4  # in bytes
number_of_rows = 8  # must be multiple of 2
ways = 2  # can be any number (n)
max_storage_bits = 800 
# max number of bits all fields can take, tag, valid, LRU, data, etc.
# <cache's byte size> <cache block's byte size> <number of associativity>
# number_of_sets = 4  # must be multiple of 2 (r)
# Set Associative requires LRU for each way ceil(lg n)
# Fully Associative requires LRU for each row ceil(lg r)

miss_cost = 18 + (3 * block_size)
hit_cost = 1


def checkDirectMap():
    row_bits = math.ceil(math.log(number_of_rows, 2))
    index_bits = math.ceil(math.log(block_size, 2))
    tag_bits = address_size - row_bits - index_bits
    valid_bits = 1
    row_size = tag_bits + (8 * block_size) + valid_bits
    table_size = row_size * number_of_rows
    if table_size > max_storage_bits:
        print("Cache is too large, change your numbers: " + str(table_size) + "/" + str(max_storage_bits))
    else:
        print("Cache is within size constraints: " + str(table_size) + "/" + str(max_storage_bits));


def checkSetAssociative():
    row_bits = math.ceil(math.log(number_of_rows, 2))
    index_bits = math.ceil(math.log(block_size, 2))
    tag_bits = address_size - row_bits - index_bits
    valid_bits = 1
    LRU_bits = math.ceil(math.log(ways, 2))
    row_size = (tag_bits + (8 * block_size) + valid_bits + LRU_bits) * ways
    table_size = row_size * number_of_rows
    if table_size > max_storage_bits:
        print("Cache is too large, change your numbers: " + str(table_size))
    else:
        print("Cache is within size constraints: " + str(table_size) + "/" + str(max_storage_bits));


def checkFullyAssociative():
    index_bits = math.ceil(math.log(block_size, 2))
    tag_bits = address_size - index_bits
    LRU_bits = math.ceil(math.log(number_of_rows, 2))
    valid_bits = 1
    row_size = tag_bits + (8 * block_size) + valid_bits + LRU_bits
    table_size = row_size * number_of_rows
    if table_size > max_storage_bits:
        print("Cache is too large, change your numbers: " + str(table_size))
    else:
        print("Cache is within size constraints: " + str(table_size) + "/" + str(max_storage_bits));


def missTime():
    print("A cache miss will cost you: " + str(miss_cost) + " cycles")


def simulateDirectMap():
    tags = [0] * number_of_rows
    valid = [0] * number_of_rows
    miss_count = 0;
    total_instructions = 0;
    for i in range(0,3):
        for addr in addresses:
            #  addr = addresses[i]
            offset = addr % block_size
            row = (addr // block_size) % number_of_rows
            tag = addr // (block_size * number_of_rows)
            print("Address: " + str(addr) + ", tag: " + str(tag) + ", row: " + str(row) + ", offset: " + str(offset), end="\t")
            if valid[int(row)] == 0:
                print("placing item")
                valid[int(row)] = 1
                tags[int(row)] = tag
            elif tag != tags[int(row)]:
                tags[int(row)] = tag
                print("Cache Miss - updating row " + str(row))
                if i > 0:
                    miss_count += 1
            else:
                print("Cache Hit on row " + str(row))
            if i > 0:
                total_instructions += 1
            
            # print("row\tvalid\ttag")
            # for j in range(0, number_of_rows):
            #     print(str(j) + "\t" + str(valid[j]) + "\t" + str(tags[j]))

        print("END OF CYCLE " + str(i))
        print("")
        

    print("row\tvalid\ttag")
    for j in range(0, number_of_rows):
        print(str(j) + "\t" + str(valid[j]) + "\t" + str(tags[j]))
    cpi = ((miss_cost * miss_count) + (total_instructions - miss_count)) / total_instructions
    print("CPI: " + str(cpi))
    print("SIMULATION COMPLETE")


def simulateSetAssociative():
    tags = [[-1 for i in range(0, ways)] for i in range(0, number_of_rows)]
    valid = [[0 for i in range(0, ways)] for i in range(0, number_of_rows)]
    LRU = [deque() for i in range(0,number_of_rows)]

    miss_count = 0
    total_instructions = 0

    for i in range(0, 3):
        for addr in addresses:
            offset = addr % block_size
            row = (addr // block_size) % number_of_rows
            tag = addr // (block_size * number_of_rows)
            print("Address: " + str(addr) + ", tag: " + str(tag) + ", row: " + str(row) + ", offset: " + str(offset), end="\t")
            flag = False
            if (tag in tags[row]) and (valid[row][tags[row].index(tag)]): # if our tag is in our row and its valid
                print("Cache Hit")
                if i > 0:
                    total_instructions += 1
                continue # go to the next address, we found this one

            for j in range(0,ways): # if we couldn't find it, see if there is an open spot
                if valid[row][j] == 0:
                    tags[row][j] = tag
                    if j in LRU[row]:
                        LRU[row].remove(j)
                    LRU[row].append(j)
                    valid[row][j] = 1
                    flag = True
                    print("added item for the first time")
                    break
            if flag == False: # The tag was wrong
                leastUsedWay = LRU[row].popleft()
                tags[row][leastUsedWay] = tag
                if i > 0:
                    miss_count += 1
                LRU[row].append(leastUsedWay)
                print("Cache Miss - updating entry")

            if i > 0:
                total_instructions += 1
        print("END OF CYCLE: " + str(i))
        print("")

    print("row\tvalid\ttag\t|\tvalid\ttag")
    for j in range(0, number_of_rows):
        print(str(j) + "\t", end="")
        for k in range(0, ways):
            print(str(valid[j][k]) + "\t" + str(tags[j][k]) + "\t|\t",end="")
        print("")


    cpi = ((miss_cost * miss_count) + (total_instructions - miss_count)) / total_instructions
    print("CPI: " + str(cpi))
    print("SIMULATION COMPLETE")


def simulateFullyAssociative():
    tags1 = [-1] * number_of_rows
    valid1 = [0] * number_of_rows
    tags2 = [-1] * number_of_rows * 2
    valid2 = [0] * number_of_rows * 2
    LRU1 = deque()
    LRU2 = deque()

    miss_count = 0
    total_instructions = 0

    for i in range(0, 3):
        for addr in addresses:
            offset = addr % block_size
            tag = addr // (block_size)
            print("Address: " + str(addr) + ", tag: " + str(tag) + ", offset: " + str(offset), end="\t")

            # see if tag is in table - hit
            if tag in tags1:
                location = tags1.index(tag)
                if location in LRU1:
                    LRU1.remove(location)
                LRU1.append(location)
                print("Cache1 Hit")

            # see if there is an invalid row, - miss, add it
            elif 0 in valid1:
                location = valid1.index(0)
                tags1[location] = tag
                valid1[location] = 1
                if i > 0:
                    miss_count += 1
                if location in LRU1:
                    LRU1.remove(location)
                    print("THIS SHOULDNT HAPPEN!!!!!!!!!!!!")
                LRU1.append(location)
                print("Cache1 Miss - adding to empty row")

            # else, find least recently used and update - miss
            else:
                # see if tag is in table - hit
                if tag in tags2:
                    location = tags2.index(tag)
                    if location in LRU2:
                        LRU2.remove(location)
                    leastUsedLoc = LRU1.popleft()
                    oldtag = tags1[leastUsedLoc]
                    tags1[leastUsedLoc] = tag
                    tags2[location] = oldtag
                    LRU1.append(leastUsedLoc)
                    LRU2.append(location)
                    print("Cache2 Hit")

                # see if there is an invalid row, - miss, add it
                elif 0 in valid2:
                    location = valid2.index(0)
                    valid2[location] = 1
                    if i > 0:
                        miss_count += 1
                    if location in LRU2:
                        LRU2.remove(location)
                        print("THIS SHOULDNT HAPPEN!!!!!!!!!!!!")
                    leastUsedLoc = LRU1.popleft()
                    oldtag = tags1[leastUsedLoc]
                    tags1[leastUsedLoc] = tag
                    tags2[location] = oldtag
                    LRU1.append(leastUsedLoc)
                    LRU2.append(location)
                    print("Cache2 Miss - adding to empty row")

                # else, find least recently used and update - miss
                else:
                    location = LRU2.popleft()
                    leastUsedLoc = LRU1.popleft()
                    if i > 0:
                        miss_count += 1
                    if leastUsedLoc in LRU1:
                        LRU1.remove(leastUsedLoc)
                        print("THIS SHOULDNT HAPPEN!!!!!!!!!!!!")                  
                    oldtag = tags1[leastUsedLoc]
                    tags1[leastUsedLoc] = tag
                    tags2[location] = oldtag
                    LRU1.append(leastUsedLoc)
                    LRU2.append(location)
                    print("Cache2 Miss - replacing row")

            if i > 0:
                total_instructions += 1
                     
            print("Cache1 -------------------------------- ")
            print("LRU1 locations deque: " + str(LRU1))
            print("row\tvalid\ttag")
            for j in range(0, number_of_rows):
                print(str(j) + "\t" + str(valid1[j]) + "\t" + str(tags1[j]))
            print("Cache2 -------------------------------- ")
            print("LRU2 locations deque: " + str(LRU2))
            print("row\tvalid\ttag")
            for j in range(0, number_of_rows * 2):
                print(str(j) + "\t" + str(valid2[j]) + "\t" + str(tags2[j]))
        
        print("END OF CYCLE: " + str(i))
        print("")
        
    cpi = ((miss_cost * miss_count) + (total_instructions - miss_count)) / total_instructions
    print("CPI: " + str(cpi))
    print("SIMULATION COMPLETE")


def main():
    # checkDirectMap()
    # checkSetAssociative()
    checkFullyAssociative()

    missTime()

    # simulateDirectMap()
    # simulateSetAssociative()
    simulateFullyAssociative()


if __name__ == "__main__":
    main()