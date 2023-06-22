import random
import codecs

from error import *


def cs_P(self, token, *objs):  # Print
    obj_vals = []
    for obj in objs:
        obj_vals.append(codecs.decode(str(obj), 'unicode_escape'))
    print(*obj_vals)


def cs_I(self, token, prompt):  # Input
    prompt = codecs.decode(str(prompt), 'unicode_escape') if len(prompt) > 0 else ""
    return input(prompt)


def cs_RND(self, token, min, max):  # Random Int
    return random.randint(min, max)


def cs_CS(self, token, obj):  # Cast to String
    return str(obj)


def cs_CI(self, token, obj):  # Cast to Int
    return int(obj)


def cs_CF(self, token, obj):  # Cast to Float
    return float(obj)


def cs_CB(self, token, obj):  # Cast to Bool
    return bool(obj)


def cs_A(self, token, collection, *args):  # Add to collection
    if not isinstance(collection, (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"A<> takes a list or dict as the first parameter, not '{type(collection).__name__}'")

    if isinstance(collection, list):
        if len(args) == 2:
            index = args[0]
            element = args[1]
            if not isinstance(index, int):
                self.error(ErrorCode.PARAMETER_ERROR, token, f"A<> takes an int as the index to insert into, not '{type(index).__name__}'")
            collection.insert(index, element)
        else:
            element = args[0]
            collection.append(element)
    else:
        if len(args) != 2:
            self.error(ErrorCode.PARAMETER_ERROR, token, f"Appending to a dictionary requires 3 parameters and {len(args) + 1} were passed")
        key = args[0]
        value = args[1]
        collection[key] = value


def cs_RM(self, token, collection, index):
    if not isinstance(collection, (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"RM<> takes a list or dict as the first parameter, not '{type(collection).__name__}'")

    if isinstance(collection, list):
        if not isinstance(index, int):
            self.error(ErrorCode.PARAMETER_ERROR, token, f"RM<> takes an int as the index to remove from, not '{type(index).__name__}'")
        collection.pop(index)
    else:
        key = index
        if key not in collection:
            self.error(ErrorCode.KEY_NOT_FOUND, token, f"Key '{key}' not found in dictionary: {collection}")
        del collection[key]


def cs_RMV(self, token, collection, value):
    if not isinstance(collection, (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"RMV<> takes a list or dict as the first parameter, not '{type(collection).__name__}'")

    if isinstance(collection, list):
        if value not in collection:
            self.error(ErrorCode.VALUE_NOT_FOUND, token, f"Value '{value}' not found in list: {collection}")
        collection.remove(value)
    else:
        if value not in collection.values():
            self.error(ErrorCode.VALUE_NOT_FOUND, token, f"Value '{value}' not found in dictionary: {collection}")
        for k, v in collection.items():
            if v == value:
                del collection[k]
                break


def cs_L(self, token, collection):
    if not isinstance(collection, (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"Argument passed into L<> must be a list or dict, not '{type(collection).__name__}'")

    return len(collection)
