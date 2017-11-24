import pandas as pd
import numpy as np
from pymongo import MongoClient
from config_chatbot import *
import math

df = pd.read_excel('testmammo5.xlsx')
df2 = df.set_index("condlist")


"""
author: Alexandra Zhuravlyov
ai_ranking is an algorithm that shows probability of a specific condition given an array of symptoms
"""

client = MongoClient("mongodb://yuri:rxLPDCJPXWHOozeV@cluster0-shard-00-00-lnxfa.mongodb.net:27017,"
                     "cluster0-shard-00-01-lnxfa.mongodb.net:27017,cluster0-shard-00-02-lnxfa.mongodb.net:27017/test?ssl=true&replicaSet="
                     "Cluster0-shard-0&authSource=admin")
db = client.eyetoai
findings = db.fill.distinct("conditions.findings.name", {"modality": "Mammography"})

def increase(d, c):
    temp = [d[key] for key in d]
    coll = np.array(temp)
    newmatrix = coll * c
    return newmatrix



def entr(maxentrd, entrd, arr):
    max_key = max(maxentrd, key=lambda k: maxentrd[k])
    ch_f = str(input("Is there " + max_key + "?"))
    if max_key in arr:
        data = list(df[max_key])
        if ch_f.lower() == "yes":
            del entrd[max_key]
            modality = "Mammography"
            user_input = []
            finding_input = {}
            finding_input["name"] = max_key
            names = list(db.fill.aggregate(get_parameter_names(modality, max_key)))[0]['uniqueValues']
            parameters_input = []
            for name in names:
                values_arr = list(db.fill.aggregate(get_value(modality, max_key, name)))[0]['uniqueValues']
                value = str(input(name + ' is: ' + str(values_arr)))
                parameters_input.append((name, value))
            finding_input["parameters"] = parameters_input
            print(finding_input["parameters"])
            user_input.append(finding_input)
            print(user_input)
            probs = []
            finding_dict = dict((key, value) for (key, value) in zip(df["condlist"], data))
            print(finding_dict)
            for condition in list(df["condlist"]):
                cursor_c0 = db.fill.find({"conditions.conditionName": condition}).count()  # total number of specific conditions
                cursor_findings = [db.fill.find(get_f_params_val(modality, condition, ui)).count() for ui in user_input]
                cursor_cond = db.fill.aggregate([{"$unwind": "$conditions"}, {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])
                print("number of conditions with selected parameters is: ", cursor_findings)
                if sum(cursor_findings)!=0:
                    if 0 in cursor_findings:
                        selected_f = min(filter(lambda x: x !=0,cursor_findings))
                        print(selected_f)
                    else:
                        selected_f = min(cursor_findings)  # total number of condition with values
                    if cursor_c0:
                        total = sum(result['sum'] for result in cursor_cond) # total number of reports in the database (splitted)
                        if total:
                            p_v_ci = selected_f / cursor_c0 # P(Values | Ci)
                            p_ci = cursor_c0 / total # specific condition / total num of reports
                            prob = p_v_ci * p_ci * finding_dict[condition] # P(Ci | val)
                            print(prob, finding_dict[condition], condition)
                            if prob!=0:
                                probs+=[{"id": condition, "entropy": prob}]
                else:
                    probs += [{"id": condition, "entropy": 0}]
            entropy = -sum(item['entropy'] *math.log2(item['entropy']) for item in probs)
            for key in entrd:
                entrd[key] = [entropy * key for key in entrd[key]]
            print("entr for", max_key, "is: ",entropy)
            print(entrd)
            return entr
        elif ch_f.lower() == 'no':
            del entrd[max_key]
            entropy = 1
            for key in entrd:
                entrd[key] = [entropy * key for key in entrd[key]]
            print("entr for", max_key, "is: ", entropy)
            print(entrd)
            return entr


"""
for key in a:
    print(key)
    
a
b
c
keys = [key for key in a]
keys
Out[60]: 
['a', 'b', 'c']
a
Out[61]: 
{'a': [1, 2], 'b': [3, 4], 'c': [5, 6]}
keys
Out[62]: 
['a', 'b', 'c']
ui = input('key?')
key?>? a
for i in range(len(keys)-1):
    if ui in keys:
        del a[ui]
        for k in a:
            a[k] = [2*k for k in a[k]]  
            x = max(a, key = lambda k: a[k])
print(a)

"""


def get_params():
    elems = []
    for elem in findings:
        names = list(db.fill.aggregate(get_parameter_names("Mammography", elem)))[0]['uniqueValues']
        elems_tmp = []
        for name in names:
            values_arr = list(db.fill.aggregate(get_value("Mammography", elem, name)))[0]['uniqueValues']
            elems_tmp += [values_arr]
        elems += [elems_tmp]
    return elems

    # 3 arrays, create combination for each row, add to new element of arr
    # check if works for f_list - should reduce next lines
def cartesian(arrays, out=None):
    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype
    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)
    m = n // arrays[0].size
    out[:, 0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m, 1:])
        for j in range(1, arrays[0].size):
            out[j * m:(j + 1) * m, 1:] = out[0:m, 1:]
    return out



if __name__ == '__main__':
    entropy_arr = []
    heads = df2.columns.tolist()
    print(heads)
    calc = df2['Calcifications'].values
    assym = df2['Assymetry'].values
    lnodes = df2['Lymph nodes'].values
    mass = df2['Mass'].values
    entropy_arr = [calc, assym, lnodes, mass]
    entr_dict = dict((key, value) for (key, value) in zip(heads, entropy_arr))
    max_dict = dict((key, value) for (key, value) in zip(heads, df2.loc[:, heads].max()))
    entr(max_dict,entr_dict,heads)
    for x in range(len(entr_dict)):
        entr(entr_dict,entr_dict,heads)
