from pymongo import MongoClient
import numpy as np
import json


client = MongoClient('localhost', 27017)
db = client.reports
reportsColl = db.reportsColl

def cond_freq(condition):
    cursor_cond = db.reportsColl.aggregate([
        {"$unwind": "$conditions"},
        {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])

    total = sum(result['sum'] for result in cursor_cond)
    cursor_c0 = db.reportsColl.find({"conditions.conditionName": condition}).count()
    freq = cursor_c0 / total
    return freq


def finding_condition(finding, condition):
    cursor_finding = db.reportsColl.find({"$and": [{"conditions.findings.name": finding},
                                                   {"conditions.conditionName": condition}]}).count()
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


#curl -X POST -H "Content-Type: application/json" -d "{ \"condition\": \"Fibroadenoma\" }" http://localhost:8080/calc

if __name__ == '__main__':
    get_results('Fibroadenoma', ['Mass', 'Calcifications'])


