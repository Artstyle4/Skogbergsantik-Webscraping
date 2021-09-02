from tkinter.constants import Y
import requests
import os
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
import urllib
from io import BytesIO
from tkinter import ttk


# url som används för scrapingen

# hitta platsen som scriptet körs ifrån
dir_path = os.path.dirname(os.path.realpath(__file__))
img_list = []


# hämtar ett Beautiful-Soupobjekt från urlen
def parse_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


# skriver om htmlkoden till text och skriver till .csvfilen
def get_imageUrl():
    url = "http://www.skogbergsantik.com"
    soup = parse_site(url)
    galleryOne = soup.find('a', {'title': 'Bildgalleri 1'})['href']
    galleryTwo = soup.find('a', {'title': 'Bildgalleri 2'})['href']

    return [galleryOne, galleryTwo]


def get_images():
    url = "http://www.skogbergsantik.com" + get_imageUrl()[1]
    soup = parse_site(url)
    images = soup.find_all('img')
    for image in images:
        if "files/120x120" in image['src']:
            trimmed_image = image['src'].replace('/120x120', '')
            img_list.append("http://skogbergsantik.com/" + trimmed_image)


def select_photos():
    row_number = 1
    column_number = 0

    for image in img_list:
        print("Working on item number: " + str(img_list.index(image)+1) +
              "/" + str(len(img_list)), end="\r")

        URL = image
        u = urllib.request.urlopen(URL)
        raw_data = u.read()
        u.close()
        im = Image.open(BytesIO(raw_data))
        resized_image = im.resize((250, 250), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(resized_image)
        label = tk.Label(image_frame, image=photo)
        label.image = photo
        label.grid(row=row_number, column=column_number)
        column_number += 1
        if((img_list.index(image)+1) % 5 == 0):
            all_labels.append(label)
            row_number += 1
            column_number = 0


# saves all images into img_list
get_images()
img_list = img_list
all_labels = []


root = tk.Tk()
root.title('Skogbergs Antik Pictionary ')
root.geometry("1280x1024")
# create a main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# create a canvas
my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# add scrollbar
my_scrollbar = ttk.Scrollbar(
    main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=Y)


# Configure canvas
my_canvas.configure(yscrollcommand=my_scrollbar)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
    scrollregion=my_canvas.bbox('all')))


image_frame = tk.Frame(my_canvas)
my_canvas.create_window((0, 0), window=image_frame, anchor="nw")


select_photos()


root.mainloop()
