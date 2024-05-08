import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import operator
from PIL import Image

image_size = (120, 120)
class_names = ['black-bishop',
 'black-king',
 'black-knight',
 'black-pawn',
 'black-queen',
 'black-rook',
 'none',
 'white-bishop',
 'white-king',
 'white-knight',
 'white-pawn',
 'white-queen',
 'white-rook']

print(tf.__version__)

model = tf.keras.models.load_model('./model.h5')
model.summary()

img = keras.preprocessing.image.load_img(
    "black-bishop_original_Captura.PNG_0dbe4368-b208-4820-92aa-bf81f9f5effb.PNG", target_size=image_size
)

img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array)
#score = predictions[0]
print(predictions)
max_value = max(predictions)
print(predictions.argmax())
predicted_class = class_names[predictions.argmax()]
print(predicted_class)