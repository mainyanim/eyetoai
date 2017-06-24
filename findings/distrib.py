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
from collections import Counter


#read excel
df = pd.read_excel("output.xlsx")
OUTPUT_FILE = 'report.xlsx'

#read Condition Name into 1D-array
name_arr = df.Name.unique()
name_arr = list(name_arr)


#Choose Params for disease

wb = load_workbook('output.xlsx')
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

#def probslist
import random

def concatvals(row, col, width, start, stop):
    val_arr = []
    prob_head = list(df)[start:stop]
    prob_arr = []
    j = 0
    for i in range(width):
        value_temp = df.iloc[row, col]
        if (isinstance(value_temp, float)) == False:
            value = [x.strip() for x in value_temp.split(',')]
            k = 0
            for k in range(len(value)):
                prob_arr.append(prob_head[i])
                k = k + 1
            for i in range(len(value)):
                val_arr.append(value[i])
        else:
            num_empty = j+1
            for k in range(num_empty-1):
                prob_arr.append(prob_head[i])
                k = k + 1
                for i in range(num_empty):
                    val_arr.append(value[i])
            pass
        col = col+1

    p = normalize(prob_arr)
    randparameter = random.choices(val_arr, prob_arr, k=1)
    return randparameter


def get_dic_from_two_lists(keys, values):
    return { keys[i] : values[i] for i in range(len(keys)) }

#Create random with parameter of report numbers
def report(items):
    for i in range(items):
        br_p = normalize(b)
        a = list(A)
        br = random.choices(a, br_p, k=1)
        name = df['Name'].values.tolist()[0:1]
        "create list of values and slice empty entities from list"
        cd = df['Condition description'].values.tolist()[0:1]
        rm = df['Relevant modalities'].values.tolist()[0:26]
        r = random.choice(rm)
        #mammo params
        if r == 'Mammography':
            f_list = df['Relevant findings'].values.tolist()[0:8]
            #"random finding"
            f = random.choice(f_list)
            if f == 'Mass':
                shape = concatvals(0, 14, 5, 14, 19)
                margin = concatvals(1, 14, 5, 14, 19)
                density = concatvals(2, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Shape', 'Margin', 'Density']
                dict_values = [name, br, cd,r,f, shape, margin, density]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
                #print(report)
            elif f == 'Calcifications':
                t_b = concatvals(3, 14, 5, 14, 19)
                s_morph = concatvals(4, 14, 5, 14, 19)
                distrib = concatvals(5, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Typically benign', 'Suspicious morphology', 'Distribution']
                dict_values = [name, br, cd, r, f, t_b, s_morph, distrib]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'Assymetry':
                a = concatvals(6, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Assymetry']
                dict_values = [name, br, cd, r, f, a]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            else:
                l_nodes = concatvals(7, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Lymph nodes']
                dict_values = [name, br, cd, r, f, l_nodes]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
        elif r == 'US':
            f_list = df['Relevant findings'].values.tolist()[8:15]
            f = random.choice(f_list)
            if f == 'Mass':
                shape = concatvals(8, 14, 5, 14, 19)
                margin = concatvals(9, 14, 5, 14, 19)
                echo = concatvals(10, 14, 5, 14, 19)
                posterior = concatvals(11, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Shape', 'Margin', 'Echo', 'Posterior']
                dict_values = [name, br, cd, r, f, shape, margin, echo, posterior]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'Calcifications US':
                calc = concatvals(12, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Calcifications']
                dict_values = [name, br, cd, r, f, calc]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'Lymph nodes':
                l_nodes = concatvals(13, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Lymph Nodes']
                dict_values = [name, br, cd, r, f, l_nodes]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            else:
                sp_c = concatvals(14, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Special Cases']
                dict_values = [name, br, cd, r, f, sp_c]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
        elif r == 'MRI':
            f_list = df['Relevant findings'].values.tolist()[15:25]
            f = random.choice(f_list)
            if f == 'Mass':
                shape = concatvals(15, 14, 5, 14, 19)
                margin = concatvals(16, 14, 5, 14, 19)
                int_enh = concatvals(17, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Shape', 'Margin', 'Internal enhancement']
                dict_values = [name, br, cd, r, f, shape, margin, int_enh]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'MRI featues':
                mri_f = concatvals(18, 14, 5, 14, 19)
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'MRI features']
                dict_values = [name, br, cd, r, f, mri_f]
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'Kinetic curve assessment':
                kin_c_a = concatvals(19, 14, 5, 14, 19)
                dict_values = [name, br, cd, r, f, kin_c_a]
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Kinetic curve assessment']
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'Non-mass enhancement (NME)':
                distrib = concatvals(20, 14, 5, 14, 19)
                int_enh_patt = concatvals(21, 14, 5, 14, 19)
                dict_values = [name, br, cd, r, f, distrib, int_enh_patt]
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Relevant Finding', 'Distribution','Internal enhacement patterns']
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'Non-enhancing findings':
                nef = concatvals(22, 14, 5, 14, 19)
                dict_values = [name, br, cd, r, f, nef]
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Non-enhancing patterns']
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            elif f == 'Lymph nodes':
                l_nodes = concatvals(22, 14, 5, 14, 19)
                dict_values = [name, br, cd, r, f, l_nodes]
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Lymph nodes']
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)
            else:
                fcl = concatvals(23, 14, 5, 14, 19)
                dict_values = [name, br, cd, r, f, fcl]
                dict_keys = ['Name', 'BiRad', 'Condition description', 'Relevant Modality', 'Fat containing lesions']
                data = get_dic_from_two_lists(dict_keys, dict_values)
                report = json.dumps(data)
                print(report)

reports = report(100)

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
