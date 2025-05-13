# import cv2
# import os
# import numpy as np
# import csv
# import time
# import pickle
# from sklearn.neighbors import KNeighborsClassifier
# from datetime import datetime
# from sklearn.metrics import accuracy_score
# with open('data/names.pkl', 'rb') as file:
#     LABELS = pickle.load(file)

# with open('data/face_data.pkl', 'rb') as file:
#     FACES = pickle.load(file)

# knn = KNeighborsClassifier(n_neighbors=5)
# knn.fit(FACES, LABELS)

# vid = cv2.VideoCapture(0)
# detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# imgbg = cv2.imread("bg.png")
# Col_Name = ['NAME', 'TIME']

# if not os.path.exists('Attendance'):
#     os.makedirs('Attendance')

# frame_count = 0
# process_interval = 1

# while True:
#     ret, frame = vid.read()
#     frame = cv2.resize(frame, (640, 480))
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     if frame_count % process_interval == 0:
#         faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        
#         for (x, y, w, h) in faces:
#             crop_img = frame[y:y+h, x:x+w, :]
#             resized = cv2.resize(crop_img, (100, 100)).flatten().reshape(1, -1)
#             op = knn.predict(resized)
            
#             timestamp = datetime.now().strftime("%H:%M-%S")
#             date = datetime.now().strftime("%d-%m-%Y")
#             attendance = [str(op[0]), timestamp]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
#             cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
#             cv2.putText(frame, str(op[0]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

#             imgbg[162:162 + 480, 55:55 + 640] = frame

#         file_path = f"Attendance/Attendance_{datetime.now().strftime('%d-%m-%Y')}.csv"
#         file_exists = os.path.isfile(file_path)
        
#         k = cv2.waitKey(1)
#         if k == ord('o'):
#             with open(file_path, "a", newline='') as csvfile:
#                 writer = csv.writer(csvfile)
#                 if not file_exists:
#                     writer.writerow(Col_Name)
#                 writer.writerow(attendance)

#     frame_count += 1
#     cv2.imshow("frame", imgbg)
    
#     k = cv2.waitKey(1)
#     if k == ord('q'):
#         break
# acc=accuracy_score()
# vid.release()
# cv2.destroyAllWindows()


import cv2
import os
import numpy as np
import csv
import time
import pickle
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

with open('data/names.pkl', 'rb') as file:
    LABELS = pickle.load(file)

with open('data/face_data.pkl', 'rb') as file:
    FACES = pickle.load(file)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(FACES, LABELS, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Predict the labels for the test set
y_pred = knn.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

vid = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
imgbg = cv2.imread("bg.png")
Col_Name = ['NAME', 'TIME']

if not os.path.exists('Attendance'):
    os.makedirs('Attendance')

frame_count = 0
process_interval = 1

while True:
    ret, frame = vid.read()
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if frame_count % process_interval == 0:
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized = cv2.resize(crop_img, (30, 30)).flatten().reshape(1, -1)
            op = knn.predict(resized)
            
            timestamp = datetime.now().strftime("%H:%M-%S")
            date = datetime.now().strftime("%d-%m-%Y")
            attendance = [str(op[0]), timestamp]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, str(op[0]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

            imgbg[162:162 + 480, 55:55 + 640] = frame

        file_path = f"Attendance/Attendance_{datetime.now().strftime('%d-%m-%Y')}.csv"
        file_exists = os.path.isfile(file_path)
        
        k = cv2.waitKey(1)
        if k == ord('o'):
            with open(file_path, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(Col_Name)
                writer.writerow(attendance)

    frame_count += 1
    cv2.imshow("frame", imgbg)
    
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()