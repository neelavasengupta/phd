import pandas as pd
import pathlib
import os.path
import re
from inout.neucube_data import NeuCubeRawData


class DataReader:

    def read_from_csv(self, path, separator, header):

        try:
            df = pd.read_csv(path, sep=separator, header=header)
        except:
            print('Cannot read a CSV file!')
            sys.exit(1)
        return df

    def read_from_folder(self, path, separator=',', header=None):
        samples = []

        print('Reading files from folder', path)

        # get the folder and all the file paths in the folder
        folder_path = pathlib.Path(path)
        file_paths = list(folder_path.glob('*'))

        # get the sample paths and the target paths in two different list

        (sample_file_paths, target_file_path) = self.get_csv_file_paths(file_paths)

        # create the sample datastructure as a list of dataframes
        print('reading sample files', end='')
        for s in sample_file_paths:
            sample_dataframe = self.read_from_csv(s, separator, header)
            samples.append(sample_dataframe)
            print('.', end='')
        print('completed!!')

        print('reading target file...', end='')
        target = self.read_from_csv(target_file_path[0], separator, header)
        print('completed!!')

        dataset = NeuCubeRawData(samples, target)
        return dataset

    def get_csv_file_paths(self, file_paths):
        sample_file_paths = []
        target_file_path = []
        for f in file_paths:
                if f.is_file():
                    filename = os.path.basename(str(f))
                    if re.match(r"(sam\d+).*\.csv", filename):
                        sample_file_paths.append(os.path.dirname(str(f))+os.sep+filename)
                    elif re.match(r"(tar).*\.csv", filename):
                        target_file_path.append(os.path.dirname(str(f))+os.sep+filename)

        # check for the number of sample and target file for sanity
        if len(target_file_path) != 1:
            print('No target file found in the folder!')
            sys.exit(1)
        if len(sample_file_paths) < 2:
            print('At least two sample files are expected!')
            sys.exit(1)
        return sample_file_paths, target_file_path


