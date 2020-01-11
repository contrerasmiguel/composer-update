from ruamel.yaml import YAML
from ruamel.yaml import StringIO
from collections import MutableMapping

def to_dict(raw_yaml):
    return YAML().load(StringIO(raw_yaml))

def debug_print(value):
    print('')
    print(value)
    print('')

def rec_merge(d1, d2):
    '''
    Update two dicts of dicts recursively, 
    if either mapping has leaves that are non-dicts, 
    the second's leaf overwrites the first's.
    '''
    for k, v in d1.items(): # in Python 2, use .iteritems()!
        if k in d2:
            # this next check is the only difference!
            if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                d2[k] = rec_merge(v, d2[k])
            # we could further check types and merge as appropriate here.
    d3 = d1.copy()
    d3.update(d2)
    return d3

def ordereddict_to_dict(value):
    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = ordereddict_to_dict(v)
    return dict(value)