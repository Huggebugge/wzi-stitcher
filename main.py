import pyautogui
import os
from pynput import mouse, keyboard
import cv2
from imutils import paths


pressed_location = 0, 0
released_location = 0, 0
image_number = 0


def mouse_click(x, y, button, pressed):
    if button == mouse.Button.left:
        print('{} at {}'.format(
            'Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
        global pressed_location
        global released_location
        if pressed:
            pressed_location = x, y
        else:
            released_location = x, y
            return False


def keyboard_click(key):
    if key == keyboard.Key.space:
        global pressed_location
        global released_location
        global image_number
        image_number += 1
        im = pyautogui.screenshot(region=(
            pressed_location[0], pressed_location[1], released_location[0]-pressed_location[0], released_location[1]-pressed_location[1]))
        file_name = "./images/%s.png" % image_number
        im.save(file_name)
        print("Image Saved")
    else:
        print('Other button pressed')
        return False


def stitch():
    print('Stitching, will probably take a while')
    images = []
    imagePaths = sorted(list(paths.list_images('./images/')))
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        images.append(image)
    stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
    (status, stitched) = stitcher.stitch(images)
    if status == 0:
        cv2.imwrite('out.png', stitched)
        print('Stitching done')
    else:
        print("Image stitching failed ({})".format(status))


if os.path.isdir('./images') is False:
    os.mkdir('./images')
just_stitch = False
print('Image Stitcher for WZI')
if just_stitch is False:
    print('---')
    print('Zoom out completely and minimize the bottom information before starting')
    print('Start in the top left corner of the game window, press the left mouse button and drag it to the bottom right')
    listener = mouse.Listener(on_click=mouse_click)
    listener.start()
    listener.join()
    print('Ok, now zoom in and start looking in the top left corner of the map.')
    print('Press space, then move the map and try to capture the next part of it. Some overlap is required for it to work')
    print('When you have captured the entire map, press a different key to exit')
    kblistener = keyboard.Listener(on_press=keyboard_click)
    kblistener.start()
    kblistener.join()

stitch()
print('Hope all went well, if so the image should be stored in out.png')
