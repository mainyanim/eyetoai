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
    modality = input('Modality is: ').title()
    cond = input('Condition you want to check is: ').title()
    find_arr = db.reportsNew.distinct("conditions.findings.name", {"modality": modality})

    num_findings = int(input('How many findings do you have: '))
    user_input = []
    for i in range(num_findings):
        finding_input = {}
        ch_f = input('Choose finding from the list: ' + str(find_arr)).title()
        finding_input["name"] = ch_f
        names = list(db.reportsNew.aggregate(get_parameter_names(modality, ch_f)))[0]['uniqueValues']
        parameters_input = []
        for name in names:
            values_arr = list(db.reportsNew.aggregate(get_value(modality, ch_f, name)))[0]['uniqueValues']
            value = str(input(name + ' is: ' + str(values_arr)))
            parameters_input.append((name, value))
        finding_input["parameters"] = parameters_input
        user_input.append(finding_input)

    cursor_findings = [db.reportsNew.find(get_f_params_val(modality, cond, ui)).count() for ui in user_input]

    probs = []
    cursor_c0 = db.reportsNew.find({"conditions.conditionName": cond}).count()  # num of conditions
    cursor_cond = db.reportsNew.aggregate([{"$unwind": "$conditions"}, {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])
    total = sum(result['sum'] for result in cursor_cond)
    freq = cursor_c0 / total
    for cursor_finding in cursor_findings:
        # print(cursor_finding)
        # print('total is', total)
        # print('cursor is ', cursor_c0)
        # print(freq)  # condition frequency = P(Ci)
        prob = cursor_finding / cursor_c0
        probs.append(prob)
        # print(prob)
    print("Frequency is " + str(freq))
    print("Probabilities are " + str(probs))
    probs_norm = [float(i) / sum(probs) for i in probs]
    result = np.prod(np.array(probs_norm))*freq
    print("Result is " + str(result))



if __name__ == '__main__':
    ddata()
