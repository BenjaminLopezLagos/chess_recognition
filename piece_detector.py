import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import operator
from PIL import Image
import cv2

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

fen_classes = {
    # black pieces
    class_names[0]: 'b',
    class_names[1]: 'k',
    class_names[2]: 'n',
    class_names[3]: 'p',
    class_names[4]: 'q',
    class_names[5]: 'r',
    # not fen exception
    class_names[6]: 'none',
    # white pieces
    class_names[7]: 'B',
    class_names[8]: 'K',
    class_names[9]: 'N',
    class_names[10]: 'P',
    class_names[11]: 'Q',
    class_names[12]: 'R',
}

def predict_piece(img_array, size = (120, 120)):
    img_array = cv2.resize(img_array, size)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)
    #score = predictions[0]
    print(predictions)
    max_value = max(predictions)
    print(predictions.argmax())
    predicted_class = class_names[predictions.argmax()]
    print(predicted_class)
    
    return  fen_classes[predicted_class]

print(tf.__version__)

model = tf.keras.models.load_model('./model.h5')
model.summary()

img = keras.preprocessing.image.load_img(
    "black-bishop_original_Captura.PNG_0dbe4368-b208-4820-92aa-bf81f9f5effb.PNG", target_size=image_size
)
img_array = keras.preprocessing.image.img_to_array(img)
print(predict_piece(img_array))

