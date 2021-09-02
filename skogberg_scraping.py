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
    gallery = []
    url = "http://www.skogbergsantik.com"
    soup = parse_site(url)
    for x in soup.find_all('a'):
        #print (x.get('href'))
        if "gallery_" in str(x):
            gallery.append(x['href'])
        
    gallery = list(dict.fromkeys(gallery))
    return gallery

    
    # finds all image urls from the soup object and appends this to the img_list


def get_images():
    global img_list
    img_list = []
    
    for url in get_imageUrl():
        site_url = "http://www.skogbergsantik.com" + url
        soup = parse_site(site_url)
        images = soup.find_all('img')
        for image in images:
            if "files/120x120" in image['src']:
                trimmed_image = image['src'].replace('/120x120', '')
                img_list.append("http://skogbergsantik.com/" + trimmed_image)
    
    

# function to post all images to the GUI


def publish_photos():
    
    global row_number
    global column_number
    global all_labels
    global images
    row_number = 2
    column_number = 1
    all_labels = []

    # This doesnt work... should create 4 threads and then iterate the create_label function
    # over the list of urls and add it to the all_labels array to post to the image_frame
    pool = ThreadPool(11)
    
    print("starting threading")
    images = pool.map(download_images, img_list)
    create_labels()

def download_images(url):
    print("Working on item number: " + str(img_list.index(url)+1) +
              "/" + str(len(img_list)), end="\r")
    u = urllib.request.urlopen(url)
    raw_data = u.read()
    u.close()
    im = Image.open(BytesIO(raw_data))
    resized_image = im.resize((250, 250), Image.ANTIALIAS)
    return resized_image
    


# takes an image url from img_list then parses that via a PIL object to a label and returns the label
def create_labels():
    global images
    global image_frame
    global row_number
    global column_number
    for image in images:
        
        current_image = ImageTk.PhotoImage(image)

        label = tk.Label(image_frame, image=current_image)
        label.image = current_image
        label.grid(row=row_number, column=column_number)
        
        # every 5th image we will increase the row and reset the column number to post 5 images on each row
        if((images.index(image)) % 5 == 0):
            
            
            column_number = 0
            row_number += 1
        column_number += 1
        

# Gui stuff to create a canvas for the images.


def run_script():
    start = time.time()
    global image_frame
    global column_number
    global row_number
    
    #fills the img_list with imgurls via get_images() and set basic variables
    get_images()
    

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
    main_canvas.create_window((1, 1), window=image_frame, anchor="nw")
    publish_photos()

    end = time.time()
    print("")
    print("This took " + str(round(end - start, 2)) + "s")
    
    root.mainloop()

run_script()
