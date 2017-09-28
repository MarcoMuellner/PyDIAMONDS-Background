from background import Background
from background.models import NoiseBackgroundModel

kicID = "123456789"
nestedSampler = Background(kicID,NoiseBackgroundModel,rootPath="exampleFileStructure")
nestedSampler.run()
nestedSampler.writeResults("exampleFileStructure/results/KIC123456789/run","backgound")