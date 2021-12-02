from flask import Flask,request,jsonify
app = Flask(__name__)
import spacy
import es_core_news_md
import glob
import yaml
import json
nlp = es_core_news_md.load()
verbTomoTotal = {}
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


verbsTomo1 = readModule("Modulo1")
verbsTomo2 = readModule("Modulo2")
verbsTomo3 = readModule("Modulo3")

verbTomoTotal = dict(verbTomoTotal, **verbsTomo1)
verbTomoTotal = dict(verbTomoTotal, **verbsTomo2)
verbTomoTotal = dict(verbTomoTotal, **verbsTomo3)
verbListTomoTotal = list(verbTomoTotal.keys())


def getVerbfSentence(sentence):
  
    sentenceWithNLP = nlp(sentence)
    suitableVerbs = {verb:sentenceWithNLP.similarity(nlp(verb))  for verb in verbListTomoTotal }
    
    
    return dict(sorted(suitableVerbs.items(),key=lambda item: item[1],reverse=True))

@app.route('/', methods =['GET'])
def getWorSimliar():
    data = request.json
    wordSimilard = data["word"]
    print(wordSimilard)
    resultSimilar = getVerbfSentence(wordSimilard)
    keyResult = list(resultSimilar.keys())[0]
    valueResult = resultSimilar[keyResult]
    resultDict = {keyResult:valueResult}
    jsonResult = json.dumps(resultDict)
    return jsonResult

