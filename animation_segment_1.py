# import required libraries
import spacy
from spacy import displacy 
import json
import os
import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# initiate global variables
destinFolder = "ParaInfo/"
nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])

# define required libraries
def DictonaryToTable(op):
  return {"SubAtt":["-" if "Subject" not in op.keys() else ["-" if "Attribute" not in op["Subject"].keys() else op["Subject"]["Attribute"]][0]][0],
          "SubName":["-" if "Subject" not in op.keys() else op["Subject"]["Name"]][0],
          "ActionName":["-" if "Action" not in op.keys() else op["Action"]["Name"]][0],
          "ActionRelation":["-" if "Action" not in op.keys() else ["-" if "Relation" not in op["Action"].keys() else op["Action"]["Relation"]][0]][0],
          "ObjectName":["-" if "Object" not in op.keys() else op["Object"]["Name"]][0],
          "ObjectAtt":["-" if "Object" not in op.keys() else ["-" if "Attribute" not in op["Object"].keys() else op["Object"]["Attribute"]][0]][0]
          }
def FinalizeOP(op):
    filename = 'Segment1.2/DecisionTree.sav'
    Model = pickle.load(open(filename, 'rb'))
    filename = 'Segment1.2/tokenizer.tok'
    tokenizer = pickle.load(open(filename, 'rb'))
    table = pd.DataFrame(columns=["SubAtt","SubName","ActionName","ActionRelation","ObjectName","ObjectAtt"])
    row = DictonaryToTable(op)
    table = table.append(row,ignore_index=True)
    x = [table.to_string().split("\n")[i].split()[1:] for i in range(1,len(table)+1)]
    Data = np.array(tokenizer.texts_to_sequences(x))
    print(Data)
    NewY = Model.predict(Data)
    names = tokenizer.sequences_to_texts(NewY)[0].split()

    op = [{
      "Name":names[0].capitalize()+"_"+names[1].capitalize(),
      "Location":[0,3,0],
      "Rotation":[1.5707964897155762, -0.0, 0.4363323152065277],
      "Scale":-1
      },{
      "Name":names[2].capitalize()+"_"+names[3].capitalize(),
      "Location":[0,0,0],
      "Rotation":[0,0,0],
      "Scale":-1
      }]
    return op

def CleanDestinFolder(destinFolder):
    for x in os.listdir(destinFolder):
        os.remove(destinFolder + x)
    return
def depTag(token,OP={},parent=None):
  if token.dep_.lower() == "root":
    OP["Action"] = {"Name":token.text}
  if "sub" in token.dep_.lower():
    try:
      compound = [children.text for children in token.children if children.dep_.lower() == "compound"][0]
      OP["Subject"] = {"Name":compound + " " + token.text}
    except IndexError :
      OP["Subject"] = {"Name":token.text}
  if token.dep_.lower() == "amod" or token.pos_.lower()=="adj":
    if "sub" in parent.dep_.lower():
      if "Attribute" not in OP["Subject"].keys():
        OP["Subject"]["Attribute"] = token.text
      else:
        OP["Subject"]["Attribute"] += ', ' +  token.text
    elif "obj" in parent.dep_.lower():
      if "Attribute" not in OP["Object"].keys():
        OP["Object"]["Attribute"] = token.text
      else:
        OP["Object"]["Attribute"] += ', ' +  token.text
  if "obj" in token.dep_.lower():
    try:
      compound = [children.text for children in token.children if children.dep_.lower() == "compound"][0]
      OP["Object"] = {"Name":compound + " " + token.text}
    except IndexError :
      OP["Object"] = {"Name":token.text}
  if token.dep_.lower() == "prep" and parent.pos_.lower()=="verb":
    OP["Action"]["Relation"] =  token.text
  for children in token.children:
    depTag(children,OP,token)
  return 

if __name__ == "__main__":
    # -- Clear the destin folder for new inputs
    print("\nClearing Destination Folder .....")
    CleanDestinFolder(destinFolder)
    CleanDestinFolder("BasicInfo/")
    #Paragraph = input("Enter the script in 'Simple Sentence' here -- > ")
    Paragraph = sys.argv[1]
    Lines = [x.strip().capitalize() for x in Paragraph.split(".") if len(x) != 0]

    for i in range(len(Lines)):
        line = Lines[i]
        TokenizedLine = nlp(line)
        for token in TokenizedLine:
            if token.dep_.lower() == "root":
                op = {}
                depTag(token,op)
                break
        
        print(line)

        # Writing to sample.json
        print("BasicInfo")
        print(json.dumps(op, indent = 4))
        with open("BasicInfo/" + str(i) + ".json", "w") as outfile:
            outfile.write(json.dumps(op, indent = 4))

        op = FinalizeOP(op)
        JsonOutput = json.dumps(op, indent = 4)
        print("AdditionalInfo")
        print(JsonOutput)

        # Writing to sample.json
        with open(destinFolder + str(i) + ".json", "w") as outfile:
            outfile.write(JsonOutput)
        print("----------\n")

