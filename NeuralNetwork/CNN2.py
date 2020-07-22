
from keras.layers import Input, Dense, Embedding, Conv2D, MaxPool2D
from keras.layers import Reshape, Flatten, Dropout, Concatenate
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.models import Model
from dataFormatter import DataFormatter
import os

DataFormatr=DataFormatter()
Train_X, Test_X, Train_Y, Test_Y = DataFormatr.getDataAs2DMatrix(10000)


def getModel():
    inputs = Input(shape=(300,50,1),)

    num_filters = 256
    filter_sizes = [3,4,5]
    embedding_dim=50
    sequence_length=300
    drop = 0.5

    convul0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(inputs)
    convul1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(inputs)
    convul2 = Conv2D(num_filters, kernel_size=(filter_sizes[2], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(inputs)

    maxpool0 = MaxPool2D(pool_size=(sequence_length - filter_sizes[0] + 1, 1), strides=(1,1), padding='valid')(convul0)
    maxpool1 = MaxPool2D(pool_size=(sequence_length - filter_sizes[1] + 1, 1), strides=(1,1), padding='valid')(convul1)
    maxpool2 = MaxPool2D(pool_size=(sequence_length - filter_sizes[2] + 1, 1), strides=(1,1), padding='valid')(convul2)

    concatenated_tensor = Concatenate(axis=1)([maxpool0, maxpool1, maxpool2])
    flatten = Flatten()(concatenated_tensor)
    dropout = Dropout(drop)(flatten)
    output = Dense(2, activation='softmax')(dropout)

    return Model(inputs=inputs, outputs=output)

print("Creating Model...")
model = getModel()

#checkpoint = ModelCheckpoint('weights.{epoch:03d}-{val_acc:.4f}.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='auto')
adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])


print("Traning Model...")
epochs = 100
batch_size = 30
model.fit(Train_X,Train_Y, batch_size=batch_size, epochs=epochs, verbose=1 , validation_data=(Test_X, Test_Y))  # starts training


model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")
print("Saved model to disk")


sent=DataFormatr.getSingleSentenseAs2dMatrix("you are the best teacher ever, how is the vector normalized")
res=model.predict(sent)
print(res)


