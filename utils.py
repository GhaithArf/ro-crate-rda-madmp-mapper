import json
import requests
from collections import OrderedDict

ROCRATE_CURRENT_VERSION = 1.0
_SCHEMA_URL = "https://researchobject.github.io/ro-crate/{}/context.jsonld".format(
    ROCRATE_CURRENT_VERSION)
_LOG_PREFIX_ROCRATE = "[RO-Crate]"
_LOG_PREFIX_MADMP = "[MADMP]"
_LOG_PREFIX_MAPPER = "[MAPPER]"


def load_rocrate_schema():
    """Retrieve the RO-Crate JSON-LD Context and parse its content

    :return: dict including the content of rocrate context
    """
    try:
        response = requests.get(_SCHEMA_URL)
        response.raise_for_status()
        return json.loads(response.text)
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        raise Exception(
            "Unable to connect to the RO-Crate JSON-LD Context url!")


def get_json_keys(dictonary, keys_list):
    """Add all keys from a nested dict structure to a list.

    :param dictonary: dict object
    :param keys_list: list where keys will be added
    """
    if isinstance(dictonary, dict):
        for k, v in dictonary.items():
            keys_list.append(k)
            get_json_keys(v, keys_list)
    elif isinstance(dictonary, list):
        for i in dictonary:
            get_json_keys(i, keys_list)


def find_parent_keys(dictonary, value):
    """Recursively find all parents of a specific key based on its value.

    :param dictonary: dict object
    :param value: string representing the value for which the keys will be retrieved.

    :return: generator of the current sequence of keys.
    """
    if type(dictonary) is dict:
        for k, v in dictonary.items():
            if isinstance(v, dict) or isinstance(v, list):
                p = list(find_parent_keys(v, value))
                if p:
                    yield [k] + p[0]
            elif v == value:
                yield [k]
    elif type(dictonary) is list:
        for item, i in zip(dictonary, range(len(dictonary))):
            p = list(find_parent_keys(item, value))
            if p != []:
                yield [i] + p[0]


def flatten_json(dictionary):
    """Recursively flattens a nested json.

    :param dictionary: dict object to flatten
    :return: dict object containing flat json.
    """
    out = {}

    def flatten(element, name=''):
        if type(element) is dict:
            for a in element:
                flatten(element[a], name + a + '.')
        elif type(element) is list:
            i = 0
            for a in element:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = element
    flatten(dictionary)
    out_ordered = OrderedDict()
    for key, value in sorted(out.items()):
        out_ordered[key] = value
    return out_ordered


def unflatten_json(dictionary):
    """Recursively unflattens a nested json.

    :param dictionary: dict object to unflatten
    :return: dict containing nested json.
    """
    # TODO : clean
    resultDict = {}
    for key, value in dictionary.items():
        parts = key.split(".")
        d = resultDict
        for i, part in zip(range(len(parts[:-1])), parts[:-1]):
            if part not in d:
                if parts[i+1].isdigit():
                    d[part] = []
                elif part.isdigit():
                    d.append({})
                else:
                    d[part] = {}
            if part.isdigit():
                d = d[int(part)]
            else:
                d = d[part]

        if parts[-1].isdigit():
            d.append(value)
        else:
            d[parts[-1]] = value
        d = resultDict
        for part in parts[:-1]:
            if part.isdigit():
                d = d[int(part)]
            else:
                d = d[part]
            if type(d) is list:
                while {} in d:
                    d.remove({})
    return resultDict


def get_sequence_keys(directory):
    """Recursively get all key sequences of a dict.

    :param dictionary: dict object for which key sequences will be extracted
    :return: list containing all key sequences.
    """
    keys_paths = []

    def get_files(directory, prefix=[]):
        if type(directory) is dict:
            for filename in directory.keys():
                path = prefix+[filename]
                if isinstance(directory[filename], dict) or isinstance(directory[filename], list):
                    get_files(directory[filename], path)
                else:
                    keys_paths.append(path)
        elif type(directory) is list:
            for i, element in zip(range(len(directory)), directory):
                path = prefix+[i]
                get_files(element, path)
    get_files(directory)
    return keys_paths


def remove_digits_string(string):
    """Remove digits from a string and remove "." at the end of the string.

    :param string: str to delete the digits from
    :return: str without any digits
    """
    clean_string = ''.join(i for i in string if not i.isdigit()
                           ).replace("..", ".")
    clean_string = clean_string[:-
                                1] if clean_string.endswith(".") else clean_string
    return clean_string

def _add_key_value_all(dictonary, key="@id", value=""):
    """Recursively add key ("@id") with value ("") to facilitate tracking.

    :param dictonary: dict object
    :param key: str of the key to add
    :param value: str of the value to add
    """
    if type(dictonary) is dict:
        for k, v in dictonary.items():
            if type(v) is list:
                _add_key_value_all(v, key, value)
            elif type(v) is dict:
                v[key] = value
                _add_key_value_all(v, key, value)
    elif type(dictonary) is list:
        for item in dictonary:
            if not type(item) is str:
                item[key] = value
                _add_key_value_all(item, key, value)

def get_unnested_jsonld(dictionary):
    """Unnest json to prepare for jsonld format.
        "@id" should be present

    :param dictionary: dict object to unnest
    :return: dict object containing unnested json
    """
    keys_sequences = get_sequence_keys(dictionary)
    for record in keys_sequences:
        del record[-1]
    keys_sequences = [list(i) for i in set(tuple(i)
                                           for i in keys_sequences)]
    keys_sequences.sort(key=len, reverse=True)

    out = dictionary.copy()
    for keys_sequence in keys_sequences:
        if len(keys_sequence) >= 2:
            val = out
            for level in keys_sequence[:-1]:
                val = val[level]
            if type(val) is dict:
                current_dict = val[keys_sequence[-1]]
                current_dict["@type"] = keys_sequence[-1]
            out.append(current_dict) if current_dict not in out else out
            val2 = out
            for level in keys_sequence[:-2]:
                val2 = val2[level]
            try:
                val2[keys_sequence[-2]
                     ] = {"@id": val2[keys_sequence[-2]][keys_sequence[-1]]["@id"]}
            except:
                print("Warning: @id not found")
    return out


def log(msg):
    """Add prefix to the provided message and print the result.

    :param msg: message to be printed.
    """
    # TODO: Implement this
    # Dynamically identify the module where the function was called, add prefix accordignly and print
    module = ""
    if "mapper" in module.lower():
        print("{}: {}".format(_LOG_PREFIX_MAPPER, msg))
    elif "rocrate" in module.lower():
        print("{}: {}".format(_LOG_PREFIX_ROCRATE, msg))
    elif "madmp" in module.lower():
        print("{}: {}".format(_LOG_PREFIX_MADMP, msg))
