from interface import *
from db_config import *
import numpy as np
import pandas as pd
from db_test import db_conditions


"""
1. generate np.array([m_round,m_obsc, m_low .. ], [f2_p1, f2_p2], ..])
2. calculate median for each element in a row
3. each row relates to condition
4. Pr(F) = E P (Param|Ci) * P (param), where p Param = cell, P (Param|Ci) from interface 
5. Pr (C| EX, F) = P (EX, F | C) * P (C) 
6. Entropy = 

Pr (EX| C) * Pr (F|C) * Pr (C) = P in Entropy
H = - E *log 2 (P)

"""

"""
1.1. for each finding get all parameters
1.2 for each parameters get all combinations 
1.3 generate vector

"""

import itertools


findings = db.fill.distinct("conditions.findings.name", {"modality": "Mammography"})
#print(findings)
#check if query works

def get_params():
    elems = []
    for elem in findings:
        names = list(db.fill.aggregate(get_parameter_names("Mammography", elem)))[0]['uniqueValues']
        elems_tmp = []
        for name in names:
            values_arr = list(db.fill.aggregate(get_value("Mammography", elem, name)))[0]['uniqueValues']
            elems_tmp += [values_arr]
        elems+=[elems_tmp]
    return elems

    # 3 arrays, create combination for each row, add to new element of arr
    # check if works for f_list - should reduce next lines

def mean(arr):
    return float(sum(arr)) / max(len(arr), 1)


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


new_data = []
for e in get_params():
    new_data+=[cartesian(e)]
#print(new_data)
db_condlist = db.fill.distinct("conditions.conditionName")
print(new_data[0], new_data[1], new_data[3])

mass_cond = []
calc_cond = []
assym_cond = []
lnodes_cond = []

for cond in db_condlist:
    calc_mean = []
    for j in new_data[0]:
        parameters_input = []
        user_input = []
        finding_input = {}
        finding_input["name"] = "Calcifications"
        params = ["Distribution", "Suspicious morphology", "Typically benign"]
        for param in range(len(params)):
            name = params[param]
            value = j[param]
            parameters_input.append((name, value))
            finding_input["parameters"] = parameters_input[::-1]
        user_input.append(finding_input)
        cursor_findings = [db.fill.find(get_f_params_val("Mammography", cond, ui)).count() for ui in user_input]
        calc_mean += cursor_findings

    norm = [float(i) / sum(calc_mean) for i in calc_mean]
    calc_mean_final = mean(norm)
    calc_cond += [calc_mean_final]
    print("Calc mean for", cond, "is: ", calc_mean_final)


for cond in db_condlist:
    lnodes_mean = []
    for j in new_data[1]:
        parameters_input = []
        user_input = []
        finding_input = {}
        finding_input["name"] = "Lymph nodes"
        params = ["Lymph nodes"]
        for param in range(len(params)):
            name = params[param]
            value = j[param]
            parameters_input.append((name, value))
            finding_input["parameters"] = parameters_input[::-1]
        user_input.append(finding_input)
        cursor_findings = [db.fill.find(get_f_params_val("Mammography", cond, ui)).count() for ui in user_input]
        lnodes_mean += cursor_findings

    norm = [float(i) / sum(lnodes_mean) for i in lnodes_mean]
    lnodes_mean_final = mean(norm)
    lnodes_cond += [lnodes_mean_final]
    print("Lymph mean for", cond, "is: ", lnodes_mean_final)

for cond in db_condlist:
    mass_mean = []
    for i in new_data[2]:
        parameters_input = []
        test_r = i
        user_input =[]
        finding_input = {}
        finding_input["name"] = "Mass"
        params = ["Density", "Margin", "Shape"]
        for param in range(len(params)):
            name = params[param]
            value = i[param]
            parameters_input.append((name,value))
            finding_input["parameters"] = parameters_input[::-1]
        user_input.append(finding_input)
        cursor_findings = [db.fill.find(get_f_params_val("Mammography", cond, ui)).count() for ui in user_input]
        mass_mean+=cursor_findings

    norm = [float(i) / sum(mass_mean) for i in mass_mean]
    mass_mean_final = mean(norm)
    mass_cond+=[mass_mean_final]
    print("Mass mean for", cond,  "is: ",mass_mean_final)


for cond in db_condlist:
    assym_mean = []
    for j in new_data[3]:
        parameters_input = []
        user_input = []
        finding_input = {}
        finding_input["name"] = "Assymetry"
        params = ["Assymetry"]
        for param in range(len(params)):
            name = params[param]
            value = j[param]
            parameters_input.append((name, value))
            finding_input["parameters"] = parameters_input[::-1]
        user_input.append(finding_input)
        cursor_findings = [db.fill.find(get_f_params_val("Mammography", cond, ui)).count() for ui in user_input]
        assym_mean += cursor_findings

    norm = [float(i) / sum(assym_mean) for i in assym_mean]
    assym_mean_final = mean(norm)
    assym_cond += [assym_mean_final]
    print("Assym mean for", cond, "is: ", assym_mean_final)


d = {'condlist': db_condlist,'mass': mass_cond, 'calc': calc_cond, 'lymph nodes': lnodes_cond, 'assym': assym_cond}
df = pd.DataFrame(data = d)
df.to_csv('testmammo3', header=True, index = True)

import xlsxwriter
writer_orig = pd.ExcelWriter('testmammo3.xlsx', engine='xlsxwriter')
df.to_excel(writer_orig, index=True, sheet_name='report')
writer_orig.save()

#normalize values
