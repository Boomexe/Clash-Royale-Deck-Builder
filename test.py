import json

with open("test.json", "r", encoding="utf-8") as f:
  f = json.load(f)
  
for i in f:
  print(f["currentDeck"])