from flask import Flask, render_template, request, make_response
from keras.preprocessing.image import load_img
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import cv2
from scipy.ndimage import gaussian_filter
from sklearn.utils import resample
from keras.models import load_model
import os
import json
import requests

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


@app.route('/report')
def report():
    return render_template('report.html')


@app.route('/tumor', methods=['POST'])
def predict_tumour_type():
    # Assigning the voting for tumor detection
    label_mapping_detector = {0: "Tumor", 1: "Normal"}

    # Label mapping for side detection
    label_mapping_side = {0: 'Axial', 1: 'Coronal', 3: 'Sagittal'}

    label_mapping_classification = {0: 'Glioma', 1: 'Meningioma', 3: 'Pituitary', 2: 'NoTumor'}

    label_mapping_multi_disease = {0: 'Tumor', 1: 'Alzheimer', 2: 'Stroke'}

    label_mapping_meningioma_stroke = {'Meningioma': 0, 'Stroke': 1}

    imagefile = request.files['imagefile']
    image_path = "./static/predictingBrainClassificationImages/" + imagefile.filename
    imagefile.save(image_path)

    classification_image = load_img(image_path, target_size=(256, 256))
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

    imagefile = request.files['imagefile']
    image_path = "./static/predictingStrokeImages/" + imagefile.filename
    imagefile.save(image_path)
    image = load_img(image_path, target_size=(256, 256))
    plt.imshow(image)
    plt.show()
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


from keras.preprocessing.image import img_to_array


@app.route('/alzheimer', methods=['POST'])
def predict_alzheimer():
    label_mapping_side = {0: 'Axial', 1: 'Coronal', 3: 'Sagittal'}

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

    multi_image_array = apply_gamma_correction(classification_image, 1.5)

    # Convert PIL Classification image to array
    multi_image_array = img_to_array(multi_image_array)

    # Expand dimensions to match the input shape expected by the model
    multi_image_array = np.expand_dims(multi_image_array, axis=0)

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


@app.route('/generateReport', methods=['POST'])
def generateReport():
    disease_status = {"Tumour": "Not Detected", "Tumour Type": "Not Detected", "Alzheimer": "Not Detected",
                      "Stroke": "Not Detected", "Edge": "Not Detected"}
    disease_score = {"Tumour": 0, "Tumour Type": 0, "Alzheimer": 0, "Stroke": 0, "Edge": 0}
    label_mapping_detector = {0: "Tumor", 1: "Normal"}
    label_mapping_classification = {0: 'Glioma', 1: 'Meningioma', 3: 'Pituitary', 2: 'NoTumor'}
    label_mapping_alzheimer = {'VeryMildDemented': 0, 'NonDemented': 1, 'ModerateDemented': 2, 'MildDemented': 3}

    imagefile = request.files['imagefile']
    image_path = "./static/PredictingAlzheimerImages/" + imagefile.filename
    print(image_path)
    imagefile.save(image_path)
    image = load_img(image_path, target_size=(256, 256))
    plt.imshow(image)

    image = img_to_array(image)

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

            generate_pdf()

            return render_template('ReportGenerator.html', image_path=image_path, score=disease_score,
                                   predicted_class=disease_status)

        else:
            disease_status["Tumour"] = label_mapping_detector[detector_prediction]
            disease_score["Tumour"] = "{:.2f}".format(detector_score)

            disease_status["Tumour Type"] = label_mapping_detector[detector_prediction]
            disease_score["Tumour Type"] = "{:.2f}".format(detector_score)

            generate_pdf()

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

        generate_pdf()

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

        generate_pdf()

        return render_template('ReportGenerator.html', image_path=image_path, score=disease_score,
                               predicted_class=disease_status)

    return render_template('ReportGenerator.html', image_path=image_path)


def generate_dynamic_data():

    tumourDiseaseStatus = disease_status.get("Tumour")
    tumourDiseaseProbabilityStatus = disease_score.get("Tumour Score")

    tumourTypeStatus = disease_status.get("Tumour Type")
    tumourTypeProbabilityStatus = disease_score.get("Tumour Type Score")

    AlzheimerDiseaseStatus = disease_status.get("Alzheimer")
    AlzheimerDiseaseProbabilityStatus = disease_score.get("Alzheimer Score")

    strokeDieseaseStatus  = disease_status.get("Stroke")
    strokeDieseaseProbabiltyStatus = disease_score.get("Stroke Score")

    edgeStatus  = disease_status.get("Edge")
    edgeProbabiltyStatus = disease_score.get("Edge Score")


    data = {
        'edge_data': edgeStatus,
        'edge_probability': edgeProbabiltyStatus,
        'tumour_data': tumourDiseaseStatus,
        'tumour_probability': tumourDiseaseProbabilityStatus,
        'tumour_type_data': tumourTypeStatus,
        'tumour_type_probability': tumourTypeProbabilityStatus,
        'stroke_data': strokeDieseaseStatus,
        'stroke_probability': strokeDieseaseProbabiltyStatus,
        'alzheimers_data': AlzheimerDiseaseStatus,
        'alzheimers_probability': AlzheimerDiseaseProbabilityStatus,
    }
    return data

# Change the data in the html
def reportGennerator():
    dynamic_data = generate_dynamic_data()
    return render_template('report.html', data=dynamic_data)


# download the pdf after changing the data
def download_pdf():
    dynamic_data = generate_dynamic_data()
    html_content = render_template('report.html', data=dynamic_data)

    # Save the HTML content to a temporary file
    with open('temp_file.html', 'w', encoding='utf-8') as temp_file:
        temp_file.write(html_content)


   # Configure pdfkit to use A4 page size
    options = {
        'page-size': 'A4',
    }
    # Convert HTML to PDF using pdfkit
    pdfkit.from_file('temp_file.html', 'temp_file.pdf', options=options)

    # Send the PDF file as a response and delete the temporary files
    return send_file('temp_file.pdf', as_attachment=True, download_name='generated_report_Uzman.pdf', mimetype='application/pdf', cache_timeout=0)

# # pip install requests

# # The authentication key (API Key).
# # Get your own by registering at https://app.pdf.co
# API_KEY = "lakshancooray23@gmail.com_bx1ri33VsBaJRE18N2Kavme02m3ARIY1Y1LW44dj4P3dv7rF83rJ22YhZFGg7qS0"

# # Base URL for PDF.co Web API requests
# BASE_URL = "https://api.pdf.co/v1"

# # HTML template
# file_read = open("templates/report.html", mode='r', encoding='utf-8')
# SampleHtml = file_read.read()
# file_read.close()

# # Destination PDF file name
# DestinationFile = ".\\result.pdf"


def generate_pdf(args=None):
    GeneratePDFFromHtml(SampleHtml, DestinationFile)


def GeneratePDFFromHtml(SampleHtml, destinationFile):
    """Converts HTML to PDF using PDF.co Web API"""

    # Prepare requests params as JSON
    # See documentation: https://apidocs.pdf.co/?#1-json-pdfconvertfromhtml
    parameters = {}

    # Input HTML code to be converted. Required.
    parameters["html"] = SampleHtml

    #  Name of resulting file
    parameters["name"] = os.path.basename(destinationFile)

    # Set to css style margins like 10 px or 5px 5px 5px 5px.
    parameters["margins"] = "0 0 0 0"

    # Can be Letter, A4, A5, A6 or custom size like 200x200
    parameters["paperSize"] = "Letter"

    # Set to Portrait or Landscape. Portrait by default.
    parameters["orientation"] = "Portrait"

    # true by default. Set to false to disable printing of background.
    parameters["printBackground"] = "true"

    # If large input document, process in async mode by passing true
    parameters["async"] = "false"

    # Set to HTML for header to be applied on every page at the header.
    parameters["header"] = ""

    # Set to HTML for footer to be applied on every page at the bottom.
    parameters["footer"] = ""

    # Prepare URL for 'HTML To PDF' API request
    url = "{}/pdf/convert/from/html".format(
        BASE_URL
    )

    # Execute request and get response as JSON

    response = requests.post(url, data=parameters, headers={"x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            #  Get URL of result file
            resultFileUrl = json["url"]
            # Download result file
            r = requests.get(resultFileUrl, stream=True)
            if (r.status_code == 200):
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            # Show service reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
