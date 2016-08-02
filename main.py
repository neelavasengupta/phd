from inout import reader

def main():

    # read data from folder
    folder_path = '/home/neelava/Desktop/data/share_price'
    datareader = reader.DataReader()
    dataset = datareader.read_from_folder(folder_path)


if __name__ == '__main__':
    main()
