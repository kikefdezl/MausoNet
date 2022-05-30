from model import mausoNet
import cv2
import os

def size_to_fit(image, max_height = 1440, max_width=2550):
    y, x, _ = image.shape

    ratio = x/y
    if y > max_height:
        y = max_height - 300
        x = y*ratio

    ratio = y/x
    if x > max_width:
        x = max_width - 300
        y = x*ratio

    return cv2.resize(image, (int(x), int(y)))

def main():
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    # image_path = "C:\\Users\\Kike\\Documents\\mausodb\\no_maus"

    image_path = "C:\\Users\\Kike\\Desktop\\IMAGENES"
    list_of_images = [os.path.join(image_path, image) for image in os.listdir(image_path)]

    model_checkpoint = "mausonet_ckpt.h5"

    model = mausoNet()
    model.load_weights(model_checkpoint)

    for image_filename in list_of_images:

        image = cv2.imread(image_filename)
        pred_image = cv2.resize(image, (224, 224))
        pred_image = pred_image.reshape(1, 224, 224, 3)


        prediction = model.predict(pred_image)
        if prediction < 0.5:
            print("En esta foto SI sale mausoñin :)")
        else:
            print("En esta foto NO sale mausoñin :(")

        image = size_to_fit(image)
        cv2.imshow("Prediction Image", image)

        if cv2.waitKey(0) == 27:
            break

if __name__ == "__main__":
    main()