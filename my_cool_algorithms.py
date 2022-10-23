def generate_L1(input_data,a):
    itemset = generate_itemset(input_data)
    minsup = int(a.min_sup*len(itemset.keys()))
    
    L1 = dict()
    for Id,items in itemset.items():
        for item in items:
            if item in L1.keys():
                L1[item] += 1 
            else:
                L1[item] = 1
    print(len(L1))
    L1 = prune(L1,minsup)
    print(len(L1))
    return L1

def generate_itemset(input_data):
    itemset = dict()
    for data in input_data:
        Id = data[0]
        item = data[2]
        if Id in itemset.keys():
            itemset[Id].append(item)
        else:
            itemset[Id] = [item]
    return itemset
    
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
    L = generate_L1(input_data,a)
    for k,v in L.items():
        print(k,v)
    
