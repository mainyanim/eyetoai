from pymongo import MongoClient
from db_config import *
import re

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
    find_arr = db.fill.distinct("conditions.findings.name", {"modality": re.compile(modality, re.IGNORECASE)})

    num_findings = int(input('How many findings do you have: '))
    user_input = []
    for _ in range(num_findings):
        finding_input = {}
        ch_f = input('Choose finding from the list: ' + str(find_arr))
        finding_input["name"] = ch_f
        parameters_input = []
        if ch_f!='Mass':
            names = list(db.fill.aggregate(get_parameter_names(modality, ch_f)))[0]['uniqueValues']
        else:
            names = list(db.fill.aggregate(get_parameter_names(modality, ch_f)))[0]['uniqueValues']
            print(names)
            if 'Location' in names:
                names.remove('Location')
        for name in names:
            values_arr = list(db.fill.aggregate(get_value(modality, ch_f, name)))[0]['uniqueValues']
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
    """
    probs = []
    db_condlist = db.reportsNew.distinct("conditions.conditionName")

    for condition in db_condlist:
        cursor_findings = [db.fill.find(get_f_params_val(modality, condition, ui)).count() for ui in user_input]
        print("number of conditions with selected parameters is: ", cursor_findings)
        if 0 in cursor_findings:
            #print("Finding with selected parameters doesn't exist in the database")
            pass
        selected_f = min(cursor_findings)  # total number of condition with values
        cursor_c0 = db.fill.find({"conditions.conditionName": condition}).count()  # total number of specific conditions
        if cursor_c0:
            cursor_cond = db.fill.aggregate([{"$unwind": "$conditions"}, {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])
            total = sum(result['sum'] for result in cursor_cond) # total number of reports in the database (splitted)
            if total:
                p_v_ci = selected_f / cursor_c0 # P(Values | Ci)
                p_ci = cursor_c0 / total # specific condition / total num of reports
                prob = p_v_ci * p_ci # P(Ci | val)
                if prob!=0:
                    probs+=[{"id": condition, "prob": prob}]
    #probs.sort()

    print(probs)
    from operator import itemgetter
    probs_sorted = sorted(probs, key=itemgetter('prob'))[::-1]
    print(probs_sorted)
    #print("Prob is: ", prob)


if __name__ == '__main__':
    ddata()
