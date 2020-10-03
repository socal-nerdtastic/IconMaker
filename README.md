# IconMaker
Make tkinter icons embedded into the source code. This program will turn an image of your choice into an icon for your tkinter program. By embedding the icon into a python file and importing it this method is will work for all OSes and is robust to freezing (.exe conversion). The image is loaded, optionally resized, converted to a .gif and encoded as base64. 

Note this sets the icon of the program when running, it does not set the icon of the file. That's a different icon that is set in a different way (although many programs use the same image for both). 

## How to use

1. Download and run the iconmaker.py program. 
0. Select if you want your image to be resized and what size you want. Generally this is a value between 64 and 256. 
0. Click browse to choose an image to use as an icon. The conversion happens as soon as you select the file to use. 
0. Click save to save your new file. Save it in your project folder and give it a name like "icon.py". 
0. Add this code to your tkinter program, after you have created the tkinter root window. Adjust the import to match the name you gave the file. 

```python3
import icon
icon.apply_icon(root)
```

## Alternate how to use

Use the output file to write your code in. See the program itself as inspiration of this method. 

## Tested

Currently only tested on Python 3.6, Linux Mint. 

## TODO (help please):

* Add more image filetypes (and test)
* Disable image size controls when resize checkbox is unchecked
* Disable resize checkbox when PIL is not found
* add PIL install instructions to documentation
* Add code and instructions to apply to Toplevel windows
* Make interface more intuative, prettier
* Improve this document with better instructions and images
* Python 2 compatibility layer and test
* Test in Windows and Mac
* Test with pyinstaller (and other freezing programs)
* Add to this list
