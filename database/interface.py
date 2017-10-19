from pymongo import MongoClient
from cond_data import *
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
    find_arr = db.reportsNew.distinct("conditions.findings.name",
                                        {"modality": modality})
    ch_f = input('Choose finding from the list: ' + str(find_arr)).title()
    if ch_f == 'Mass':
        cursor_finding = db.reportsNew.find({
            "$and": [
                {"modality": modality},
                {"conditions": {
                    "$elemMatch": {
                        "conditionName": cond,
                        "findings": {
                            "$elemMatch": {
                                "name": ch_f,
                                "parameters": {
                                    "$elemMatch": {
                                        "name": str(input('Choose parameter from the list: '+ get_cond_population_mammo(cond).mass)).title(),
                                        "value": str(input('Please enter value: ')).title()
                                    }
                                }
                            }
                        }
                    }
                }}
            ]
        }).count()
        print(cursor_finding)



if __name__ == '__main__':
    ddata(  )
