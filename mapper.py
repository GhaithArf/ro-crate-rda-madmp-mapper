from argparse import ArgumentParser
from rocrate import *
from madmp import *
from os.path import join


logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s][%(module)s]: %(message)s")


class Mapper:

    # TODO: Integrate "CalcyteJS: https://code.research.uts.edu.au/eresearch/CalcyteJS" within madmp_to_rocrate to
    # 		generate a preview web page after mapping.

    def __init__(self, root_folder_path, output_path):
        self.root_folder_path = root_folder_path
        self.output_path = output_path
        self.madmp = {}

    def is_rocrate(self):
        """Check on a high level whether the provided root folder is for a rocrate."""
        logging.info("Checking if file is a ro-crate...")
        filenames = [p[2] for p in walk(self.root_folder_path)]
        for filename in filenames:
            for file in filename:
                if file == "ro-crate-metadata.jsonld":
                    logging.info("File is a ro-crate...")
                    return True
        logging.info("File is NOT a ro-crate...")
        return False

    def is_madmp(self):
        try:
            logging.info("Checking if file is a madmp...")
            self.madmp = MADMP(self.root_folder_path)
            return True
        except:
            logging.info("File is NOT a madmp...")
            return False

    def rocrates_to_madmp(self):
        try:
            logging.info("Converting ro-crate(s) to madmp...")
            filepaths = [join(path, name) for path, subdirs, files in walk(
                self.root_folder_path) for name in files]
            all_parts = []
            for filepath in filepaths:
                if filepath.endswith("ro-crate-metadata.jsonld"):
                    rocrate = ROCrate(filepath.split(
                        "ro-crate-metadata.jsonld")[0])
                    part_of_madmp = rocrate.convert_rocrate_to_madmp()
                    all_parts.append(part_of_madmp)
            rocrate.merge_converted_rocrates(all_parts, self.output_path)
            logging.info("Conversion is complete.")
        except Exception as e:
            logging.error("Failed to convert ro-crate(s) to madmp.")
            logging.error("ERROR: {}".format(e))

    def madmp_to_rocrate(self, generate_preview=False):
        try:
            logging.info("Converting madmp to ro-crate(s)...")
            self.madmp.convert_madmp_to_rocrate(self.output_path)
        except Exception as e:
            logging.error("Failed to convert madmp to ro-crate(s).")
            logging.error("ERROR: {}".format(e))


def run(root_folder_path, output_path):
    mapper = Mapper(root_folder_path, output_path)
    if mapper.is_rocrate():
        mapper.rocrates_to_madmp()
    elif mapper.is_madmp():
        mapper.madmp_to_rocrate()
    else:
        logging.error("The root folder includes neither ro-crate nor madmp.")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-path", dest="input_path", help="Path to the root folder corresponding "
                        "to a maDMP or RO-Crate.")
    parser.add_argument("-o", "--output-path", dest="output_path",
                        help="Path where to mapped data will be stored.")
    args = parser.parse_args()
    run(args.input_path, args.output_path)
