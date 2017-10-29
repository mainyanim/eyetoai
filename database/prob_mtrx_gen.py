from interface import *
from db_config import *
import numpy as np
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


#mass
names = list(db.reportsNew.aggregate(get_parameter_names("Mammography", "Mass")))[0]['uniqueValues']
print(names)
mass = []
for name in names:
    values_arr = list(db.reportsNew.aggregate(get_value("Mammography", "Mass", name)))[0]['uniqueValues']
    mass += [values_arr]
    # 3 arrays, create combination for each row, add to new element of arr

#calc
names = list(db.reportsNew.aggregate(get_parameter_names("Mammography", "Calcifications")))[0]['uniqueValues']
print(names)
calc = []
for name in names:
    values_arr = list(db.reportsNew.aggregate(get_value("Mammography", "Calcifications", name)))[0]['uniqueValues']
    calc += [values_arr]

#assymetry
names = list(db.reportsNew.aggregate(get_parameter_names("Mammography", "Assymetry")))[0]['uniqueValues']
print(names)
assym = []
for name in names:
    values_arr = list(db.reportsNew.aggregate(get_value("Mammography", "Assymetry", name)))[0]['uniqueValues']
    assym += [values_arr]

#lymph nodes
names = list(db.reportsNew.aggregate(get_parameter_names("Mammography", "Lymph nodes")))[0]['uniqueValues']
print(names)
lnodes = []
for name in names:
    values_arr = list(db.reportsNew.aggregate(get_value("Mammography", "Lymph nodes", name)))[0]['uniqueValues']
    lnodes += [values_arr]

values = [mass, calc, assym, lnodes]


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
for e in values:
    new_data+=[cartesian(e)]

print(len((new_data)), new_data)