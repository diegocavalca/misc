# Load dataset
load data.mat
#disp(fieldnames(data))

# Data
#data.testData
#data.trainData
#data.validData
#data.vocab

# Carregando registros em variaveis (mini-batches de 100]
# This will load the data, separate it into inputs and target, and make
# mini-batches of size 100 for the training set.
[train_x, train_t, valid_x, valid_t, test_x, test_t, vocab] = load_data(100);

# Treinando o modelo
# train.m implements the function that trains a neural net language model.
model = train(10);