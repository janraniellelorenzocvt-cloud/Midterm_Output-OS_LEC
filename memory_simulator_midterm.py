def run_sim(strat, holes, requests):
    memory = []
    for i in range(len(holes)):
        memory.append({'id': i+1, 'size': holes[i], 'is_free': True, 'process': None, 'frag': 0})
    
    alloc_list = []
    rejected = []
    
    print("\n==========================================")
    print(" SIMULATING: " + strat)
    print("==========================================")
    
    for req in requests:
        action = req[0]
        p_id = req[1]
        sz = req[2]
        
        if action == 'alloc':
            target = None
            
            if strat == 'First-Fit':
                for block in memory:
                    if block['is_free'] == True and block['size'] >= sz:
                        target = block
                        break 
                        
            elif strat == 'Best-Fit':
                best_i = -1
                smallest_left = 9999999 
                for i in range(len(memory)):
                    if memory[i]['is_free'] and memory[i]['size'] >= sz:
                        leftover = memory[i]['size'] - sz
                        if leftover < smallest_left:
                            smallest_left = leftover
                            best_i = i
                if best_i != -1:
                    target = memory[best_i]
                    
            elif strat == 'Worst-Fit':
                worst_i = -1
                biggest_left = -1
                for i in range(len(memory)):
                    if memory[i]['is_free'] and memory[i]['size'] >= sz:
                        leftover = memory[i]['size'] - sz
                        if leftover > biggest_left:
                            biggest_left = leftover
                            worst_i = i
                if worst_i != -1:
                    target = memory[worst_i]
            
            if target != None:
                target['is_free'] = False
                target['process'] = p_id
                target['frag'] = target['size'] - sz
                alloc_list.append(p_id)
                print(f"ALLOCATED: {p_id} ({sz} KB) to Block {target['id']} ({target['size']} KB) - Int Frag: {target['frag']} KB")
            else:
                rejected.append(p_id)
                print(f"REJECTED: {p_id} ({sz} KB) not enough space left")
                
        elif action == 'dealloc':
            for block in memory:
                if block['process'] == p_id:
                    block['is_free'] = True
                    block['process'] = None
                    block['frag'] = 0
                    print(f"DEALLOCATED: {p_id} is done. Block {block['id']} is free again.")
                    break
                    
    int_frag_total = 0
    ext_frag_total = 0
    largest_hole = 0
    
    for b in memory:
        if b['is_free'] == False:
            int_frag_total += b['frag']
        if b['is_free'] == True:
            ext_frag_total += b['size']
            if b['size'] > largest_hole:
                largest_hole = b['size']
                
    print("\nFINAL METRICS:")
    print("Allocated:", alloc_list)
    print("Rejected:", rejected)
    print("Memory Map:")
    for b in memory:
        if b['is_free']:
            print(f"  Hole {b['size']} KB -> Free")
        else:
            print(f"  Hole {b['size']} KB -> Taken by {b['process']}")
    print("Total Internal Frag:", int_frag_total, "KB")
    print(f"Total External Frag: {ext_frag_total} KB vs Largest Hole: {largest_hole} KB")

holes_start = [100, 500, 200, 300, 600]

processes = [
    ('alloc', 'P1', 212),
    ('alloc', 'P2', 417),
    ('alloc', 'P3', 112),
    ('alloc', 'P4', 426),
    ('dealloc', 'P2', 0), 
    ('alloc', 'P5', 200)
]

run_sim('First-Fit', holes_start, processes)
run_sim('Best-Fit', holes_start, processes)
run_sim('Worst-Fit', holes_start, processes)