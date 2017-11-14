import pandas as pd
df = pd.read_excel('testmammo5.xlsx')
df2 = df.set_index("condlist")


from pymongo import MongoClient
from config_chatbot import *


"""
author: Alexandra Zhuravlyov
ai_ranking is an algorithm that shows probability of a specific condition given an array of symptoms
"""

client = MongoClient("mongodb://yuri:rxLPDCJPXWHOozeV@cluster0-shard-00-00-lnxfa.mongodb.net:27017,"
                     "cluster0-shard-00-01-lnxfa.mongodb.net:27017,cluster0-shard-00-02-lnxfa.mongodb.net:27017/test?ssl=true&replicaSet="
                     "Cluster0-shard-0&authSource=admin")
db = client.eyetoai


def ddata():
    heads = df2.columns.tolist()
    max_dict = dict((key, value) for (key, value) in zip(heads, df2.loc[:, heads].max()))
    max_key = max(max_dict, key=lambda k: max_dict[k])
    ch_f = str(input("Is there " + max_key + "?"))
    data = list(df[max_key])
    if ch_f.lower() == "yes":
        modality = "Mammography"
        user_input = []
        finding_input = {}
        finding_input["name"] = max_key
        names = list(db.fill.aggregate(get_parameter_names(modality, max_key)))[0]['uniqueValues']
        parameters_input = []
        for name in names:
            values_arr = list(db.fill.aggregate(get_value(modality, max_key, name)))[0]['uniqueValues']
            value = str(input(name + ' is: ' + str(values_arr)))
            parameters_input.append((name, value))
        finding_input["parameters"] = parameters_input
        user_input.append(finding_input)
        print(user_input)
        probs = []
        db_condlist = db.fill.distinct("conditions.conditionName")
        finding_dict = dict((key, value) for (key, value) in zip(df["condlist"], data))
        print(finding_dict)
        for condition in list(df["condlist"]):
            cursor_c0 = db.fill.find({"conditions.conditionName": condition}).count()  # total number of specific conditions
            cursor_findings = [db.fill.find(get_f_params_val(modality, condition, ui)).count() for ui in user_input]
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
                        prob = p_v_ci * p_ci * finding_dict[condition] # P(Ci | val)
                        print(prob, finding_dict[condition], condition)
                        if prob!=0:
                            probs+=[{"id": condition, "entropy": prob}]
            else:
                probs += [{"id": condition, "entropy": 0}]
        from operator import itemgetter
        import math
        p_i = sum(item['entropy'] for item in probs)
        entropy = -p_i*math.log2(p_i)
        print(entropy)
        """
        min_entr = min(probs, key=lambda x: x['entropy'])
        print(min_entr)
        return min_entr
        """
        #print("Prob is: ", prob)

if __name__ == '__main__':
    ddata()