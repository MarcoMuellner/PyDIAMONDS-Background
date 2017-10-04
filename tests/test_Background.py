import os
from pyDiamonds import UniformPrior, KmeansClusterer, MultiEllipsoidSampler
from shutil import rmtree

import numpy as np
from numpy import ndarray
import pytest

from pyDiamondsBackground import Background
from pyDiamondsBackground.models import WhiteNoiseOnlyModel,WhiteNoiseOscillationModel
from pyDiamondsBackground.strings import SkillingsLog, SkillingsInformationGain, SkillingsErrorLog

kicID = "123456789"
testFilePath = "tests/testFiles/"
testPath = "tests/playground/"

def createFolders():
    os.mkdir(testPath)
    os.mkdir(testPath + "data")
    os.mkdir(testPath + "results")
    os.mkdir(testPath + "results/KIC" + kicID)
    os.mkdir(testPath + "empty")
    return os.path.abspath(testPath)+"/"

def deleteFolders():
    rmtree(testPath)

modelsList = [(WhiteNoiseOnlyModel,"_noise"),
              (WhiteNoiseOscillationModel,"")]

@pytest.fixture(scope='function',params=modelsList)
def fileObject(request):
    root = createFolders()
    request.addfinalizer(deleteFolders)
    return Background(kicID,modelObject = request.param[0], rootPath=str(root))

@pytest.fixture(scope='function',params=modelsList)
def valueObject(request):
    createFolders()
    modelName = request.param[1]
    data = np.loadtxt(testFilePath + "KICTestFile.txt").T
    priors = np.loadtxt(testFilePath+"background_hyperParameters"+modelName+".txt").T
    nsmc = np.loadtxt(testFilePath+"NSMC_configuringParameters.txt")
    xmeans = np.loadtxt(testFilePath+"Xmeans_configuringParameters.txt")
    nyquist = float(np.loadtxt(testFilePath+"NyquistFrequency.txt"))
    request.addfinalizer(deleteFolders)
    return Background(kicID,data = data,modelObject=request.param[0],priors = priors,nsmcConfiguringParameters=nsmc
                      ,nyquistFrequency=nyquist,xmeansConfiguringParameters=xmeans)

#General failure tests
def testBackground_ExceptionConditions(valueObject: Background):
    dataList = [valueObject._setupData
               ,valueObject._setupPriors]

    fullList = dataList +  [valueObject._setupKmeans,valueObject._setupNestedSampling]

    def testBackground_NoAtribute():
        for method in dataList:
            with pytest.raises(AttributeError):
                method(kicID)
    def testBackground_NoFile():
        for method in fullList:
            with pytest.raises(IOError):
                try:
                    method(kicID, dataPath="this_does_not_exist/")
                except:
                    method(dataPath="this_does_not_exist/")
    @pytest.mark.parametrize("typeErrors", [1, 1.1, "str"])
    def testBackground_WrongType(typeErrors):
        for method in fullList:
            with pytest.raises(TypeError):
                try:
                    method(kicID,data=typeErrors)
                except:
                    method(data=typeErrors)

#TestSetup Data
##Correct Data
def testSetupData_CorrectData(valueObject: Background):
    fileName = testFilePath+"KICTestFile.txt"
    def testSetupData_File():
        return valueObject._setupData("TestFile",dataPath=testFilePath)
    def testSetupData_Data():
        data = np.loadtxt(fileName).T
        return valueObject._setupData(kicID,data=data)
    results = [testSetupData_File(),testSetupData_Data()]
    for result in results:
        assert isinstance(result, np.ndarray)
        assert len(result) == 2
        assert len(result[0]) == len(result[1])
##Deprecated Data
def testSetupData_deprecated(valueObject: Background):
    arrayList = [np.array(([0,1,2,3,4],[0,1,2,3]))
                ,np.array(([0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4]))]
    def testSetupData_deprecatedData():
        for array in arrayList:
            with pytest.raises(ValueError):
                valueObject._setupData(kicID,data=array)
    def testSetupData_deprecatedFileData():
        dummyPath = testPath + "KICdummyFile.txt"
        for array in arrayList:
            np.savetxt(dummyPath, array)
            with pytest.raises(ValueError):
                valueObject._setupData("dummy", dataPath=testPath)

#TestSetup_Prior
##Correct Data
@pytest.mark.parametrize("model",modelsList)
def testSetupPriors_CorrectData(valueObject:Background,model):
    fileName = testFilePath+"background_hyperParameters"+valueObject.model.fileAppendix+".txt"
    def testSetupPriors_File():
        return valueObject._setupPriors(kicID,dataPath=testFilePath)
    def testSetupPriors_Data():
        data = np.loadtxt(fileName).T
        return valueObject._setupPriors(kicID,data=data)
    results = [testSetupPriors_File(),testSetupPriors_Data()]
    for result in results:
        assert isinstance(result, UniformPrior)
        assert len(result.getMinima()) == valueObject.model.dimension
        assert len(result.getMaxima()) == valueObject.model.dimension

##Deprecated Data
@pytest.mark.parametrize("model",modelsList)
def testSetupData_deprecated(valueObject: Background,model):
    fileName = testFilePath + "background_hyperParameters" + valueObject.model.fileAppendix + ".txt"
    loadedData = np.loadtxt(fileName).T
    arrayList = [np.array((loadedData[1],loadedData[0]))
                 ,np.array((loadedData[0][:-1],loadedData[1][:-1]))
                 ,np.array((loadedData[0],loadedData[1][-1]))]

    def testSetupData_deprecatedData():
        for array in arrayList:
            with pytest.raises(ValueError):
                valueObject._setupPriors(kicID,data=array)

    def testSetup_deprecatedFileData():
        for array in arrayList:
            dummyPath = testPath + "background_hyperParametersDummy.txt"
            np.savetxt(dummyPath,array)
            with pytest.raises(ValueError):
                valueObject._setupPriors(kicID,dataPath=testPath)

#TestSetup_Kmeans&NSMC
##Correct Data
def testSetupKMeansNestedSampling_correctData(valueObject:Background):
    fileNameXMeans = testFilePath+"Xmeans_configuringParameters.txt"
    fileNameNSMC = testFilePath+"NSMC_configuringParameters.txt"
    def testSetup_File(method):
        return method(dataPath=testFilePath)
    def testSetup_Data(method,fileName):
        data = np.loadtxt(fileName).T
        return method(data=data)
    def testSetup_Empty(method):
        return method()
    def testSetup_NoFile(method):
        return method(dataPath=testPath + "empty/")


    testFunctions = {
        fileNameXMeans:(valueObject._setupKmeans,KmeansClusterer),
        fileNameNSMC:(valueObject._setupNestedSampling,MultiEllipsoidSampler)
    }
    for file,(method,object) in testFunctions.items():
        assert isinstance(testSetup_File(method),object)
        assert isinstance(testSetup_Data(method,file),object)
        assert isinstance(testSetup_Empty(method), object)
        assert isinstance(testSetup_NoFile(method), object)

def testSetupKMeansNestedSampling_deprecated(valueObject:Background):
    arrayList = [np.array([0]),np.array([0,1,2]),np.array(([0,1],[0,1]))]
    def testSetup_File(method,array):
        np.savetxt(testPath+"Xmeans_configuringParameters.txt",array)
        return method(dataPath=testPath)
    def testSetup_Data(method,array):
        return method(data=array)

    testFunctions = [valueObject._setupKmeans,
                     valueObject._setupNestedSampling]

    for method in testFunctions:
        for array in arrayList:
            with pytest.raises(ValueError):
                testSetup_File(method,array)
                testSetup_Data(method,array)

def testRun(valueObject:Background):
    valueObject.run()
    def testWriteResults():
        valueObject.writeResults(testPath+"results/KIC"+kicID+"")
        items = os.listdir(testPath+"results/KIC"+kicID+"")
        assert "evidenceInformation.txt" in items
        assert "logLikelihood.txt" in items
        assert "evidenceWeights.txt" in items
        assert "parameterSummary.txt" in items
        assert "posteriorDistribution.txt" in items

        for i in range(0,valueObject.model.dimension-1):
            assert "parameter00"+str(i) in items
            assert "marginalDistribution00"+str(i) in items


    def testGetResults():

        def testGetParameters():
            dim = valueObject.model.dimension
            assert len(valueObject.parameters) == dim
            for i in range(0,dim-1):
                assert isinstance(valueObject.parameters[i],ndarray)
                assert isinstance(valueObject.parameters[i], ndarray)
                assert len(valueObject.parameters[i])

        def testGenericProperty(property):
            assert isinstance(property, ndarray)
            assert len(property) > 1

        def testGetEvidenceInformation():
            assert isinstance(valueObject.evidenceInformation,dict)
            assert valueObject.evidenceInformation[SkillingsLog] != 0
            assert valueObject.evidenceInformation[SkillingsInformationGain] != 0
            assert valueObject.evidenceInformation[SkillingsErrorLog] != 0

        def testGetPosteriorProbabilty():
            assert isinstance(valueObject.posteriorProbability,ndarray)
            assert len(valueObject.posteriorProbability) > 1

        def testGetParameterSummary():
            assert isinstance(valueObject.parameterSummary,ndarray)
            assert len(valueObject.parameterSummary) == 7
            for i in range(0,len(valueObject.parameterSummary)-1):
                assert len(valueObject.parameterSummary[i]) == valueObject.model.dimension

        def testGetMarginalDistributions():
            """
            assert isinstance(valueObject.marginalDistributions,ndarray)
            assert len(valueObject.marginalDistributions) == 2
            """
            with pytest.raises(NotImplementedError):
                valueObject.marginalDistributions

        testGetParameters()
        testGenericProperty(valueObject.logLikelihood)
        testGenericProperty(valueObject.logWeights)
        testGetEvidenceInformation()
        testGetPosteriorProbabilty()
        testGetParameterSummary()
        testGetMarginalDistributions()

    #testWriteResults()
    testGetResults()





