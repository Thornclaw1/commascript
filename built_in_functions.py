import random
import codecs


def cs_P_arg_validation(self, args):
    return True


def cs_P(self, args):  # Print
    arg_vals = []
    for arg in args:
        arg_vals.append(codecs.decode(str(self.visit(arg)), 'unicode_escape'))
    print(*arg_vals)


def cs_I_arg_validation(self, args):
    return len(args) in (0, 1)


def cs_I(self, args):  # Input
    prompt = codecs.decode(str(self.visit(args[0])), 'unicode_escape') if len(args) > 0 else ""
    return input(prompt)


def cs_RND_arg_validation(self, args):
    return len(args) == 2


def cs_RND(self, args):  # Random Int
    return random.randint(self.visit(args[0]), self.visit(args[1]))


def cs_CS_arg_validation(self, args):
    return len(args) == 1


def cs_CS(self, args):  # Cast to String
    return str(self.visit(args[0]))


def cs_CI_arg_validation(self, args):
    return len(args) == 1


def cs_CI(self, args):  # Cast to Int
    return int(self.visit(args[0]))


def cs_CF_arg_validation(self, args):
    return len(args) == 1


def cs_CF(self, args):  # Cast to Float
    return float(self.visit(args[0]))


def cs_CB_arg_validation(self, args):
    return len(args) == 1


def cs_CB(self, args):  # Cast to Bool
    return bool(self.visit(args[0]))
