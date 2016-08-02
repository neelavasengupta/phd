from inout import reader

def main():

    # read data from folder
    folder_path = '/home/neelava/Desktop/data/wrist_movement_eeg'
    datareader = reader.DataReader()
    dataset = datareader.read_from_folder(folder_path)
    dataset = dataset.normalise_samples()

if __name__ == '__main__':
    main()
