import math

hit_counter = 0
miss_counter = 0
file_tracer_map = dict()


def calculeteNoOfSets(cache_size, set_ways):
    #print("printing cache size from file", cache_size)
    multiplier = int(cache_size[:-1])
    
    if cache_size[-1] == "M":
        multiplier = multiplier * 1024 * 1024
    if cache_size[-1] == 'K':
        multiplier = multiplier * 1024 

    #print("value of multiplier...", multiplier)
    return int(multiplier / (set_ways * 64 ))
    

def printTable(table):
    for i in range(16):
        print(table[i])

def LRU(table, offset_addr, idx_addr, tag_addr, set_ways):
    """
    way tag valid data
     0   1    2    3
    """

    #print("inside LRU function...")
    global hit_counter
    global miss_counter
    cache_hit = False
    for i in range(set_ways):
        #print(tag_addr, " --------- ", table[i][1])
        #cache hit
        if table[i][2] == 1 and table[i][1] == tag_addr:
            print("cache hit!")
            cache_hit = True
            break
    
    inserted = False
    if cache_hit == False:
        #either all valid bit 1 or some cache line with valid bit 0 exists'
        print("cache miss....")
        
        for i in range(set_ways):
            
            if table[i][2] == 0:    #empty row
                #print("value of i", i)
                #print("inserting...", table[i])
                table[i][0] = i
                table[i][1] = tag_addr
                table[i][2] = 1
                table[i][3] = "data" + offset_addr
                inserted = True
                
                print("after inserted ")
                
                break
    #table is full and first row is evicted
    #LRU need to be implemented more perfectly
    if inserted == False:
        
        print("when inserted false")
        
        table[0][0] = 0
        table[0][1] = tag_addr
        table[0][2] = 1
        table[0][3] = "data" + offset_addr
        print(table[i])
        inserted = True    
    

    ########## counting miss and hit
    if cache_hit == True:
        hit_counter += 1
    else:
        miss_counter += 1



def fileTracerMapping():
    
    global file_tracer_map

    cache_file_tracer = open('file_tracer.txt', 'r')
    file_tracer_lines = cache_file_tracer.readlines()

    for line in file_tracer_lines:
        file_name = line.split('|')[0]
        file_bit = line.split('|')[1].replace('\n', '')
        file_tracer_map[file_name] = file_bit


def getSplittedAddress(binary_address, offset, idx, tag):

    #print("Offset ", binary_address[tag + idx:])
    #print("idx ", binary_address[tag:tag + idx])
    #print("tag ", binary_address[:tag])
    return binary_address[:tag], binary_address[tag:tag + idx], binary_address[tag + idx:]


def main():
    print("LRU cache")
    global file_tracer_map

    fileTracerMapping()
    print(file_tracer_map)

    #file name issue need to be addressed
    file_name = '1KB_64B'
    file = open('memory_traces/1KB_64B', 'r') 
    
    lines = file.readlines() 
    total_lines = len(lines)
    print("total lines ", total_lines)
    

    #need to come from a function
    set_ways = 16
    offset = 6
    
    total_set = calculeteNoOfSets(file_tracer_map[file_name], set_ways)
    #tag = 58
    idx = int(math.log(total_set, 2))
    
    tag = 64 - offset - idx

    print("***### value of idx and tag ", idx, tag)


    #create structure
    rows, cols = (total_lines, 4) 
    #set = [[0]*cols]*rows
    table = [[0 for i in range(cols)] for j in range(rows)]
    set_list = list()
    for i in range(total_set):
        print("****")
        set_list.append(table)

    
    #print(set_list[0])
    temp_table = set_list[0]
    
    

    for line in lines:
        hex_address = line.split(" ")[2]
        #print(address, end='')
        binary_address = bin(int(hex_address, 16)).replace('0b', '').zfill(64)
        #print(binary_address)

        tag_addr, idx_addr, offset_addr = getSplittedAddress(binary_address, offset, idx, tag)

        #print(offset_addr, "---" ,  idx_addr, "---",  tag_addr)
        if idx_addr == '':
            idx_addr = '0'
        print("idx addr.............", type(idx_addr))
        table = set_list[int(idx_addr, 2)] #will work only for the first file
        print("new call")
        LRU(table, offset_addr, idx_addr, tag_addr, set_ways)
        

    global hit_counter
    global miss_counter
    print(hit_counter, " ", miss_counter)
    misss_rate = (miss_counter) / (hit_counter + miss_counter)
    print("miss rate = ", misss_rate)

if __name__ == "__main__":
    main()