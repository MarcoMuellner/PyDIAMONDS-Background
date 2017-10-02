from pyDiamondsBackground import Background
from pyDiamondsBackground.models import WhiteNoiseOnlyModel

bg = Background(kicID='123456789', modelObject=WhiteNoiseOnlyModel, rootPath="exampleFiles")
bg.run()
bg.writeResults("exampleFiles/results/KIC123456789/run", "background_")