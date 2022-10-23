itemset = dict()

def generate_L(L,minsup,k):
    global itemset
    Lk = dict()
    keys = list(L.keys())
    keys.sort()
    newkeys = apriori_gen(L,minsup)
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
    
def apriori_gen(L,minsup):
    keys = list(L.keys())
    newkeys = []
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            s1 = set(str2numbers(keys[i]))
            s2 = set(str2numbers(keys[j]))
            if len(s1 & s2) == len(s1)-1:
                D = [s1 - s2,s2 - s1]
                B = s1 & s2
                Bs = []
                for b in B:
                    Bs.append(B-b)
                AddKey = True
                for bs in Bs:
                    if AddKey == False:
                        break
                    for d in D:
                        checkComb = list(bs|d)
                        newkey = list2str(checkCom)
                        if newkey not in keys:
                            AddKey = False
                            break
                if AddKey:
                    newkeys.append(list2str(list(s1|s2)))
    return newkeys
                    
def list2str(List):
    s = ""
    for i in range(len(List)):
        if i != 0:
            s += " "
        s += str(List[i])
    return s

def str2numbers(s):
    if isinstance(s, str):
        strs = s.split()
        numbers = []
        for n in numbers:
            numbers.append(int(n))
    elif isinstance(s,int):
        numbers = [s]
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
    L1 = generate_L1(minsup)
    for k,v in L1.items():
        print(k,v)
    Lk = [L1]
    L = L1
    while True:
        L = generate_L(L,minsup,len(Lk)+1)
        if len(L) == 0:
            break
        Lk.append(L)
    print(Lk)