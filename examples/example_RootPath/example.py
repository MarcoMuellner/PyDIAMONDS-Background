from background import Background
from background.models import NoiseBackgroundModel

bg = Background(kicID='123456789', modelObject=NoiseBackgroundModel, rootPath="exampleFiles")
bg.run()
bg.writeResults("exampleFiles/results/KIC123456789/run", "background_")