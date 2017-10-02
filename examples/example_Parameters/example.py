from background import Background
from background.models import WhiteNoiseOnlyModel,WhiteNoiseOscillationModel
import numpy as np

data = np.loadtxt("exampleFiles/KIC123456789.txt").T
nyquistFrequency = float(np.loadtxt("exampleFiles/NyquistFrequency.txt"))
priors_noise = np.loadtxt("exampleFiles/background_hyperParameters_noise.txt").T
priors = np.loadtxt("exampleFiles/background_hyperParameters.txt").T

Background(kicID="123456789", modelObject=WhiteNoiseOnlyModel, data=data, nyquistFrequency=nyquistFrequency,
                priors=priors_noise).run()


Background(kicID="123456789", modelObject=WhiteNoiseOscillationModel, data=data, nyquistFrequency=nyquistFrequency,
                priors=priors).run()
