itemset = dict()

def apriori_gen(L,minsup,k):
    Lk = dict()
    keys = list(L.keys())
    keys.sort()
    
    sel_win = []
    for i in range(k):
        sel_win.append(0)
    print(sel_win)
    while True:
        sel_win = sw_inc(sel_win,len(keys))
        print(sel_win)
        if sel_win==-1:
            return
    C = Lk.keys()
    
    # Scan itemset

def sw_inc(sel_win,maximum): #sel_win increment, maximum is the maximum number it can have
    for i in range(len(sel_win)-1,-1,-1):
        if sel_win[i] != maximum-(len(sel_win)-1-i): # example: [0 3 4] for maximum = 4, next should be [1,2,3] but not [0 4 ?]
            sel_win[i] += 1
            for j in range(i+1,len(sel_win)):
                sel_win[j] = sel_win[j-1]+1
            return sel_win
    return -1

def str2numbers(s):
    strs = s.split()
    numbers = []
    for n in numbers:
        numbers.append(int(n))
    return numbers
    
def generate_L1(minsup):   
    L1 = dict()
    for Id,items in itemset.items():
        for item in items:
            if item in L1.keys():
                L1[item] += 1 
            else:
                L1[item] = 1
    L1 = prune(L1,minsup)
    return L1

def generate_itemset(input_data):
    for data in input_data:
        Id = data[0]
        item = data[2]
        if Id in itemset.keys():
            itemset[Id].append(item)
        else:
            itemset[Id] = [item]
            
def prune(itemset,minsup):
    delete = []
    for k,v in itemset.items():
        if v<minsup:
            delete.append(k)
    print(len(delete))
    for d in delete:
        del itemset[d]
    return itemset
              
def apriori(input_data, a):
    generate_itemset(input_data)
    minsup = int(a.min_sup*len(itemset.keys()))
    L = generate_L1(minsup)
    for k,v in L.items():
        print(k,v)
    apriori_gen(L,minsup,3)
    
