from os import listdir, makedirs
from os.path import isfile, isdir, join, dirname, abspath
import pprint
import copy
import logging
import re

from utils import *


logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)s][%(module)s]: %(message)s")


class MADMP:

    def __init__(self, path):
        self.path = path
        self.madmp = self.load_madmp()

    def load_madmp(self):
        """Load the metadata file from the given path"""
        json_path = None
        if isfile(self.path) and self.path.lower().endswith(".json"):
            json_path = self.path
        elif isdir(self.path):
            # Look in the root path only! Do not look in subfolders since dataset itself may include json files
            for file in listdir(self.path):
                if file.lower().endswith('.json'):
                    json_path = join(self.path, file)
                    with open(json_path, 'r') as file:
                        try:
                            madmp = json.loads(file.read())
                            logging.info(
                                "Successfully located the maDMP json file within the provided path.")
                            # Update path accordingly
                            setattr(self, "path", json_path)
                            logging.info(
                                "The maDMP path is set to {}".format(json_path))
                            break
                        except:
                            pass
        if not json_path:
            raise Exception(
                "Unable to locate the maDMP json file using the provided path.")
        try:
            with open(json_path, 'r') as file:
                logging.info("Loading maDMP file...")
                try:
                    return json.loads(file.read())
                except json.JSONDecodeError:
                    raise Exception("maDMP file is not a valid JSON document.")
        except FileNotFoundError:
            raise Exception("Unable to open the json maDMP file.")

    def convert_madmp_to_rocrate(self, output_path):
        """Converts madmp to many rocrates and save them to json files.
        """
        # load mapping data
        with open("mapping.json", 'r') as outfile:
            mapping_data = json.loads(outfile.read())
        for i in range(len(self.madmp["dmp"]["dataset"])):
            # keep only one dataset for each iteration (one-to-many)
            current_dataset = copy.deepcopy(self.madmp)
            current_dataset["dmp"]["dataset"] = current_dataset["dmp"]["dataset"][i]
            rocrate = self._convert_one_of_many(
                current_dataset, mapping_data)
            # create folders for each rocrate and save json file there
            try:
                folder_name = current_dataset["dmp"]["dataset"]["title"]
            except:
                folder_name = "dataset_" + str(i)
            self._save_one_rocrate(rocrate, output_path, folder_name)

    @staticmethod
    def _save_one_rocrate(rocrate, output_path, title):
        title = re.sub('[><:/\"|?*]', "", title).replace("\\", "")
        path_direc = join(dirname(
            abspath(__file__)), join(output_path, title))
        if len(path_direc) >= 240:
            path_direc = u'\\\\?\\' + path_direc
        try:
            makedirs(path_direc, exist_ok=True)
        except OSError as e:
            logging.error("Creation of the directory %s failed" %
                          join(output_path, title))
            raise e
        else:
            logging.info("Successfully created the directory %s " %
                         join(output_path, title))
        try:
            logging.info(
                "Saving the generated rocrate of {}to the provided path...".format(title))
            with open(join(path_direc, "ro-crate-metadata.jsonld"), 'w') as f:
                json.dump(rocrate, f, indent=4)
            logging.info("Saving is complete.")
        except:
            logging.error("Failed to save the generated rocrate.")

    def _convert_one_of_many(self, current_dataset, mapping_data):
        """Convert one of the dataset to a rocrate.

        :param current_dataset: dict object consisting of the dmp with only one dataset left.
        :return: dict object including a converted madmp.
        """
        rocrate = {}
        status_list = []
        # flaten json
        add_key_value_all(current_dataset)
        json_flattened = flatten_json(current_dataset)
        level_id = 0
        new_item = False
        for key_flat, value_flat in json_flattened.items():
            key_clean = remove_digits_string(key_flat)
            level_id, new_item = self._check_if_new_item(
                level_id, new_item, key_clean)
            # search for rocrate map eq to madmp map
            changed_chars = 0
            k_flat = key_clean
            for rocrate_att, madmp_att in mapping_data.items():
                if k_flat.find(madmp_att) != -1:
                    changed_chars += len(madmp_att)
                    k_flat = k_flat.replace(madmp_att, rocrate_att)
            # only keep keys which changed entirely (all chars replaced)
            if changed_chars == len(key_clean):
                self._update_status_list(
                    level_id, new_item, k_flat, status_list)
                for level in status_list:
                    k_flat = k_flat.replace(
                        "." + level[0] + ".", "." + level[0] + "." + str(level[2]) + ".")
                new_item = False
                rocrate[k_flat] = value_flat
        rocrate = unflatten_json(rocrate)
        rocrate = self.convert_json_jsonld(rocrate)
        return rocrate

    @staticmethod
    def _check_if_new_item(level_id, new_item, key):
        """ Checks if the current key is corresponding to a new item.
            A new item includes "@id" in its key. 

        :param level_id: int including level of @id from latest key
        :param new_item: True if item is new, otherwise False
        :param key: str including the key to the new item
        :return: True if key corresponds to a new item, otherwise False
        :return: int which is updated if it is a new item, otherwise int old 
        """
        if "@id" in key:
            level_id = key.split(".").index("@id")
            return level_id, True
        return level_id, new_item

    @staticmethod
    def convert_json_jsonld(json_nested):
        """ Convert from json to jsonld and include other missing mandatory attributes.

        :param json_nested: dict object to convert
        :return: dict object containg the obtained jsonld
        """
        jsonld = {}
        jsonld["@context"] = "https://w3id.org/ro/crate/1.0/context"
        json_inter = []
        json_inter.append(json_nested)
        jsonld["@graph"] = get_unnested_jsonld(json_inter)
        jsonld["@graph"].append({
            "@type": "CreativeWork",
            "@id": "ro-crate-metadata.jsonld",
            "conformsTo": {"@id": "https://w3id.org/ro/crate/1.0"},
            "about": {"@id": "./"}
        })
        elements_to_keep = []
        for elmnt in jsonld["@graph"]:
            if "_root_" not in elmnt:
                elements_to_keep.append(elmnt)
        jsonld["@graph"] = elements_to_keep

        for elmnt in jsonld["@graph"]:
            try:
                if elmnt["@type"] == "_root_":
                    elmnt["@type"] = "Dataset"
                    elmnt["@id"] = "./"
            except:
                pass

        return jsonld

    @staticmethod
    def _update_status_list(level_id, new_item, k_flat, status_list):
        """ Creates a status list. It is needed in order not to overwrite 
        other keys with the same name. This is relevant for attributes with
        type list or nested structure. The nested list includes:
            - the attribute name for which there is more than one value.
            - level_id to monitor at which level the attribute was encountered.
                Attributes can be used at different levels
            - the number of occurences of that attribute

        :param level_id: int including level of @id from latest key
        :param new_item: True if key corresponds to a new item, otherwise False
        :param k_flat: str including the key to the current key
        :param status_list: list of lists reflecting the current status
        """
        # TODO : test the method thoroughly
        rocratetype_list = ["hasPart", "creator",
                            "author", "distribution", "project"]
        for x in k_flat.split("."):
            if x in rocratetype_list:
                if x not in [kk[0] for kk in status_list]:
                    status_list.append([x, level_id, 0])
                else:
                    for level in status_list:
                        if level[0] == x and level[1] == level_id and new_item:
                            level[2] += 1

    def __repr__(self):
        return pprint.pformat(self.madmp)
