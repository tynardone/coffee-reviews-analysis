import pickle

with open('data/roast-urls.pkl', 'rb') as f:
    obj = pickle.load(f)
    

print(obj)
print(type(obj))