import numpy as np
from scipy import signal


class EncoderBase:

    def calculate_decoding_rmse(self, data, recon_data):
        data = np.array(data)
        recon_data = np.array(recon_data)
        absolute_error = data-recon_data
        rmse = np.sqrt(np.sum(absolute_error*absolute_error)/absolute_error.size)
        return rmse


class TC(EncoderBase):

    def __init__(self, factor):
        self.factor = factor

    def encode(self, temporal_data):
        temporal_data = np.array(temporal_data)
        num_features, num_time = temporal_data.shape
        spike_train = np.zeros(temporal_data.shape)

        changes = np.diff(temporal_data, n=1, axis=1)
        spike_threshold = np.mean(abs(changes), axis=1) + self.factor*np.std(abs(changes), axis=1)
        changes = np.concatenate((np.zeros((num_features, 1)), changes), axis=1)

        for i in range(0,num_features):
            for j in range(0,num_time):
                if changes[i, j] > spike_threshold[i]:
                    spike_train[i, j] = 1
                elif changes[i, j] < -spike_threshold[i]:
                    spike_train[i, j] = -1

        recon_data = self.decode(spike_train, spike_threshold)
        decoding_rmse = self.calculate_decoding_rmse(temporal_data, recon_data)
        return spike_train.tolist(), spike_threshold.tolist(), decoding_rmse

    def decode(self, spike_train, spike_threshold):
        spike_train = np.array(spike_train)
        num_features, num_time = spike_train.shape
        temporal_data = np.zeros(spike_train.shape)
        for i in range(0,num_features):
            for j in range(1,num_time):
                if spike_train[i, j] > 0:
                    temporal_data[i, j] = temporal_data[i, j-1]+spike_threshold[i]
                elif spike_train[i, j] < 0:
                    temporal_data[i, j] = temporal_data[i, j-1]-spike_threshold[i]
                else:
                    temporal_data[i, j] = temporal_data[i, j-1]

        return temporal_data.tolist()


class BSA(EncoderBase):
    def __init__(self, num_tap, cutoff, bsa_threshold):
        self.num_tap = num_tap
        self.cutoff = cutoff
        self.bsa_threshold = bsa_threshold
        self.filt = signal.firwin(num_tap, cutoff, window='hamming')  # differs from matlab implementation

    def encode(self, temporal_data):
        temporal_data = np.array(temporal_data)
        spike_train = np.zeros(temporal_data.shape)
        filt = np.array(self.filt)
        filt_length = filt.size
        num_features, num_time = temporal_data.shape

        for i in range(0, num_features):
            for j in range(0, (num_time-filt_length+1)):
                error1 = 0
                error2 = 0
                for k in range(0, filt_length):
                    error1 = error1 + np.abs(temporal_data[i, j+k] - filt[k])
                    error2 = error2 + np.abs(temporal_data[i, j+k])

                if error1 <= (error2-self.bsa_threshold):
                    spike_train[i, j] = 1
                    for k in range(0, filt_length):
                        temporal_data[i, j+k] = temporal_data[i, j+k]-filt[k]

        recon_data = self.decode(spike_train)
        decoding_rmse = self.calculate_decoding_rmse(temporal_data, recon_data)
        return spike_train.tolist(), decoding_rmse

    def decode(self, spike_train):
        spike_train = np.array(spike_train)
        temporal_data = np.zeros(spike_train.shape)
        filt = np.array(self.filt)
        filt_length = filt.size
        num_features, num_time = spike_train.shape
        for i in range(0, num_features):
            for j in range(0, num_time-filt_length+1):
                if spike_train[i, j] == 1:
                    for k in range(0, filt_length):
                        temporal_data[i, j+k] = temporal_data[i, j+k] + filt[k]
        return temporal_data.tolist()


my_data = [[1.43, 2.00, 0.53, 7.21], [5.34, 2.87, 1.11,3.21], [1.43, 2.00, 5.33, 2.21]]
temp_cont =TC(0.5)
result = temp_cont.encode(my_data)
print(result)
bens_spiker = BSA(3, 0.05, 0.6)
result = bens_spiker.encode(my_data)
print(result)
