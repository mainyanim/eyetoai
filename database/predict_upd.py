from pymongo import MongoClient
import numpy as np
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
    res_arr = [finding_condition(arr[x],condition) for x in range(len(arr))]
    final_temp = list(map(lambda x: cond_freq(condition)*x,res_arr))
    final = [final_temp[k] for k in range(len(final_temp))]
    result = np.prod(np.array(final))
    """
    for k in range(len(final_temp)):
        k*=final_temp[k]
    print(k)
    """
    print(result)
    return result


if __name__ == '__main__':
    cond_freq("Fibroadenoma")
    findings_arr = ['Mass', 'Lymph nodes', 'Calcifications']

    get_results('Mastitis', findings_arr)
    get_results('Fibroadenoma', findings_arr)
