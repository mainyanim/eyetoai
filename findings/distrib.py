import pandas as pd
import numpy as np
import random
import json
from openpyxl import load_workbook
from openpyxl import Workbook
import numpy as np
import math
#define values check and append to arr
#define probability array
#read excel

df = pd.read_excel("output.xlsx")
wb = load_workbook('output.xlsx')
ws = wb.get_sheet_by_name('Sheet1') #Define worksheet



def get_dic_from_two_lists(keys, values):
    return { keys[i] : values[i] for i in range(len(keys)) }

#Define function to normalize arr values
def normalize(items):
    problist = [x/sum(items) for x in items]
#def probslist

def concatvals(row, start, stop):
    prob_head = list(df)[start:stop]
    width = stop-start
    col = start
    val_arr = []
    prob_arr = []
    for i in range(width):
        value_temp = df.iloc[row, col]
        if isinstance(value_temp, float) is False:
            value = [x.strip() for x in value_temp.split(',')]
            for k in range(len(value)):
                prob_arr.append(prob_head[i])
            for i in range(len(value)):
                val_arr.append(value[i])
        col+=1
    randparameter = random.choices(val_arr, prob_arr, k = 1)
    return randparameter
    print(val_arr,prob_arr, randparameter)

def get_name(infile):
    with open(infile, 'r') as f:
        contents_of_file = f.read()
        lines = contents_of_file.splitlines()
    line_number = random.randrange(0, len(lines))
    person_name = lines[line_number]
    return person_name

def get_cond_name():
    name_arr = df.Name.unique()
    n = list(name_arr)
    n_arr = []
    for i in range(len(name_arr)):
        if (isinstance(n[i], float)) is False:
            n_arr += [n[i]]
    rand_cond_name = random.choice(n_arr)
    return rand_cond_name

def check_row(cond_name):
    from xlrd import open_workbook
    book = open_workbook("output.xlsx")
    for sheet in book.sheets():
        for rowidx in range(sheet.nrows):
            row = sheet.row(rowidx)
            for colidx, cell in enumerate(row):
                if cell.value == cond_name :
                    return rowidx+1


#Create random with parameter of report numbers
def generate_report(items, infile):
    data_list = []
    for i in range(items):
        a = np.array([[i.value for i in j] for j in ws['C1':'I1']]).ravel()
        b = np.array([[i.value for i in j] for j in ws['C2':'I2']]).ravel()
        #Read BiRads Probabilities into list
        #Read BiRads into list
        person_name = get_name(infile)
        p_id = random.randrange(100)
        p_age = random.randrange(25, 65)
        br_p = normalize(b)
        br = random.choices(a, br_p, k=1)
        #Random condition name
        name = get_cond_name()
        row = check_row(name)
        print(row)
        "create list of values and slice empty entities from list"
        rm = df['Relevant modalities'].values.tolist()[0:26]
        r = 'Mammography'
        #r = random.choice(rm)
        dict_keys = ['Id', 'First name', 'Age', 'Condition Name', 'BiRad', 'Relevant Modality']
        dict_values = [p_id, person_name, p_age, name, br, r]
        #mammo params

        if r == 'Mammography':
            f_list = df['Relevant findings']
            #f = random.choice(f_list)
            f = 'Mass'
            if f == 'Mass':
                shape = concatvals(0, 14, 19) #if row = 0
                margin = concatvals(1, 14, 19) #here row should be 1
                density = concatvals(2, 14, 19) # and here 2 - how can I achieve that?
                dict_keys += ['Relevant Finding','Shape', 'Margin', 'Density']
                dict_values += [f, shape, margin, density]

            elif f == 'Calcifications':
                t_b = concatvals(3, 14, 5, 14, 19)
                s_morph = concatvals(4, 14, 5, 14, 19)
                distrib = concatvals(5, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Typically benign', 'Suspicious morphology', 'Distribution']
                dict_values += [f, t_b, s_morph, distrib]
                #print(report)
            elif f == 'Assymetry':
                a = concatvals(6, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Assymetry']
                dict_values += [f, a]
            #print(report)
            else:
                l_nodes = concatvals(7, 14, 5, 14, 19)
                dict_keys += ['Lymph nodes']
                dict_values += [l_nodes]
                #print(report)
        elif r == 'US':
            f_list = df['Relevant findings'].values.tolist()[8:15]
            f = random.choice(f_list)
            if f == 'Mass':
                shape = concatvals(8, 14, 5, 14, 19)
                margin = concatvals(9, 14, 5, 14, 19)
                echo = concatvals(10, 14, 5, 14, 19)
                posterior = concatvals(11, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Shape', 'Margin', 'Echo', 'Posterior']
                dict_values += [f, shape, margin, echo, posterior]

                #print(report)
            elif f == 'Calcifications US':
                calc = concatvals(12, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Calcifications']
                dict_values += [f, calc]

            elif f == 'Lymph nodes':
                l_nodes = concatvals(13, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Lymph Nodes']
                dict_values += [f, l_nodes]

                #print(report)
            else:
                sp_c = concatvals(14, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Special Cases']
                dict_values += [f, sp_c]

                #print(report)
        elif r == 'MRI':
            f_list = df['Relevant findings'].values.tolist()[15:25]
            f = random.choice(f_list)
            if f == 'Mass':
                shape = concatvals(15, 14, 5, 14, 19)
                margin = concatvals(16, 14, 5, 14, 19)
                int_enh = concatvals(17, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Shape', 'Margin', 'Internal enhancement']
                dict_values += [f, shape, margin, int_enh]

                #print(report)
            elif f == 'MRI featues':
                mri_f = concatvals(18, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'MRI features']
                dict_values += [f, mri_f]

                #print(report)
            elif f == 'Kinetic curve assessment':
                kin_c_a = concatvals(19, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Kinetic curve assessment']
                dict_values += [f, kin_c_a]

                #print(report)
            elif f == 'Non-mass enhancement (NME)':
                distrib = concatvals(20, 14, 5, 14, 19)
                int_enh_patt = concatvals(21, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding', 'Distribution','Internal enhacement patterns']
                dict_values += [f, distrib, int_enh_patt]

                #print(report)
            elif f == 'Non-enhancing findings':
                nef = concatvals(22, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding','Non-enhancing patterns']
                dict_values += [f, nef]

                #print(report)
            elif f == 'Lymph nodes':
                l_nodes = concatvals(22, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding','Lymph nodes']
                dict_values += [f, l_nodes]

            else:
                fcl = concatvals(23, 14, 5, 14, 19)
                dict_keys += ['Relevant Finding','Fat containing lesions']
                dict_values += [f, fcl]

                #print(report)
        data = get_dic_from_two_lists(dict_keys, dict_values)
        data_list.append(data)
        report_temp = json.dumps(data_list)
    print(report_temp)

def main():
    reports = generate_report(5, "first-names.txt")
main()
#define values check

#report general outlook
#name
#condition description
#birad
#relevant modality
#unique findings
#additional info
#parameters + value_according_to_prob
#Pathogenomonic
#Negative
#Ignore
#Associated conditions
#Differential_diagnosis
#notes
