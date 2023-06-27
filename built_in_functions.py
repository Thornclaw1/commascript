import random
import codecs
import io

from error import *


def cs_p(self, token, *objs):  # Print
    obj_vals = []
    for obj in objs:
        obj_vals.append(codecs.decode(str(obj), 'unicode_escape'))
        # obj_vals.append(codecs.decode(str(obj), 'unicode_escape').encode('utf-8').decode('utf-8'))
        # obj_vals.append(codecs.decode(str(obj), 'utf-8'))
        # obj_vals.append(str(obj, encoding='utf-8'))
    print(*obj_vals)


def cs_i(self, token, prompt):  # Input
    prompt = codecs.decode(str(prompt), 'unicode_escape') if len(prompt) > 0 else ""
    # prompt = codecs.decode(str(prompt), 'utf-8') if len(prompt) > 0 else ""
    return input(prompt)


def cs_rnd(self, token, min, max):  # Random Int
    return random.randint(min, max)


def cs_cs(self, token, obj):  # Cast to String
    return str(obj)


def cs_ci(self, token, obj):  # Cast to Int
    return int(obj)


def cs_cf(self, token, obj):  # Cast to Float
    return float(obj)


def cs_cb(self, token, obj):  # Cast to Bool
    return bool(obj)


def cs_a(self, token, collection, *args):  # Add to collection
    if not isinstance(collection, (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"a<> takes a list or dict as the first parameter, not '{type(collection).__name__}'")

    if isinstance(collection, list):
        if len(args) == 2:
            index = args[0]
            element = args[1]
            if not isinstance(index, int):
                self.error(ErrorCode.PARAMETER_ERROR, token, f"a<> takes an int as the index to insert into, not '{type(index).__name__}'")
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


def cs_rm(self, token, collection, index):
    if not isinstance(collection, (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"rm<> takes a list or dict as the first parameter, not '{type(collection).__name__}'")

    if isinstance(collection, list):
        if not isinstance(index, int):
            self.error(ErrorCode.PARAMETER_ERROR, token, f"rm<> takes an int as the index to remove from, not '{type(index).__name__}'")
        collection.pop(index)
    else:
        key = index
        if key not in collection:
            self.error(ErrorCode.KEY_NOT_FOUND, token, f"Key '{key}' not found in dictionary: {collection}")
        del collection[key]


def cs_rmv(self, token, collection, value):
    if not isinstance(collection, (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"rmv<> takes a list or dict as the first parameter, not '{type(collection).__name__}'")

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


def cs_l(self, token, obj):
    if not isinstance(obj, (list, dict, tuple, str, int, float)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"Argument passed into l<> must be a list, dict, tuple, string or number, not '{type(obj).__name__}'")

    if isinstance(obj, (int, float)):
        return len(str(obj))
    return len(obj)


def cs_wf(self, token, file, string):
    # if len(self.open_file_stack) == 0:
    #     self.error(ErrorCode.INVALID_FUNCTION_CALL, token, "There is no open file to write to")
    try:
        # self.open_file_stack[-1].write(string)
        file.write(codecs.decode(str(string), 'unicode_escape'))
    except:
        self.error(ErrorCode.INVALID_FUNCTION_CALL, token, "Cannot write to a file that is opened for reading")


def cs_rf(self, token, file):
    # if len(self.open_file_stack) == 0:
    #     self.error(ErrorCode.INVALID_FUNCTION_CALL, token, "There is no open file to read from")
    try:
        # return self.open_file_stack[-1].read()
        return file.read()
    except:
        self.error(ErrorCode.INVALID_FUNCTION_CALL, token, "Cannot read from a file that is opened for writing")
