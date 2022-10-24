itemset = dict()

# Generate Frequent Itemset

def generate_L(L,minsup,k):
    global itemset
    print(f"Generating L{k}")
    Lk = dict()
    keys = list(L.keys())
    keys.sort()
    newkeys = apriori_gen(L,minsup)
    #print(f"newkeys:{newkeys}")
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
        subset = []
        for i in range(k):
            subset.append(items[sel_win[i]])
        subset.sort()
        key = list2key(subset)
        subsets.append(key)
    return subsets
    
def apriori_gen(L,minsup):
    keys = list(L.keys())
    newkeys = []
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            s1 = set(str2numbers(keys[i]))
            s2 = set(str2numbers(keys[j]))
            if len(s1 & s2) == len(s1)-1:         
                # Check prune or not
                D = (s1 - s2)|(s2 - s1)
                B = s1 & s2
                Bs = []
                if len(B) != 1:
                    for b in B:
                        Bs.append(B-{b})
                else:
                    Bs = [D]
                AddKey = True
                newkey = list2key(list(s1|s2))
                #print(f"B:{B}, Base:{Bs}")
                if len(Bs) == 0: # For generate L2
                    newkeys.append(newkey)
                    #print(f"newkeys to append {newkey}")
                elif len(Bs) == 1: # For generate L3
                    checkkey = list2key(list(Bs[0]))
                    #print(f"Checkkey:{checkkey}")
                    if checkkey in keys:
                        newkeys.append(newkey)
                else: # For generate Lk>3
                    for bs in Bs:
                        if AddKey == False:
                            break
                        checkkey = list2key(list(bs|D))
                        if checkkey not in keys:
                            AddKey = False
                            break
                    if AddKey:
                        newkeys.append(newkey)
    return newkeys

def list2key(List): # Same as list2str, but include sort
    #print(f"{List} to key: ",end="")
    List.sort()
    key = list2str(List)
    #print(key)
    return key

def list2str(List): # Convert list of int to str
    s = ""
    for i in range(len(List)):
        if i != 0:
            s += " "
        s += str(List[i])
    return s

def str2numbers(s): # Convert str/key to int list
    if isinstance(s, str):
        strs = s.split()
        numbers = []
        for n in strs:
            numbers.append(int(n))
    elif isinstance(s,int):
        numbers = [s]
    return numbers
    
def generate_L1(minsup):   
    L1 = dict()
    for Id,items in itemset.items():
        for item in items:
            if str(item) in L1.keys():
                L1[str(item)] += 1 
            else:
                L1[str(item)] = 1
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
    
def set2list(Dict): # Convert set value of a dictionary to list value
    for k,v in Dict.items():
        Dict[k] = list(v)
    return Dict

def set2key(s): #Convert set to key/str
    # First convert to list
    s = list(s)
    s = list2key(s)
    return s

def key2set(s):#Convert key/str to set
    s = str2numbers(s)
    s = set(s)
    return s
            
def prune(itemset,minsup):
    delete = []
    for k,v in itemset.items():
        #print(f"{k}:{v}")
        if v<minsup:
            delete.append(k)
    print(f"Prune {len(delete)} itemset")
    for d in delete:
        del itemset[d]
    return itemset

def sort_itemset():
    global itemset
    for k,v in itemset.items():
        itemset[k].sort()
        
# Generate Association Rule
## Association Rule: ["x1 x2 ...","y1 y2 ..."}] indicate {x1,x2,...} -> {y1,y2,...}
def cal_conf(rule,L):
    s1 = set(str2numbers(rule[0]))
    s2 = set(str2numbers(rule[1]))
    s = s1 | s2
    s_list = list(s)
    s_list.sort()
    key = list2str(s_list)
    num = L[len(s)-1][key]
    den = L[len(s1)-1][rule[0]]
    return float(num/den)

def gen_rule(Lk,min_conf):
    Rules = []
    for i in range(len(Lk)-1,0,-1): # Ignore L1 as it cannot form a rule
        for k,v in Lk[i].items():
            # Generate the first layer of rule
            rules = gen_r1(k)
            print(rules)
            
            #Prune rule less than min_conf
            rules = prune_rule(rules,min_conf,Lk)
            
            # Generate rule by merging 2 rules
            newrules = gen_r(rules)
            
def gen_r1(k):
    Rules = []
    nums = set(str2numbers(k))
    for num in nums:
        lhs = set2key(nums-{num})
        rhs = list2key([num])
        Rules.append([lhs,rhs])
    return Rules

def prune_rule(rules,min_conf,Lk):
    remove_rule = []
    for r in rules:
        conf = cal_conf(r,Lk)
        print(f"conf for {r} = {conf}")
        if conf<min_conf:
            remove_rule.append(r)
    print(f"Prune {len(remove_rule)} rule")
    for r_rule in remove_rule:
        rules.remove(r_rule)
    return rules

def gen_r(rules):
    new_rules = []
    for i in range(len(rules)):
        for j in range(i,len(rules)):
            lhs1 = key2set(rules[i][0])
            lhs2 = key2set(rules[j][0])
            rhs1 = key2set(rules[i][1])
            rhs2 = key2set(rules[j][1])
            
            if len(lhs1 & lhs2) == len(lhs1)-1 and len(lhs1 & lhs2) != 0:
                new_lhs = lhs1 & lhs2
                new_rhs = rhs1 | rhs2
                new_rule = [set2key(new_lhs),set2key(new_rhs)]
                if new_rule in new_rules:
                    break
                new_rules.append(new_rule)
    print(f"new rules generated:{new_rules}")
    return new_rules

def apriori(input_data, a):
    global itemset
    generate_itemset(input_data)
    
    minsup = int(a.min_sup*len(itemset.keys()))
    
    itemset = {'1':[0,3,1,2],
               '2':[1,2,4,5],
               '3':[0,1,4],
               '4':[0,1,2,3]}
    minsup = 2
    sort_itemset()
    L1 = generate_L1(minsup)
    Lk = [L1]
    L = L1
    print(L1)
    while True:
        L = generate_L(L,minsup,len(Lk)+1)
        if len(L) == 0:
            break
        Lk.append(L)
    print(Lk)
    min_conf = 0.7#a.min_conf
    gen_rule(Lk,min_conf)
    