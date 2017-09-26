import numpy as np
import pyDiamonds as diamonds
import os
from models.StandardModels import NoiseBackgroundModel

kicID = "002436458"
runID = "fullBackground"

#some paths
inputDir = os.path.abspath("data/")
inputFileName = os.path.abspath("data/KIC"+kicID+".txt")
outputDir = os.path.abspath("results/KIC"+kicID+"/")
outputPathPrefix = outputDir + "/" + runID + "/background_"

#Read the input dataset
data = np.loadtxt(inputFileName).T
if(len(data) != 2):
    raise ValueError("Input dataset for KIC"+kicID+".txt hast "+str(len(data))+" columns. 2 are needed")

covariates = data[0].astype(float)
observations = data[1].astype(float)

#1. setup priors
priorFileName = outputDir + "/background_hyperParameters_noise.txt"
priors = np.loadtxt(priorFileName).T

if len(priors) != 2:
    raise ValueError("Wrong number of input prior boundaries. "+str(len(priors))+" are provided, 2 are needed")

if len(priors[0]) not in [12,10,7]:
    raise ValueError("Wrong number of dimensions for hyper-parameters for background model. The dimension of the "
                     "parameter are "+str(len(priors))+", 12,10 or 7 are needed")

hyperParametersMinima = priors[0].astype(float)
hyperParametersMaxima = priors[1].astype(float)

uniformPriors = diamonds.UniformPrior(hyperParametersMinima,hyperParametersMaxima)

fullPathHyperParameters = outputPathPrefix + "hyperParametersUniform.txt"

uniformPriors.writeHyperParametersToFile(fullPathHyperParameters)

#2. setup models for the inference problem
nyqFreqFile = outputDir+"/NyquistFrequency.txt"
model = NoiseBackgroundModel(covariates,nyqFreqFile)
#3 setup likelihood

likelihood = diamonds.ExponentialLikelihood(observations,model)

#4 setup kmeans
configuringParameters = np.loadtxt(outputDir + "/Xmeans_configuringParameters.txt").T

if len(configuringParameters) != 2:
    raise ValueError("Wrong number of input parameters for X-means algorithm. Need 2, got " + str(len(configuringParameters)))

minNclusters = configuringParameters[0]
maxNclusters = configuringParameters[1]

if minNclusters <= 0 or maxNclusters <= 0 or maxNclusters < minNclusters:
    raise ValueError("Minimum or maximum number of clusters cannot be <=0 and minimum of clusters cannot be larger"
                     "than maximum number of clusters")

Ntrials = 10
relTolerance = 0.01

myMetric = diamonds.EuclideanMetric()
kmeans = diamonds.KmeansClusterer(myMetric,int(minNclusters),int(maxNclusters),Ntrials,float(relTolerance))

#5 setup and run nested sampling

configuringParameters = np.loadtxt(outputDir + "/NSMC_configuringParameters.txt")

if len(configuringParameters) != 8:
    raise ValueError("Wrong number of input parameters for NSMC algorithm")

printOnScreen = True
initialNlivePoints = configuringParameters[0]
minNlivePoints = configuringParameters[1]
maxNdrawAttempts = configuringParameters[2]
NinitialIterationsWithoutClustering = configuringParameters[3]
NiterationsWithSameClustering = configuringParameters[4]
initialEnlargementFraction = 0.267*(len(priors[0]))**0.643
shrinkingRate = configuringParameters[6]

if shrinkingRate > 1 or shrinkingRate < 0:
    raise ValueError("Shrinking Rate for ellipsoids must be in range [0,1]")

terminationFactor = configuringParameters[7]

nestedSampler = diamonds.MultiEllipsoidSampler(printOnScreen,[uniformPriors],likelihood,myMetric,kmeans,int(initialNlivePoints),int(minNlivePoints),
                                               initialEnlargementFraction,shrinkingRate)

tolerance = 1.e2
exponent = 0.4
livePointsReducer = diamonds.PowerlawReducer(nestedSampler,tolerance,exponent,terminationFactor)

nestedSampler.run(livePointsReducer,int(NinitialIterationsWithoutClustering),int(NiterationsWithSameClustering),int(maxNdrawAttempts),
                  float(terminationFactor),outputPathPrefix)

"""
results = diamonds.Results(nestedSampler)
results.writeParametersToFile("parameter")
results.writeLogLikelihoodToFile("loglikelihood.txt")
results.writeLogWeightsToFile("logWeights.txt")
results.writeEvidenceInformationToFile("evidenceInformation.txt")
results.writePosteriorProbabilityToFile("posteriorDistribution.txt")

credibleLevel = 68.3
writeMarginalDistributionToFile = True
results.writeParametersSummaryToFile("parameterSummary",credibleLevel,writeMarginalDistributionToFile)
"""







