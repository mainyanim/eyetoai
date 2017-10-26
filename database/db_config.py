import re

def get_f_params_val(modality, cond, user_input):
    return {
        "$and": [
            {"modality": modality},
            {"conditions": {
                "$elemMatch": {
                    "conditionName": cond ,
                    "findings": {
                        "$elemMatch": {
                            "name": user_input["name"],
                            "$and": [
                                {
                                    "parameters": {
                                        "$elemMatch": {
                                            "name": query_tuple[0],
                                            "value": query_tuple[1]
                                        }
                                    }
                                }
                            for query_tuple in user_input["parameters"]]
                        }
                    }
                }
            }}
        ]
    }


def get_value(modality, finding, parameter):
    return [
        {
            "$match": {"modality": modality}
        },
        {
            "$unwind": "$conditions"
        },
        {
            "$unwind": "$conditions.findings"
        },
        {
            "$match": {"conditions.findings.name": finding}
        },
        {
            "$unwind": "$conditions.findings.parameters"
        },
        {
            "$match": {"conditions.findings.parameters.name": parameter}
        },
        {
            "$group": {"_id": "null", "uniqueValues": {"$addToSet": "$conditions.findings.parameters.value"}}
        }
    ]


def get_parameter_names(modality, finding):
    return [
        {
            "$match": {"modality": modality}
        },
        {
            "$unwind": "$conditions"
        },
        {
            "$unwind": "$conditions.findings"
        },
        {
            "$match": {"conditions.findings.name": finding}
        },
        {
            "$unwind": "$conditions.findings.parameters"
        },
        {
            "$match": {"conditions.findings.parameters.value": {"$exists": "true"}}
        },
        {
            "$group": {"_id": "null", "uniqueValues": {"$addToSet": "$conditions.findings.parameters.name"}}
        }
    ]
