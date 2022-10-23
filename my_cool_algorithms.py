itemset = dict()

def apriori_gen(L,minsup,k):
    global itemset
    Lk = dict()
    keys = list(L.keys())
    keys.sort()
    newkeys = subset(keys,k)
    for newkey in newkeys:
        Lk[newkey] = 0
    Ck = list(Lk.keys())
    Ck = set(Ck)
    # Scan itemset
    for Id,items in itemset.items():
        if len(items)<k:
            continue
        t = subset(items,k)
        Ct = list(Ck.intersection(t))
        for c in Ct:
            Lk[c] += 1
    Lk = prune(Lk,minsup)
    return Lk
            
def sw_inc(sel_win,maximum): #sel_win increment, maximum is the maximum number it can have
    for i in range(len(sel_win)-1,-1,-1):
        if sel_win[i] != maximum-(len(sel_win)-1-i): # example: [0 3 4] for maximum = 4, next should be [1,2,3] but not [0 4 ?]
            sel_win[i] += 1
            #print(i,sel_win[i],maximum-(len(sel_win)-1-i))
            for j in range(i+1,len(sel_win)):
                sel_win[j] = sel_win[j-1]+1
            return sel_win
    return -1

def subset(items,k):
    sel_win = []
    subsets = []
    for i in range(k):
        sel_win.append(0)

    while True:
        sel_win = sw_inc(sel_win,len(items)-1)
        if sel_win==-1:
            break
        subset = ""
        for i in range(k):
            if i!=0:
                subset += " "
            subset += str(items[sel_win[i]])
        subsets.append(subset)
    return subsets
    

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
    global itemset
    for data in input_data:
        Id = data[0]
        item = data[2]
        if Id in itemset.keys():
            itemset[Id].add(item)
        else:
            itemset[Id] = set([item])
            
    itemset = set2list(itemset)
    
def set2list(Dict):
    for k,v in Dict.items():
        Dict[k] = list(v)
    return Dict
            
def prune(itemset,minsup):
    delete = []
    for k,v in itemset.items():
        if v<minsup:
            delete.append(k)
    print(f"Prune {len(delete)} itemset")
    for d in delete:
        del itemset[d]
    return itemset
              
def apriori(input_data, a):
    generate_itemset(input_data)
    minsup = int(a.min_sup*len(itemset.keys()))
    L = generate_L1(minsup)
    for k,v in L.items():
        print(k,v)
    L2 = apriori_gen(L,minsup,2)
    for k,v in L2.items():
        print(k,v)
