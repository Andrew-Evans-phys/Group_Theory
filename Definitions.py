#imports
import sys
from Errors import *

#Group definition
class Group:
    def __init__(self, _set, _operation_var) -> None:
        identity = None
        identity_found = False
        for e_test in _set: #what happens if this ends and finds no identity? -> Error
            if(e_test == _operation_var(e_test, e_test)): #identity test x = x^2 => x = e
                identity_found = True
                identity = e_test
                break

        if(identity_found == False):
            raise FailsIdentity

        inverses = [] #stored as a list of set of pairs of x and x_inv
        for x in _set:
            x_inv_found = False
            for x_inv in _set:
                inv_pair = {x, x_inv}
                if(identity == _operation_var(x_inv, x) and identity == _operation_var(x, x_inv)):
                    inverses_contained = bool(inverses.count(inv_pair))
                    if(inverses_contained):
                        x_inv_found = True
                        pass
                    else:
                        inverses.append(inv_pair)
                        x_inv_found = True

            if(x_inv_found == False):
                raise FailsInverse

        set_form = set(_set)
        for a in _set:
            for b in _set:
                ab = _operation_var(a,b)
                if(ab not in set_form):
                    raise FailsClosure
                for c in _set:
                    if(not(_operation_var(ab,c) == _operation_var(a,_operation_var(b,c)))):
                        raise FailsAssociativity

        #Assuming all the above conditions were met you now have a brand new group!
        self._set = _set
        self._operation_var = _operation_var
        self.order = len(_set)
        self.identity = identity

    def _operation(self, a, b): #type should be looked into, varible function return?
        set_form = self._set_to_set()
        if(a not in set_form or b not in set_form):
            raise NotAnElement
        return self._operation_var(a, b)

    def _set_to_set(self):
        return set(self._set)

#Cyclic subgroup generated by a
class Cyclic_subgroup(Group):
    def __init__(self, _set, _operation, a) -> None:
        super().__init__(_set, _operation)
        a_to_n = a
        _replace_set = [a_to_n]
        while(self.identity != a_to_n):
            a_to_n = self._operation(a_to_n, a)
            _replace_set.append(a_to_n)
        self._set = _replace_set


def gcd(a, b):
    if(b == 0):
        return abs(a)
    else:
        return gcd(b, a % b)