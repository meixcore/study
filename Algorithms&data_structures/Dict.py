class MyDict:
    def __init__(self):
        self._dict = []

    def __str__(self):
        return str(self._dict)

    def __getitem__(self, key):
        for k, v in self._dict:
            if k == key:
                return v
        return False

    def __contains__(self, key):
        for k, v in self._dict:
            if k == key:
                return True
        return False

    def __setitem__(self, key, value):
        for i, (k, v) in enumerate(self._dict):
            if k == key:
                self._dict[i] = (k, v)
        self._dict.append((key, value))

    def __delitem__(self, key):
        for i, (k, v) in enumerate(self._dict):
            if k == key:
                self._dict.pop(i)
                return

    def keys(self):
        return [k for k,v in self._dict]

    def values(self):
        return [v for k, v in self._dict]

    def items(self):
        return list(self._dict)

my_dict = MyDict()
my_dict['name'] = 'Alice'
my_dict['age'] = 30
print(my_dict['name'])  # Вернет 'Alice'
print('city' in my_dict)  # Вернет False
del my_dict['age']
print(my_dict.keys())  # Вернет ['name']
print(my_dict.values())  # Вернет ['Alice']