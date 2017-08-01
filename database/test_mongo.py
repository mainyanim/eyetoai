import pymongo
import pprint
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.test_database
reports = db.reports

new_reports = [
{
  "patient_id": 35,
  "patient_name": "Bette-Ann",
  "relevantModality": "Mammography",
  "conditions_number": 3,
  "conditions": [
    {
      "condition_name": "lymphoma",
      "condition_details": [
        {
          "relevant_finding": [
            {
              "finding_name": "calcifications",
              "finding_parameters": {
                "typicallyBenign": "Coarse or \u201cpopcorn-like\u201d",
                "suspiciousMorphology": "Fine linear or fine-linear branching",
                "distribution": "Grouped"
              }
            }
          ]
        }
      ]
    },
    {
      "condition_name": "invasiveDuctalCarcinomaIdc",
      "condition_details": [
        {
          "relevant_finding": [
            {
              "finding_name": "mass",
              "finding_parameters": {
                "shape": "Oval",
                "margin": "Circumscribed",
                "density": "High density"
              }
            }
          ]
        }
      ]
    }
  ]
},
{
  "patient_id": 96,
  "patient_name": "Darb",
  "relevantModality": "Mammography",
  "conditions_number": 2,
  "conditions": [
    {
      "condition_name": "papilloma",
      "condition_details": [
        {
          "relevant_finding": [
            {
              "finding_name": "calcifications",
              "finding_parameters": {
                "typicallyBenign": "Large rod-like",
                "suspiciousMorphology": "Amorphous",
                "distribution": "Segmental"
              }
            }
          ]
        }
      ]
    },
    {
      "condition_name": "fibroadenoma",
      "condition_details": [
        {
          "relevant_finding": [
            {
              "finding_name": "calcifications",
              "finding_parameters": {
                "typicallyBenign": "Round",
                "suspiciousMorphology": "Coarse heterogeneous",
                "distribution": "Diffuse"
              }
            }
          ]
        }
      ]
    }
  ]
}
]
result = reports.insert_many(new_reports)
print(reports.count())