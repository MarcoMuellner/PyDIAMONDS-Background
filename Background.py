import os
from models.BackgroundModel import BackgroundModel
from numpy import ndarray
import numpy as np
from pyDiamonds import UniformPrior,KmeansClusterer,MultiEllipsoidSampler

class Background:
    """
    This class allows for backgroundfitting of a Powerspectraldensity of a star. Poviding the PSD and a Model to fit
    the data against, it will run a Nested Sampling algorithm provided by the PyDIAMONDS package
    (see https://github.com/muma7490/PyDIAMONDS) of the data.
    """
    def __init__(self,kicID, model ,data = None, priors = None,nsmcConfiguringParameters = None, nyquistFrequency = None
                 ,xmeansConfiguringParameters = None,rootPath = None):
        """
        The constructor of the class sets up the Nested Sampler. For this you need all the parameters of the
        constructor, namely the kicID of the star, the runID on which DIAMONDS should run, the Uniform Priors with
        which DIAMONDS will try to fit the data, the NSMC configuring parameters, which will setup the nested sampler,
        the XMeans configuring parameter which wil setup the Kmeans clusterer. See the documentation of the parameters
        for information on how the content has to look like.

        It is also possible, to read these values from files, which will occur if the rootPath parameter is set and
        any of the other parameters are not set. This assumes, that a data/ and results/ path are available at rootPath.
        The files are read in this locations:

        - data: root/data/KIC*KICID*.txt, where *KICID* is the kicID

        - priors: root/results/KIC*KICID*/background_hyperParameters_*modelName*.txt where *KICID* is the kicID and
                    *modelname* represents the Modelname, taken from the Model class

        - nyquistFrequency: root/results/KIC*KICID*/NyquistFrequency where *KICID* is the kicID. See the documentation
                            of the parameter for further information.

        -nsmcConfiguringParameters: root/results/KIC*KICID*/NSMC_configuringParameters.txt. *KICID* is the kicID.
                                    This is optional, a default configuration is provided

        -xmeansConfiguringParameters: root/results/KIC*KICID*/Xmeans_configuringParameters.txt. *KICID* is the kicID.
                                      This is optional, a default configuration is provided.

        Call the run method to start the analysis. Call getResults for direct results and writeResults to write the
        results to the filesystem.

        :param kicID: The KicID (name) of the star. This is needed for various files.
        :type kicID:str
        :param model: The model for which DIAMONDS performs the fitting. This has to be derived from
                        models.BackgroundModel. See the documentation for BackgroundModel on further information
        :type model: BackgroundModel
        :param priors: The priors on which DIAMONDS will perform the fitting. In general this is a numpy array with
                        2xn values in it, where n represents the number of priors which depend on the model.
                        Background will check if the dimensions have the correct number of values, in accordance to
                        the parameterDimensions property of the model.
                        The priors are assumed to be uniform. The first column describes the min values of the
                        priors, the second column describes the max values of the priors.
        :type priors:ndarray
        :param nyquistFrequency: The nyquist frequency of the dataset. This has to be computed outside of Background.
        :type nyquistFrequency: float
        :param nsmcConfiguringParameters: The NSMC configuring parameters for the DIAMONDS run. In general this doesn't
                                            need to be set, as default parameters are provided. For completeness here
                                            is a list of values which should be available:
                                            - Initial N live points
                                            - Minimum N live points
                                            - Maximum N live points
                                            - N inital Iterations without clustering
                                            - N iterations with same clustering
                                            - Initial enlargement fraction
                                            - Shrinking rate
                                            - Termination factor
        :type nsmcConfiguringParameters: ndarray
        :param xmeansConfiguringParameters: The Xmeans configuring parameters for the DIAMONDS run. In general this
                                            doesn't need to be set, as default parameters are provided. For completeness
                                            here is a list of values which should be available:
                                            - Minimum N clusters
                                            - Maximum N clusters
        :type xmeansConfiguringParameters: ndarray
        :param rootPath: The root path where the files are assumed. If this is set, it will try to find the files
                        according to the scheme above.
        :type rootPath:str
        """
        pass

    def _setupData(self,kicID,dataPath = None,data = None):
        """
        This method sets up the data, checks its validity and returns it. Generally only used internally. Either
        dataPath or data have to be set. If both are set, data is used.
        :param kicID: the kicID of the star.
        :type kicID: str
        :param dataPath: The path where the data is found in the form of KIC*KICID*.txt.
        :type dataPath: str
        :param data: The data of the star. Has to be a powerspectraldensity with 2xn dimensions.
        :type data:ndarray
        :return:Returns the data of the star in form of a 2xn numpy array
        :rtype:ndarray
        """
        pass

    def _setupPriors(self,kicID, resultsPath = None, priors = None):
        """
        This method sets up the priors, checks their validity and returns a UniformPrior object. Generally only
        used internally. Either resultsPath or priors have to be set.
        :param kicID: the kicID of the star.
        :type kicID: str
        :param resultsPath: the results path of the star where the prior file is found according to the scheme in
                            the constructor.
        :type resultsPath: str
        :param priors: The actual priors provided through the constructor. Has to be a 2xn numpy array. Will be checked
                        against the dimensions defined in the model.
        :type priors: ndarray
        :return: The UniformPrior object, which will then be used in the analysis
        :rtype: UniformPrior
        """
        pass

    def _setupModel(self,model):
        """
        This method sets up the model. Generally only used internally
        :param model: The model. Has to be derived from BackgroundModel
        :type model: BackgroundModel
        :return: The model
        :rtype: BackgroundModel
        """
        pass

    def _setupKmeans(self,resultsPath = None, configuringParameters = None):
        """
        Sets up the KMeans parameters. Generally only used internally. If configuringParmeters is None and
        there is no Xmeans_configuringParameters.txt file available in resultsPath, default values will be used.
        Returns the KmeansClusterer object used for the analysis.
        :param resultsPath: The path where Xmeans_configuringParameters.txt should be found.
        :type resultsPath: str
        :param configuringParameters: The configuringParameters. See constructor documentation for further information.
        :type configuringParameters: ndarray
        :return: The KmeansClusterer object used for the analysis.
        :rtype: KmeansClusterer
        """
        pass

    def _setupNestedSampling(self,resultsPath = None,configuringParameters = None):
        """
        Sets up the Nested sampling parameters. Generally only used internally. If configuringParameters is None and
        there is no NSMC_configuringParameters.txt file available in resultsPath, default values will be used. Returns
        the MultiEllispoidSampler object used for the analysis
        :param resultsPath: The path where NSMC_configuringParameters.txt should be found
        :type resultsPath: str
        :param configuringParameters: The configuringParameters. See constructor documentation for further information.
        :type configuringParameters: ndarray
        :return: The MultiEllipsoidSampler used to run DIAMONDS.
        :rtype: MultiEllipsoidSampler
        """
        pass

    def run(self):
        """
        Starts the process of fitting diamonds.
        """
        pass

    def getResults(self):
        """
        Returns the results for diamonds. Work in progress.
        """
        pass

    def writeResults(self,path,prefix= None):
        """
        Writes the results to path.
        :param path: Path where the data is saved.
        :type path:str
        :param prefix: An optional prefix used for all files.
        :type prefix: str
        """
        pass