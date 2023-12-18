import json

a = {'a': 1, 'b': {'c': 2}}
a0 = json.dumps(a, sort_keys=True, indent=4, separators=(',', ': '))
a1 = json.loads(a0)

b0 = "111"
b1 = json.loads(b0)

print(a1['b']['c'])

