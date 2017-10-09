from pymongo import MongoClient
import numpy as np
from flask_api import FlaskAPI, status, exceptions
from flask import request, abort
import math
import json, requests
import ssl

"""
author: Alexandra Zhuravlyov
ai_ranking is an algorithm that shows probability of a specific condition given an array of symptoms
"""

client = MongoClient("mongodb://yuri:rxLPDCJPXWHOozeV@cluster0-shard-00-00-lnxfa.mongodb.net:27017,cluster0-shard-00-01-lnxfa.mongodb.net:27017,cluster0-shard-00-02-lnxfa.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client.eyetoai

"""
pymongo driver for local usage
client = MongoClient('localhost', 27017)
db  = client.reports
"""
reportsNew = db.reportsNew
app = FlaskAPI(__name__)


def cond_freq(condition):
    cursor_cond = db.reportsNew.aggregate([{"$unwind": "$conditions"},
                                         {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])

    total = sum(result['sum'] for result in cursor_cond)
    cursor_c0 = db.reportsNew.find({"conditions.conditionName": condition}).count()
    freq = cursor_c0 / total
    print("cond freq is ",freq)
    return freq


def finding_condition(finding, parameter, p_value, condition, modality ):
    cursor_finding = db.reportsNew.find({
    "$and": [
        {"modality": modality},
        { "conditions": {
            "$elemMatch": {
                "conditionName": condition,
                "findings": {
                    "$elemMatch": {
                        "name": finding,
                        "parameters": {
                            "$elemMatch": {
                                "name": parameter,
                                "value": p_value
                            }
                        }
                    }
                }
            }
        }}
    ]
}).count()


    print("count with params: ", cursor_finding)
    return cursor_finding


def get_results(condition,  findings_arr, parameter_arr, values_arr, modality):
    res_arr = [finding_condition(findings_arr[x], parameter_arr[x], values_arr[x], condition, modality)
               for x in range(len(findings_arr))]
    final_temp = list(map(lambda x: cond_freq(condition) * x, res_arr))
    if sum(final_temp) !=0:
        print(final_temp)
        norm = [float(i) / sum(final_temp) for i in final_temp]
        print("normalized", norm)
        final = [norm[k] for k in range(len(norm))]
        result = np.prod(np.array(final))
        print("result is: ",result)
        return result
    else:
        # result = cond_freq(condition)
        print("no selected params")

def get_entropy(condition_arr, findings_arr, parameter_arr, values_arr, modality):
    for x in range(len(condition_arr)):
        prob = get_results(condition_arr[x], findings_arr, parameter_arr, values_arr, modality)
        if prob:
            e = -sum([prob*math.log2(prob)])
            print(condition_arr[x], "entropy is: ", e)






"""
@app.route("/", methods=['POST'])
def predict():
    if not request.json:
        abort(400)
    print(request.json)
    condition = request.json.get("condition")
    findings = request.json.get("findings")
    parameters = request.json.get("parameters")
    values = request.json.get("values")
    result = str(get_results(condition,findings,parameters,values))
    return result
"""

if __name__ == '__main__':
    get_entropy(['Condition 1', 'Mastitis'], ["Mass", "Calcifications"], ["Shape", "Typically benign"],
                ["Irregular", "Vascular"], "Mammography")



"""
test curl request for getting a result:
curl -X POST -H "Content-Type: application/json" -d "{ \"condition\": \"Fibroadenoma\",\"findings\": [\"Mass\", \"Calcifications\"], \"parameters\": [\"Shape\", \"Margin\", \"Density\", \"Typically benign\", \"Suspicious morphology\", \"Distribution\"], \"values\": [\"Round\", \"Circumscribed\", \"High density\", \"Skin\", \"Coarse heterogeneous\", \"Linear\"] }" http://localhost:8080/
"""
