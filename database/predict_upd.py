from pymongo import MongoClient
from functools import reduce
import operator

client = MongoClient('localhost', 27017)
db = client.reports
reportsColl = db.reportsColl

def cond_freq(condition):
    cursor_cond = db.reportsColl.aggregate([
            {"$unwind": "$conditions"},
            {"$group": {"_id": "$_id", "sum": { "$sum": 1}}}])

    total = sum(result['sum'] for result in cursor_cond)
    cursor_c0 = db.reportsColl.find({"conditions.conditionName": condition}).count()
    freq = cursor_c0/total
    return freq


def finding_condition(finding, condition):
    cursor_finding = db.reportsColl.find({"$and": [{"conditions.findings.name" : finding},
                                                {"conditions.conditionName" : condition}]}).count()
    return cursor_finding

def get_results(condition,arr):
    res_arr = []
    for x in range(len(arr)):
        x = finding_condition(arr[x], condition)
        res_arr += [x]
    final = list(map(lambda x: cond_freq(condition)*x,res_arr))
    for k in range(len(final)):
        k*=final[k]
    print(k)

if __name__ == '__main__':
    cond_freq("Fibroadenoma")
    findings_arr = ['Mass', 'Lymph nodes', 'Calcifications']
    get_results('Mastitis', findings_arr)
    get_results('Fibroadenoma', findings_arr)
