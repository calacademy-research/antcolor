from Watershed import Watershed


from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk
import numpy
import sys,os,os.path,glob,signal
import re
import functools
import math
import random
import copy
if sys.version_info[0] == 3:
    import tkinter as Tkinter
    from tkinter.constants import *
else:
    import Tkinter    
    from Tkconstants import *
import pymsgbox
import time

#___________________________________  Utility functions  ____________________________________

def ctrl_c_handler( signum, frame ):             
    print("Killed by Ctrl C")                       
    os.kill( os.getpid(), signal.SIGKILL )       
signal.signal( signal.SIGINT, ctrl_c_handler )   

def file_index(file_name):
    '''
    This function is needed if you are analyzing an image in the scanning mode.
    In this mode, the module runs a non-overlapping scanning window over the image,
    dumps the image data inside the scanning window at each position of the window
    in a directory.  Each file is given a name that includes a numerical index
    indicating its position in the original images.  This function returns the
    numerical index in the name of a file.
    '''
    m = re.search(r'_(\d+)\.jpg$', file_name)
    return int(m.group(1))

#______________________________  ImageScanner Class Definition  ________________________________

class ImageScanner(Watershed):
    '''
    This class is useful when dealing with large images that contain small objects of
    interest. Consider the fact that large digital images (images of size 5472x3648
    or larger) can now be routinely recorded with inexpensive digital cameras.  If
    you are interested in segmenting out small objects (objects that may occupy only
    a couple of hundred pixels), the algorithm development for detections is best
    carried out on a subimage basis.  That is, you first divide the large image into
    overlapping or non-overlapping subimages and then focus on reliable object
    detection in the subimages.  This is where you'll find the ImageScanner class
    useful.  This class comes with methods that allow you to see the results of the
    operations carried out in the subimages individually in the original large image.
    '''

    def __init__(self, *args, **kwargs ):
        if args:
            raise ValueError(  
                   '''ImageScanner constructor can only be called with keyword arguments for 
                      the following keywords: data_image, binary_or_gray_or_color,
                      gradient_threshold_as_fraction, level_decimation_factor, padding,
                      size_for_calculations, max_gradient_to_be_reached_as_fraction, 
                      color_filter, sigma, scanner_dump_directory, scanning_window_width, 
                      scanning_window_height, subimage_filename, and debug''')   
        scanning_window_width = scanning_window_height = scanner_dump_directory = subimage_filename = dump_directory = debug = min_brightness_level = min_area_threshold = max_area_threshold = max_number_of_blobs = object_shape = None
        if 'scanner_dump_directory' in kwargs        :   scanner_dump_directory = kwargs.pop('scanner_dump_directory')
        if 'scanning_window_width' in kwargs         :   scanning_window_width = kwargs.pop('scanning_window_width')
        if 'scanning_window_height' in kwargs        :   scanning_window_height = kwargs.pop('scanning_window_height')
        if 'subimage_filename' in kwargs             :   subimage_filename = kwargs.pop('subimage_filename')
        if 'min_brightness_level' in kwargs          :   min_brightness_level = kwargs.pop('min_brightness_level')
        if 'min_area_threshold' in kwargs            :   min_area_threshold = kwargs.pop('min_area_threshold')
        if 'max_area_threshold' in kwargs            :   max_area_threshold = kwargs.pop('max_area_threshold')
        if 'max_number_of_blobs' in kwargs           :   max_number_of_blobs = kwargs.pop('max_number_of_blobs')
        if 'object_shape' in kwargs                  :   object_shape = kwargs.pop('object_shape')
        Watershed.__init__(self, **kwargs)
        self.mw = None
        self.canvas = None
        self.image_w, self.image_h = None, None
        self.scanning_window_width, self.scanning_window_height  =  scanning_window_width, scanning_window_height
        self.subimage_filename = subimage_filename
        self.min_area_threshold = min_area_threshold
        self.max_area_threshold = max_area_threshold
        self.max_number_of_blobs = max_number_of_blobs
        self.min_brightness_level = min_brightness_level
        self.scanner_dump_directory = scanner_dump_directory
        self.object_shape = object_shape
        self.scale_x, self.scale_y = None, None
        self.moves_horizontal, self.moves_vertical = None, None
        self.delta_x, self.delta_y = None, None
        self.x_incr, self.y_incr = 0,0
        self.old_posx, self.old_posy = 0,0
        self.iteration_index = 0
        self.rect = None
        self.total_num_window_pos = None
        self.num_remaining_pos = None
        self.block_index = 0
        if debug:                             
            self.debug = debug
        else:
            self.debug = 0
        self.wshed = Watershed(**kwargs)

    def analyze_scanner_dump(self):
        '''
        The purpose of this method is to analyze ALL images in the scanner dump
        directory, generate the object detection results from each subimage in the
        directory, and, finally, display the locations of the detections collected
        from all the subimages in the original image.
        '''
        if (not os.path.exists("scanner_dump")) or (len(glob.glob("scanner_dump/*")) == 0):
            sys.exit("Before you call analyze_scanner_dump_and_show_intermediate_results(), you must create a scan dump by invoking scan_image_for_detections_interactive() or scan_image_for_detections() on an instance of the ImageScanner class).  See the relevant example script in the ExamplesScanner directory for why.")
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        self.image_width, self.image_height = self.original_im.size
        print("size of the image is: %s" % str((self.image_width, self.image_height)))
        print("\n\nAnalyzing contents of the subimage in file: %s" % self.subimage_filename)
        M,N = self.scanning_window_width, self.scanning_window_height
        image_name = self.data_im_name
        hpos = self.image_width // self.scanning_window_width
        vpos = self.image_height // self.scanning_window_height
        positions_of_detected_objects = []
        blocks_examined = 0
        mw = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (self.image_height * 1.0 / self.image_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (self.image_width * 1.0 / self.image_height))
        scaled_image = self.original_im.copy().resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title( image_name + ": Displaying detections" ) 
        mw.configure( height = winsize_y, width = winsize_x )         
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,            
                             width = winsize_x,             
                             cursor = "crosshair" )   
        canvas.pack(fill=BOTH, expand=True)
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = image_name + "_detections.jpg") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            

        photo = ImageTk.PhotoImage( scaled_image )
        canvas.create_image(winsize_x//2,winsize_y//2,image=photo)
        scale_x = winsize_x / (self.image_width * 1.0)
        scale_y = winsize_y / (self.image_height * 1.0) 
        print("\nx_scale: %f" % scale_x)
        print("y_scale: %f" % scale_y)
        rectscan = canvas.create_rectangle((0, 0, int(M*scale_x), int(N*scale_y)), width='7', outline='red') 
        old_posx, old_posy = 0,0
        delta_x_mov_rect, delta_y_mov_rect = int(M * scale_x), int(N * scale_y)
        canvas.update()
        mw.update()
        for filename in sorted(glob.glob("scanner_dump/*"), key=lambda x: file_index(x)):
            print("\n\nAnalyzing contents of image block in file: %s" % filename)
            if self.debug:
                if blocks_examined in [0,1,2,3,4]:
                    blocks_examined += 1
                    continue
            image_file_index = file_index(filename)
            image_item = Image.open(filename)
            width,height = image_item.size
            tk2 = Tkinter.Toplevel(takefocus = True)
            winsize_x,winsize_y = None,None
            screen_width,screen_height = tk2.winfo_screenwidth(),tk2.winfo_screenheight()
            if screen_width <= screen_height:
                winsize_x = int(0.5 * screen_width)
                winsize_y = int(winsize_x * (height * 1.0 / width))            
            else:
                winsize_y = int(0.5 * screen_height)
                winsize_x = int(winsize_y * (width * 1.0 / height))
            display_image = image_item.resize((winsize_x,winsize_y), Image.ANTIALIAS)
            tk2.title("wait until results calculated for this subimage")   
            frame = Tkinter.Frame(tk2, relief=RIDGE, borderwidth=2)
            frame.pack(fill=BOTH,expand=1)
            photo_image = ImageTk.PhotoImage( display_image )
            label = Tkinter.Label(frame, image=photo_image)
            label.pack(fill=X, expand=1)
            tk2.update()
            # The second arg in what follows is for suppressing the showing of intermediate results
            filtered_im = self.apply_color_filter_hsv_to_named_image_file(filename, False)
            pixel_coords = self.connected_components_of_filtered_output(filtered_im, self.min_brightness_level, self.min_area_threshold, self.max_area_threshold, self.max_number_of_blobs, self.object_shape, False) 
            print("Number of objects detected: %d" % len(pixel_coords))
            upper_left_corner = ((image_file_index % hpos) * M, (image_file_index//hpos) * N)
            real_pixel_coords = map(lambda x: (upper_left_corner[0] + x[0], upper_left_corner[1] + x[1]), pixel_coords)
            positions_of_detected_objects += real_pixel_coords
            print("Pixel coordinates for detections: %s" % str(pixel_coords))
            print("Real coordinates for detections: %s" % str(real_pixel_coords))
            print("All coordinates for detections: %s" % str(positions_of_detected_objects))
            original_image = self.original_im.copy()
            width,height = original_image.size
            for pixel in positions_of_detected_objects:
                if all(x > 20 for x in pixel) and (pixel[0] < width-20) and (pixel[1] < height-20):
                    rect = canvas.create_rectangle((pixel[0]-20)*scale_x, (pixel[1]-20)*scale_y, 
                                   (pixel[0]+20)*scale_x, (pixel[1]+20)*scale_y, width='2', outline='red', fill='red') 
            canvas.update()
            tk2.destroy()
            new_posx = old_posx + delta_x_mov_rect
            if new_posx + delta_x_mov_rect < int(self.image_width * scale_x):
                canvas.move( rectscan, delta_x_mov_rect, 0)
                old_posx = new_posx
            elif old_posy + 2 * delta_y_mov_rect < int(self.image_height * scale_y):
                # now we need to move rect all the way back to the first column in the next row:
                canvas.move( rectscan, -1 * (hpos-1) * delta_x_mov_rect, delta_y_mov_rect ) 
                old_posx = 0
                old_posy += delta_y_mov_rect
            canvas.update()
            blocks_examined += 1
        canvas.delete(rectscan)
        canvas.update()
        mw.mainloop()
        return positions_of_detected_objects

    def analyze_scanner_dump_and_show_intermediate_results(self):
        '''
        The purpose of this method is to analyze ALL images in the scanner dump directory,
        generate the object detection results from each subimage in the directory,
        and, finally, display the locations of the detections collected from all the
        subimages in the original image.  This method will also display the intermediate
        results obtained as the subimages are processed for object detections.  The
        intermediate results correspond to color filtering, binarizing, component labeling,
        etc.
        '''
        if (not os.path.exists("scanner_dump")) or (len(glob.glob("scanner_dump/*")) == 0):
            sys.exit("Before you call analyze_scanner_dump_and_show_intermediate_results(), you must create a scan dump by invoking scan_image_for_detections_interactive() or scan_image_for_detections() on an instance of the ImageScanner class).  See the relevant example script in the ExamplesScanner directory for why.")
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        self.image_width, self.image_height = self.original_im.size
        print("size of the image is: %s" % str((self.image_width,self.image_height)))
        print("\n\nAnalyzing contents of the subimage in file: %s" % self.subimage_filename)
        M,N = self.scanning_window_width, self.scanning_window_height
        image_name = self.data_im_name
        hpos = self.image_width // self.scanning_window_width
        vpos = self.image_height // self.scanning_window_height
        positions_of_detected_objects = []
        blocks_examined = 0
        for filename in sorted(glob.glob(self.scanner_dump_directory + "/*"), key=lambda x: file_index(x)):
            print("\n\nAnalyzing contents of image block in file: %s" % filename)
            if self.debug:
                if blocks_examined in [0,1,2,3,4]:
                    blocks_examined += 1
                    continue
            image_file_index = file_index(filename)
            image_item = Image.open(filename)
            self.displayImage3(image_item, "image: %s -- close window when done viewing" % filename)
            filtered_im = self.apply_color_filter_hsv_to_named_image_file(filename)
            pixel_coords = self.connected_components_of_filtered_output(filtered_im, self.min_brightness_level, self.min_area_threshold, self.max_area_threshold, self.max_number_of_blobs, self.object_shape) 
            print("Number of objects detected: %d" % len(pixel_coords))
            upper_left_corner = ((image_file_index % hpos) * M, (image_file_index//hpos) * N)
            real_pixel_coords = map(lambda x: (upper_left_corner[0] + x[0], upper_left_corner[1] + x[1]), pixel_coords)
            positions_of_detected_objects += real_pixel_coords
            print("Pixel coordinates for detections: %s" % str(pixel_coords))
            print("Real coordinates for detections: %s" % str(real_pixel_coords))
            print("All coordinates for detections: %s" % str(positions_of_detected_objects))
            original_image = self.original_im.copy()
            width,height = original_image.size
            for pixel in positions_of_detected_objects:
                if all(x > 20 for x in pixel) and (pixel[0] < width-20) and (pixel[1] < height-20):
                    for i in range(-20,20):
                        for j in range(-20,20):
                            original_image.putpixel((pixel[0]+i,pixel[1]+j), (255,0,0))
            self.displayImage6(original_image, "image with detections -- close window when done viewing")
            blocks_examined += 1
        return positions_of_detected_objects

    def analyze_single_subimage_from_image_scan(self):
        '''
        The purpose of this method is examine the results of object detection for a single subimage 
        extracted during a scan of the large input image.  It is assumed that the subimage to be examined is 
        in a file in a directory dump_directory instance variable.
        '''
        if (not os.path.exists("scanner_dump")) or (len(glob.glob("scanner_dump/*")) == 0):
            sys.exit("Before you call analyze_single_subimage_from_image_scan(), you must create a scan dump by invoking scan_image_for_detections_interactive() or scan_image_for_detections() on an instance of the ImageScanner class).  See the relevant example script in the ExamplesScanner directory for why.")
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        self.image_width, self.image_height = self.original_im.size
        print("size of the image is: %s" % str((self.image_width,self.image_height)))
        print("\n\nAnalyzing contents of the subimage in file: %s" % self.subimage_filename)
        M,N = self.scanning_window_width, self.scanning_window_height
        subimage_file_index = file_index(self.subimage_filename)
        image_name = self.data_im_name
        hpos = self.image_width // self.scanning_window_width
        vpos = self.image_height // self.scanning_window_height
        positions_of_detected_objects = []
        subimage = Image.open(self.subimage_filename)
        mw = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (self.image_height * 1.0 / self.image_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (self.image_width * 1.0 / self.image_height))
        scaled_image = self.original_im.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title( image_name + ": Displaying detections" ) 
        mw.configure( height = winsize_y, width = winsize_x )         
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,            
                             width = winsize_x,             
                             cursor = "crosshair" )   
        canvas.pack(fill=BOTH, expand=True)
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = image_name + "_detections.jpg") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            

        photo = ImageTk.PhotoImage( scaled_image )
        canvas.create_image(winsize_x//2,winsize_y//2,image=photo)
        scale_x = winsize_x / (self.image_width * 1.0)
        scale_y = winsize_y / (self.image_height * 1.0) 
        print("\nx_scale: %f" % scale_x)
        print("y_scale: %f" % scale_y)
        rectscan = canvas.create_rectangle((0, 0, int(M*scale_x), int(N*scale_y)), width='7', outline='red') 
        horiz_move_to_pos = (subimage_file_index % hpos) * int(M * scale_x)
        vert_move_to_pos = (subimage_file_index // hpos) * int(N * scale_y)
        canvas.move(rectscan, horiz_move_to_pos, vert_move_to_pos)
        canvas.update()
        mw.update()
        image_item = Image.open(self.subimage_filename)
        width,height = image_item.size
        tk2 = Tkinter.Toplevel(takefocus = True)
        winsize_x,winsize_y = None,None
        screen_width,screen_height = tk2.winfo_screenwidth(),tk2.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (self.scanning_window_height * 1.0 / self.scanning_window_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (self.scanning_window_width * 1.0 / self.scanning_window_height))
        display_image = image_item.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk2.title("wait for the results to appear in the other window")   
        frame = Tkinter.Frame(tk2, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk2.update()
        filtered_im = self.apply_color_filter_hsv_to_named_image_file(self.subimage_filename, False)
        pixel_coords = self.connected_components_of_filtered_output(filtered_im, self.min_brightness_level, self.min_area_threshold, self.max_area_threshold, self.max_number_of_blobs, self.object_shape, False) 
        print("Number of objects detected: %d" % len(pixel_coords))
        upper_left_corner = ((subimage_file_index % hpos) * M, (subimage_file_index//hpos) * N)
        real_pixel_coords = map(lambda x: (upper_left_corner[0] + x[0], upper_left_corner[1] + x[1]), pixel_coords)
        positions_of_detected_objects += real_pixel_coords
        print("Pixel coordinates for detections: %s" % str(pixel_coords))
        print("Real coordinates for detections: %s" % str(real_pixel_coords))
        print("All coordinates for detections: %s" % str(positions_of_detected_objects))
        original_image = self.original_im.copy()
        width,height = original_image.size
        for pixel in positions_of_detected_objects:
            if all(x > 20 for x in pixel) and (pixel[0] < width-20) and (pixel[1] < height-20):
                rect = canvas.create_rectangle((pixel[0]-20)*scale_x, (pixel[1]-20)*scale_y, 
                               (pixel[0]+20)*scale_x, (pixel[1]+20)*scale_y, width='2', outline='red', fill='red') 
        canvas.update()
        mw.mainloop()
        return positions_of_detected_objects

    def analyze_single_subimage_from_image_scan_and_show_intermediate_results(self):
        '''
        The purpose of this method is examine the results of object detection for a single subimage 
        extracted during a scan of the large input image.  It is assumed that the subimage to be examined is 
        in a file in a directory dump_directory instance variable.
        '''
        if (not os.path.exists("scanner_dump")) or (len(glob.glob("scanner_dump/*")) == 0):
            sys.exit("Before invoking analyze_single_subimage_from_image_scan_and_show_intermediate_results(), you must first create scan dump of subimages by invoking scan_image_for_detections_interactive() or scan_image_for_detections() on an instance of the ImageScanner class.  See the relevant example script in the ExamplesScanner directory for why.")
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        self.image_width, self.image_height = self.original_im.size
        print("size of the image is: %s" % str((self.image_width,self.image_height)))
        print("\n\nAnalyzing contents of the subimage in file: %s" % self.subimage_filename)
        M,N = self.scanning_window_width, self.scanning_window_height
        subimage_file_index = file_index(self.subimage_filename)
        image_name = self.data_im_name
        hpos = self.image_width // self.scanning_window_width
        vpos = self.image_height // self.scanning_window_height
        positions_of_detected_objects = []
        subimage = Image.open(self.subimage_filename)
        tk2 = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = tk2.winfo_screenwidth(),tk2.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (self.scanning_window_height * 1.0 / self.scanning_window_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (self.scanning_window_width * 1.0 / self.scanning_window_height))
        display_image = subimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk2.title("subimage -- close when done viewing")   
        frame = Tkinter.Frame(tk2, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk2.mainloop()
        filtered_im = self.apply_color_filter_hsv_to_named_image_file(self.subimage_filename)
        pixel_coords = self.connected_components_of_filtered_output(filtered_im, self.min_brightness_level, self.min_area_threshold, self.max_area_threshold, self.max_number_of_blobs, self.object_shape) 
        print("Number of objects detected: %d" % len(pixel_coords))
        upper_left_corner = ((subimage_file_index % hpos) * M, (subimage_file_index//hpos) * N)
        real_pixel_coords = map(lambda x: (upper_left_corner[0] + x[0], upper_left_corner[1] + x[1]), pixel_coords)
        positions_of_detected_objects += real_pixel_coords
        print("Pixel coordinates for detections: %s" % str(pixel_coords))
        print("Real coordinates for detections: %s" % str(real_pixel_coords))
        print("All coordinates for detections: %s" % str(positions_of_detected_objects))
        import pymsgbox
        response = pymsgbox.confirm("Do you want to see the object coordinates in the main image?")
        if response == "OK": 
            orig_image = self.original_im.copy()
            orig_image_w,orig_image_h = self.original_im.size
            print("size of the image is: %s" % str((orig_image_w,orig_image_h)))
            mw = Tkinter.Tk()
            winsize_x,winsize_y = None,None
            screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
            if screen_width <= screen_height:
                winsize_x = int(0.5 * screen_width)
                winsize_y = int(winsize_x * (orig_image_h * 1.0 / orig_image_w))            
            else:
                winsize_y = int(0.5 * screen_height)
                winsize_x = int(winsize_y * (orig_image_w * 1.0 / orig_image_h))
            scaled_image = orig_image.resize((winsize_x,winsize_y), Image.ANTIALIAS)
            mw.title( image_name + ": Displaying detections" ) 
            mw.resizable(True,True)
            mw.configure( height = winsize_y, width = winsize_x )         
            canvas = Tkinter.Canvas( mw,                         
                                 height = winsize_y,            
                                 width = winsize_x,             
                                 cursor = "crosshair" )   
            canvas.pack(fill=BOTH, expand=True)
            frame = Tkinter.Frame(mw)                            
            frame.pack( side = 'bottom' )                             
            Tkinter.Button( frame,         
                    text = 'Save',                                    
                    command = lambda: canvas.postscript(file = image_name + "_detections.jpg") 
                  ).pack( side = 'left' )                             
            Tkinter.Button( frame,                        
                    text = 'Exit',                                    
                    command = lambda: mw.destroy(),                    
                  ).pack( side = 'right' )                            
    
            photo = ImageTk.PhotoImage( scaled_image )
            canvas.create_image(winsize_x//2,winsize_y//2,image=photo)
            scale_x = winsize_x / (orig_image_w * 1.0)
            scale_y = winsize_y / (orig_image_h * 1.0) 
            print("\nx_scale: %f" % scale_x)
            print("y_scale: %f" % scale_y)
            rectscan = canvas.create_rectangle((0, 0, int(M*scale_x), int(N*scale_y)), width='7', outline='red') 
            horiz_move_to_pos = (subimage_file_index % hpos) * int(M * scale_x)
            vert_move_to_pos = (subimage_file_index // hpos) * int(N * scale_y)
            canvas.move(rectscan, horiz_move_to_pos, vert_move_to_pos)
            for pixel in positions_of_detected_objects:
                if all(x > 20 for x in pixel) and (pixel[0] < orig_image_w-20) and (pixel[1] < orig_image_h-20):
                    rect = canvas.create_rectangle((pixel[0]-20)*scale_x, (pixel[1]-20)*scale_y, 
                                   (pixel[0]+20)*scale_x, (pixel[1]+20)*scale_y, width='2', outline='red', fill='red') 
            canvas.update()
            mw.update()
            mw.mainloop()
        return positions_of_detected_objects

    def scan_image_for_detections_interactive(self):
        '''
        This method creates a dump of subimages extracted from a large image.  The method is 
        interactive in the sense that it does shows the user each subimage for his/her examination 
        before dumping it in the dump directory.
        '''
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        M,N = self.scanning_window_width, self.scanning_window_height
        image = self.original_im.copy()
        self.image_width,self.image_height = self.original_im.size
        print("size of the image is: %s" % str((self.image_width,self.image_height)))
        self.array_R = numpy.zeros((M, N), dtype="int")
        self.array_G = numpy.zeros((M, N), dtype="int")
        self.array_B = numpy.zeros((M, N), dtype="int")
        mw = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (self.image_height * 1.0 / self.image_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (self.image_width * 1.0 / self.image_height))
        image = image.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title( "Image scanner in action" ) 
        mw.configure( height = winsize_y, width = winsize_x )         
        self.canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,            
                             width = winsize_x,             
                             cursor = "crosshair" )   
        self.canvas.pack(fill=BOTH, expand=True)
        photo = ImageTk.PhotoImage( image )
        self.canvas.create_image(winsize_x//2,winsize_y//2,image=photo)
        self.scale_x = winsize_x / (self.image_width * 1.0)
        self.scale_y = winsize_y / (self.image_height * 1.0) 
        print("\nx_scale: %f" % self.scale_x)
        print("y_scale: %f" % self.scale_y)
        horizontal_positions_of_scan_window = self.image_width // self.scanning_window_width
        vertical_positions_of_scan_window = self.image_height // self.scanning_window_height
        total_scan_window_positions = horizontal_positions_of_scan_window * vertical_positions_of_scan_window
        self.rect = self.canvas.create_rectangle((0, 0, int(M*self.scale_x), 
                                                         int(N*self.scale_y)), width='7', outline='red') 
        self.canvas.update()
        self.horizontal_positions_of_scan_window = horizontal_positions_of_scan_window
        self.vertical_positions_of_scan_window = vertical_positions_of_scan_window
        if os.path.exists("scanner_dump"):
            files = glob.glob("scanner_dump/*")
            map(lambda x: os.remove(x), files)
        else:
           os.mkdir("scanner_dump")
        self.moves_horizontal = self.image_width // self.scanning_window_width - 1
        self.moves_vertical = self.image_height // self.scanning_window_height - 1
        self.delta_x = int(self.scanning_window_width * self.scale_x)
        self.delta_y = int(self.scanning_window_height * self.scale_y)
        self.x_incr, self.y_incr = 0,0
        self.old_posx, self.old_posy = 0,0
        self.iteration_index = 0
        self.total_num_window_pos = (self.moves_horizontal + 1) * (self.moves_vertical + 1)
        self.num_remaining_pos = self.total_num_window_pos
        self.block_index = 0
        print("horizontal moves max index: %d" % self.moves_horizontal)
        print("vertical moves max index: %d" % self.moves_vertical)
        self._move()
        mw.mainloop()

    def scan_image_for_detections_noninteractive(self):
        '''
        This method creates a dump of subimages extracted from a large image.  The method is 
        noninteractive in the sense that it does not show the user each subimage for his/her
        examination before dumping it in the dump directory.
        '''
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        M,N = self.scanning_window_width, self.scanning_window_height
        image = self.original_im.copy()
        self.image_width,self.image_height = self.original_im.size
        print("size of the image is: %s" % str((self.image_width,self.image_height)))
        self.array_R = numpy.zeros((M, N), dtype="int")
        self.array_G = numpy.zeros((M, N), dtype="int")
        self.array_B = numpy.zeros((M, N), dtype="int")
        mw = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (self.image_height * 1.0 / self.image_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (self.image_width * 1.0 / self.image_height))
        image = image.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title( "Image scanner in action" ) 
        mw.configure( height = winsize_y, width = winsize_x )         
        self.canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,            
                             width = winsize_x,             
                             cursor = "crosshair" )   
        self.canvas.pack(fill=BOTH, expand=True)
        photo = ImageTk.PhotoImage( image )
        self.canvas.create_image(winsize_x//2,winsize_y//2,image=photo)
        self.scale_x = winsize_x / (self.image_width * 1.0)
        self.scale_y = winsize_y / (self.image_height * 1.0) 
        print("\nx_scale: %f" % self.scale_x)
        print("y_scale: %f" % self.scale_y)
        horizontal_positions_of_scan_window = self.image_width // self.scanning_window_width
        vertical_positions_of_scan_window = self.image_height // self.scanning_window_height
        total_scan_window_positions = horizontal_positions_of_scan_window * vertical_positions_of_scan_window
        self.rect = self.canvas.create_rectangle((0, 0, int(M*self.scale_x), 
                                                         int(N*self.scale_y)), width='7', outline='red') 
        self.canvas.update()
        self.horizontal_positions_of_scan_window = horizontal_positions_of_scan_window
        self.vertical_positions_of_scan_window = vertical_positions_of_scan_window
        if os.path.exists("scanner_dump"):
            files = glob.glob("scanner_dump/*")
            map(lambda x: os.remove(x), files)
        else:
           os.mkdir("scanner_dump")
        self.moves_horizontal = self.image_width // self.scanning_window_width - 1
        self.moves_vertical = self.image_height // self.scanning_window_height - 1
        self.delta_x = int(self.scanning_window_width * self.scale_x)
        self.delta_y = int(self.scanning_window_height * self.scale_y)
        self.x_incr, self.y_incr = 0,0
        self.old_posx, self.old_posy = 0,0
        self.iteration_index = 0
        self.total_num_window_pos = (self.moves_horizontal + 1) * (self.moves_vertical + 1)
        self.num_remaining_pos = self.total_num_window_pos
        self.block_index = 0
        print("horizontal moves max index: %d" % self.moves_horizontal)
        print("vertical moves max index: %d" % self.moves_vertical)
        self._move_noninteractive()
        mw.mainloop()

    #______________________  Private Methods of the ImageScanner Class  ________________

    def _move(self):
        self.num_remaining_pos -= 1
        print("Creating pixel values array for local window at block index: %d" % self.block_index)
        for x in range(self.x_incr * self.scanning_window_width, (self.x_incr + 1) * self.scanning_window_width):        
            for y in range(self.y_incr * self.scanning_window_height, (self.y_incr + 1) * self.scanning_window_height):
                r,g,b = self.original_im.getpixel((x,y))
                self.array_R[y % self.scanning_window_height, x % self.scanning_window_width] = r
                self.array_G[y % self.scanning_window_height, x % self.scanning_window_width] = g
                self.array_B[y % self.scanning_window_height, x % self.scanning_window_width] = b
        height,width = self.array_R.shape
        newimage = Image.new("RGB", (width,height), (0,0,0))
        for i in range(0, height):
            for j in range(0, width):
                r,g,b = self.array_R[i,j], self.array_G[i,j], self.array_B[i,j]
                newimage.putpixel((j,i), (r,g,b))
        newimage.save(self.scanner_dump_directory +  "/subimage_" + str(self.block_index) + ".jpg")
        width,height = newimage.size
        tk2 = Tkinter.Toplevel(takefocus = True)
        winsize_x,winsize_y = None,None
        screen_width,screen_height = tk2.winfo_screenwidth(),tk2.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        display_image = newimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk2.title("scanned window")   
        frame = Tkinter.Frame(tk2, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk2.update()
        print("=========  done with scan window display =========")
        response = pymsgbox.confirm("Done with viewing scan window?")
        if response == "OK": 
            tk2.after(10, self._callback, tk2)
        new_posx = self.old_posx + self.delta_x
        if new_posx + self.delta_x < int(self.image_width * self.scale_x):
            self.canvas.move( self.rect, self.delta_x, 0)
            self.old_posx = new_posx
            self.x_incr += 1
        elif self.old_posy + 2 * self.delta_y < int(self.image_height * self.scale_y):
            self.canvas.move( self.rect, -1 * self.moves_horizontal * self.delta_x, self.delta_y ) 
            self.old_posx = 0
            self.x_incr = 0
            self.old_posy += self.delta_y
            self.y_incr += 1    
        self.canvas.update()
        self.block_index += 1
        if self.num_remaining_pos > 0:
            self._move()

    def _move_noninteractive(self):
        if self.block_index == 0:
            time.sleep(1)             # one second
        self.num_remaining_pos -= 1
        print("Creating pixel values array for local window at block index: %d" % self.block_index)
        for x in range(self.x_incr * self.scanning_window_width, (self.x_incr + 1) * self.scanning_window_width):        
            for y in range(self.y_incr * self.scanning_window_height, (self.y_incr + 1) * self.scanning_window_height):
                r,g,b = self.original_im.getpixel((x,y))
                self.array_R[y % self.scanning_window_height, x % self.scanning_window_width] = r
                self.array_G[y % self.scanning_window_height, x % self.scanning_window_width] = g
                self.array_B[y % self.scanning_window_height, x % self.scanning_window_width] = b
        height,width = self.array_R.shape
        newimage = Image.new("RGB", (width,height), (0,0,0))
        for i in range(0, height):
            for j in range(0, width):
                r,g,b = self.array_R[i,j], self.array_G[i,j], self.array_B[i,j]
                newimage.putpixel((j,i), (r,g,b))
        newimage.save(self.scanner_dump_directory + "/subimage_" + str(self.block_index) + ".jpg")
        new_posx = self.old_posx + self.delta_x
        if new_posx + self.delta_x < int(self.image_width * self.scale_x):
            self.canvas.move( self.rect, self.delta_x, 0)
            self.old_posx = new_posx
            self.x_incr += 1
        elif self.old_posy + 2 * self.delta_y < int(self.image_height * self.scale_y):
            # we need to bring the window back from the last col to the first col in the next row:
            self.canvas.move( self.rect, -1 * self.moves_horizontal * self.delta_x, self.delta_y ) 
            self.old_posx = 0
            self.x_incr = 0
            self.old_posy += self.delta_y
            self.y_incr += 1
        self.canvas.update()
        self.block_index += 1
        if self.num_remaining_pos > 0:
            self._move_noninteractive()

    def _callback(self,arg):
        arg.destroy()

#_________________________  End of ImageScanner Class Definition ___________________________

