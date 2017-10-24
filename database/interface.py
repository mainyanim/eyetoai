from pymongo import MongoClient
from cond_data import *
from db_config import *
import collections
import numpy as np
from flask import request, abort
import math
import json, requests
import ssl

"""
author: Alexandra Zhuravlyov
ai_ranking is an algorithm that shows probability of a specific condition given an array of symptoms
"""

client = MongoClient("mongodb://yuri:rxLPDCJPXWHOozeV@cluster0-shard-00-00-lnxfa.mongodb.net:27017,"
                     "cluster0-shard-00-01-lnxfa.mongodb.net:27017,cluster0-shard-00-02-lnxfa.mongodb.net:27017/test?ssl=true&replicaSet="
                     "Cluster0-shard-0&authSource=admin")
db = client.eyetoai


def ddata():
    modality = input('Modality is: ')
    #cond = input('Condition you want to check is: ').title()
    find_arr = db.qa2_lnodes.distinct("conditions.findings.name", {"modality": modality})

    num_findings = int(input('How many findings do you have: '))
    user_input = []
    for _ in range(num_findings):
        finding_input = {}
        ch_f = input('Choose finding from the list: ' + str(find_arr))
        finding_input["name"] = ch_f
        parameters_input = []
        if ch_f!='Mass':
            names = list(db.qa2_lnodes.aggregate(get_parameter_names(modality, ch_f)))[0]['uniqueValues']
        else:
            names = list(db.qa2_lnodes.aggregate(get_parameter_names(modality, ch_f)))[0]['uniqueValues']
            print(names)
            if 'Location' in names:
                names.remove('Location')
        for name in names:
            values_arr = list(db.qa2_lnodes.aggregate(get_value(modality, ch_f, name)))[0]['uniqueValues']
            value = str(input(name + ' is: ' + str(values_arr)))
            parameters_input.append((name, value))
        finding_input["parameters"] = parameters_input
        user_input.append(finding_input)
    """
    cursor_findings = [db.qa2_lnodes.find(get_f_params_val(modality, cond, ui)).count() for ui in user_input]
    print("number of conditions with selected parameters is: ", cursor_findings)
    if 0 in cursor_findings:
        print("Finding with selected parameters doesn't exist in the database")
    selected_f = min(cursor_findings) # total number of condition with values
    print("selected f are: ", selected_f)
    probs = []
    """

    db_condlist = db.qa2_lnodes.distinct("conditions.conditionName")

    for condition in db_condlist:
        cursor_findings = [db.qa2_lnodes.find(get_f_params_val(modality, condition, ui)).count() for ui in user_input]
        print("number of conditions with selected parameters is: ", cursor_findings)
        if 0 in cursor_findings:
            print("Finding with selected parameters doesn't exist in the database")
        selected_f = min(cursor_findings)  # total number of condition with values
        cursor_c0 = db.qa2_lnodes.find({"conditions.conditionName": condition}).count()  # total number of specific conditions
        if cursor_c0:
            cursor_cond = db.qa2_lnodes.aggregate([{"$unwind": "$conditions"}, {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])
            total = sum(result['sum'] for result in cursor_cond) # total number of reports in the database (splitted)
            if total:
                p_v_ci = selected_f / cursor_c0 # P(Values | Ci)
                p_ci = cursor_c0 / total # specific condition / total num of reports
                prob = p_v_ci * p_ci # P(Ci | val)
                print("Prob is: ", prob)



            """
            for cursor_finding in cursor_findings:
                
                # print(cursor_finding)
                # print('total is', total)
                # print('cursor is ', cursor_c0)
                # print(freq)  # condition frequency = P(Ci)
                prob = cursor_finding / cursor_c0
                probs.append(prob)
                # print(prob)
            if (sum(probs)!=0):
                print("Frequency is " + str(freq))
                print("Probabilities are " + str(probs))
                probs_norm = [float(i) / sum(probs) for i in probs]
                result = np.prod(np.array(probs_norm))*freq
                print("Result is " + str(result))
            else:
                result = np.prod(np.ones((len(cursor_findings),), dtype=np.int)) * freq
                print("Result is " + str(result))
        else:
            print("Finding with selected parameters doesn't exist in the database")
    else:
        print("Condition doesn't exist")
    """


if __name__ == '__main__':
    ddata()
