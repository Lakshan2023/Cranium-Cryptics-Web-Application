from flask import Flask, render_template, request
from keras.preprocessing.image import load_img
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import cv2
from scipy.ndimage import gaussian_filter
from sklearn.utils import resample
from keras.models import load_model

app = Flask(__name__)
# model_tumor_classification_vgg16 = load_model(
#     'C:/Users/laksh/OneDrive/Desktop/Web/models/brain_tumor_classification_vgg19.h5')
# model_resnet50_stroke = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/ischemic_stroke_vgg16.h5')
# model_efficient_net_alzheimer = load_model(
#     'C:/Users/laksh/OneDrive/Desktop/Web/models/alzhimer_classification_efficientNet.h5')


# Load the model
@app.route('/')
def dashboard():
    return render_template('Dashboard.html', data="dashboard")


@app.route('/BrainStrokeDetector')
def BrainStrokeDetector():
    return render_template('BrainStrokeDetector.html')


@app.route('/Dashboard')
def Dashboard():
    return render_template('Dashboard.html')


@app.route('/BrainTumourDetector')
def BrainTumourDetector():
    return render_template('BrainTumourDetector.html')


@app.route('/AlzheimerDiseaseDetector')
def AlzheimerDiseaseDetector():
    return render_template('AlzheimerDiseaseDetector.html')


@app.route('/ReportGenerator')
def ReportGenerator():
    return render_template('ReportGenerator.html')


@app.route('/Register')
def Register():
    return render_template('Register.html')


@app.route('/login')
def login():
    return render_template('login.html')


# @app.route('/tumor', methods=['POST'])
# def predict_tumour_type():
#     imagefile = request.files['imagefile']
#     image_path = "./static/predictingBrainClassificationImages/" + imagefile.filename
#     imagefile.save(image_path)
#     image = load_img(image_path, target_size=(256, 256))
#     plt.imshow(image)
#     plt.show()
#     image = apply_gamma_correction(image, 1.5)
#     plt.imshow(image)
#     plt.show()
#
#     label_mapping = {0: 'Glioma', 1: 'Meningioma', 3: 'Pituitary', 2: 'NoTumor'}
#
#     # Convert PIL image to array
#     image_array = img_to_array(image)
#     # Expand dimensions to match the input shape expected by the model
#     image_array = np.expand_dims(image_array, axis=0)
#
#     # Predict class probabilities
#     probabilities = model_tumor_classification_vgg16.predict(image_array)[0]
#
#     # Get the predicted class index
#     predicted_class_index = np.argmax(probabilities)
#
#     # Get the predicted class label
#     predicted_class = label_mapping[predicted_class_index]
#
#     # Get the score of the predicted class
#     score = probabilities[predicted_class_index]
#
#     print(f"Predicted Class: {predicted_class}, Score: {score}")
#
#     return render_template('BrainTumourDetector.html', image_path=image_path, predicted_class=predicted_class,
#                            score=score)
#
#
# # Function to apply gamma correction
# def apply_gamma_correction(image, gamma=1.5):
#     image_array = np.array(image)
#
#     # Normalize pixel values to the range [0, 1]
#     normalized_image = image_array / 255.0
#
#     # Apply gamma correction
#     corrected_image = np.power(normalized_image, gamma)
#
#     # Denormalize the image to the original range [0, 255]
#     corrected_image = (corrected_image * 255).astype(np.uint8)
#
#     # Convert numpy array back to image
#     corrected_image = Image.fromarray(corrected_image)
#
#     return corrected_image
#
#
# def apply_sobel8_filter(image):
#     image = np.array(image)
#
#     # Apply Gaussian blur to reduce noise
#     blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
#
#     # Applying Sobel filter
#     sobel_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=-1)
#     sobel_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=-1)
#     edges = cv2.magnitude(sobel_x, sobel_y)
#
#     # Normalize edges
#     edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX)
#
#     # Convert to uint8
#     edges = edges.astype('uint8')
#
#     return edges
#
#
# @app.route('/stroke', methods=['POST'])
# def predict_stroke():
#     imagefile = request.files['imagefile']
#     image_path = "./static/predictingStrokeImages/" + imagefile.filename
#     imagefile.save(image_path)
#     image = load_img(image_path, target_size=(256, 256))
#     plt.imshow(image)
#     plt.show()
#     image = apply_sobel8_filter(image)
#     plt.imshow(image)
#     plt.show()
#
#     label_mapping = {0: 'Ischemic', 1: 'Normal'}
#     image = np.expand_dims(image, axis=0)
#     predictions = model_resnet50_stroke.predict(image)
#     class_name = np.argmax(predictions)
#
#     # Get the prediction score
#     prediction_score = predictions[0][class_name]
#
#     print(label_mapping[class_name])
#     print(predictions)
#     print(np.argmax(predictions))
#
#     print(f"Predicted Class: {label_mapping[class_name]}, Score: {prediction_score}")
#
#     return render_template('BrainStrokeDetector.html', image_path=image_path, class_name=label_mapping[class_name],
#                            prediction_score=prediction_score)
#
#
# def apply_random_up_sampler_gaussian_filter(image):
#     sampled_img = resample([image], n_samples=2)[0]
#     filtered_img = gaussian_filter(sampled_img, sigma=1)
#     return filtered_img
#
#
# from keras.preprocessing.image import img_to_array
#
#
# @app.route('/alzheimer', methods=['POST'])
# def predict_alzheimer():
#     imagefile = request.files['imagefile']
#     image_path = "./static/PredictingAlzheimerImages/" + imagefile.filename
#     print(image_path)
#     imagefile.save(image_path)
#     image = load_img(image_path, target_size=(256, 256))
#     plt.imshow(image)
#     plt.show()
#     image = apply_random_up_sampler_gaussian_filter(image)
#     plt.imshow(image)
#     plt.show()
#
#     label_mapping = {'VeryMildDemented': 0, 'NonDemented': 1, 'ModerateDemented': 2, 'MildDemented': 3}
#
#     # Convert PIL image to array
#     image_array = img_to_array(image)
#     # Expand dimensions to match the input shape expected by the model
#     image_array = np.expand_dims(image_array, axis=0)
#
#     # Predict class probabilities
#     probabilities = model_efficient_net_alzheimer.predict(image_array)[0]
#
#     # Get the predicted class index
#     predicted_class_index = np.argmax(probabilities)
#
#     # Get the predicted class label
#     predicted_class = list(label_mapping.keys())[predicted_class_index]
#
#     # Get the score of the predicted class
#     score = probabilities[predicted_class_index]
#
#     print(f"Predicted Class: {predicted_class}, Score: {score}")
#
#     return render_template('AlzheimerDiseaseDetector.html', image_path=image_path, predicted_class=predicted_class,
#                            score=score)

if __name__ == '__main__':
    app.run(debug=True)
