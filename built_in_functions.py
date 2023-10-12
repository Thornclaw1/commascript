import random
import codecs
import io
import time

from error import *


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


def join_tuple(tuple):
    if isinstance(tuple, type):
        return tuple.__name__
    return ", ".join([v_type.__name__ for v_type in tuple[:-1]]) + " or " + tuple[-1].__name__


def argument_validation(self, token, func_name, args, valid_types):
    for idx, arg in enumerate(args):
        if not isinstance(arg, valid_types[idx]):
            self.error(ErrorCode.PARAMETER_ERROR, token,
                       f"The {ordinal(idx+1)} argument passed into {func_name}<> must be of type {join_tuple(valid_types[idx])}, not {type(arg).__name__}")


def cs_p(self, token, *objs):  # Print
    obj_vals = []
    for obj in objs:
        obj_vals.append(codecs.decode(str(obj), 'unicode_escape'))
        # obj_vals.append(codecs.decode(str(obj), 'unicode_escape').encode('utf-8').decode('utf-8'))
        # obj_vals.append(codecs.decode(str(obj), 'utf-8'))
        # obj_vals.append(str(obj, encoding='utf-8'))
    print(*obj_vals)


def cs_i(self, token, prompt):  # Input
    prompt = codecs.decode(
        str(prompt), 'unicode_escape') if len(prompt) > 0 else ""
    # prompt = codecs.decode(str(prompt), 'utf-8') if len(prompt) > 0 else ""
    return input(prompt)


def cs_rnd(self, token, min, max, count=1, unique=False):  # Random Int
    argument_validation(self, token, "rnd",
                        (min, max, count, unique), (int, int, int, bool))
    if count > 1:
        val = []
        int_range = list(range(min, max+1))
        while count >= 1 and int_range:
            idx = random.randint(0, len(int_range) - 1)
            val.append(int_range[idx])
            count -= 1
            if unique:
                int_range.pop(idx)
        return val
    return random.randint(min, max)


def cs_lrnd(self, token, collection, count=1, unique=False):  # Random element from list/tuple
    argument_validation(self, token, "lrnd",
                        (collection, count, unique), ((list, tuple), int, bool))
    if count > 1:
        if unique:
            count = len(collection) if count > len(collection) else count
            return random.sample(collection, k=count)
        return random.choices(collection, k=count)
    return random.choice(collection)


def cs_cs(self, token, obj):  # Cast to String
    argument_validation(self, token, "cs",
                        (obj,), ((int, float, str, bool),))
    return str(obj)


def cs_ci(self, token, obj):  # Cast to Int
    argument_validation(self, token, "ci",
                        (obj,), ((int, float, str, bool),))
    return int(obj)


def cs_cf(self, token, obj):  # Cast to Float
    argument_validation(self, token, "cf",
                        (obj,), ((int, float, str, bool),))
    return float(obj)


def cs_cb(self, token, obj):  # Cast to Bool
    argument_validation(self, token, "cb",
                        (obj,), ((int, float, str, bool),))
    return bool(obj)


def cs_a(self, token, collection, *args):  # Add to collection
    argument_validation(self, token, "a", (collection,), ((list, dict),))

    if isinstance(collection, list):
        if len(args) == 2:
            index = args[0]
            element = args[1]
            if not isinstance(index, int):
                self.error(ErrorCode.PARAMETER_ERROR, token,
                           f"a<> takes an int as the index to insert into, not '{type(index).__name__}'")
            collection.insert(index, element)
        else:
            element = args[0]
            collection.append(element)
    else:
        if len(args) != 2:
            self.error(ErrorCode.PARAMETER_ERROR, token,
                       f"Appending to a dictionary requires 3 parameters and {len(args) + 1} were passed")
        key = args[0]
        value = args[1]
        collection[key] = value


def cs_rm(self, token, collection, index):
    argument_validation(self, token, "rm", (collection,), ((list, dict),))

    if isinstance(collection, list):
        if not isinstance(index, int):
            self.error(ErrorCode.PARAMETER_ERROR, token,
                       f"rm<> takes an int as the index to remove from, not '{type(index).__name__}'")
        collection.pop(index)
    else:
        key = index
        if key not in collection:
            self.error(ErrorCode.KEY_NOT_FOUND, token,
                       f"Key '{key}' not found in dictionary: {collection}")
        del collection[key]


def cs_rmv(self, token, collection, value):
    argument_validation(self, token, "rmv", (collection,), ((list, dict),))

    if isinstance(collection, list):
        if value not in collection:
            self.error(ErrorCode.VALUE_NOT_FOUND, token,
                       f"Value '{value}' not found in list: {collection}")
        collection.remove(value)
    else:
        if value not in collection.values():
            self.error(ErrorCode.VALUE_NOT_FOUND, token,
                       f"Value '{value}' not found in dictionary: {collection}")
        for k, v in collection.items():
            if v == value:
                del collection[k]
                break


def cs_pop(self, token, collection, index=-1):
    argument_validation(self, token, "pop", (collection,), ((list, dict),))

    if isinstance(collection, list):
        if not isinstance(index, int):
            self.error(ErrorCode.PARAMETER_ERROR, token,
                       f"pop<> takes an int as the index to pop from, not '{type(index).__name__}'")
        return collection.pop(index)
    else:
        key = index
        if key not in collection:
            self.error(ErrorCode.KEY_NOT_FOUND, token,
                       f"Key '{key}' not found in dictionary: {collection}")
        return collection.pop(key)


def cs_l(self, token, obj):
    argument_validation(self, token, "l", (obj,),
                        ((list, dict, tuple, str, int, float),))

    if isinstance(obj, (int, float)):
        return len(str(obj))
    return len(obj)


def cs_wf(self, token, file, string):
    try:
        file.write(codecs.decode(str(string), 'unicode_escape'))
    except:
        self.error(ErrorCode.INVALID_FUNCTION_CALL, token,
                   "Cannot write to a file that is opened for reading")


def cs_rf(self, token, file):
    try:
        return file.read()
    except:
        self.error(ErrorCode.INVALID_FUNCTION_CALL, token,
                   "Cannot read from a file that is opened for writing")


def cs_slp(self, token, secs):
    argument_validation(self, token, "slp", (secs,), ((int, float),))
    time.sleep(secs)


def cs_srt(self, token, collection, reverse=False):
    argument_validation(self, token, "srt",
                        (collection, reverse), (list, bool))
    collection.sort(reverse=reverse)


def cs_srtd(self, token, collection, reverse=False):
    argument_validation(self, token, "srtd",
                        (collection, reverse), (list, bool))
    return sorted(collection, reverse=reverse)


def cs_abs(self, token, number):
    argument_validation(self, token, "abs", (number,), ((int, float),))
    return abs(number)


def cs_max(self, token, *objs):
    if len(objs) > 0 and isinstance(objs[0], (list, tuple)):
        return max(objs[0])
    return max(objs)


def cs_min(self, token, *objs):
    if len(objs) > 0 and isinstance(objs[0], (list, tuple)):
        return min(objs[0])
    return min(objs)


def cs_all(self, token, iterable):
    argument_validation(self, token, "all", (iterable,), (list,))
    return all(iterable)


def cs_any(self, token, iterable):
    argument_validation(self, token, "any", (iterable,), (list,))
    return any(iterable)


def cs_upp(self, token, string):
    argument_validation(self, token, "upp", (string,), (str,))
    return string.upper()


def cs_low(self, token, string):
    argument_validation(self, token, "low", (string,), (str,))
    return string.lower()


def cs_cap(self, token, string):
    argument_validation(self, token, "cap", (string,), (str,))
    return string[0].upper() + string[1:].lower()


def cs_splt(self, token, string, sep=None, maxsplit=-1):
    argument_validation(self, token, "splt", (string,
                        sep if sep else "", maxsplit), (str, str, int))
    return string.split(sep, maxsplit)


def cs_join(self, token, collection, sep=" "):
    argument_validation(self, token, "join", (collection, sep), (list, str))
    return sep.join([str(ele) for ele in collection])
