from pymongo import MongoClient
from db_config import *
import re
from flask_api import FlaskAPI, status, exceptions
from flask import request, abort
import json, requests

"""
author: Alexandra Zhuravlyov
ai_ranking is an algorithm that shows probability of a specific condition given an array of symptoms
"""

client = MongoClient("mongodb://yuri:rxLPDCJPXWHOozeV@cluster0-shard-00-00-lnxfa.mongodb.net:27017,"
                     "cluster0-shard-00-01-lnxfa.mongodb.net:27017,cluster0-shard-00-02-lnxfa.mongodb.net:27017/test?ssl=true&replicaSet="
                     "Cluster0-shard-0&authSource=admin")
db = client.eyetoai
app = FlaskAPI(__name__)


def ddata():
    num_findings = len(request.json.get("findings"))
    findings = request.json.get("findings")
    print(findings)
    print(num_findings)
    modality = request.json.get("modality")
    user_input = []
    for f in range(num_findings):
        finding_input = {}
        ch_f = request.json.get("findings")[f]["name"]
        finding_input["name"] = ch_f
        params = request.json.get("findings")[f]["parameters"]
        parameters_input = []
        for param in range(len(params)):
            name = params[param]["name"]
            value = params[param]["value"]
            parameters_input.append((name, value))
            finding_input["parameters"] = parameters_input
            print(finding_input)
        user_input.append(finding_input)
        print(user_input)
    probs = []
    db_condlist = db.reportsNew.distinct("conditions.conditionName")
    for condition in request.json.get("conditions"):
        cursor_c0 = db.fill.find({"conditions.conditionName": condition["name"]}).count()  # total number of specific conditions
        cursor_findings = [db.fill.find(get_f_params_val(modality, condition["name"], ui)).count() for ui in user_input]
        cursor_cond = db.fill.aggregate([{"$unwind": "$conditions"}, {"$group": {"_id": "$_id", "sum": {"$sum": 1}}}])
        print("number of conditions with selected parameters is: ", cursor_findings)
        if sum(cursor_findings)!=0:
            if 0 in cursor_findings:
                selected_f = min(filter(lambda x: x !=0,cursor_findings))
                print(selected_f)
            else:
                selected_f = min(cursor_findings)  # total number of condition with values
            if cursor_c0:
                total = sum(result['sum'] for result in cursor_cond) # total number of reports in the database (splitted)
                if total:
                    p_v_ci = selected_f / cursor_c0 # P(Values | Ci)
                    p_ci = cursor_c0 / total # specific condition / total num of reports
                    prob = p_v_ci * p_ci # P(Ci | val)
                    if prob!=0:
                        probs+=[{"id": condition["id"], "ranking": prob}]
        else:
            probs += [{"id": condition["id"], "ranking": 0}]
    from operator import itemgetter
    probs_sorted = sorted(probs, key=itemgetter('ranking'))[::-1]
    return probs_sorted
    #print("Prob is: ", prob)



@app.route("/", methods=['POST'])
def predict():
    if not request.json:
        abort(400)
    print(request.json)
    a = str(ddata())
    print(a)
    return a

if __name__ == '__main__':
    app.run(host = 'localhost', port = 8080, debug = True)


"""a
"""
"""
curl -X POST -H "Content-Type:application/json" -d "{\"modality\":\"Mammography\",\"conditions\":[{\"name\":\"Fibroadenoma\",\"id\":1},{\"name\":\"Adenosis\",\"id\":9},{\"name\":\"Granular cell tumor\",\"id\":10}],\"findings\":[{\"parameters\":[{\"name\":\"Typically benign\",\"value\":\"Suture\"},{\"name\":\"Suspicious morphology\",\"value\":\"Amorphous\"},{\"name\":\"Distribution\",\"value\":\"Diffuse\"}],\"name\":\"Calcifications\",\"id\":0},{\"parameters\":[{\"name\":\"Shape\",\"value\":\"Round\"},{\"name\":\"Density\",\"value\":\"High density\"},{\"name\":\"Margin\",\"value\":\"Circumscribed\"}],\"name\":\"Mass\",\"id\":0}],\"condition_db\":[{\"name\":\"Fibroadenoma\",\"id\":1},{\"name\":\"Fat necrosis\",\"id\":9},{\"name\":\"Granular cell tumor\",\"id\":10},{\"name\":\"Diabetic mastopathy\",\"id\":11},{\"name\":\"Adenosis\",\"id\":12},{\"name\":\"Fibrosis\",\"id\":13},{\"name\":\"Fibromatosis\",\"id\":14},{\"name\":\"Hamartoma\",\"id\":17},{\"name\":\"fibroadenoma 2\",\"id\":18},{\"name\":\"Fibrocystic breast changes\",\"id\":19},{\"name\":\"Epidermal inclusion cyst\",\"id\":20},{\"name\":\"Duct ectasia\",\"id\":21},{\"name\":\"Galactocele\",\"id\":22},{\"name\":\"Sebaceous cysts\",\"id\":23},{\"name\":\"INVASIVE LOBULAR CARCINOMA (ILC)\",\"id\":24},{\"name\":\"lymphoma\",\"id\":27},{\"name\":\"Mastitis\",\"id\":28},{\"name\":\"Invasive ductal carcinoma (IDC)\",\"id\":29},{\"name\":\"Condition 1\",\"id\":30},{\"name\":\"Papilloma\",\"id\":31},{\"name\":\"Intramammary lymph nodes\",\"id\":32}]}" http://localhost:8080
"""