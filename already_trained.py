import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder

print("---------------------------------------------\n")
print("Team BrickStove - Profiler using OSINT + ML\n")
print("---------------------------------------------\n")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):

    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def show_prediction_labels_on_image(img_path, predictions):
    """
    predict and draws a box and saves the image as out.jpg
    """
    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # PIL draw box
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        
        name = name.encode("UTF-8")

        # Add name
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    del draw

    # Displaying and saving the out.jpg
    pil_image.show()
    pil_image.save("out.jpg", "JPEG", quality=80, optimize=True, progressive=True)


if __name__ == "__main__":
  


    # Using the trained classifier, make predictions for unknown images
    for image_file in os.listdir("test"):
        full_file_path = os.path.join("test", image_file)

        print("Looking for faces in {}".format(image_file))

        # Find all people in the image using a trained classifier model
       
        predictions = predict(full_file_path, model_path="trained_knn_model.clf")

        # result on console
        for name, (top, right, bottom, left) in predictions:
            print("- Found @{} at ({}, {})".format(name, left, top))

        # result on img
        show_prediction_labels_on_image(os.path.join("test", image_file), predictions)
        
        # Dumps the output username in a text file for the profiler to use it as an Input.
file1 = open("usernames.txt","w")
file1.write(name)
file1.close()