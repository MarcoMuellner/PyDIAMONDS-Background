import numpy as np
import pyDiamonds as diamonds

class Background:
    def __init__(self,kicID,model,data,resultsPath,backgroundHyperParameters,nyquistFrequency,
                 xMeansConfiguratingParameters = None,nsmConfiguringParameters = None):
        self.backgroundModel = model
        self.data = data
        self._resultsPath = resultsPath
        self.backgroundHyperParameters = backgroundHyperParameters
        self._nyquistFrequency = nyquistFrequency

        if xMeansConfiguratingParameters is not None:
            self._xMeansConfigurating =xMeansConfiguratingParameters
        else:
            self._xMeansConfigurating = self.xMeansDefault()


        if nsmConfiguringParameters is not None:
            self._nsmConfiguringParameters = nsmConfiguringParameters
        else:
            self._nsmConfiguringParameters = self.nsmcDefault()

        self._uniformPriors = self.uniformPriorsObject(backgroundHyperParameters[0],backgroundHyperParameters[1])
        self._likelihood = diamonds.ExponentialLikelihood(data[1],model)
        self._kMeansClusterer = diamonds.KmeansClusterer(diamonds.EuclideanMetric(),xMeansConfiguratingParameters[0],
                                                         xMeansConfiguratingParameters[1],10,0.01)

    @property
    def backgroundModel(self):
        return self._backgroundModel

    @backgroundModel.setter
    def backgroundModel(self,model):
        self._backgroundModel = model

    @property
    def backgroundHyperParameters(self):
        return self._backgroundHyperParameters

    @backgroundHyperParameters.setter
    def backgroundHyperParameters(self,parameters):
        self._backgroundHyperParameters = parameters

    def xMeansDefault(self):
        pass

    def nsmcDefault(self):
        return np.array([500,500,50000,1500,50,2.10,0.01,0.001])


    def uniformPriorsObject(self,minParameters,maxParameters):
        return diamonds.UniformPrior(minParameters,maxParameters)

