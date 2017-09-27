from Background import Background
from models.StandardModels import NoiseBackgroundModel
import numpy as np

kicID = "123456789"
nestedSampler = Background(kicID,NoiseBackgroundModel,rootPath="exampleFileStructure")
nestedSampler.run()
nestedSampler.writeResults("exampleFileStructure/results/KIC123456789/run","backgound")