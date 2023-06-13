import random
import codecs

from error import *


def cs_P_arg_validation(self, token, args):
    return True


def cs_P(self, token, args):  # Print
    arg_vals = []
    for arg in args:
        arg_vals.append(codecs.decode(str(arg), 'unicode_escape'))
    print(*arg_vals)


def cs_I_arg_validation(self, token, args):
    return len(args) in (0, 1)


def cs_I(self, token, args):  # Input
    prompt = codecs.decode(str(args[0]), 'unicode_escape') if len(args) > 0 else ""
    return input(prompt)


def cs_RND_arg_validation(self, token, args):
    return len(args) == 2


def cs_RND(self, token, args):  # Random Int
    return random.randint(args[0], args[1])


def cs_CS_arg_validation(self, token, args):
    return len(args) == 1


def cs_CS(self, token, args):  # Cast to String
    return str(args[0])


def cs_CI_arg_validation(self, token, args):
    return len(args) == 1


def cs_CI(self, token, args):  # Cast to Int
    return int(args[0])


def cs_CF_arg_validation(args):
    return len(args) == 1


def cs_CF(args):  # Cast to Float
    return float(args[0])


def cs_CB_arg_validation(args):
    return len(args) == 1


def cs_CB(args):  # Cast to Bool
    return bool(args[0])


def cs_A_arg_validation(self, token, args):  # collection, index?, element
    return len(args) in (2, 3)


def cs_A(self, token, args):  # Add to collection
    if not isinstance(args[0], (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"Function 'A' takes a list or dict as the first parameter, not {type(args[0])}")
    collection = args[0]
    if isinstance(collection, list):
        if len(args) == 3:
            index = args[1]
            element = args[2]
            if not isinstance(index, int):
                self.error(ErrorCode.PARAMETER_ERROR, token, f"Function 'A' takes an int as the index to insert into, not {type(index)}")
            collection.insert(index, element)
        else:
            element = args[1]
            collection.append(element)
    else:
        if len(args) == 2:
            self.error(ErrorCode.PARAMETER_ERROR, token, f"Appending to a dictionary requires 3 parameters and 2 were passed")
        key = args[1]
        value = args[2]
        collection[key] = value


def cs_RM_arg_validation(self, token, args):  # collection, index
    return len(args) == 2


def cs_RM(self, token, args):
    if not isinstance(args[0], (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"Function 'RM' takes a list or dict as the first parameter, not {type(args[0])}")
    collection = args[0]
    if isinstance(collection, list):
        index = args[1]
        if not isinstance(index, int):
            self.error(ErrorCode.PARAMETER_ERROR, token, f"Function 'RM' takes an int as the index to remove from, not {type(index)}")
        collection.pop(index)
    else:
        key = args[1]
        if key not in collection:
            self.error(ErrorCode.KEY_NOT_FOUND, token, f"Key '{key}' not found in dictionary {collection}")
        del collection[key]


def cs_RMV_arg_validation(self, token, args):  # collection, value
    return len(args) == 2


def cs_RMV(self, token, args):
    if not isinstance(args[0], (list, dict)):
        self.error(ErrorCode.PARAMETER_ERROR, token, f"Function 'RMV' takes a list or dict as the first parameter, not {type(args[0])}")
    collection = args[0]
    if isinstance(collection, list):
        value = args[1]
        if value not in collection:
            self.error(ErrorCode.VALUE_NOT_FOUND, token, f"Value '{value}' not found in list {collection}")
        collection.remove(value)
    else:
        value = args[1]
        if value not in collection.values():
            self.error(ErrorCode.VALUE_NOT_FOUND, token, f"Value '{value}' not found in dictionary {collection}")
        for k, v in collection.items():
            if v == value:
                del collection[k]
                break
