from utils import timer

itemset = dict()

# Generate Frequent Itemset

def generate_L(L,minsup,k):
    global itemset
    print(f"Generating L{k}")
    Lk = dict()
    newkeys = apriori_gen(L,minsup)
    print(f"newkeys#:{len(newkeys)}")
    for newkey in newkeys:
        Lk[newkey] = 0
    Ck = list(Lk.keys())
    Ck = set(Ck)
    
    # Scan itemset
    for items in itemset.values():
        if len(items)<k:
            continue
        Ct = []
        it = set(items)
        for c in Ck:
            ci = key2set(c)
            if ci.issubset(it):
                Ct.append(c)
        for c in Ct:
            Lk[c] += 1
    Lk = prune(Lk,minsup)
    #print(Lk)
    return Lk
            

def apriori_gen(L,minsup):
    keys = list(L.keys())
    newkeys = []
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            s1 = set(str2numbers(keys[i]))
            s2 = set(str2numbers(keys[j]))
            D = s1^s2
            if len(D) == 2:         
                # Check prune or not
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
                        checkkey = set2key(bs|D)
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


def key2set(s):#Convert key/str to set
    s = str2numbers(s)
    s.sort()
    s = set(s)
    return s

def set2list(Dict): # Convert set value of a dictionary to list value
    for k,v in Dict.items():
        Dict[k] = list(v)
    return Dict

def set2key(s): #Convert set to key/str
    # First convert to list
    s = list(s)
    s = list2key(s)
    return s

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
    if len(itemset.keys()) != 0:
        return
    for data in input_data:
        Id = data[0]
        item = data[2]
        if Id in itemset.keys():
            itemset[Id].add(item)
        else:
            itemset[Id] = {item}
            
    itemset = set2list(itemset)
            
def prune(L,minsup):
    delete = []
    global itemset
    T = len(itemset.keys())
    for k,v in L.items():
        #print(f"{k}:{v}")
        if v<minsup:
            delete.append(k)
    print(f"Prune {len(delete)} item")
    for d in delete:
        del L[d]
    return L

def sort_itemset(resort = False,freq_table = None):
    global itemset
    if resort == False:
        for k,v in itemset.items():
            itemset[k].sort()
    else:
        for k,v in itemset.items():
            itemset[k] = sorted(itemset[k], key = lambda item : get_count(item,freq_table),reverse = True)
        
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

def cal_sup(rule,L):
    global itemset
    s1 = set(str2numbers(rule[0]))
    s2 = set(str2numbers(rule[1]))
    s = s1 | s2
    s_list = list(s)
    s_list.sort()
    key = list2str(s_list)
    num = L[len(s1)-1][rule[0]]
    den = len(itemset.keys())
    return float(num/den)

def gen_rule(Lk,min_conf):
    Rules = []
    for i in range(len(Lk)-1,0,-1): # Ignore L1 as it cannot form a rule
        for k,v in Lk[i].items():
            # Generate the first layer of rule
            rules = gen_r1(k)
            #print(f"First layer rules:{rules}")
            
            #Prune rule less than min_conf
            rules = prune_rule(rules,min_conf,Lk)
            
            # Generate rule by merging 2 rules
            
            while True:
                Rules.append(rules)
                newrules = gen_r(rules)
                #Prune new rules
                rules = prune_rule(newrules,min_conf,Lk)
                
                if len(rules)== 0:
                    break
    # Flatten list
    Rules = [rule for rules in Rules for rule in rules]
    #print(f"Total rules:{len(Rules)}")
    return Rules
            
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
        #print(f"conf for {r} = {conf}")
        if conf<min_conf:
            remove_rule.append(r)
    #print(f"Prune {len(remove_rule)} rule")
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
    #print(f"new rules generated by merges:{new_rules}")
    return new_rules

@timer
def apriori(input_data, a):
    global itemset
    generate_itemset(input_data)
    
    minsup = int(round(a.min_sup*len(itemset))) #For accelerate
    min_conf = a.min_conf
    '''
    itemset = {'1':[0,1,2],
               '2':[0,3],
               '3':[0,4],
               '4':[0,1,3],
               '5':[1,4],
               '6':[0,4],
               '7':[1,4],
               '8':[0,1,4,2],
               '9':[0,1,4]}
    minsup = 2./9.-0.001
    min_conf = 0.5#a.min_conf
    '''
    sort_itemset()
    L1 = generate_L1(minsup)
    Lk = [L1]
    L = L1
    #print(L1)
    while True:
        L = generate_L(L,minsup,len(Lk)+1)
        if len(L) == 0:
            break
        Lk.append(L)
    #print(Lk)
    
    Rules = gen_rule(Lk,min_conf)
    print("In apriori:")
    return output_rule_data(Rules,Lk)

def output_rule_data(Rules,Lk):
    rule_data = []
    for r in Rules:
        ant = "{"+r[0]+"}"
        con = "{"+r[1]+"}"
        sup = cal_sup(r,Lk)
        conf = cal_conf(r,Lk)
        #print(f"{ant}->{con}, sup = {sup},conf = {conf}")
        sup = round(sup, 3)
        conf = round(conf, 3)
        rule_data.append([ant,con,sup,conf])    
    return rule_data

# FP tree
@timer
def fp_growth(input_data,a):
    global itemset
    generate_itemset(input_data)
    minsup = int(round(a.min_sup*len(itemset))) # For acceleration
    min_conf = a.min_conf
    '''
    itemset = {'1':[0,1,2],
               '2':[0,3],
               '3':[0,4],
               '4':[0,1,3],
               '5':[1,4],
               '6':[0,4],
               '7':[1,4],
               '8':[0,1,4,2],
               '9':[0,1,4]}
    minsup = 2./9.-0.001
    min_conf = 0.5#a.min_conf
    '''
    sort_itemset()
    
    # Construct FP-Tree with L1
    print("Constructing Fp")
    fp,freq_table = cons_FP()
    print("Finish construction")
    
    # Find the order of item
    print("Finding the order of item")
    freq_table = get_order(freq_table)
    print("Finish order_key creation")
    #for k,v in freq_table.items():
    #    print(f"{k}:{v['count']}")
        
    # Rebuild FP-tree to ascending order
    sort_itemset(resort = True,freq_table = freq_table)

    print("Reconstructing Fp")
    fp,freq_table = cons_FP()
    print("Finish construction")
    
    # Find the order of item
    print("Finding the order of item")
    freq_table = get_order(freq_table)
    print("Finish order_key creation")
    
    # Find frequent set
    print("Finding frequent set")
    patterns = freq_set(fp,freq_table,minsup)
    print("Finish")
    
    print("Separating patterns")
    Lk = pat_separation(patterns)
    print(Lk)
    print("Finish separation")
    
    # Generate rule
    print("Generating rules")
    Rules = gen_rule(Lk,min_conf)
    rule_data = []
    print("In FP-tree:")
    return output_rule_data(Rules,Lk)

def get_count(item,freq_table):
    return freq_table[item]['count']

def pat_separation(patterns): # Separate patterns found into L1,L2,L3,...
    Lk = []
    for pat,count in patterns.items():
        while True:
            if len(str2numbers(pat))>len(Lk):
                Lk.append(dict())
            else:
                Lk[len(str2numbers(pat))-1][pat] = count
                break
    return Lk
    
    
def cons_FP():
    global itemset
    fp = []
    freq_table = dict()
    for Id,items in itemset.items():
        dfs(items,fp,"",freq_table)
    #print(fp)
    #print(freq_table)
    return fp,freq_table
    
def get_order(freq_table):
    order = dict()
    for item,info in freq_table.items():
        order[item] = info['count']
    order = dict(sorted(order.items(), key=lambda item: item[1]))
    
    for item in order.keys():
        order[item] = freq_table[item]
    return order

# FP-tree data structure:
## Tree: List[Dict]
## Node: Dict with 4 keys: item:(int);count:(int);prefix = 'x1 x2 x3';fnode:(List[Node])/(Tree)
## Leaf: Dict with 4 keys: item:(int);count:(int);prefix = 'x1 x2 x3';fnode:null

# Frequency table
## Table: Dict with 1 key: item->Info
## Info: Dict with 2 keys: count->(int);prefix_set->{'x1 x2 x3','y1 y2 y3 ...'}
def dfs(item,tree,prefix,freq_table):
    if len(item)==0:
        return
    if len(prefix) != 0:
        next_prefix = prefix+" "+str(item[0])
    else:
        next_prefix = str(item[0])
        
    for node in tree:
        if item[0] == node['item']:
            node['count'] += 1
            freq_table[item[0]]['count'] += 1
            dfs(item[1:],node['fnode'],next_prefix,freq_table)
            return
    # Create new node
    Node = {'item':item[0],
            'count':1,
            'prefix':prefix,
            'fnode':[]
    }
    
    # Only add prefix when node is first created
    if item[0] in freq_table.keys():
        freq_table[item[0]]['count'] += 1
        freq_table[item[0]]['prefix_set'].add(prefix)
    else:
        freq_table[item[0]] ={'count': 1,
                         'prefix_set':{prefix}}
    tree.append(Node)
    
    dfs(item[1:],tree[-1]['fnode'],next_prefix,freq_table)
    
def freq_set(fp,table,minsup):
    global itemset
    T = len(itemset)
    
    freq_pats = []
    for item in table.keys():
        # Path addition
        paths = table[item]['prefix_set']
        paths = path_addition(item,paths,fp,minsup)
        freq_pats.append(gen_path(item,paths))
    
    # Merge all the frequent patterns
    patterns = dict()
    for pat_dict in freq_pats:
        for k,v in pat_dict.items():
            patterns[k]=v
            
    # Add L1 by table
    for item,info in table.items():
        if info['count']>=minsup:
            patterns[str(item)] = info['count']
    
    return patterns

def gen_path(item,paths):
    pats = dict()
    for p,v in paths.items():
        pat = str2numbers(p)
        pat.append(item)
        pat = list2key(pat)
        pats[pat] = v
    return pats
        
def path_addition(item,paths,fp,minsup):
    global itemset
    T = len(itemset)
    #print(f"Path addition on item {item}")
    path = dict()
    for p in paths:
        #print(f"Working on {p}")
        p_num = str2numbers(p)
        p_num.append(item)
        path[p] = get_count_path(p_num,fp)
    
    #total = 0
    #for p,count in path.items():
    #    total+=count
    #print(f"{item}: Before addition have:{len(path.keys())}, total path = {total}")
    
    # Add path counting from its subset
    ## Sort the paths from longest to shortest
    p_set = list(map(str2numbers,paths))
    p_set = sorted(p_set,key=len,reverse=True)


    new_path_count = path.copy()
    for i in range(len(p_set)):
        for j in range(i+1,len(p_set)):
            p1 = list2str(p_set[i])
            p2 = list2str(p_set[j])
            if p2 in p1: #p2 is a sub-path of p1
                new_path_count[p2] += path[p1]

    path = new_path_count.copy()
    # Prune path
    #total = 0
    #for p,count in path.items():
    #    total+=count
    #print(f"{item}: Before prune have:{len(path.keys())}, total path = {total}")

    path = prune_path(path,minsup)
    #total = 0
    #for p,count in path.items():
    #    total+=count
    #print(f"{item}: After prune left:{len(path.keys())}, total path = {total}")
    
    # Generate sub-path
    cur_path = path.keys()
    Subpaths = dict()
    for p,count in path.items():
        subpaths = gen_subpath(p)
        for subpath in subpaths:
            if subpath not in cur_path:
                Subpaths[subpath] = count
                #print(f"{p} generates {subpath}")
    for subpath,count in Subpaths.items():
        path[subpath] = count
    return path

def gen_subpath(path):
    path = str2numbers(path)
    path.sort()
    
    # Use binary window:
    bin_win = []
    for i in range(len(path)):
        bin_win.append(0)
        
    paths = []
    while True:
        bin_win = bin_inc(bin_win)
        if bin_win == -1:
            break
        else:
            p_temp = []
            for i in range(len(bin_win)):
                if bin_win[i]==1:
                    p_temp.append(path[i])
            paths.append(list2key(p_temp))
    return paths
        
def bin_inc(bin_win):
    for i in range(len(bin_win)-1,-1,-1):
        if bin_win[i] == 0:
            bin_win[i] = 1
            break
        elif bin_win[i] == 1:
            bin_win[i] = 0
            if i == 0:
                return -1
    return bin_win
    
def prune_path(path,minsup):
    global itemset
    T = len(itemset)
    del_list = []
    for p,v in path.items():
        if v<minsup:
            del_list.append(p)
        elif len(p)==0:
            del_list.append(p)
    #print(f"Prune {len(del_list)} paths")
    for d in del_list:
        path.pop(d,None)
    return path
            
def get_count_path(p_num,fp):
    for root in fp:
        if root['item'] == p_num[0]:
            tree = root
            break
    i = 1
    while True:
        if i == len(p_num):
            return tree['count']
        for node in tree['fnode']:
            if node['item'] == p_num[i]:
                #print(f"Found {i}th node \'{p_num}\' ")
                tree = node
                i+=1
                break
            
    

    
    