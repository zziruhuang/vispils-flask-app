import pickle



import pickle

filename='extracted_inputs.pkl'

# Read dictionary pkl file
with open(filename, 'rb') as fp:
    person = pickle.load(fp)

print(type(person))
print(person.keys())
print(len(person['1']))
print(len(person['1'][0]))