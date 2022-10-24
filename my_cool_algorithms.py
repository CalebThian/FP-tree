itemset = dict()

# Generate Frequent Itemset

def generate_L(L,minsup,k):
    global itemset
    print(f"Generating L{k}")
    Lk = dict()
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
    print(Lk)
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


def key2set(s):#Convert key/str to set
    s = str2numbers(s)
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
    for data in input_data:
        Id = data[0]
        item = data[2]
        if Id in itemset.keys():
            itemset[Id].add(item)
        else:
            itemset[Id] = set([item])
            
    itemset = set2list(itemset)
            
def prune(L,minsup):
    delete = []
    global itemset
    T = len(itemset.keys())
    for k,v in L.items():
        #print(f"{k}:{v}")
        sup = float(v/T)
        if sup<minsup:
            delete.append(k)
    print(f"Prune {len(delete)} item")
    for d in delete:
        del L[d]
    return L

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
            #print(rules)
            
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
    '''                
    # Print the rules with sup and conf
    for k,rules in enumerate(Rules):
        print(f"Rule with {k+1} element on left")
        for r in rules:
            print(f"{r[0]}->{r[1]}, sup = {cal_sup(r,Lk)},conf = {cal_conf(r,Lk)}")
    '''
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
    
    minsup = a.min_sup
    min_conf = a.min_conf
    '''
    itemset = {'1':[0,3,1,2],
               '2':[1,2,5],
               '3':[1,4],
               '4':[0,1,2,3]}
    minsup = 2
    min_conf = 0.7#a.min_conf
    '''
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
    
    Rules = gen_rule(Lk,min_conf)
    rule_data = []
    print("In apriori:")
    for r in Rules:
        ant = key2set(r[0])
        con = key2set(r[1])
        sup = cal_sup(r,Lk)
        conf = cal_conf(r,Lk)
        print(f"{ant}->{con}, sup = {sup},conf = {conf}")
        sup = round(sup, 3)
        conf = round(conf, 3)
        rule_data.append([ant,con,sup,conf])    
    return rule_data


# FP tree
def fp_growth(input_data,a):
    global itemset
    generate_itemset(input_data)
    minsup = a.min_sup
    min_conf = a.min_conf
    
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
    min_conf = 0.7#a.min_conf
    sort_itemset()
    
    # Construct FP-Tree with L1
    fp,freq_table = cons_FP(minsup)
    
    # Find the order of obect
    order_key = get_order(freq_table)
    
    # Find frequent set
    patterns = freq_set(fp,freq_table,order_key,minsup)
    print(patterns)
    
def cons_FP(minsup):
    global itemset
    fp = []
    freq_table = dict()
    for Id,items in itemset.items():
        dfs(items,fp,"",freq_table)
    print(fp)
    print(freq_table)
    return fp,freq_table
    
def get_order(freq_table):
    order = dict()
    for item,info in freq_table.items():
        order[item] = info['count']
    order = dict(sorted(order.items(), key=lambda item: item[1]))
    return order.keys()


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
            dfs(item[1:],node['fnode'],next_prefix,freq_table)
            freq_table[item[0]]['count'] += 1
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
    
def freq_set(fp,table,order,minsup):
    global itemset
    T = len(itemset)
    
    freq_pats = []
    for item in order:
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
        if float(info['count']/T)>=minsup:
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
    
    path = dict()
    for p in paths:
        p_num = str2numbers(p)
        p_num.append(item)
        path[p] = get_count_path(p_num,fp)
    print(item,path)
    
    # Add path counting from its subset
    ## Sort the paths from longest to shortest
    p_set = list(map(str2numbers,paths))
    p_set = sorted(p_set,key=len,reverse=True)

    for i in range(len(p_set)):
        for j in range(i+1,len(p_set)):
            p1 = list2str(p_set[i])
            p2 = list2str(p_set[j])
            if p2 in p1: #p2 is a sub-path of p1
                path[p2] += path[p1]
                # If longer path will be pruned, perform addition once, else perform on all
                if float(path[p1]/T)<minsup:
                    break
    # Prune path
    path = prune_path(path,minsup)
    
    # Generate sub-path
    cur_path = path.keys()
    Subpaths = dict()
    for p,count in path.items():
        subpaths = gen_subpath(p)
        for subpath in subpaths:
            if subpath not in cur_path:
                Subpaths[subpath] = count
                print(f"{p} generates {subpath}")
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
        sup = float(v/T)
        if sup<minsup:
            del_list.append(p)
        elif len(p)==0:
            del_list.append(p)
    print(f"Prune {len(del_list)} paths")
    for d in del_list:
        del path[d]
    return path
            
def get_count_path(p_num,fp):
    for root in fp:
        if root['item'] == p_num[0]:
            tree = root
    i = 1
    while True:
        if i>=len(p_num):
            return tree['count']
        for node in tree['fnode']:
            if node['item'] == p_num[i]:
                tree = node
                i+=1
                break
            
    

    
    