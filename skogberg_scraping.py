# imports
from tkinter.constants import Y
import requests
import os
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
import urllib
from io import BytesIO
from tkinter import ttk
import time
from multiprocessing.dummy import Pool as ThreadPool


# Create a beautiful soup object from the url www.skogbergantik.com
def parse_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

# finds the urls from the homepage for the image sub-pages and saves it to two variables; galleryOne and galleryTwo since there are always just two gallery pages.


def get_imageUrl():
    url = "http://www.skogbergsantik.com"
    soup = parse_site(url)
    galleryOne = soup.find('a', {'title': 'Bildgalleri 1'})['href']
    galleryTwo = soup.find('a', {'title': 'Bildgalleri 2'})['href']

    return [galleryOne, galleryTwo]
    # finds all image urls from the soup object and appends this to the img_list


def get_images():
    global img_list
    img_list = []

    url = "http://www.skogbergsantik.com" + get_imageUrl()[1]
    soup = parse_site(url)
    images = soup.find_all('img')
    for image in images:
        if "files/120x120" in image['src']:
            trimmed_image = image['src'].replace('/120x120', '')
            img_list.append("http://skogbergsantik.com/" + trimmed_image)

# function to post all images to the GUI


def publish_photos():
    start = time.time()
    global row_number
    global column_number
    global all_labels
    all_labels = []

    # This doesnt work... should create 3 threads and then iterate the create_label function
    # over the list of urls and add it to the all_labels array to post to the image_frame
    pool = ThreadPool(4)
    all_labels = pool.map(create_labels, img_list)

    end = time.time()
    print("")
    print("This took " + str(round(end - start, 2)) + "s")


# takes an image url from img_list then parses that via PIL to a label and returns the label
def create_labels(image):
    global img_list
    global image_frame
    global row_number
    global column_number
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
    # every 5th image we will increase the row and reset the column number to post 5 images on each row
    if((img_list.index(image)) % 5 == 0):
        row_number += 1
        column_number = 0

    column_number += 1
    return label

# Gui stuff to create a canvas for the images.


def run_script():
    global image_frame
    global column_number
    global row_number
    #fills the img_list with imgurls via get_images() and set basic variables
    get_images()
    row_number = 1
    column_number = 1
    #creates a gui to present the pictures to
    root = tk.Tk()
    root.title('Skogbergs Antik Pictionary ')
    root.geometry("1280x1024")
    # create a main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # create a canvas
    main_canvas = tk.Canvas(main_frame)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # add scrollbar
    main_scrollbar = ttk.Scrollbar(
        main_frame, orient=tk.VERTICAL, command=main_canvas.yview)
    main_scrollbar.pack(side=tk.RIGHT, fill=Y)

    # Configure canvas
    main_canvas.configure(yscrollcommand=main_scrollbar)
    main_canvas.bind('<Configure>', lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox('all')))

    image_frame = tk.Frame(main_canvas)
    main_canvas.create_window((0, 0), window=image_frame, anchor="nw")

    publish_photos()

    root.mainloop()



run_script()
