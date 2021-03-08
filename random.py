stages = []
for n in range(5):
    stages.append({"stage": n})

stages[0]["nextStage"]=stages[0]["stage"]+10
stages[0]["objectives"] = []
print(stages)
