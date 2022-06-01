import os
import yaml
import tkinter as tk
import tkinter.font as font
from PIL import ImageTk, Image
from shutil import move

class GUI:

    def __init__(self, database_dir, unlabelled, dog, no_dog):
        self.database_dir = database_dir
        self.unlabelled = unlabelled
        self.dog = dog
        self.no_dog = no_dog

        self.unlabelled_dir = os.path.join(database_dir, unlabelled)
        self.dog_dir = os.path.join(database_dir, dog)
        self.no_dog_dir = os.path.join(database_dir, no_dog)

        if not os.path.exists(self.dog_dir):
            os.mkdir(self.dog_dir)
        if not os.path.exists(self.no_dog_dir):
            os.mkdir(self.no_dog_dir)

        extensions = ['.png', '.jpg', '.jpeg', '.tif']

        self.unlabelled_images = [os.path.join(self.unlabelled_dir, filename) for filename in os.listdir(self.unlabelled_dir)
                             if os.path.splitext(filename)[1] in extensions]

        if not self.unlabelled_images:
            print(f"Unlabelled folder is empty in {self.unlabelled_dir}, exiting...")
            exit(0)

        self.current_image_index = 0
        self.window_size = (1600, 1200)

        self.window = tk.Tk()
        self.window.geometry(f"{self.window_size[0]}x{self.window_size[1]}")

        self.buttons_frame = tk.Frame(self.window, width=1600, height=300)
        self.buttons_frame.pack()
        self.buttons_frame.place(anchor='s', relx=0.5, rely=1.0)

        self.image_frame = tk.Frame(self.window, width=1600, height=900)
        self.image_frame.pack()
        self.image_frame.place(anchor='n', relx=0.5, rely=0.0)

        fnt = font.Font(size=70)
        self.dog_button = tk.Button(self.buttons_frame, text=dog, command=self.put_into_dog)
        self.dog_button['font'] = fnt
        self.dog_button.pack(side='left', fill='both', expand=True)

        self.no_dog_button = tk.Button(self.buttons_frame, text=no_dog, command=self.put_into_no_dog)
        self.no_dog_button['font'] = fnt
        self.no_dog_button.pack(side='right', fill='both', expand=True)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side=tk.TOP)
        self.update_image()

        print("Created image labelling GUI with folders:")
        print(f"Unlabelled images: {self.unlabelled_dir}")
        print(f"Dog images: {self.dog_dir}")
        print(f"No dog images: {self.no_dog_dir}")

    def update_image(self):
        self.raw_image = Image.open(self.unlabelled_images[0])
        self.raw_image = resize_image(self.raw_image)
        self.img = ImageTk.PhotoImage(self.raw_image)

        self.image_label.configure(image=self.img)

    def put_into_dog(self):
        src = self.unlabelled_images[self.current_image_index]
        dst = os.path.join(self.dog_dir, os.path.basename(src))

        move(src, dst)
        print(f"Moved {src} to {dst}")
        self.unlabelled_images.pop(0)

        if not self.unlabelled_images:
            exit(0)

        self.update_image()
        print(f"{len(self.unlabelled_images)} images remaining.")

    def put_into_no_dog(self):
        src = self.unlabelled_images[self.current_image_index]
        dst = os.path.join(self.no_dog_dir, os.path.basename(src))

        move(src, dst)
        print(f"Moved {src} to {dst}")
        self.unlabelled_images.pop(0)

        if not self.unlabelled_images:
            exit(0)
        self.update_image()
        print(f"{len(self.unlabelled_images)} images remaining.")


    def main(self):
        self.window.mainloop()


def resize_image(image, max_height=900, max_width=1600):
    x, y = image.size

    ratio = x / y
    if y > max_height:
        y = max_height
        x = y * ratio

    ratio = y / x
    if x > max_width:
        x = max_width
        y = x * ratio

    return image.resize((int(x), int(y)))


def main():
    with open('../config.yaml') as yf:
        cfg = yaml.safe_load(yf)

    database_dir = cfg['DATASET_LABELLING']['database_dir']
    unlabelled = cfg['DATASET_LABELLING']['unlabelled']
    dog = cfg['DATASET_LABELLING']['dog_label']
    no_dog = cfg['DATASET_LABELLING']['no_dog_label']

    gui = GUI(database_dir, unlabelled, dog, no_dog)

    gui.main()

if __name__ == "__main__":
    main()