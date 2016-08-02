import pandas as pd


class NeuCubeRawData:

    def __init__(self, sample, target):
        assert isinstance(target, pd.DataFrame)
        assert isinstance(sample, list)
        self.sample = sample
        self.target = target

    def get_sample(self):
        return self.sample

    def set_sample(self, sample):
        """

        :type sample: list
        """
        assert isinstance(sample, list)
        self.sample = sample

    def get_target(self):
        return self.target

    def set_target(self, target):
        """

        :type target: DataFrame
        """
        assert isinstance(target, pd.DataFrame)
        self.target = target
