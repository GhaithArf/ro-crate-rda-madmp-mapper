import json
from os import listdir, walk
from os.path import isfile, join
import pprint
from utils import get_json_keys, load_rocrate_schema, find_parent_keys, flatten_json, unflatten_json, remove_digits_string
import re
import ast


_ROCRATE_METADATA_FILENAME = "ro-crate-metadata.jsonld"
_ROCRATE_PREVIEW = "ro-crate-preview.html"


class ROCrate:

    # TODO: Use class methods
    # TODO: Create separate classes for preview and metadata???
    # TODO: GENERAL: Use prefixes for the different components of the framework when "logging"/stdout printing
    #		Example: [RO-Crate] log message
    #				 [maDMP] log message
    #		Look at log helper function in utils
    # TODO: Fix docstrings

    def __init__(self, path):
        self.root_folder = self.locate_root_folder(path)
        self.metadata = self.load_metadata()
        # self.preview = self.load_preview()

    @staticmethod
    def locate_root_folder(path, check_name=True):
        """Locate the root folder of the project based on the RO-Crate metadata file.

        :param path: path to crawl
        :param check_name: if True look for "ro-crate-metadata.jsonld", otherwise consider all "jsonld" files.
        :return: path of the root directory of the project
        """
        # The RO-Crate Metadata File MUST be named ro-crate-metadata.jsonld and appear in the RO-Crate Root
        # This method will locate the first folder that contains metadata file and does not check for multiple
        # TODO: Consider the case where mutliple metadata files exist
        subdirs = [p[0] for p in walk(path)]
        for dir in subdirs:
            if check_name:
                if isfile(join(dir, _ROCRATE_METADATA_FILENAME)):
                    return dir
            else:
                for file in listdir(dir):
                    if file.lower().endswith('.jsonld'):
                        return dir

    def load_metadata(self):
        """Load the metadata file located at the root folder."""
        metadata_file = [file for file in listdir(
            self.root_folder) if file.endswith('.jsonld')]
        if metadata_file:
            with open("{}/{}".format(self.root_folder, metadata_file[0]), 'r') as file:
                if metadata_file != _ROCRATE_METADATA_FILENAME:
                    print("Warning: Metadata file name: '{}' is different than {}".format(
                        metadata_file, _ROCRATE_METADATA_FILENAME))
                print("Loading metadata file...")
                try:
                    return json.loads(file.read())
                except json.JSONDecodeError:
                    raise Exception(
                        "RO-Crate metadata file is not a valid JSON document.")
        else:
            raise Exception("Unable to locate metadata file.")

    def check_metadata_schema(self):
        """Return True if the metadata schema matches the expected one, False otherwise."""
        # TODO: Consider all metadata attributes
        current_attributes = []
        get_json_keys(self.metadata, current_attributes)
        schema_attributes = []
        rocrate_schema = load_rocrate_schema()
        get_json_keys(rocrate_schema, schema_attributes)
        return set(current_attributes).issubset(set(schema_attributes))

    def load_preview(self, check_name=True, check_metadata=True):
        """Return True if a RO-Crate website exists, False otherwise.

        :param check_name: if True look for "ro-crate-preview.html", otherwise consider all "html" files.
        """
        # html file: MUST Contain a copy of the RO-Crate JSON-LD in a script element of the head element of the HTML
        # TODO: Clean and probably restructure (too many local variables)
        subdirs = [p[0] for p in walk(self.root_folder)]
        html_path = None
        for dir in subdirs:
            if check_name:
                if isfile(join(dir, _ROCRATE_PREVIEW)):
                    html_path = join(dir, _ROCRATE_PREVIEW)
                    break
            else:
                for file in listdir(dir):
                    if file.endswith('.html'):
                        html_path = join(dir, _ROCRATE_PREVIEW)
                        break
        if html_path:
            print("Loading preview webpage...")
            html_file = open(html_path, 'r', encoding="utf-8")
            source_code = html_file.read()
            if check_metadata:
                # TODO: IMPROVE: use python native html parser instead of relyin on regex
                source_code_trimmed = source_code.replace(
                    "\n", "").replace('\r', '')
                search = re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>', source_code_trimmed)
                if not json.loads((search[0])) == self.metadata:
                    raise Exception(
                        "Preview webpage found, but does not contain a copy of the RO-Crate metadata.")
            return source_code
        else:
            print("Unable to locate preview webpage.")
            return None

    def nest_rocrate(self, include_type=True):
        """Converts self.metadata from a flat jsonld to a nested json.

        :param include_type: if True include "@type" in value to nest, otherwise it is not included.
        """
        jsonld_graph = self.metadata["@graph"]
        idns = []
        self._get_identifiers(jsonld_graph, idns)

        for idn in idns:
            # get all set of parents of the current id's value
            keys_maps = list(find_parent_keys(jsonld_graph, idn))
            # get the attribute that has to be nested (contains only two keys)
            att_to_nest = [keys_map[0]
                           for keys_map in keys_maps if len(keys_map) == 2]
            delete_att = False
            # if there is an attribute to nest, iterate over all key sequences and nest
            if att_to_nest != []:
                for keys_map in keys_maps:
                    val = jsonld_graph
                    if len(keys_map) > 2:
                        value_att_tonest = jsonld_graph[att_to_nest[0]]
                        self._nest_current_id(
                            keys_map, value_att_tonest, val, include_type)
                        delete_att = True
            # once att is nested in a deeper structure, delete it from flat structure
            if delete_att:
                del jsonld_graph[att_to_nest[0]]
        self.metadata = jsonld_graph

    def flatten_rocrate(self):
        """Converts self.metadata from a nested json to a flat json."""
        self.metadata = flatten_json(self.metadata)

    def flat_rocrate_to_madmp(self):
        """Converts flat rocrate to madmp.

        :return: dict object represent madmp
        """
        with open("mapping.json", 'r') as outfile:
            mapping_data = json.loads(outfile.read())
        madmp = {}
        status_list = []
        eq_dmp = self._get_root_keys()
        madmp_initial = {}
        self._modify_based_on_root(eq_dmp, madmp_initial)
        # convert the keys
        level_id = 0
        for key_flat, value_flat in madmp_initial.items():
            key_clean = remove_digits_string(key_flat)
            level_id, new_item = self._check_if_new_item(level_id, key_clean)
            # search for madmp map eq to rocrate map
            changed_chars = 0
            k_flat = key_clean
            for rocrate_att, madmp_att in mapping_data.items():
                if k_flat.find(rocrate_att) != -1:
                    changed_chars += len(rocrate_att)
                    k_flat = k_flat.replace(rocrate_att, madmp_att)
            # only keep keys which changed entirely (all chars replaced)
            if changed_chars == len(key_clean):
                self._update_status_list(
                    level_id, new_item, k_flat, status_list)
                for level in status_list:
                    k_flat = k_flat.replace(
                        "." + level[0] + ".", "." + level[0] + "." + str(level[2]) + ".")
                madmp[k_flat] = value_flat
        self.add_necessary_missing_att(madmp)
        madmp = unflatten_json(madmp)
        return madmp

    def has_preview_files(self):
        pass

    def has_dataset_payload(self):
        # The base RO-Crate specification makes no assumptions about the presence of any specific files or folders
        # beyond the reserved RO-Crate files described above. Payload files may appear directly in the RO-Crate Root
        # alongside the RO-Crate Metadata File, and/or appear in sub-directories of the RO-Crate Root. Each file and
        # directory MAY be represented as Data Entities in the RO-Crate Metadata File.
        pass

    @staticmethod
    def _get_identifiers(jsonld_graph, idns):
        """Get all identifiers (value of attribute starting with "@id") in "@graph" element.

        :param jsonld_graph: dict object corresponding to the element @graph of jsonld
        :param idns: list where all values of "@id" will be added
        """
        for sub in jsonld_graph:
            for key_elmt, value_elmt in sub.items():
                if type(value_elmt) is list:
                    for element in value_elmt:
                        if "@id" in element:
                            idns.append(element["@id"])
                else:
                    idns.append(sub['@id'])

    @staticmethod
    def _nest_current_id(keys_map, value_att_tonest, val, include_type):
        """Nest attribute corresponding to the current sequence of keys_map.

        :param keys_map: list that includes all parents of a specific "@id" value
        :param value_att_tonest: string of unmodified value of the attribute to nest
        :param val: dict object that will reflect the changes of new nested attribute
        :param include_type: if True include "@type" in value to nest, otherwise it is not included.
        """
        # create modified value of att to nest
        for level in keys_map[: -1]:
            val = val[level]
        if not include_type:
            feed_val = str(dict([(key, value) for key, value in value_att_tonest.items(
            ) if key not in ["@type"]]))
        else:
            feed_val = str(dict([(key, value) for key, value in value_att_tonest.items(
            )]))
        # create modified key of att to nest based on "@type"
        feed_key = value_att_tonest["@type"]
        # nest value and delete @id from parent
        val[feed_key if type(feed_key) is str else feed_key[0]] = ast.literal_eval(
            feed_val)
        del val["@id"]

    def _get_root_keys(self):
        """Get the keys corresponding to the root. The root is when the value of @id is "./".
        (The root is equivalent to "dmp" attribute in madmp.)
        (This is implemented because the root is different for different versions of ro-crate.)

        :return: str containing joint keys corresponding to the root.
        """
        for key_flat, value_flat in self.metadata.items():
            if key_flat.endswith("path") or key_flat.endswith("@id") and value_flat == "./":
                return ".".join(key_flat.split(".")[:-1])

    def _modify_based_on_root(self, eq_dmp, madmp_initial):
        """Replace the keys corresponding to the root with __root__ and delete att not related to root.

        :param madmp_initial: dict object including rocrate attributes starting with __root__
        """
        for key_flat, value_flat in self.metadata.items():
            if key_flat.startswith(eq_dmp):
                new_key = key_flat.replace(eq_dmp, "_root_", 1)
                madmp_initial[new_key] = value_flat

    @staticmethod
    def _check_if_new_item(level_id, key):
        """ Checks if the current key is corresponding to a new item.
            A new item includes "@id" in its key. 

        :param level_id: int including level of @id from latest key
        :param key: str including the key to the new item
        :return: True if key corresponds to a new item, otherwise False
        :return: int which is updated if it is a new item, otherwise int old 
        """
        if "@id" in key:
            level_id = key.split(".").index("@id")
            return level_id, True
        return level_id, False

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
        dmptype_list = ["distribution", "contributor", "contact"]
        for x in k_flat.split("."):
            if x in dmptype_list:
                if x not in [kk[0] for kk in status_list]:
                    status_list.append([x, level_id, 0])
                else:
                    for level in status_list:
                        if level[0] == x and level[1] == level_id and new_item:
                            level[2] += 1

    def add_necessary_missing_att(self, madmp):
        """Add the attributes which should be present in madmp. But, are missing.
            The madmp schema should be loaded.
            https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard/blob/master/examples/JSON/JSON-schema/1.0/maDMP-schema-1.0.json
            If attribute is in required and is not in madmp, it should be defautled."""
        # TODO: implement
        pass

    def __repr__(self):
        return pprint.pformat(self.metadata)
