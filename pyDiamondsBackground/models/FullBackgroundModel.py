import numpy as np

from pyDiamondsBackground.models.BackgroundModel import BackgroundModel


class FullBackgroundModel(BackgroundModel):
    def __init__(self, covariates):
        self._covariates = covariates
        BackgroundModel.__init__(self, covariates, 12, "Full Background model")

    def predict(self, predictions, modelParameters):
        flatNoiseLevel = modelParameters[0]
        amplitudeNoise = modelParameters[1]
        frequenceNoise = modelParameters[2]
        amplitudeHarvey1 = modelParameters[3]
        frequencyHarvey1 = modelParameters[4]
        amplitudeHarvey2 = modelParameters[5]
        frequencyHarvey2 = modelParameters[6]
        amplitudeHarvey3 = modelParameters[7]
        frequencyHarvey3 = modelParameters[8]
        heightOscillation = modelParameters[9]
        nuMax = modelParameters[10]
        sigma = modelParameters[11]

        zeta = 2 * np.sqrt(2) / np.pi
        predictions = zeta * amplitudeHarvey1 ** 2 / (
            frequencyHarvey1 * (1 + np.power(self._covariates / frequencyHarvey1, 4)))

        predictions += zeta * amplitudeHarvey2 ** 2 / (
            frequencyHarvey2 * (1 + np.power(self._covariates / frequencyHarvey2, 4)))

        predictions += zeta * amplitudeHarvey3 ** 2 / (
            frequencyHarvey3 * (1 + np.power(self._covariates / frequencyHarvey3, 4)))

        predictions += heightOscillation * np.exp(-1*np.power(nuMax-self._covariates,2)/(2*sigma**2))

        predictions *= self._responseFunction

        predictions += flatNoiseLevel
        predictions += 2*np.pi*amplitudeNoise**2/(frequenceNoise(1+np.power(self._covariates/frequenceNoise,2)))

        return predictions
