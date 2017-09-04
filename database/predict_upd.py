from pymongo import MongoClient
import numpy as np
from flask_api import FlaskAPI, status, exceptions
from flask import request, abort
import json, requests
import ssl

"""
author: Alexandra Zhuravlyov
"""

client = MongoClient("mongodb://yuri:rxLPDCJPXWHOozeV@cluster0-shard-00-00-lnxfa.mongodb.net:27017,cluster0-shard-00-01-lnxfa.mongodb.net:27017,cluster0-shard-00-02-lnxfa.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client.eyetoai

"""
pymongo driver for local usage
client = MongoClient('localhost', 27017)
db  = client.reports
"""
reports = db.reports
app = FlaskAPI(__name__)


def cond_freq(condition):
    cursor_cond = db.reports.aggregate([{"$unwind": "$Conditions"},
                                         {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])

    total = sum(result['sum'] for result in cursor_cond)
    cursor_c0 = db.reports.find({"Conditions.ConditionName": condition}).count()
    freq = cursor_c0 / total
    return freq


def finding_condition(finding, condition):
    cursor_finding = db.reports.find({"$and": [{"Conditions.Findings.Name": finding},
                                                   {"Conditions.ConditionName": condition}]}).count()
    return cursor_finding


def get_results(condition, arr):
    if len(arr) != 0:
        res_arr = [finding_condition(arr[x], condition) for x in range(len(arr))]
        final_temp = list(map(lambda x: cond_freq(condition) * x, res_arr))
        final = [final_temp[k] for k in range(len(final_temp))]
        result = np.prod(np.array(final))
        print(result)
    else:
        result = cond_freq(condition)
        print(result)
    return result



@app.route("/", methods=['POST'])
def predict():
    if not request.json:
        abort(400)
    print(request.json)
    condition = request.json.get("condition")
    findings = request.json.get("findings")
    result = str(get_results(condition,findings))
    return result

if __name__ == '__main__':
    app.run(host = 'localhost', port = 8000, debug = True)

"""
test curl request for getting a result:
curl -X POST -H "Content-Type: application/json" -d "{ \"condition\": \"Fibroadenoma\",\"findings\": [\"Mass\"] }" http://localhost:8000/
"""