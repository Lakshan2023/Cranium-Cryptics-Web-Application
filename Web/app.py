from PIL.Image import fromarray
from flask import Flask, render_template, request, make_response
from keras.preprocessing.image import load_img
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import cv2
from scipy.ndimage import gaussian_filter
from sklearn.utils import resample
from keras.models import load_model

app = Flask(__name__)

# Multi disease detection model
model_multi_disease = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/vgg19_multi_disease.h5')

# Tumor Detection Models
tumor_vgg_16 = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/TumorDetectionModel_VGG-16.h5')
tumor_vgg_19 = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/tumormodel_vgg19.h5')
tumor_resnet_50 = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/BrainTumor_Rnetl.h5')

# Tumour Classification Models
classification_vgg_16 = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/brain_tumor_classification_vgg16.h5')
classification_vgg_19 = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/brain_tumor_classification_vgg19.h5')
classification_resnet_50 = load_model(
    'C:/Users/laksh/OneDrive/Desktop/Web/models/brain_tumor_classification_resnet50.h5')

# Side Detection Model
side_detection_vgg_16 = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/brain_side_vgg16.h5')

model_side_detection = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/brain_side_vgg16.h5')
model_tumor_classification_vgg16 = load_model(
    'C:/Users/laksh/OneDrive/Desktop/Web/models/brain_tumor_classification_vgg19.h5')
model_resnet50_stroke = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/ischemic_stroke_vgg16.h5')
model_efficient_net_alzheimer = load_model(
    'C:/Users/laksh/OneDrive/Desktop/Web/models/alzhimer_classification_efficientNet.h5')

model_brain_image_detection = load_model('C:/Users/laksh/OneDrive/Desktop/Web/models/brain_image_detection.h5')


# Load the model
@app.route('/')
def dashboard():
    return render_template('login.html', data="dashboard")


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


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/tumor', methods=['POST'])
def predict_tumour_type():
    # Assigning the voting for tumor detection
    label_mapping_detector = {0: "Tumor", 1: "Normal"}

    label_mapping_brain = {1: 'BrainImages', 0: 'NotBrainImage'}

    # Label mapping for side detection
    label_mapping_side = {0: 'Axial', 1: 'Coronal', 3: 'Sagittal'}

    label_mapping_classification = {0: 'Glioma', 1: 'Meningioma', 3: 'Pituitary', 2: 'NoTumor'}

    label_mapping_multi_disease = {0: 'Tumor', 1: 'Alzheimer', 2: 'Stroke'}

    label_mapping_meningioma_stroke = {'Meningioma': 0, 'Stroke': 1}

    imagefile = request.files['imagefile']
    image_path = "./static/predictingBrainClassificationImages/" + imagefile.filename
    imagefile.save(image_path)

    classification_image = load_img(image_path, target_size=(256, 256))

    image = load_img(image_path, target_size=(256, 256))
    image = np.array(image)
    gray_scale_image = apply_gaussian_gray_scale_filter(image)

    plt.imshow(gray_scale_image, cmap='gray')
    plt.title("Gray Scale Image")
    plt.show()

    print(gray_scale_image.shape)

    # Prepare the grayscale image for prediction
    brain_image = np.expand_dims(gray_scale_image, axis=0)

    # Predict the class probabilities for the brain image
    class_probabilities = model_brain_image_detection.predict(brain_image)

    # Get the predicted class index
    predicted_class_index = np.argmax(class_probabilities)

    # Get the corresponding class name from the label mapping
    predicted_class_name = label_mapping_brain[predicted_class_index]

    # Get the score for the predicted class
    brain_detection_score = class_probabilities[0][predicted_class_index]

    detector_image = load_img(image_path, target_size=(256, 256))

    # Plotting the classification image
    plt.imshow(classification_image)
    plt.title("Classification Image")
    plt.show()

    # Plotting the detector image
    plt.imshow(detector_image)
    plt.title("Detector Image")
    plt.show()

    # Apply gamma correction to the classification image
    classification_image = apply_gamma_correction(classification_image, 1.5)
    plt.imshow(classification_image)
    plt.title("Gamma Corrected Classification Image")
    plt.show()

    # Apply gamma correction to the detector image
    detector_image = apply_gamma_correction(detector_image, 1.5)
    plt.imshow(detector_image)
    plt.title("Gamma Corrected Detector Image")
    plt.show()

    # Convert PIL Classification image to array
    classification_image_array = img_to_array(classification_image)

    # Convert PIL Detector image to array
    detector_image_array = img_to_array(detector_image)

    # Expand dimensions to match the input shape expected by the model
    classification_image_array = np.expand_dims(classification_image_array, axis=0)

    # Expand dimensions to match the input shape expected by the model
    detector_image_array = np.expand_dims(detector_image_array, axis=0)

    prediction_array = [0, 0]
    score_array = [0, 0]

    if predicted_class_name == 'NotBrainImage':
        prediction_array[0] = "Not Brain Image"
        prediction_array[1] = "Not Brain Image"
        score_array[0] = "{:.2f}".format(brain_detection_score)
        score_array[1] = "{:.2f}".format(brain_detection_score)
        return render_template('BrainTumourDetector.html', image_path=image_path, predicted_class=prediction_array,
                               score=score_array)

    all_disease_vgg_19_probability = model_multi_disease.predict(classification_image_array)[0]
    print(all_disease_vgg_19_probability)
    all_disease_score = all_disease_vgg_19_probability[np.argmax(all_disease_vgg_19_probability)]
    all_disease_prediction = np.argmax(all_disease_vgg_19_probability)

    if all_disease_prediction != 0:
        prediction_array[0] = "Normal"
        prediction_array[1] = "No Tumour"
        score_array[0] = "{:.2f}".format(all_disease_score)
        score_array[1] = "{:.2f}".format(all_disease_score)
        return render_template('BrainTumourDetector.html', image_path=image_path, predicted_class=prediction_array,
                               score=score_array)

    detector_vgg_16_probability = tumor_vgg_16.predict(detector_image_array)[0]

    detector_score = detector_vgg_16_probability[np.argmax(detector_vgg_16_probability)]
    detector_prediction = np.argmax(detector_vgg_16_probability)

    detector_class = label_mapping_detector[detector_prediction]

    prediction_array[0] = detector_class
    score_array[0] = "{:.2f}".format(detector_score)

    print("Hello", detector_vgg_16_probability[0])
    print()

    probabilities_side = model_side_detection.predict(classification_image_array)[0]

    print(probabilities_side)

    # Predict class probabilities
    probability_vgg16 = classification_vgg_16.predict(classification_image_array)[0]
    probability_vgg19 = classification_vgg_19.predict(classification_image_array)[0]
    probability_resnet50 = classification_resnet_50.predict(classification_image_array)[0]

    probabilities = ((probability_vgg16 + probability_vgg19 + probability_resnet50) / 3)

    score = probabilities[np.argmax(probabilities)]

    score_array[1] = "{:.2f}".format(score)

    print("Probability : ", score_array[1])

    # Get the predicted class index
    predicted_class_index = np.argmax(probabilities)

    # Get the predicted class label
    predicted_class = label_mapping_classification[predicted_class_index]

    prediction_array[1] = predicted_class

    # Get the score of the predicted class
    score1 = probabilities[predicted_class_index]

    print(f"Predicted Class: {predicted_class}, Score: {score1}")

    print("Predicted class array:", prediction_array)

    return render_template('BrainTumourDetector.html', image_path=image_path, predicted_class=prediction_array,
                           score=score_array)


# Function to apply gamma correction
def apply_gamma_correction(image, gamma=1.5):
    image_array = np.array(image)

    # Normalize pixel values to the range [0, 1]
    normalized_image = image_array / 255.0

    # Apply gamma correction
    corrected_image = np.power(normalized_image, gamma)

    # Denormalize the image to the original range [0, 255]
    corrected_image = (corrected_image * 255).astype(np.uint8)

    # Convert numpy array back to image
    corrected_image = Image.fromarray(corrected_image)

    return corrected_image


def apply_sobel8_filter(image):
    image = np.array(image)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Applying Sobel filter
    sobel_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=-1)
    sobel_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=-1)
    edges = cv2.magnitude(sobel_x, sobel_y)

    # Normalize edges
    edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX)

    # Convert to uint8
    edges = edges.astype('uint8')

    return edges


@app.route('/stroke', methods=['POST'])
def predict_stroke():
    # Label mapping for side detection
    label_mapping_side = {0: 'Axial', 1: 'Coronal', 3: 'Sagittal'}
    label_mapping_brain = {1: 'BrainImages', 0: 'NotBrainImage'}

    imagefile = request.files['imagefile']
    image_path = "./static/predictingStrokeImages/" + imagefile.filename
    imagefile.save(image_path)
    image = load_img(image_path, target_size=(256, 256))
    plt.imshow(image)
    plt.show()

    image = np.array(image)

    gray_scale_image = apply_gaussian_gray_scale_filter(image)

    plt.imshow(gray_scale_image, cmap='gray')
    plt.title("Gray Scale Image")
    plt.show()

    print(gray_scale_image.shape)

    # Prepare the grayscale image for prediction
    brain_image = np.expand_dims(gray_scale_image, axis=0)

    # Predict the class probabilities for the brain image
    class_probabilities = model_brain_image_detection.predict(brain_image)

    # Get the predicted class index
    predicted_class_index = np.argmax(class_probabilities)

    # Get the corresponding class name from the label mapping
    predicted_class_name = label_mapping_brain[predicted_class_index]

    # Get the score for the predicted class
    brain_detection_score = class_probabilities[0][predicted_class_index]

    print(predicted_class_name)

    if predicted_class_name == 'NotBrainImage':
        class_name = ["Not Brain Image", "Not Brain Image"]
        prediction_score = ["{:.2f}".format(brain_detection_score), "{:.2f}".format(brain_detection_score)]
        return render_template('BrainStrokeDetector.html', image_path=image_path, class_name=class_name,
                               prediction_score=prediction_score)

    image = apply_sobel8_filter(image)
    plt.imshow(image)
    plt.show()

    classification_image = load_img(image_path, target_size=(256, 256))

    multi_image_array = apply_gamma_correction(classification_image, 1.5)

    # Convert PIL Classification image to array
    multi_image_array = img_to_array(multi_image_array)

    # Expand dimensions to match the input shape expected by the model
    multi_image_array = np.expand_dims(multi_image_array, axis=0)

    all_disease_vgg_19_probability = model_multi_disease.predict(multi_image_array)[0]
    all_disease_score = all_disease_vgg_19_probability[np.argmax(all_disease_vgg_19_probability)]
    all_disease_prediction = np.argmax(all_disease_vgg_19_probability)

    if all_disease_prediction != 2:
        side_prediction = model_side_detection.predict(multi_image_array)
        side_prediction_score = side_prediction[0][np.argmax(side_prediction)]
        side_class = np.argmax(side_prediction)
        side_name = label_mapping_side[side_class]

        class_name = ["Normal", side_name]
        prediction_score = ["{:.2f}".format(all_disease_score), "{:.2f}".format(side_prediction_score)]
        return render_template('BrainStrokeDetector.html', image_path=image_path, class_name=class_name,
                               prediction_score=prediction_score)

    side_prediction = model_side_detection.predict(multi_image_array)
    side_prediction_score = side_prediction[0][np.argmax(side_prediction)]
    side_class = np.argmax(side_prediction)
    side_name = label_mapping_side[side_class]

    print(f"Predicted Side: {side_name}, Score: {side_prediction_score}")

    label_mapping = {0: 'Ischemic', 1: 'Normal'}
    image = np.expand_dims(image, axis=0)
    predictions = model_resnet50_stroke.predict(image)
    class_name = np.argmax(predictions)

    # Get the prediction score
    prediction_score = predictions[0][class_name]

    print(label_mapping[class_name])
    print(predictions)
    print(np.argmax(predictions))

    print(f"Predicted Class: {label_mapping[class_name]}, Score: {prediction_score}")

    class_name = [label_mapping[class_name], side_name]
    prediction_score = [prediction_score, side_prediction_score]

    return render_template('BrainStrokeDetector.html', image_path=image_path, class_name=class_name,
                           prediction_score=prediction_score)


def apply_random_up_sampler_gaussian_filter(image):
    sampled_img = resample([image], n_samples=2)[0]
    filtered_img = gaussian_filter(sampled_img, sigma=1)
    return filtered_img


def apply_gaussian_gray_scale_filter(image):
    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Convert image to grayscale
    gray_scale_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)

    return gray_scale_image


from keras.preprocessing.image import img_to_array


@app.route('/alzheimer', methods=['POST'])
def predict_alzheimer():
    label_mapping_side = {0: 'Axial', 1: 'Coronal', 3: 'Sagittal'}
    label_mapping_brain = {1: 'BrainImages', 0: 'NotBrainImage'}

    imagefile = request.files['imagefile']
    image_path = "./static/PredictingAlzheimerImages/" + imagefile.filename
    print(image_path)
    imagefile.save(image_path)
    image = load_img(image_path, target_size=(256, 256))
    plt.imshow(image)
    plt.show()
    image = apply_random_up_sampler_gaussian_filter(image)
    plt.imshow(image)
    plt.show()

    classification_image = load_img(image_path, target_size=(256, 256))

    gray_scale_image = apply_gaussian_gray_scale_filter(image)

    plt.imshow(gray_scale_image, cmap='gray')
    plt.title("Gray Scale Image")
    plt.show()

    print(gray_scale_image.shape)

    # Prepare the grayscale image for prediction
    brain_image = np.expand_dims(gray_scale_image, axis=0)

    # Predict the class probabilities for the brain image
    class_probabilities = model_brain_image_detection.predict(brain_image)

    # Get the predicted class index
    predicted_class_index = np.argmax(class_probabilities)

    # Get the corresponding class name from the label mapping
    predicted_class_name = label_mapping_brain[predicted_class_index]

    # Get the score for the predicted class
    brain_detection_score = class_probabilities[0][predicted_class_index]

    multi_image_array = apply_gamma_correction(classification_image, 1.5)

    # Convert PIL Classification image to array
    multi_image_array = img_to_array(multi_image_array)

    # Expand dimensions to match the input shape expected by the model
    multi_image_array = np.expand_dims(multi_image_array, axis=0)

    if predicted_class_name == 'NotBrainImage':
        class_name = ["Not Brain Image", "Not Brain Image"]
        prediction_score = ["{:.2f}".format(brain_detection_score), "{:.2f}".format(brain_detection_score)]
        return render_template('AlzheimerDiseaseDetector.html', image_path=image_path,
                               predicted_class=class_name,
                               score=prediction_score)

    all_disease_vgg_19_probability = model_multi_disease.predict(multi_image_array)[0]
    all_disease_score = all_disease_vgg_19_probability[np.argmax(all_disease_vgg_19_probability)]
    all_disease_prediction = np.argmax(all_disease_vgg_19_probability)

    if all_disease_prediction != 1:
        side_prediction = model_side_detection.predict(multi_image_array)
        side_prediction_score = side_prediction[0][np.argmax(side_prediction)]
        side_class = np.argmax(side_prediction)
        side_name = label_mapping_side[side_class]

        class_name = ["Normal", side_name]
        prediction_score = ["{:.2f}".format(all_disease_score), "{:.2f}".format(side_prediction_score)]
        return render_template('AlzheimerDiseaseDetector.html', image_path=image_path,
                               predicted_class=class_name,
                               score=prediction_score)

    label_mapping = {'VeryMildDemented': 0, 'NonDemented': 1, 'ModerateDemented': 2, 'MildDemented': 3}

    # Convert PIL image to array
    image_array = img_to_array(image)
    # Expand dimensions to match the input shape expected by the model
    image_array = np.expand_dims(image_array, axis=0)

    # Predict class probabilities
    probabilities = model_efficient_net_alzheimer.predict(image_array)[0]

    # Get the predicted class index
    predicted_class_index = np.argmax(probabilities)

    # Get the predicted class label
    predicted_class = list(label_mapping.keys())[predicted_class_index]

    # Get the score of the predicted class
    score = probabilities[predicted_class_index]

    side_prediction = model_side_detection.predict(multi_image_array)
    side_prediction_score = side_prediction[0][np.argmax(side_prediction)]
    side_class = np.argmax(side_prediction)
    side_name = label_mapping_side[side_class]

    predicted_class_array = [predicted_class, side_name]
    score_array = ["{:.2f}".format(score), "{:.2f}".format(side_prediction_score)]

    print(f"Predicted Class: {predicted_class}, Score: {score}")

    return render_template('AlzheimerDiseaseDetector.html', image_path=image_path,
                           predicted_class=predicted_class_array,
                           score=score_array)


disease_status = {"Tumour": "Not Detected", "Tumour Type": "Not Detected", "Alzheimer": "Not Detected",
                  "Stroke": "Not Detected", "Edge": "Not Detected"}

disease_score = {"Tumour": 0.00, "Tumour Type": 0.00, "Alzheimer": 0.00, "Stroke": 0.00, "Edge": 0.00}

required_image = None


@app.route('/generateReport', methods=['POST'])
def generateReport():
    global disease_status, disease_score
    disease_status = {"Tumour": "Not Detected", "Tumour Type": "Not Detected", "Alzheimer": "Not Detected",
                      "Stroke": "Not Detected", "Edge": "Not Detected"}

    disease_score = {"Tumour": 0.00, "Tumour Type": 0.00, "Alzheimer": 0.00, "Stroke": 0.00, "Edge": 0.00}

    label_mapping_brain = {1: 'BrainImages', 0: 'NotBrainImage'}
    label_mapping_side = {0: 'Axial', 1: 'Coronal', 3: 'Sagittal'}
    label_mapping_detector = {0: "Tumor", 1: "Normal"}
    label_mapping_classification = {0: 'Glioma', 1: 'Meningioma', 3: 'Pituitary', 2: 'NoTumor'}
    label_mapping_alzheimer = {'VeryMildDemented': 0, 'NonDemented': 1, 'ModerateDemented': 2, 'MildDemented': 3}

    imagefile = request.files['imagefile']
    image_path = "./static/PredictingAlzheimerImages/" + imagefile.filename

    global required_image
    required_image = image_path

    print(required_image)

    print(image_path)
    imagefile.save(image_path)
    image = load_img(image_path, target_size=(256, 256))
    plt.imshow(image)

    image = img_to_array(image)

    gray_scale_image = apply_gaussian_gray_scale_filter(image)

    plt.imshow(gray_scale_image, cmap='gray')
    plt.title("Gray Scale Image")
    plt.show()

    print(gray_scale_image.shape)

    # Prepare the grayscale image for prediction
    brain_image = np.expand_dims(gray_scale_image, axis=0)

    # Predict the class probabilities for the brain image
    class_probabilities = model_brain_image_detection.predict(brain_image)

    # Get the predicted class index
    predicted_class_index = np.argmax(class_probabilities)

    # Get the corresponding class name from the label mapping
    predicted_class_name = label_mapping_brain[predicted_class_index]

    # Get the score for the predicted class
    brain_detection_score = class_probabilities[0][predicted_class_index]

    if predicted_class_name == 'NotBrainImage':
        disease_status["Tumour"] = "Not Brain Image"
        disease_score["Tumour"] = "{:.2f}".format(brain_detection_score)
        disease_status["Tumour Type"] = "Not Brain Image"
        disease_score["Tumour Type"] = "{:.2f}".format(brain_detection_score)
        disease_status["Alzheimer"] = "Not Brain Image"
        disease_score["Alzheimer"] = "{:.2f}".format(brain_detection_score)
        disease_status["Stroke"] = "Not Brain Image"
        disease_score["Stroke"] = "{:.2f}".format(brain_detection_score)
        disease_status["Edge"] = "Not Brain Image"
        disease_score["Edge"] = "{:.2f}".format(brain_detection_score)
        return render_template('ReportGenerator.html', image_path=image_path, score=disease_score,
                               predicted_class=disease_status)

    gamma_image = apply_gamma_correction(image, 1.5)
    plt.imshow(gamma_image)
    plt.title("Gamma Corrected Image")
    plt.show()

    sobel_image = apply_sobel8_filter(gamma_image)
    plt.imshow(sobel_image)
    plt.title("Sobel Filter Image")
    plt.show()

    gamma_image_expand = np.expand_dims(gamma_image, axis=0)

    all_disease_vgg_19_probability = model_multi_disease.predict(gamma_image_expand)[0]
    all_disease_score = all_disease_vgg_19_probability[np.argmax(all_disease_vgg_19_probability)]
    all_disease_prediction = np.argmax(all_disease_vgg_19_probability)

    print(all_disease_prediction)

    side_prediction = model_side_detection.predict(gamma_image_expand)
    side_prediction_score = side_prediction[0][np.argmax(side_prediction)]
    side_class = np.argmax(side_prediction)
    side_name = label_mapping_side[side_class]

    disease_status["Edge"] = side_name
    disease_score["Edge"] = "{:.2f}".format(side_prediction_score)

    if all_disease_prediction == 0:
        detector_vgg_16_probability = tumor_vgg_16.predict(gamma_image_expand)[0]
        detector_score = detector_vgg_16_probability[np.argmax(detector_vgg_16_probability)]
        detector_prediction = np.argmax(detector_vgg_16_probability)

        if detector_prediction == 0:
            # Predict class probabilities
            probability_vgg16 = classification_vgg_16.predict(gamma_image_expand)[0]
            probability_vgg19 = classification_vgg_19.predict(gamma_image_expand)[0]
            probability_resnet50 = classification_resnet_50.predict(gamma_image_expand)[0]

            probabilities = ((probability_vgg16 + probability_vgg19 + probability_resnet50) / 3)

            score = probabilities[np.argmax(probabilities)]

            # Get the predicted class index
            predicted_class_index = np.argmax(probabilities)

            # Get the predicted class label
            predicted_class = label_mapping_classification[predicted_class_index]

            print(predicted_class)

            disease_status["Tumour"] = label_mapping_detector[detector_prediction]
            disease_score["Tumour"] = "{:.2f}".format(detector_score)

            disease_status["Tumour Type"] = predicted_class
            disease_score["Tumour Type"] = "{:.2f}".format(detector_score)

            return render_template('ReportGenerator.html', image_path=image_path, score=disease_score,
                                   predicted_class=disease_status)

        else:
            disease_status["Tumour"] = label_mapping_detector[detector_prediction]
            disease_score["Tumour"] = "{:.2f}".format(detector_score)

            disease_status["Tumour Type"] = label_mapping_detector[detector_prediction]
            disease_score["Tumour Type"] = "{:.2f}".format(detector_score)

            return render_template('ReportGenerator.html', image_path=image_path, score=disease_score,
                                   predicted_class=disease_status)


    elif all_disease_prediction == 1:
        image = load_img(image_path, target_size=(256, 256))
        plt.imshow(image)
        plt.show()
        image = apply_random_up_sampler_gaussian_filter(image)
        plt.imshow(image)
        plt.show()

        # Convert PIL image to array
        image_array = img_to_array(image)
        # Expand dimensions to match the input shape expected by the model
        image_array = np.expand_dims(image_array, axis=0)

        # Predict class probabilities
        probabilities = model_efficient_net_alzheimer.predict(image_array)[0]

        # Get the predicted class index
        predicted_class_index = np.argmax(probabilities)

        # Get the predicted class label
        predicted_class = list(label_mapping_alzheimer.keys())[predicted_class_index]

        # Get the score of the predicted class
        score = probabilities[predicted_class_index]

        disease_status["Alzheimer"] = predicted_class
        disease_score["Alzheimer"] = "{:.2f}".format(score)

        print(predicted_class)

        return render_template('ReportGenerator.html', image_path=image_path, score=disease_score,
                               predicted_class=disease_status)


    elif all_disease_prediction == 2:
        label_mapping = {0: 'Ischemic', 1: 'Not Detected'}
        image = np.expand_dims(sobel_image, axis=0)
        predictions = model_resnet50_stroke.predict(image)
        class_name = np.argmax(predictions)

        # Get the prediction score
        prediction_score = predictions[0][class_name]

        print(label_mapping[class_name])

        disease_status["Stroke"] = label_mapping[class_name]

        disease_score["Stroke"] = "{:.2f}".format(prediction_score)

        return render_template('ReportGenerator.html', image_path=image_path, score=disease_score,
                               predicted_class=disease_status)

    return render_template('ReportGenerator.html', image_path=image_path)


@app.route('/report')
def report():
    print(required_image)
    return render_template('report.html', score=disease_score,
                           predicted_class=disease_status, image_path=required_image)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
