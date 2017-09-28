from background import Background
from background.models import NoiseBackgroundModel
import numpy as np

data = np.loadtxt("exampleFiles/KIC123456789.txt").T
nyquistFrequency = float(np.loadtxt("exampleFiles/NyquistFrequency.txt"))
priors = np.loadtxt("exampleFiles/background_hyperParameters_noise.txt").T

bg = Background(kicID="123456789",modelObject=NoiseBackgroundModel,data=data,nyquistFrequency=nyquistFrequency,
                priors=priors).run()
