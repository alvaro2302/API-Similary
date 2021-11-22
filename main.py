from flask import Flask
app = Flask(__name__)

import glob
import yaml


def readModule(name):
  verbsWordsComplete = {}
  path = "./"+ name +"/*.yaml"
  for file in glob.glob(path):
    print(file)
    "reading verbs of TOMO"
    with open(file, 'r') as stream:
        try:
            verbs = yaml.safe_load(stream)
            dictTomo = {word["expression"]:name for word in verbs}
            verbsWordsComplete = dict(verbsWordsComplete, **dictTomo)
        except yaml.YAMLError as exc:
            print(exc)
  return verbsWordsComplete

def readTotalModule():
    verbTomoTotal = {}
    verbsTomo1 = readModule("Modulo1")
    verbsTomo2 = readModule("Modulo2")
    verbsTomo3 = readModule("Modulo3")

    verbTomoTotal = dict(verbTomoTotal, **verbsTomo1)
    verbTomoTotal = dict(verbTomoTotal, **verbsTomo2)
    verbTomoTotal = dict(verbTomoTotal, **verbsTomo3)
    verbListTomoTotal = list(verbTomoTotal.keys())
    print(verbTomoTotal)
    print(verbListTomoTotal)
    print(type(verbListTomoTotal))
    print(len(verbListTomoTotal))

@app.route('/')
def getWorSimliar():
    readTotalModule()
    return "Hey i will terminated"

