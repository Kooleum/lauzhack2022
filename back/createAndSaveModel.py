import neuronalNet

model = neuronalNet.train()
neuronalNet.saveModel("savedModels/words.h5", model)