import timeit

def method1():
    for key in COLLECTION_MAP.keys():
        if key in data:
            common_key = key
            break

def method2():
    common_key = set(COLLECTION_MAP.keys()) & set(data.keys())
    if common_key:
        common_key = common_key.pop()

def method3():
    common_key = next((k for k in COLLECTION_MAP.keys() if k in data), None)

# setup code
COLLECTION_MAP = {'key5': 'value1', 'key2': 'value2', 'key1': 'value3'}
data = {'key3': 'value3', 'key4': 'value4', 'key4': 'value4', 'key5': 'value5', 'key6': 'value5', 'key7': 'value5', 'key8': 'value5'}

# run timeit
print('method1 time:', timeit.timeit(method1, number=1000000))
print('method2 time:', timeit.timeit(method2, number=1000000))
print('method3 time:', timeit.timeit(method3, number=1000000))
