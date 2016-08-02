import pandas as pd
import numpy as np

class NeuCubeRawData:

    def __init__(self, samples, sample_indices, target):
        assert isinstance(target, pd.DataFrame)
        assert isinstance(samples, list)
        self.samples = samples
        self.sample_indices = sample_indices
        self.target = target
        self.number_of_samples = len(samples)
        self.number_of_features, self.number_of_timepoints = samples[0].shape

    def get_samples(self):
        return self.samples

    def set_samples(self, samples):
        """

        :type sample: list
        """
        assert isinstance(samples, list)
        self.samples = samples

    def get_target(self):
        return self.target

    def set_target(self, target):
        """

        :type target: DataFrame
        """
        assert isinstance(target, pd.DataFrame)
        self.target = target

    def normalise_samples(self):
        normalised_samples = []
        for i in range(0, len(self.samples)):
            data_to_normalise = self.samples[i].values
            maximum = np.max(data_to_normalise, axis=0)
            minimum = np.min(data_to_normalise, axis=0)
            data_to_normalise = (data_to_normalise - minimum)/(maximum-minimum)
            normalised_samples.append(pd.DataFrame(data_to_normalise))
            return NeuCubeRawData(normalised_samples, self.sample_indices, self.target)

