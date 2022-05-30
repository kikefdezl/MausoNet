from keras.models import Model
from keras.applications import EfficientNetB0
from keras.layers import Dense, Flatten

def mausoNet():

    effnet = EfficientNetB0(include_top=False, classes=2, weights='imagenet', input_shape=(224, 224, 3))
    net = Flatten()(effnet.output)
    prediction = Dense(1, activation='sigmoid')(net)

    return Model(inputs=effnet.input, outputs=prediction)