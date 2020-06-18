from argparse import ArgumentParser

from rocrate import *
from madmp import *
from os.path import join


class Mapper:

    # TODO: The user does not have to explicitally mention the desired operation (rocrate to madmp or madmp to rocrate)
    #  		Based on the provided path, identify the type of the input and perform the mapping
    # TODO: Mapping will be based on the content of the file "mapping.json"
    # TODO: Integrate "CalcyteJS: https://code.research.uts.edu.au/eresearch/CalcyteJS" within madmp_to_rocrate to
    # 		generate a preview web page after mapping.

    def __init__(self, root_folder_path, output_path):
        self.root_folder_path = root_folder_path
        self.output_path = output_path

    def is_rocrate(self):
        """Check on a high level whether the provided root folder is for a rocrate."""
        print("Checking if file is a ro-crate...")
        files = [p[2] for p in walk(self.root_folder_path)]
        for file in files:
            if file == "ro-crate-metadata.jsonld":
                print("File is a ro-crate...")
                return True
        print("File is NOT a ro-crate...")
        return False

    def is_madmp(self):
        return False

    def rocrate_to_madmp(self):
        try:
            rocrate = ROCrate(self.root_folder_path)
            print("Converting ro-crate to madmp...")
            rocrate.nest_rocrate()
            rocrate.flatten_rocrate()
            madmp = rocrate.flat_rocrate_to_madmp()
            print("Conversion is complete.")
        except Exception as e:
            print("Failed to convert ro-crate to madmp.")
            print("ERROR:", e)
        try:
            print("Saving the generated madmp to the provided path...")
            with open(join(self.output_path, "generated-dmp.json"), 'w') as f:
                json.dump(madmp, f)
            print("Saving is complete.")
            print("The path of the generated madmp is:", join(
                self.output_path, "generated-dmp.json"))
        except Exception as e:
            print("Failed to save the generated madmp.")
            print("ERROR:", e)

    def madmp_to_rocrate(self, generate_preview=True):
        pass


def run(root_folder_path, output_path):
    mapper = Mapper(root_folder_path, output_path)
    if mapper.is_rocrate:
        mapper.rocrate_to_madmp()
    elif is_madmp:
        mapper.madmp_to_rocrate()
    else:
        raise Exception("The root folder includes neither ro-crate nor madmp.")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-r", "--root-folder", dest="root_folder_path", help="Path to the root folder corresponding "
                        "to a maDMP or RO-Crate.")
    parser.add_argument("-o", "--output-path", dest="output_path",
                        help="Path where to mapped data will be stored.")
    args = parser.parse_args()
    run(args.root_folder_path, args.output_path)
