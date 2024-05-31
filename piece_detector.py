import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import operator
from PIL import Image
import cv2

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

image_size = (224, 224)
class_names_pieces = ['bishop', 'king', 'knight', 'none', 'pawn', 'queen', 'rook']
class_names_colors = ['black', 'white']
fen_classes = {
    # black pieces
    class_names_pieces[0]: 'b',
    class_names_pieces[1]: 'k',
    class_names_pieces[2]: 'n',
    class_names_pieces[3]: 'none',
    class_names_pieces[4]: 'p',
    class_names_pieces[5]: 'q',
    class_names_pieces[6]: 'r',
}

def predict_color(img_array, size = (85, 85)):
    img_array = cv2.resize(img_array, size)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model_colors.predict(img_array)
    #score = predictions[0]
    print(predictions)
    max_value = max(predictions)
    predicted_class = class_names_colors[predictions.argmax()]
    return predicted_class

def predict_piece(img_array, size = (224, 224)):
    img_array = cv2.resize(img_array, size)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model_pieces.predict(img_array)
    #score = predictions[0]
    print(predictions)
    max_value = max(predictions)
    predicted_class = class_names_pieces[predictions.argmax()]  
    return  predicted_class

def get_piece_and_color(img_array):
    piece = fen_classes[predict_piece(img_array)]
    color = predict_color(img_array)

    if piece == 'none':
        return piece
    
    if color == 'white':
        return piece.upper()
    
    return piece
        

print(tf.__version__)

model_pieces = tf.keras.models.load_model('./model_pieces_new.h5')
model_pieces.summary()
model_colors = tf.keras.models.load_model('./model_color.h5')
model_colors.summary()

img = keras.preprocessing.image.load_img(
    "WhatsApp Image 2024-05-20 at 14.11.51.jpeg", target_size=image_size
)
img_array = keras.preprocessing.image.img_to_array(img)
print(get_piece_and_color(img_array))

