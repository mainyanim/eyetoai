import pandas as pd
import numpy as np
import random
import json
from openpyxl import load_workbook
from openpyxl import Workbook
import numpy as np

#read excel
df = pd.read_excel("output.xlsx")[0:25]

#read Condition Name into 1D-array
name_arr = df.Name.unique()
name_arr = list(name_arr)


#Choose Params for disease

wb = load_workbook('output.xlsx') #Define workbook
ws = wb.get_sheet_by_name('Sheet1') #Define worksheet

A = np.array([[i.value for i in j] for j in ws['C1':'I1']]).ravel() #Read BiRads into list
B = np.array([[i.value for i in j] for j in ws['C2':'I2']]).ravel() #Read BiRads Probabilities into list
C = np.array([[i.value for i in j] for j in ws['O1':'Q1']]).ravel() #Read Params Probabilities into list

#Convert from np-arr to 1D arr

a = list(A) #BiRads list
b = list(B) #BiRad probs integer values
c = list(C) #Params probs integer values

#Define function to normalize arr values

def normalize(items):
    sum_n = 0
    for x in items:
        sum_n += x
    problist = [x/sum_n for x in items]
    return(problist)


#Create random with parameter of report numbers
def report(num):
    for i in range(num):
        br_p = normalize(b)
        a = list(A)
        br = np.random.choice(a, 1, br_p)
        name = df['Name'].values.tolist()[0:1]
        "create list of values and slice empty entities from list"
        cd = df['Condition description'].values.tolist()
        rm = df['Relevant modalities'].values.tolist()
        r = random.choice(rm)
        #mammo params
        if r == 'Mammography':
            f_list = df['Relevant findings'].values.tolist()[0:9]
            "random finding"
            f = random.choice(f_list)
            if f == 'Mass':
                p = normalize(c)
                s = np.array([[i.value for i in j] for j in ws['O2':'Q2']]).ravel()
                s = list(s)
                shape = np.random.choice(s, 1, p)
                m = np.array([[i.value for i in j] for j in ws['O3':'Q3']]).ravel()
                m = list(m)
                margin = np.random.choice(m, 1, p)
                d = np.array([[i.value for i in j] for j in ws['O4':'Q4']]).ravel()
                d = list(d)
                density = np.random.choice(d, 1, p)
                print(name, br, r, f, shape, margin, density)
            elif f == 'Calcifications':
                p = normalize(c)
                tb = np.array([[i.value for i in j] for j in ws['O5':'Q5']]).ravel()
                tb = list(tb)
                t_benigh = np.random.choice(tb, 1, p)
                sm = np.array([[i.value for i in j] for j in ws['O6':'Q6']]).ravel()
                sm = list(sm)
                s_morph = np.random.choice(sm, 1, p)
                d = np.array([[i.value for i in j] for j in ws['O7':'Q7']]).ravel()
                d = list(d)
                distrib = np.random.choice(d, 1, p)
                print(name, br, r, f, tb, s_morph, distrib)
            elif f == 'Assymetry':
                p = normalize(c)
                a = np.array([[i.value for i in j] for j in ws['O8':'Q8']]).ravel()
                a = list(a)
                assymetry = np.random.choice(a, 1, p)
                print(name, br, r, f, assymetry)
            else:
                p = normalize(c)
                ln = np.array([[i.value for i in j] for j in ws['O9':'Q9']]).ravel()
                ln = list(ln)
                print(name, br, r, f, ln)
        #us params
        elif r == 'US':
            f_list = df['Relevant findings'].values.tolist()[10:16]
            f = random.choice(f_list)
            if f == 'Mass':
                p = normalize(c)
                s = np.array([[i.value for i in j] for j in ws['O10':'Q10']]).ravel()
                s = list(s)
                shape = np.random.choice(s, 1, p)
                m = np.array([[i.value for i in j] for j in ws['O11':'Q11']]).ravel()
                m = list(m)
                margin = np.random.choice(m, 1, p)
                e = np.array([[i.value for i in j] for j in ws['O12':'Q12']]).ravel()
                e = list(e)
                echo = np.random.choice(e, 1, p)
                pos = np.array([[i.value for i in j] for j in ws['O13':'Q13']]).ravel()
                pos = list(pos)
                posterior = np.random.choice(pos, 1, p)
                print(name, br, r, f, shape, margin, echo, posterior)
            elif f == 'Calcifications US':
                p = normalize(c)
                calc = np.array([[i.value for i in j] for j in ws['O14':'Q14']]).ravel()
                calc = list(calc)
                calc_us = np.random.choice(calc, 1, p)
                print(name, br, r, f, calc_us)
            elif f == 'Lymph nodes':
                p = normalize(c)
                ln = np.array([[i.value for i in j] for j in ws['O15':'Q15']]).ravel()
                ln = list(ln)
                l_nodes = np.random.choice(ln, 1, p)
                print(name, br, r, f, l_nodes)
            else:
                p = normalize(c)
                sc = np.array([[i.value for i in j] for j in ws['O16':'Q16']]).ravel()
                sc = list(sc)
                sp_cases = np.random.choice(sc, 1, p)
                print(name, br, r, f, sp_cases)
        else:
            f_list = df['Relevant findings'].values.tolist()[17:25]
            f = random.choice(f_list)
            if f == 'Mass':
                p = normalize(c)
                s = np.array([[i.value for i in j] for j in ws['O17':'Q17']]).ravel()
                s = list(s)
                shape = np.random.choice(m, 1, p)
                m = np.array([[i.value for i in j] for j in ws['O18':'Q18']]).ravel()
                m = list(m)
                margin = np.random.choice(m, 1, p)
                ie = np.array([[i.value for i in j] for j in ws['O19':'Q19']]).ravel()
                ie = list(ie)
                int_e = np.random.choice(ie, 1, p)
                print(name, br, r, f, shape, margin, int_e)
            elif f == 'MRI features':
                p = normalize(c)
                m_f = np.array([[i.value for i in j] for j in ws['O20':'Q20']]).ravel()
                m_f = list(m_f)
                mri_f = np.random.choice(m_f, 1, p)
                print(name, br, r, f, mri_f)
            elif f == 'Kinetic curve assessment':
                p = normalize(c)
                kca = np.array([[i.value for i in j] for j in ws['O21':'Q21']]).ravel()
                kca = list(kca)
                kin_ca = np.random.choice(kca, 1, p)
                print(name, br, r, f, kin_ca)
            elif f == 'Non-mass enhancement (NME)':
                p = normalize(c)
                distr = np.array([[i.value for i in j] for j in ws['O22':'Q22']]).ravel()
                distr = list(distr)
                distrib = np.random.choice(distr, 1, p)
                iep = np.array([[i.value for i in j] for j in ws['O23':'Q23']]).ravel()
                print(name, br, r, f, distrib, iep)
            elif f == 'Non-enhancing findings':
                p = normalize(c)
                nef = np.array([[i.value for i in j] for j in ws['O21':'Q22']]).ravel()
                nef = list(nef)
                ne_f = np.random.choice(nef, 1, p)
                print(name, br, r, f, ne_f)
            elif f == 'Lymph nodes':
                p = normalize(c)
                ln = np.array([[i.value for i in j] for j in ws['O22':'Q22']]).ravel()
                ln = list(ln)
                l_nodes = np.random.choice(ln, 1, p)
                print(name, br, r, f, l_nodes)
            else:
                p = normalize(c)
                fcl = np.array([[i.value for i in j] for j in ws['O23':'Q23']]).ravel()
                fcl= list(fcl)
                fat_cl = np.random.choice(fcl, 1, p)
                print(name, br, r, f, fat_cl)


un_list = df['Unique findings'].values.tolist()
un = random.choice(un_list)
p_list = df['Parameters'].values.tolist()
p = random.choice(p_list)
g_list = df['General'].values.tolist()
g = random.choice(g_list)
u_list = df['Unrelated'].values.tolist()
u = random.choice(u_list)
i_list = df['Ignore'].values.tolist()
i = random.choice(i_list)
a_list = df['Associated conditions'].values.tolist()
a = random.choice(a_list)
dd_list = df['Differential diagnosis'].values.tolist()
dd = random.choice(dd_list)
nt_list = df['Notes'].values.tolist()
nt = random.choice(nt_list)

"""
params = ["condition description", "relevant finding", "unique finding", "parameters", "general", "unrelated", "ignore", "associated conditions", "notes"]
keys = [cd, f, un, p, g, u, i, a, dd, nt]

rep = {}
for i in range(len(params)):

    rep[params[i]] = keys[i]

rep = json.dumps(rep)
#print(rep) """
"""
def get_names_and_probs(row, col):
    first_row = row
    first_col = col
    array_to_normalize = [] #the "a" array
    p_values = [] #the "p" array
    i = 0
    for i in range(3):

        #determine if cell has text, or is empty
        if isinstance(df.iloc[first_row, first_col + i], float): #if cell is empty, python calls it a float
            i = i+1
            continue
        temp_array = df.iloc[first_row, first_col + i].replace(" ","").split(",") #look at a cell
        j = 0
        for j in range(len(temp_array)):
            p_values.append(df.iloc[0,first_col + i])
            j = j+1
        array_to_normalize.append(temp_array)
        i = i+1
        #array_to_normalize looks like [["oval","rectangular], "irregular"]
        #p_values looks like [50, 50 , 1]

    #flatten array_to_normalize
    #https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    flat_list = [item for sublist in array_to_normalize for item in sublist]
    #for sublist in array_to_normalize:
    #    for item in sublist:
    #        flat_list.append(item)
    array_to_normalize = flat_list
    print(array_to_normalize)

    #now array to normalize should look like ['Oval', 'Round', 'Irregular']

    #a = ['Oval', 'Round', 'Irregular'] #for each row
    #p = [50, 50, 1] #one for the entire sheeet

    #convert p_values from array of strings to array of ints
    #https://stackoverflow.com/questions/5306079/python-how-do-i-convert-an-array-of-strings-to-an-array-of-numbers
    #p_values = map(int, p_values)
    #p_values = [int(numeric_string) for numeric_string in p_values]

    #normalize p_values / "p array"
    normalize(p_values)
    return array_to_normalize, p_values
# ['Oval', 'Round', 'Irregular'] , [50, 50, 1]
get_names_and_probs(1, 15)





#row = starting row of condition
#return array of arrays for condition
# pri[[a,p],[['Oval', 'Round', 'Irregular'],[50, 50, 1]],...25 times] """

#define values check
import math

def check_celval(row, col, width):
    val_arr = []
    for i in range(width):
        value_temp = df.iloc[row, col]
        if (isinstance(value_temp, float)) == False:
            value = value_temp.replace(" ","").split(",")
            for i in range(len(value)):
                val_arr.append(value[i])
            else:
                pass
        col = col+1
    print(val_arr)

check_celval(1, 14, 3)
