__version__ = '2.2.0'
__author__  = "Avinash Kak (kak@purdue.edu)"
__date__    = '2017-May-24'   
__url__     = 'https://engineering.purdue.edu/kak/distWatershed/Watershed-2.2.0.html'
__copyright__ = "(C) 2017 Avinash Kak. Python Software Foundation."

__doc__ = '''

Watershed.py

Version: ''' + __version__ + '''
   
Author: Avinash Kak (kak@purdue.edu)

Date: ''' + __date__ + '''


@title
CHANGE LOG:

  Version 2.2.0

    This version of the module incorporates an ImageScanner class that
    facilitates the segmentation and detection of small objects in large
    images.  Consider the fact that you can now purchase a rather
    inexpensive digital camera that can record images of size 5472x3648.
    Let's say you use such a camera to take a photo of a large scene and
    that you are interested in segmenting out tiny objects in such
    photos. Creating solutions for such computer vision problems frequently
    requires scanning the large image and attempting object detection in
    the subimages for the different positions of the scanning window.  It
    is for such solutions to computer vision problems that you will find
    the ImageScanner class useful.  This class has been provided with
    methods that allow you to visualize the results of the operations
    carried out on the subimages both in the subimages and in the original
    large image simultaneously.

  Version 2.0.4

    This version fixes a "small bug" I discovered in the connected
    component labeling logic.  The bug made itself evident if a connected
    component consisted of just one pixel --- a highly unlikely occurrence
    in real-world images but important nevertheless.  Additionally, this
    version allows the 'apply_otsu_threshold_to_hue()' method to report the
    number of blobs found.  This method can be supplied with a keyword
    argument that serves as the area threshold for the blobs.

  Version 2.0.3

    This version allows you to carry out histogram equalization in an image
    before subjecting it to watershed segmentation.  Histogram equalization
    is applied to the 'v' component of the HSV representation of a color
    image.  Additionally, now you can first carry out a hue-based
    foreground/background separation through a threshold based on the Otsu
    algorithm and then use watershed to extract fine structure in just the
    foreground.

  Version 2.0.2

    This version enhances the module in the following two ways: (1) You can
    now apply watershed segmentation to just a portion of the input image.
    The portion that you are interested in can be specified through mouse
    clicks or by first clicking at a point and then dragging the mouse
    pointer over the image.  And (2) You can apply a color filter to the
    image before it is segmented.  The color filter can be specified in one
    of two different ways: as a triple of scalars or as a triple of
    pairs. If you specify the filter as a triple of three scalar values,
    each scalar is used to multiply the corresponding color component.  On
    the other hand, if you specify the filter as a triple of pairs, then a
    pixel is let through only if its each color component falls in the
    range dictated by the corresponding pair.

  Version 2.0.1

    With this version, you can now directly access the segmented blobs in
    your own code.  The previous versions only displayed the segmented
    image on your terminal screen.  This version also incorporates
    improvements in the implementation of the logic of watershed
    segmentation.

  Version 2.0

    This is a Python 3.x compliant version of the Watershed module.  This
    version should work with both Python 2.7 and Python 3.x.

  Version 1.1.2

    This version fixes the module packaging errors that had crept into the
    previous version.

  Version 1.1.1

    This version presents cleaned-up documentation.  The implementation
    code remains unchanged.

  Version 1.1

    This version fixes a bug in the dilate() and erode() methods of the
    module that caused these methods to misbehave for non-square images.
    Version 1.1 also includes improvements in the explanatory comments
    included in the scripts in the Examples directory.


@title
INTRODUCTION:

    Over the years, the watershed algorithm has emerged as a powerful
    approach to image segmentation.  Image segmentation means to separate
    the foreground --- meaning the objects of interest --- from the
    background.  This approach becomes even more powerful when you allow a
    user to modify the image gradients prior to the application of the
    watershed algorithm.

    In the watershed algorithm, we think of the gradient image as a 3D
    topographic relief map that consists of mountains where the gradient
    values are high and valleys where they are low.  The watersheds are the
    ridge lines in this 3D map that delineate common basins for water
    drainage.  Note that the term watershed is also used to denote all of
    the surface area where the water drains toward a common basin (or
    valley).  When thought of as in the latter definition, watershed area
    would be delineated by the aforementioned ridge lines.  

    In computer vision algorithms, a watershed consists of the highest
    points that delineate a surface area in which the water would drain to
    a common valley.  It is important to realize that the points on a
    watershed can be at very different elevations. That is, the height
    above the ground plane along a watershed can vary significantly. Think
    of the Great Continental Divide as a watershed that divides the two
    American continents, the North and the South, into two regions, one
    that drains into the Pacific and the other that drains into the
    Atlantic.  If you were to walk along this Great Divide all the way from
    where it begins in Alaska to its final point in Patagonia at the
    southern tip of Chile, you will be at vastly different elevations above
    the sea level.  If you are on the Divide in Colorado, you are likely to
    find snow at several places even in summer months.  But if you follow
    the divide into Arizona, at several places you'll be in the middle of
    what to the naked eye would like a flat desert.

    These properties of the natural watersheds make the Watershed a
    powerful paradigm for image segmentation.  When you closely examine the
    semantically meaningful regions in typical images, you are likely to
    see a large variation in the gradient levels that separate the
    foreground regions from the background regions.  Obviously, the
    strength of the gradient that separates the foreground and the
    background is a function of the local gray levels in both the
    foreground and the background in the vicinity of the border between
    them.  So, while you cannot attribute specific values to such
    separating gradients, the gradient highlights are nonetheless real for
    the most part since that's how the human eye sees the different regions
    in an image.

    That brings us to the question of how to actually implement the
    watershed paradigm for image segmentation.  This module is based on
    what is known as the "flooding model" of computations for extracting
    the watershed from a gradient image when it is thought of as a 3D
    relief.  The flooding model is based on the idea that if we prick holes
    at the lowest points in all of the valleys of a topographic relief
    representation of a gradient image and gradually submerge the holed 3D
    structure in a pool of water, the rising flood in one valley will meet
    the flood in another valley at the watershed ridge points between the
    two valleys.  Since the watershed ridges can be at varying heights, in
    order to identify the watershed points beyond the first such point, we
    immediately put up a dam at the discovered watershed points so that the
    logic of watershed identification can be maintained at all heights.

    The flooding model that is implemented in this module is based on the
    work of Beucher, Lantuejoul, and Meyer.  A description of the algorithm
    can be found in the following Google accessible report by S. Beucher:
    "The Watershed Transformation Applied to Image Segmentation."  This
    algorithm will be refered to as the "BLM algorithm" in the rest of this
    web page.

    The BLM algorithm uses morphological operators for simulating the
    rising flood in the topographic relief map of the gradient image. The
    most important morphological operations in this context are those of
    dilations, distance mapping, calculation of the influence zones in a
    binary blob with respect to marker sets, and the determination of
    geodesic skeletons.  These operators are applied to the Z level sets
    derived from the gradient map.  For a given level, the pixels that
    belong to the Z set at that level are those whose gradient values are
    less than or equal to the level.  Flooding in the BLM algorithm is
    simulated by computing the influence zones of the flooded pixels at one
    Z level in all the pixels that belong to the next higher Z level.


@title
COMPARISON WITH THE OpenCV WATERSHED IMPLEMENTATION:

    If your main interest is in just the final output --- good-quality
    watershed segmentations based on user-supplied seeds --- then this
    Python module is not for you and you should use the OpenCV
    implementation. With regard to the speed of execution, a pure Python
    module such as this cannot hope to compete with the C-based
    implementation in the OpenCV library.

    But do bear in mind that the segmentation produced by the OpenCV
    implementation is driven entirely by the user-supplied seeds.  In fact,
    the number of image segments produced by the OpenCV algorithm equals
    the number of seeds supplied by the user --- even when two different
    seeds are placed in the same homogeneous region of the image.

    On the other hand, this Python module will give you a watershed
    segmentation even when you do not supply any seeds (or, marks, as I
    refer to them in the implementation here).  So you could say that the
    user supplied marks (seeds) for this Python module are more for the
    purpose of creating new valleys in the topographic relief
    representation of the gradient map than for nucleating the formation of
    valleys for the discovery of watersheds that must partition the image
    into a specific number of segments.
   

@title
INSTALLATION:

    The Watershed class was packaged using setuptools.  For installation,
    execute the following command in the source directory (this is the
    directory that contains the setup.py file after you have downloaded and
    uncompressed the package):
 
            sudo python setup.py install

    and/or, for the case of Python3, 

            sudo python3 setup.py install

    On Linux distributions, this will install the module file at a location
    that looks like

             /usr/local/lib/python2.7/dist-packages/

    and, for the case of Python3, at a location that looks like

             /usr/local/lib/python3.5/dist-packages/

    If you do not have root access, you have the option of working directly
    off the directory in which you downloaded the software by simply
    placing the following statements at the top of your scripts that use
    the Watershed class:

            import sys
            sys.path.append( "pathname_to_Watershed_directory" )

    To uninstall the module, simply delete the source directory, locate
    where the Watershed module was installed with "locate Watershed" and
    delete those files.  As mentioned above, the full pathname to the
    installed version is likely to look like
    /usr/local/lib/python2.7/dist-packages/Watershed*

    If you want to carry out a non-standard install of the Watershed
    module, look up the on-line information on Disutils by pointing your
    browser to

              http://docs.python.org/dist/dist.html


@title
USAGE:

    To segment an image, you would first construct an instance of the
    Watershed class and invoke the methods shown below on this instance:

        from Watershed import *

        shed = Watershed(
                   data_image = "orchid0001.jpg",
                   binary_or_gray_or_color = "color",
                   size_for_calculations = 128,
                   sigma = 1,
                   gradient_threshold_as_fraction = 0.1,
                   level_decimation_factor = 16,
                   padding = 20,
               )
        shed.extract_data_pixels()
        shed.display_data_image()
        shed.mark_image_regions_for_gradient_mods()                     #(A)
        shed.compute_gradient_image()
        shed.modify_gradients_with_marker_minima()                      #(B)
        shed.compute_Z_level_sets_for_gradient_image()
        shed.propagate_influence_zones_from_bottom_to_top_of_Z_levels()
        shed.display_watershed()
        shed.display_watershed_in_color()
        shed.extract_watershed_contours()
        shed.extract_watershed_contours_with_random_sampling(30, 50)    #(C)
        shed.display_watershed_contours_in_color()

    
    The statements in lines (A) and (B) are needed only for marker-assisted
    segmentation with the module.  For a fully automated implementation of
    the BLM algorithm, you would need to delete those two statements.

    The statement in line (C) can be replaced by

        shed.extract_watershed_contours_separated()

    for faster contour extraction.  However, if the different contours are
    expected to share pixels, you are likely to get superior results with
    the call shown in line (C) above.  Both contour extraction methods
    return a list of contours, with each contour a list of pixel
    coordinates.

    If you just want to use this module just for demonstrating basic
    morphological operations of dilations and erosions, your script would
    look like:

        shed = Watershed(
                   data_image = "triangle1.jpg", 
                   binary_or_gray_or_color = "binary",
               )
        shed.extract_data_pixels() 
        shed.display_data_image()
        dilated_image = shed.dilate(5)                                     
        shed.erode(dilated_image, 5)        

    On the other hand, if you want to use this module to demonstrate
    distance mapping of a binary blob with respect to one or more marker
    blobs, your code is likely to look like:

        shed = Watershed(
                   data_image = "artpic3.jpg",
                   binary_or_gray_or_color = "binary",
                   debug = 0,
               )
        shed.extract_data_pixels() 
        shed.display_data_image()
        shed.connected_components("data")
        shed.mark_blobs()
        shed.connected_components("marks")
        shed.dilate_mark_in_its_blob(1)

    Note that now you must make calls to "connected_components()" to
    separate out the blobs in your input binary image, and to
    "mark_blobs()" to let a user mark up a blob for distance mapping.  It
    is the last call shown above, to "dilate_mark_in_its_blob()" that
    carries out distance mapping of the chosen blob with respect to the
    mark. Note that this takes an integer argument that is supposed to be
    integer index of the mark.  If you placed only one mark in the blob,
    this arg must be set to 1.  On the other hand, if you placed, say, two
    marks in a blob, then by supplying 2 for the argument you will see
    distance mapping with respect to the other mark. So, what you supply
    for the argument is an integer value between 1 and the number of marks
    you created.

    If you want to demonstrate the calculation of influence zones with this
    module, replace the last statement in the example shown above with the
    statement:

        shed.compute_influence_zones_for_marks()

    The module also includes two static methods that allow you to create
    your own binary images for demonstrating the basic operations built
    into the module.  The syntax for calling these method looks like:

        Watershed.gendata("triangle", (100,100), (10,10), 30, "new_triangle.jpg" 

        Watershed.make_binary_pic_art_nouveau("new_art_from_me")

    The second call in particular allows you to create artsy looking binary
    blobs just by rapidly moving your mouse over the window that is shown
    as you keep your left mouse button pressed.  Alternating clicks of the
    left mouse button start and stop this process.


@title
CONSTRUCTOR PARAMETERS: 

    binary_or_gray_or_color: Must be set to either 'binary', or 'gray', or
                    'color', as the case may be.  A binary image is
                    thresholded after it is loaded in to produce binary
                    pixels.  And a color image is converted into a
                    grayscale image before the application of the watershed
                    algorithm.  Ordinarily, you would want to use binary
                    images just for demonstrating the dilation, erosion,
                    distance mapping, IZ calculation, and geodesic skeleton
                    calculation capabilities of this module.

    color_filter: The color filter can be specified in one of two different
                    ways: as a triple of scalars or as a triple of
                    pairs. If you specify the filter as a triple of three
                    scalar values, each scalar is used to multiply the
                    corresponding color component.  On the other hand, if
                    you specify the filter as a triple of pairs, then a
                    pixel is let through only if its each color component
                    falls in the range specified by the corresponding pair.

    data_image: The image you wish to segment as, say, a '.jpg' file

    gradient_threshold_as_fraction: This parameter when set allows the
                    system to ignore small gradients in the image.  Note
                    that the gradient values are normalized to be between 0
                    and 255, both ends inclusive.  The default for this
                    parameter is 0.1.

    level_decimation_factor: This factor controls the number of levels of
                    the gradient that are subject to watershed
                    calculations.  Recall that the image gradient is
                    normalized to values between 0 and 255.  If you set
                    level_decimation_factor to 8, only every 8th gradient
                    level will be considered for the flooding calculations.
                    That is, with level_decimation_factor set to 8, you
                    will have a total of 32 levels of the gradient for the
                    discovery of the watersheds.

    max_gradient_to_be_reached_as_fraction: This parameter is useful for
                    debugging purposes.  When set to, say, 0.5, it will
                    stop the rising flood at half of the maximum value for
                    image gradient.  So by setting this parameter to a
                    small value, you can carry out a more detailed
                    examination of the propagation of the influence zones
                    from one level to the next.

    padding: This parameter pads the input image with a band of zeros, the
                    width of the band being equal to the value of this
                    parameter.  You will get better results for the
                    watershed contours if you use this parameter.  The band
                    needs to be wide enough so that even after LoG
                    smoothing, the border pixels for the padded image are
                    still set to to zero.

    size_for_calculations: If the larger of the two image dimensions is
                    greater than this number, the image is reduced in size
                    so that its larger dimension corresponds to the number
                    supplied through this parameter. As you would expect,
                    the smaller this parameter, the faster your results.
                    The default for this parameter is 128.

    sigma: Controls the size of the Gaussian kernel used for smoothing the
                    image before its gradient is calculated.  Assuming the
                    pixel sampling interval to be unity, a sigma of 1 gives
                    you a 7x7 smoothing operator with Gaussian weighting.
                    The default for this parameter is 1.


@title
PUBLIC METHODS:

    (1)  apply_color_filter_hsv()

         This method applies a color filter to the HSV representation of a
         color image prior to its watershed segmentation.  The filter must
         be specified either as a triple of scalars, as in "(1,0.5,0.8)",
         or a triple of pairs, as in "((0,35),(0,255),(0,255))".  When
         specified as a triple of scalars, each color component is
         multiplied by the corresponding scalar.  And when specified as a
         triple of pairs, each color component must be within the range
         dictated by the corresponding pair. With HSV, you are more likely
         to use the second form of the filter.  For example, the filter
         "((0,35),(0,255),(0,255))" works well if you want to let through
         only the red and reddish pixels.


    (2)  apply_color_filter_rgb()

         This method applies a color filter to the RGB representation of a
         color image prior to its watershed segmentation.  The filter must
         be specified either as a triple of scalars, as in "(1,0.5,0.8)",
         or a triple of pairs, as in "((0,35),(0,255),(0,255))".  When
         specified as a triple of scalars, each color component is
         multiplied by the corresponding scalar.  And when specified as a
         triple of pairs, each color component must be within the range
         dictated by the corresponding pair. With RGB, you are more likely
         to use the first form of the filter.  For example, if you wanted
         to apply the watershed segmentation to just the R component of a
         color image, your filter would be "(1,0,0)".


    (3)  apply_otsu_threshold_to_hue( polarity=1, area_threshold=0 )

         Applies the optimum Otsu threshold to hue in order to separate the
         image into foreground and background.  If the value supplied
         through the parameter 'polarity' is -1, all pixels whose hue is
         below the optimum Otsu threshold are accepted.  On the other hand,
         if the polarity is set to '1', all pixels whose hue is higher than
         the Otsu threshold are accepted. The method also isolates out the
         blobs resulting from the application of the Otsu threshold.  All
         blobs whose areas fall below the value supplied for
         'area_threshold' are rejected.  The method returns the number of
         blobs found.


    (4)  compute_influence_zones_for_marks()

         Calculates the influence zones in a binary blob with respect to
         the marks placed inside the blob.  The method also identifies the
         pixels at the geodesic skeleton formed by the influence zones.


    (5)  compute_LoG_image()

         This method computes the Laplacian-of-Gaussian (LoG) of an image.
         The LoG image is calculated as the difference of two
         Gaussian-smoothed versions of the input image at two slightly
         difference scales.  The LoG itself is NOT used in watershed
         calculations.


    (6)  compute_Z_level_sets_for_gradient_image()

         This method computes the Z levels for the BLM watershed algorithm.
         A pixel belongs to a specified Z level if the value of the image
         gradient at the pixel is less than or equal to that level.


    (7)  connected_components(arg)

         where 'arg' is the string "data" if you want to carry out
         connected-components labeling of binary blobs.  When the same
         method is called for the binary marks created by mouse clicks, we
         change the value of 'arg' to "marks".  Obviously, the components
         labeling logic works exactly the same in both cases.  The only
         differences are in how the labels are saved for bookkeeping
         purposes.


    (8)  dilate(radius, shape)

         where 'radius' would generally be a small integer denoting the
         radius of a disk structuring element to be used for the purpose of
         dilating the input pattern.  The parameter 'shape' must be set to
         either "square" or "circular" to specify the shape of the
         structuring element.  NOTE: This method only makes sense for
         binary input images, since it only carries out binary dilations.


    (9)  dilate_mark_in_its_blob()

         This is the method that demonstrations the distance mapping
         notions used in this module.  The module carries out a distance
         transformation of the blob that the user clicked on and does so
         with respect to the mark placed in the chosen blob when the left
         button of the mouse was clicked in it.


    (10) display_all_segmented_blobs()

         This method creates a composite image consisting of rectangular
         cells.  Each segmented object is placed in a separate cell.


    (11) display_data_image():

         It is always good to call this method after you have invoked
         "extract_data_pixels()" just to confirm the output of the data
         extraction step.


    (12) display_watershed()

         This method displays the watershed pixels against the image that
         was actually used for the application of the watershed algorithm.
         Even when the input image is in color, the image used for
         calculations is a grayscale version of the input
         image. Additionally, depending on the constructor parameter
         'size_for_calculations', the image used for calculations may also
         be of reduced size.


    (13) display_watershed_contours_in_color()

         The boundary contours for the segmented regions of the image are
         displayed against the original image by this method.

         To write this result image as a jpeg file to the disk, click on
         the "save" and "exit" buttons at the bottom of the window --- as
         opposed to just closing the window.  You can subsequently display
         the image from the disk file by using, say, the 'display' function
         from the ImageMagick library.  You can create a hardcopy version
         of the result by sending the jpeg image to a printer.


    (14) display_watershed_in_color()

         This display method shows the watershed pixels in color against
         the original image supplied to the module for segmentation.

         To write this result image as a jpeg file to the disk, click on
         the "save" and "exit" buttons at the bottom of the window --- as
         opposed to just closing the window.  You can subsequently display
         the image from the disk file by using, say, the 'display' function
         from the ImageMagick library.  You can create a hardcopy version
         of the result by sending the jpeg image to a printer.


    (15) erode(radius, shape)

         where 'radius' would generally be a small integer denoting the
         radius of a disk structuring element to be used for the purpose of
         dilating the input pattern.  The parameter 'shape' must be set to
         either "square" or "circular" to specify the shape of the
         structuring element.  NOTE: This method only makes sense for
         binary input images, since it only carries out binary dilations.


    (16) histogram_equalize():

        Carries out contrast enhancement in an image.  If an image is
        generally too dark or generally too bright, you may wish to
        histogram equalize it before subjecting it to watershed
        segmentation.


    (17) extract_data_pixels():

         This is the very first method you should call in all cases.  This
         loads your image into the module. If you declared your input image
         to be binary (when your image is in, say, the Jpeg format, the
         actual pixel values will in general not be binary), the loaded
         image is binarized by thresholding it in the middle of the gray
         scale range.  If you declared your input image to be color, it is
         first converted into grayscale for the calculation of the
         watersheds.  The image may also be reduced in size if that step is
         dictated by the value you supplied for the constructor parameter
         'size_for_calculations'.  Depending on this parameter, an input
         image declared to be gray will also be downsized.


    (18) extract_image_region_interactively_through_mouse_clicks():

         This method allows a user to use a sequence of mouse clicks in
         order to specify a region of the input image that should be
         subject to watershed segmentation.  The mouse clicks taken
         together define a polygon. The method encloses the polygonal
         region by a minimum bounding rectangle, which then becomes the new
         input image for the rest of processing.


    (19) extract_image_region_interactively_by_dragging_mouse():

         This is one method you can use to apply watershed segmentation to
         just a portion of your image.  This method extract the portion you
         want.  You click at the upper left corner of the rectangular
         portion of the image you are interested in and you then drag the
         mouse pointer to the lower right corner.  Make sure that you click
         on "save" and "exit" after you have delineated the area.


    (20) extract_rectangular_masked_segment_of_image(self, horiz_start, horiz_end, vert_start, vert_end)

         This method is useful for extracting a rectangular section from
         the data image supplied to the module.  Now how the parameters
         are laid out.  The first two parameters together specify the 
         width of the rectangle and the last two parameters together 
         the height.


    (21) extract_segmented_blobs_using_contours( min_length )

         This method uses the inside/outside logic at a point (based on the
         number of times a line through the point intersects the contour)
         in order to decide whether the point is inside a closed contour or
         outside it.  A contour must be longer than 'min_length' pixels in
         order to be considered for this logic. This method returns a list
         of lists, with each list in the latter being a list of all the
         pixels that are in a segmented blob.


    (22) extract_segmented_blobs_using_region_growing( num_of_segments, min_area )

         This method uses region growing to pull out the segmented blobs
         from the output of watershed segmentation.  All such segments
         whose area (in terms of the number of pixels) is less than the
         parameter 'min_area' are discarded.  Set the first parameter,
         'num_of_segments', to the number of segmented blobs you wish to
         extract from the image.  The value given to 'num_of_segments' sets
         a maximum for the number of segmented blobs the method will seek
         out from the watershed segmentation.  This method returns a list
         of lists, with each list in the latter being a list of all the
         pixels that are in a segmented blob.


    (23) extract_watershed_contours_with_random_sampling( how_many, min_len )

         This method extracts the watershed pixels as boundary contours
         using an 8-connected boundary following algorithm. Use this method
         if the different contours are expected to share pixels.  The
         parameter 'how_many' is the number of contours you'd like to
         extract and the parameter 'min_len' sets the smallest acceptable
         length for the contours.  You can use 'min_len' to reject small
         noise induced contours.  This method returns a list of contours,
         with each contour a list of pixel coordinates.


    (24) extract_watershed_contours_separated()

         This much faster method extracts the watershed pixels as boundary
         contours using an 8-connected boundary following algorithm. Use
         this method if all contours are disjoint.  Like the previous
         method, this method also returns a list of contours, with each
         contour a list of pixel coordinates.


    (25) gendata(feature, size_tuple, location_tuple, orientation_or_radius, filename)

         This static method is useful for generating simple binary patterns
         for checking the validity of the logic used for dilation, erosion,
         IZ calculation, geodesic skeleton calculation, etc.  The
         permissible values for the 'feature' parameter are: 'line',
         'triangle', 'rectangle', 'broken_rectangle', 'disk' and
         'twin_rect'.  The parameter 'size_tuple' is for the size of the
         output image desired.  The parameter 'position' is supposed to be
         a tuple (x,y) of pixel coordinates for specifying the position of
         the binary pattern in your image.  The parameter
         'orientation_or_radius' is an integer value specifying the number
         of degrees of rotation that should be applied to the pattern for a
         given 'feature' for the case of 'line', 'triangle', 'rectangle'
         and 'broken_rectangle'.  The same parameter for the case of
         'circle' means the radius of the disk. Finally, the parameter
         'filename' names the file in which the binary image will be
         deposited.  For the parameters that take tuple values, the first
         coordinate is along the horizontal direction pointing to the right
         and the second coordinate is along vertical direction pointing
         downwards.  The origin is at the upper left corner of your
         terminal screen.


    (26) make_binary_pic_art_nouveau( filename )

         This static method can be used to make "fun" binary images for
         demonstrating distance mapping of binary blobs, calculation of
         influence zones, etc.  This method is taken from Chapter 13 of my
         book "Scripting with Objects".


    (27) mark_blobs( purpose )

        A useful method for demonstrating distance mapping of a binary blob
        with respect to a marker blob, this method allows a user to both
        select one or more blobs in a binary image for the purpose of
        distance mapping and to also place marks on the blobs.  The
        'purpose' parameter must take one of the following two values:
        'distance_mapping' or 'influence_zones'.


    (28) mark_blobs_no_image_scale_change()

        The previously listed 'mark_blobs()' method adjusts the scale of
        the image according to your screen size to make it more convenient
        to enter the marks.  However, if you do not interact with the image
        without its scale being changed, use this method instead.


    (29) mark_image_regions_for_gradient_mods()

         For mark-based segmentation with the BLM watershed algorithm, this
         method elicits mouse clicks from the user that demarcate polygonal
         regions in the image where the gradient should be modified prior
         to the flooding process.  The mouse clicks must be supplied in a
         clockwise fashion to demarcate the polygonal regions.


    (30) modify_gradients_with_marker_minima()

         For mark-based application of the Watershed algorithm, it is this
         method that actually modifies the gradient image after a user has
         defined the regions for that purpose through the mouse clicks
         elicited by the mark_image_regions_for_gradient_mods() method.  In
         the current module, this modification simply consists of setting
         the gradient values to zero in such regions.


    (31) propagate_influence_zones_from_bottom_to_top_of_Z_levels()
           
         This is the workhorse of the module for watershed based
         segmentation of an image.  As explained elsewhere in this
         documentation, this method starts at the lowest Z level to
         discover the lowest valleys in the topographic relief
         representation of the image gradients.  Subsequently, the notion
         of a rising flood is simulated by calculating the influence zones
         (IZ) of the flooded pixels for one Z level in all of the pixels
         that belong to the next Z level.  The geodesic skeletons formed by
         the IZs lead to the discovery of the watershed pixels in a
         gradient image.


@title
APPLYING SEGMENTATION TO AN IMAGE PORTION AND USING A COLOR FILTER:

    Starting with Version 2.0.2, you can apply the segmentation algorithm
    to just a portion of the input image.  You can specify the image
    portion through two different ways: (1) You can create a rectangular
    portion by clicking your mouse pointer at the upper left corner of the
    rectangular area you are interested in and then dragging the mouse
    pointer to its lower right corner. And (2) You can specify any
    polygonal shape by simply clicking clockwise at the points
    corresponding to the vertices of the polygon.  The method to call for
    the first way of defining an area for segmentation is:
    
        extract_image_region_interactively_by_dragging_mouse()

    And the method to call for the second way of defining an area is:

        extract_image_region_interactively_through_mouse_clicks()

    Starting with Version 2.0.2, you can now also apply a color filter to
    an input image before it is segmented.  A color is specified by the
    constructor option "color_filter" and the methods to call in your
    script for applying the filter are:
    
        apply_color_filter_hsv()

        apply_color_filter_rgb()

    The following script in the Examples directory illustrates segmenting
    just a portion on an image and using a color filter:

        extract_image_portion_and_apply_color_filter_demo.py        


@title
THE ImageScanner CLASS:

    Starting with Version 2.2.0, you can use all of the functionality of
    the Watershed class through the new ImageScanner class if you want to
    use a scanning approach to solving a computer vision problem.  You will
    find the ImageScanner class particularly useful if you are dealing with
    large images and you want to segment out small objects.  Consider the
    fact that you can now purchase a fairly inexpensive digital camera
    capable of recording 5472x3648 images.  Let us say you use such a
    camera to record images of large scenes and that you want to
    automatically analyze those images for the presence of very small
    objects.  Developing and testing algorithms for such problems is best
    carried out by first scanning the large image using a scanning window
    whose size is commensurate with the size of the objects you are
    interested in.  That is, you first divide the large image into
    overlapping or non-overlapping subimages and you then focus on reliable
    object detection in the subimages.  This is where you'll find the
    ImageScanner class useful.  This class has been provided with methods
    that allow you to see the results of the operations carried out on the
    subimages both in the subimages and the original image simultaneously.
    
    The ImageScanner class is programmed as a subclass of the Watershed
    class.  Therefore, it inherits all of the functionality of the parent
    Watershed class.
    
    Here is now you'd call the constructor of the ImageScanner class for
    creating a dump of the subimages collected from all the positions of a
    scanning window as it moves across the image left to right and top to
    bottom:
    
        import ImageScanner
        image_file = "DSC00780.JPG"
        scanner = ImageScanner.ImageScanner(
                       data_image = image_file,
                       binary_or_gray_or_color = "color",
                       scanner_dump_directory = "scanner_dump",
                       scanning_window_width = 800,
                       scanning_window_height = 800
                  )
        
    After you have created a dump directory of the subimages in this manner,
    you'll call the ImageScanner constructor in the following fashion for
    object detection:
    
        import ImageScanner
        image_file = "DSC00780.JPG"
        scanner = ImageScanner.ImageScanner(
                       data_image = image_file,
                       binary_or_gray_or_color = "color",
                       scanner_dump_directory = "scanner_dump",
                       scanning_window_width = 800,
                       scanning_window_height = 800,
                       color_filter = [(0,30),(0,255),(0,255)],
                       min_brightness_level = 100,
                       min_area_threshold = 800,               
                       max_area_threshold = 8000,
                       max_number_of_blobs = 20,
                       object_shape  = "circular",
                 )
        positions_of_detected_objects = scanner.analyze_scanner_dump()
        
    As to what shapes would be detected by this kind of a constructor call
    depends on the code you place in the method analyze_scanner_dump() of
    the ImageScanner class.  The code shown for that method in the module
    is just a place holder for the kind of logic you would need to place in
    that method.
    

@title 
CONSTRUCTOR PARAMETERS OF THE ImageScanner CLASS:

    Since the ImageScanner class is a subclass of the Watershed class, you
    can supply its constructor with any parameter that is recognized by the
    parent Watershed class.  Shown below is a list of parameters that are
    specific to the ImageScanner class:

    max_number_of_blobs: The maximum number of blobs you would like the
                    module to examine in each subimage for detecting the
                    object of interest.

    max_area_threshold: If you have a rough sense of the number of pixels
                    an instance of the object you are trying to detect will
                    occupy, you can use this threshold to discard blobs
                    that are significantly larger.

    min_area_threshold: As with the previous parameter, if you have a rough
                    sense of the number of pixels an instance of the object
                    you are trying to detect will occupy, you can use this
                    parameter to discard blobs that are significantly
                    smaller.

    min_brightness_level: This is a useful parameter in order to experiment
                    with the suppression of noise induced false-alarm
                    detections.

    object_shape: This characterizes the shape of the objects you want to
                    detect.  The code shown in the module is for the
                    "circular" shape.  This is just to serve as an example
                    of how to use the module.  

    scanner_dump_directory: When scanning a large image with a scanning
                    window, the subimages produced at all positions of the
                    scanning window are dumped in the directory named by
                    this parameter.

    scanning_window_height: As should be obvious by its name, this
                    parameter specifies the height of the scanning window.

    scanning_window_width: As with the previous entry, this parameter
                    specifies the width of the scanning window.


@title
PUBLIC METHODS OF THE ImageScanner CLASS:

    (1) analyze_scanner_dump():

        The purpose of this method is to analyze ALL images in the scanner
        dump directory, generate the object detection results from each
        subimage in the directory, and, finally, display the locations of
        the detections collected from all the subimages in the original
        image.


    (2) analyze_scanner_dump_and_show_intermediate_results():

        Like the previous method, the purpose of this method is to analyze
        ALL images in the scanner dump directory, generate the object
        detection results from each subimage in the directory, and,
        finally, display the locations of the detections collected from all
        the subimages in the original image.  This method will also display
        the intermediate results obtained as the subimages are processed
        for object detections.  The intermediate results correspond to
        color filtering, binarizing, component labeling, etc.


    (3) analyze_single_subimage_from_image_scan():

        The algorithm development for detecting small objects in a large
        image is best carried out by working with just the subimages in
        which it is easier to see the objects.  This method does exactly
        that.  As you would expect, when invoking this method, your
        constructor call for the ImageScanner class must name the subimage
        you are interested in.


    (4) analyze_single_subimage_from_image_scan_and_show_intermediate_results():

        This method does the same thing as the previous method, except that
        it also shows you the intermediate results obtained from the named
        subimage.  The intermediate results correspond to color filtering,
        binarizing, component labeling, etc.


    (5) scan_image_for_detections_interactive():

        Before you can use the functionality of the ImageScanner class for
        anything useful, you must execute this method (or the method named
        next) in order to create a dump of the subimages extracted for the
        large input image.  This method is interactive in the sense that it
        shows you each subimage in its own popup window before depositing
        it in the dump directory.  Since it is much easier to see small
        objects in the subimages displayed in this manner, this mode of
        scanning a large image help you better understand the object
        detection problem you are dealing with.


    (6) scan_image_for_detections_noninteractive():

        This method does exactly the same thing as the previous method ---
        it creates a directory dump of the subimages extracted from the
        large input image.  It is faster because it is not interactive.
        That is, you are NOT shown the subimages before they are deposited
        in the dump directory.
       

@title 
THE Examples DIRECTORY:

    See the Examples directory in the distribution for the different ways
    in which you can use this module.  If you just want to play with
    dilate-erode methods of the module, execute the script

        dilate_erode.py

    This script assumes a disk structuring element whose radius and shape
    are supplied as the arguments to the methods `dilate(radius,shape)' and
    `erode(radius,shape)'.  To demonstrate the usefulness of these
    operations for "repairing" breaks in edges, execute the script

        edge_repair.py

    If you want to play with the distance mapping code in the module,
    execute the script:
    
        distance_mapping.py

    This script will ask you to place a mark with a mouse click in one of
    the blobs in your binary image.  Subsequently, it will display a
    distance map of the blob with respect to that mark.  For a
    demonstration that involves more complex blobs --- these being blobs
    with holes in them --- execute the script

        distance_mapping2.py

    For a demonstration of the calculation of the influence zones (IZ) in a
    binary blob, execute the script

        influence_zones.py

    For a visually interesting demonstration of IZ calculation, you must
    place at least two marks inside a blob.  Each mark is dilated into its
    IZ and the boundaries between the IZs constitute the geodesic skeleton
    of the binary blob with respect to the marks placed in the blob.

    All of the scripts mentioned above run on binary image files.  As a
    first demonstration involving grayscale or color images, execute the
    script

        LoG.py

    that calculates the Laplacian-of-Gaussian of an image.  The LoG is
    calculated by taking a difference of two Gaussian-smoothed images with
    two different values of sigma.  The first Gaussian smoothed image is
    calculated with the sigma as set in the constructor and the second with
    a sigma that is 20% larger.

    To see an automatic watershed segmentation that does NOT involve any
    user interaction, execute the script:

        segment_automatic_and_show_watershed.py

    As you will notice, when there is no help from the user, the watershed
    algorithm over-segments the image.  For an example of the segmentation
    produced by this script, for the following image

        orchid0001.jpg

    of an orchid, the script produced the segmentation shown in

        automatic_output_segmentation_for_orchid.jpg

    To see the individual blobs extracted from your input image through the
    watershed contours, execute the following script:

        segment_automatic_and_use_contours_to_extract_blobs.py

    This script finds the blobs by using the logic that a pixel belongs to
    the region bounded by a contour if a line through the pixel intersects
    the contour an even number of times. For a totally different approach
    to blob extraction, you may wish to try the script:

        segment_automatic_and_use_region_growing_to_extract_blobs.py

    This script uses region-growing logic to pull out the individual blobs.

    That brings us to marker based watershed segmentation in which a user
    is asked to place marker points in an image in order to manually modify
    the gradient map. To see how this works, execute the script:

        segment_with_markers_and_show_watershed.py

    In order to interact with the module for this segmentation exercise,
    pay careful attention to the titles of the image frames that are
    displayed.  When it asks you to click on the "save" and then "exit"
    buttons that appear at the bottom of the image window, you must do
    exactly do that (as opposed to just closing the window).  To see
    all the markers I placed in the image in one of my own attempts at
    segmenting the orchid image, view the image file:

       composite_image_with_all_marks_orchid.jpg

    The watersheds produced by this marker-assisted segmentation can be
    seen in the output image:

       marker_assisted_segmentation_for_orchid.jpg

    To see the individual blobs extracted for the case of marker-based
    watershed segmentation, execute the following script:

        segment_with_markers_and_use_contours_to_extract_blobs.py

    As for the "automatic" version of this script, this script finds the
    blobs by using the logic that a pixel belongs to the region bounded by
    a contour if a line through the pixel intersects the contour an even
    number of times. For a totally different approach to blob extraction,
    you may wish to try the script:

        segment_with_markers_and_use_region_growing_to_extract_blobs.py

    This script uses region-growing logic to pull out the individual blobs.

    The script in the Examples directory:

        extract_image_portion_and_apply_color_filter_demo.py

    illustrates the methods you can invoke to specify just a portion of the
    image that should be subject to watershed segmentation.  There are two
    different methods that you can call on in order to specify the image
    portion that you want segmented: (1) You can click at a point and then
    drag the mouse to define a rectangular portion of the image; (2) You
    can specify any polygonal shaped area by clicking the mouse at the
    vertices of the polygon you have in mind.

    The script named above also illustrates how to apply a color filter to
    an image before it is subject to watershed segmentation. The module
    gives you two different methods for applying a color filter: You can
    apply a filter to the HSV representation of the color, or its RGB
    representation.  

    Two additional scripts in the Examples directory that you may find
    useful are:

        hist_equalize_demo.py

        otsu_threshold_hue_demo.py

    The first of these illustrates histogram equalization applied to the
    'v' component to the HSV representation of a color image.  If the image
    to which you want to apply watershed segmentation is generally too dark
    or generally too bright, you might consider first histogram equalizing
    it before subjecting it to segmentation.  The second script,
    'otsu_threshold_hue_demo.py' illustrates the power of hue filtering.
    There exist problem domains where a simple hue filter can give you
    useful foreground/background separation.

    Finally, if you want to create your own binary images for some of the
    scripts mentioned above, execute the script

        data_gen.py

    Do not forget to execute the script

        cleanup.py

    in the Examples directory after running the scripts mentioned above to
    cleanup the intermediate images created by the scripts.  Ordinarily,
    the destructor of the class would take care of such cleanup.  But
    depending on how you exit the module, that may not always happen.


@title
The ExamplesImageScanner Directory:

    This directory contains the following scripts:


    1)  RunImageScanner.py

       Given a new camera image in which you want to detect small objects,
       the first thing you must do is to run this script (or the next
       script) to divide the large image into smaller subimages.

       This scripts deposits all the subimages in a directory whose
       pathname you specify in the call to the ImageScanner constructor.

       This script is non-interactive --- in the sense that it does not let
       you visually examine each subimage before it is written out to the
       dump directory.


    2)  RunImageScannerInteractive.py

       This is the interactive version of the previous script.  Before a
       subimage is written out to the dump directory, you can examine it
       visually for as long as you want in order to "understand" your data
       for the presence or the absence of small objects.

       Note that we are talking about objects that may be so small that
       they may not be clearly visible in the original image if shown in
       the small screen of a typical laptop.

       It is easier to such objects in the subimages since they are shown
       at a scale that is much larger than how they appear in the overall
       original image.


    3)  AnalyzeSingleSubimage.py

       After you have created a scanner dump directory of subimages using
       either of the previous two scripts, you can call this script to
       debug your object detection logic on a single subimage from that
       directory.

       The object detection results produced from the specified subimage
       are shown in the original image to give you a good sense of where in
       the original image you are looking and what the object detections
       look like there.


    4)  AnalyzeSingleSubimageShowIntermediateResults.py 

       This script does the same thing as the previous script, except that
       it also shows the intermediate results in the processing of the
       designated subimages.  These intermediate results include the
       outputs produced by color filtering, by binarizing the data, by the
       connected components algorithm, etc.
           

    5)  AnalyzeScannerDump.py

       Assuming you have perfected your object detection logic, after you
       have created a subimage dump directory with either of the first two
       scripts mentioned above, you can call this script to process ALL of
       the subimages in the dump directory for object detection.


    6)  AnalyzeScannerDumpShowIntermediateResults.py
          
       This does the same thing as the previous script, except that it also
       shows you the intermediate results as each subimage is processed.
       These intermediate results include the outputs produced by color
       filtering, by binarizing the data, by the connected components
       algorithm, etc.
           

@title
CAVEATS:

    As mentioned earlier, this module is NOT meant for production work ---
    meaning situations where the primary goal is just to get good-quality
    segmentations quickly based solely on user-supplied seeds.  For that
    type of work, you should use the OpenCV implementation.  Being pure
    Python, this module is slow compared to the OpenCV implementation.
    However, in my opinion, this module makes it easier to experiment with
    different approaches for implementing the various steps that go into
    the BLM algorithm for a watershed based segmentation of images.


@title
BUGS:

    Please notify the author if you encounter any bugs.  When sending
    email, please place the string 'Watershed' in the subject line to get
    past the author's spam filter.


@title
ACKNOWLEDGMENTS:

    I wrote the code for the ImageScanner class (added to the Watershed
    module in Version 2.2.0) as a part of my collaboration with Dr. Peter
    Hirst, Professor of Horticulture, Purdue University.  We are interested
    in predicting the yield of apple trees by estimating the number of
    fruitlets on the trees in early spring.  Peter is also the source of
    the image DSC00780.JPG that you will find in the ExamplesImageScanner
    directory.


@title
ABOUT THE AUTHOR:

    The author, Avinash Kak, recently finished a 17-year long "Objects
    Trilogy Project" with the publication of the book "Designing with
    Objects" by John-Wiley. If interested, visit his web page at Purdue to
    find out what this project was all about. You might like "Designing
    with Objects" especially if you enjoyed reading Harry Potter as a kid
    (or, as an adult, for that matter).

    For all issues related to this module, contact the author at
    kak@purdue.edu

    If you send email, please place the string "Watershed" in your
    subject line to get past the author's spam filter.

@title
COPYRIGHT:

    Python Software Foundation License

    Copyright 2017 Avinash Kak

@endofdocs
'''

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

#___________________________________  Utility functions  ____________________________________


def _coalesce(lists, result_sets):
    '''
    This function is used by the connected-components labeling algorithm of the
    module.  Connected-components labeling of pixels in a binary image is usually
    carried out by raster scanning the image and assigning new labels to isolated
    pixels first encountered. Subsequently, such labels are propagated to pixels
    whose neighbors were previously assigned new or propagated labels.  When two
    pixels with two different previously assigned labels are discovered to be each
    other's 8-neighbors, we record the equivalence of those labels in a list.
    Ultimately, this list must be resolved to discover the truly unique labels.  This
    function resolves such equivalence lists.
    '''
    if len(lists) == 0:
        return result_sets
    if len(result_sets) == 0:
        result_sets.append( set(lists[0]) )
        return _coalesce(lists[1:], result_sets )
    for eachlist in lists:
        (a,b) = eachlist
        for newset in result_sets:
            if a in newset:
                for checkset in result_sets:                
                    if b in checkset:
                        newset.update(checkset)
                        if checkset != newset:
                            result_sets.remove(checkset)
                        _coalesce( lists[1:], result_sets )
                        return result_sets            
                newset.add(b)
                _coalesce( lists[1:], result_sets )
                return result_sets            
            elif b in newset:
                for checkset in result_sets:                
                    if a in checkset:
                        newset.update(checkset)
                        if checkset != newset:
                            result_sets.remove(checkset)
                        _coalesce( lists[1:], result_sets )
                        return result_sets            
                newset.add(a)
                _coalesce( lists[1:], result_sets )
                return result_sets
        result_sets.append(set(eachlist))
        _coalesce( lists[1:], result_sets )
        return result_sets

def _display_portion_of_array(array, blob_center=0, blob_diameter=0):
    '''
    This is a convenience function that is very useful for visualizing
    the watershed in a portion of the array used for a given Z level.
    '''
    height,width = array.shape
    if blob_center == 0 and blob_diameter == 0:
        imin = 0
        imax = height
        jmin = 0
        jmax = width
    else:
        imin = int(blob_center[0]) - int(blob_diameter/2.0)
        imax = int(blob_center[0]) + int(blob_diameter/2.0) + 1
        jmin = int(blob_center[1]) - int(blob_diameter/2.0)
        jmax = int(blob_center[1]) + int(blob_diameter/2.0) + 1
    for i in range(imin, imax):
        lineoutput = ""
        for j in range(jmin, jmax):        
            if array[(i,j)] < 0:
                lineoutput += "  X"
            elif array[(i,j)] >= 0 and array[(i,j)] < 10:
                lineoutput += "  " + str(array[(i,j)])
            elif array[(i,j)] >= 10 and array[(i,j)] < 99:
                lineoutput += " " + str(array[(i,j)])
            else:
                lineoutput += str(array[(i,j)])
        print(lineoutput)
    print("\n\n")

def _display_portion_of_array_binary(array, blob_center, blob_diameter):
    '''
    This is a convenience function for the visualization of distance
    transformations of small binary patterns.
    '''
    height,width = array.shape
    imin = int(blob_center[0]) - int(blob_diameter/2.0)
    imax = int(blob_center[0]) + int(blob_diameter/2.0) + 1
    jmin = int(blob_center[1]) - int(blob_diameter/2.0)
    jmax = int(blob_center[1]) + int(blob_diameter/2.0) + 1
    for i in range(imin, imax):
        lineoutput = ""
        for j in range(jmin, jmax):        
            if array[(i,j)] < 10:
                lineoutput += " " + str(array[(i,j)])
            else:
                lineoutput += str(array[(i,j)])
        print(lineoutput)
    print("\n\n")

def _gaussian(sigma):
    '''
    A 1-D Gaussian smoothing operator is generated by assuming that the pixel
    sampling interval is a unit distance.  We truncate the operator a 3 times the
    value of sigma.  So when sigma is set to 1, you get a 7-element operator.  On the
    other hand, when sigma is set to 2, you get a 13-element operator, and so on.
    '''
    win_half_width = int(3 * sigma)
    xvals = range(-win_half_width, win_half_width+1)
    gauss = lambda x: math.exp(-((x**2)/(2*float(sigma**2))))
    operator = [gauss(x) for x in xvals]
    summed = functools.reduce( lambda x, y: x+y, operator )
    operator = [x/summed for x in operator]
    return operator

def _convolution_1D(input_array, operator):
    '''
    Since the Gaussian kernel is separable in its x and y dependencies, 2D convolution
    of an image with the kernel can be decomposed into a sequence of 1D convolutions
    first with the rows of the image and then another sequence of 1D convolutions
    with the columns of the output from the first.  This function carries out a 1D
    convolution.
    '''
    height,width = input_array.shape
    result_array = numpy.zeros((height, width), dtype="float")
    w = len(operator)                   # should be an odd number
    op_half_width = int((w-1)/2)
    for i in range(height):
        for j in range(width):
            accumulated = 0.0
            for k in range(-op_half_width,op_half_width+1):
                if (j+k) >= 0 and (j+k) < width:
                    accumulated += input_array[i,(j+k)] * operator[k + op_half_width]
            result_array[(i,j)] = accumulated
    return result_array

def _convolution_2D(input_array, operator):
    '''
    Since the Gaussian kernel is separable in its x and y dependencies, 2D convolution
    of an image with the kernel can be decomposed into a sequence of 1D convolutions
    first with the rows of the image and then another sequence of 1D convolutions
    with the columns of the output from the first.  This function orchestrates the
    invocation of 1D convolutions.
    '''
    result_conv_along_x = _convolution_1D(input_array, operator)
    result_conv_along_y = _convolution_1D(result_conv_along_x.transpose(), operator)
    final_result = result_conv_along_y.transpose()
    return final_result

def _line_intersection(line1, line2):
    '''
    Each line is defined by a 4-tuple, with its first two elements defining the
    coordinates of the first endpoint and the two elements defining the coordinates
    of the second endpoint.  This function defines a predicate that tells us whether
    or not two given line segments intersect.
    '''
    line1_endpoint1_x = line1[0] 
    line1_endpoint1_y = line1[1] 
    line1_endpoint2_x = line1[2] 
    line1_endpoint2_y = line1[3] 
    line2_endpoint1_x = line2[0] + 0.5
    line2_endpoint1_y = line2[1] + 0.5    
    line2_endpoint2_x = line2[2] + 0.5
    line2_endpoint2_y = line2[3] + 0.5
    if max([line1_endpoint1_x,line1_endpoint2_x]) <= min([line2_endpoint1_x,line2_endpoint2_x]):
        return 0
    elif max([line1_endpoint1_y,line1_endpoint2_y]) <= min([line2_endpoint1_y,line2_endpoint2_y]):
        return 0
    elif max([line2_endpoint1_x,line2_endpoint2_x]) <= min([line1_endpoint1_x,line1_endpoint2_x]):
        return 0
    elif max([line2_endpoint1_y,line2_endpoint2_y]) <= min([line1_endpoint1_y,line1_endpoint2_y]):
        return 0
    # Use homogeneous representation of lines:
    hom_rep_line1 = _cross_product((line1_endpoint1_x,line1_endpoint1_y,1),(line1_endpoint2_x,line1_endpoint2_y,1))
    hom_rep_line2 = _cross_product((line2_endpoint1_x,line2_endpoint1_y,1),(line2_endpoint2_x,line2_endpoint2_y,1))
    hom_intersection = _cross_product(hom_rep_line1, hom_rep_line2)
    if hom_intersection[2] == 0:
        return 0
    intersection_x = hom_intersection[0] / (hom_intersection[2] * 1.0)
    intersection_y = hom_intersection[1] / (hom_intersection[2] * 1.0)
    if intersection_x >= line1_endpoint1_x and intersection_x <= line1_endpoint2_x and intersection_y >= line1_endpoint1_y and intersection_y <= line1_endpoint2_y:
        return 1
    return 0

def _cross_product(vector1, vector2):
    '''
    Returns the vector cross product of two triples
    '''
    (a1,b1,c1) = vector1
    (a2,b2,c2) = vector2
    p1 = b1*c2 - b2*c1
    p2 = a2*c1 - a1*c2
    p3 = a1*b2 - a2*b1 
    return (p1,p2,p3)

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


#______________________________  Watershed Class Definition  ________________________________

class Watershed(object):

    # Class variables:
    region_mark_coords = {} 
    drawEnable = startX = startY = 0
    canvas = None

    def __init__(self, *args, **kwargs ):
        if args:
            raise ValueError(  
                   '''Watershed constructor can only be called with keyword arguments for 
                      the following keywords: data_image, binary_or_gray_or_color,
                      gradient_threshold_as_fraction, level_decimation_factor, padding,
                      size_for_calculations, max_gradient_to_be_reached_as_fraction, 
                      color_filter, sigma, and debug''')   
        data_image = sigma = size_for_calculations = padding = color_filter = None
        level_decimation_factor = gradient_threshold_as_fraction = debug = None
        max_gradient_to_be_reached_as_fraction = binary_or_gray_or_color = None
        if 'data_image' in kwargs                :   data_image = kwargs.pop('data_image')
        if 'sigma' in kwargs                     :   sigma = kwargs.pop('sigma')
        if 'padding' in kwargs                   :   padding = kwargs.pop('padding')
        if 'color_filter' in kwargs              :   color_filter = kwargs.pop('color_filter')
        if 'size_for_calculations' in kwargs     :   size_for_calculations = kwargs.pop('size_for_calculations')
        if 'binary_or_gray_or_color' in kwargs   :   binary_or_gray_or_color = kwargs.pop('binary_or_gray_or_color')
        if 'level_decimation_factor' in kwargs   :   level_decimation_factor = kwargs.pop('level_decimation_factor')
        if 'debug' in kwargs                     :   debug = kwargs.pop('debug') 
        if 'gradient_threshold_as_fraction' in kwargs   :   \
                                       gradient_threshold_as_fraction=kwargs.pop('gradient_threshold_as_fraction')
        if 'max_gradient_to_be_reached_as_fraction' in kwargs  :  \
              max_gradient_to_be_reached_as_fraction = kwargs.pop('max_gradient_to_be_reached_as_fraction')
        if len(kwargs) != 0:
                     raise ValueError('''You have provided unrecognizable keyword args''')
        if data_image: 
            self.data_im_name = data_image
            self.data_im =  Image.open(data_image)
            self.original_im = Image.open(data_image)
        else:
            raise ValueError('''You must specify a data image''')
        if binary_or_gray_or_color:
            if binary_or_gray_or_color not in ['binary','gray','color']:
                raise ValueError('''You must specify either "binary" or "gray" or "color" '''
                                 '''for your input image''')  
            self.binary_or_gray_or_color = binary_or_gray_or_color
        else:
            raise ValueError('''You must specify either "binary" or "gray" or "color" '''
                             '''for your input image''')
        if sigma:
            self.sigma = sigma
        else:
            self.sigma = 1
        if padding:
            self.padding = padding
        else:
            self.padding = 0
        if color_filter:
            self.color_filter = color_filter
        if size_for_calculations:
            self.size_for_calculations = size_for_calculations
        else:
            self.size_for_calculations = 128
        if level_decimation_factor:
            self.level_decimation_factor = level_decimation_factor
        else:
            self.level_decimation = 1       
        if gradient_threshold_as_fraction:
            self.gradient_threshold_as_fraction = gradient_threshold_as_fraction
        else:
            self.gradient_threshold_as_fraction = 0.1
        if max_gradient_to_be_reached_as_fraction:
            self.max_gradient_to_be_reached_as_fraction = max_gradient_to_be_reached_as_fraction
        else:
            self.max_gradient_to_be_reached_as_fraction = 1
        self.display_size = ()                 # Set to a tuple of two values, first val for width and the second for height
        self.componentID_array = None          # This numpy 2D array holds labels for the different components in a binary
                                               #          image.  This is initialized by a call to connected_components()
        self.markID_data_array = None          # This numpy 2D array holds the labels for the different markers in all of 
                                               #          the blobs in an image.
        self.marker_image_data = None          # A numpy array of size the same as the original image that holds all the
                                               #          marks
        self.blob_dictionary = {}              # The keys are integers and the values are the corresponding blobs in the
                                               #          data image, each a numpy array of the same size as image
        self.marks_dictionary = {}             # The keys are integers and the values are the corresponding mark pixels
                                               #          as numpy arrays
        self.blob_dia_dict = {}                # Upperbound on diameters of all blobs
        self.blob_center_dict = {}             # Rough estimate of the center of a blob
        self.marks_to_blobs_mapping_dict = {}  # Shows which image blob goes with each mark
        self.blobs_to_marks_mapping_dict = {}  # Shows which marks belong to each image blob. Note that that the value for a
                                               #          key is now a list if blobs
        self.number_of_components = None       # This is the number of connected blobs in a binary image
        self.number_of_marks = None            # This is the number of marks created by a user
        self.gray_image  = None                # Stores the gray image as an Image object
        self.gray_image_as_array = None        # Stores the gray image as a numpy array
        self.gradient_image_as_array = None    # Stores gradient image as a numpy array
        self.max_number_of_levels_in_gradient =  None  # self explanatory
        self.max_grad_level = None             # Max int value of normalized gradient
        self.min_grad_level = None             # Min int value of normalized gradient

        self.Z_levels_dict = {}                # A key is a gradient level and value the set where gradient values are equal
                                               #          to or less than the key 
        self.blob_dictionary_by_level_for_Z = {}  # A key in this dict represents a specific gradient level. And the 
                                                  #       corresponding value is a dict that serves as the blob 
                                                  #       dictionary for just that level
        self.level_vs_number_of_components = {}
        self.start_label_for_labeling_blobs_vs_level = {}
        self.label_pool_at_level = {}
        self.component_labels = None
        self.componentID_array_dict = {} # Each key is a gradient level and the corresponding value the componentID array
                                         #       for that level. In a componentID array, each blob carries a distinct 
                                         #       integer label.
        self.watershed_contours = []     # This is a list of lists.  Each inner list is a watershed contour as extracted 
                                         #       by the watershed contour extractor.
        self.marks_scale = ()            # A pair of numbers. The first element is for the horizontal direction and the 
                                         #       second for the vertical
        self.region_marks_centers = {}   # Each key is region index and the corresponding value a list of tuples, with 
                                         #       each tuple the coordinates of the mark centers in that region.
        self.marked_valley_for_region={} # These are new valleys injected by the user with the help of marks.
        self.segmented_regions_as_arrays = []
        self.segmented_regions_as_images = []
        if debug:                             
            self.debug = debug
        else:
            self.debug = 0

    def apply_color_filter_rgb(self):
        if self.color_filter is None:
            sys.exit(" 'apply_color_filter()' called without specifying color filter in the constructor --- aborting")
        rf,gf,bf = self.color_filter
        width,height = self.original_im.size
        new_image = Image.new("RGB", (width,height), (0,0,0))
        if any(isinstance(x, (tuple)) for x in (rf,gf,bf)):
            if not all(isinstance(x, (tuple)) for x in (rf,gf,bf)):
                sys.exit("Cannot mix tuples and scalars in filter specification --- aborting")
            for x in range(0, width):        
                for y in range(0, height):
                    r,g,b = self.original_im.getpixel((x,y))
                    if ((rf[0] <= r <= rf[1]) and (gf[0] <= g <= gf[1]) and (bf[0] <= b <= bf[1])):
                        new_image.putpixel((x,y), (r,g,b))
        else:
            assert any(0 <= x <= 1 for x in [rf,gf,bf]), "when using a triple of scalars, the filter's three components must be between 0 and 1 --- aborting"
            for x in range(0, width):        
                for y in range(0, height):
                    r,g,b = self.original_im.getpixel((x,y))
                    new_image.putpixel((x,y), (int(r*rf),int(g*gf),int(b*bf)))
        self.displayImage6(new_image, "rgb_filtered_image -- close window when done viewing")
        self.data_im = self.original_im = new_image

    def apply_color_filter_hsv(self):
        self.displayImage6(self.original_im, "%s -- close window when done viewing" % self.data_im_name)
        if self.color_filter is None:
            sys.exit(" 'apply_color_filter()' called without specifying color filter in the constructor --- aborting")
        hf,sf,vf = self.color_filter
        hsv_image = self.original_im.copy().convert("HSV")
        width,height = self.original_im.size
        hsv_new_image = Image.new("HSV", (width,height), (0,0,0))
        if any(isinstance(x, (tuple)) for x in (hf,sf,vf)):
            if not all(isinstance(x, (tuple)) for x in (hf,sf,vf)):
                sys.exit("Cannot mix tuples and scalars in filter specification --- aborting")
            for x in range(0, width):        
                for y in range(0, height):
                    h,s,v = hsv_image.getpixel((x,y))
                    if ((hf[0] <= h <= hf[1]) and (sf[0] <= s <= sf[1]) and (vf[0] <= v <= vf[1])):
                        hsv_new_image.putpixel((x,y), (h,s,v))
        else:
            assert any(0 <= x <= 1 for x in [hf,sf,vf]), "when using a triple of scalars, the filter's three components must be between 0 and 1 --- aborting"
            for x in range(0, width):        
                for y in range(0, height):
                    h,s,v = hsv_image.getpixel((x,y))
                    hsv_new_image.putpixel((x,y), (int(h*hf),int(s*sf),int(v*vf)))
        new_image = hsv_new_image.convert("RGB")
        self.displayImage6(new_image, "hsv_filtered_image -- close window when done viewing")
        self.data_im = self.original_im = new_image
        return new_image

    def apply_color_filter_hsv_to_named_image_file(self, filename, show_intermediate_results = True):
        named_image = Image.open(filename)
        hf,sf,vf = self.color_filter
        hsv_image = named_image.copy().convert("HSV")
        width,height = named_image.size
        hsv_new_image = Image.new("HSV", (width,height), (0,0,0))
        if any(isinstance(x, (tuple)) for x in (hf,sf,vf)):
            if not all(isinstance(x, (tuple)) for x in (hf,sf,vf)):
                sys.exit("Cannot mix tuples and scalars in filter specification --- aborting")
            for x in range(0, width):        
                for y in range(0, height):
                    h,s,v = hsv_image.getpixel((x,y))
                    if ((hf[0] <= h <= hf[1]) and (sf[0] <= s <= sf[1]) and (vf[0] <= v <= vf[1])):
                        hsv_new_image.putpixel((x,y), (h,s,v))
        else:
            assert any(0 <= x <= 1 for x in [hf,sf,vf]), "when using a triple of scalars, the filter's three components must be between 0 and 1 --- aborting"
            for x in range(0, width):        
                for y in range(0, height):
                    h,s,v = hsv_image.getpixel((x,y))
                    hsv_new_image.putpixel((x,y), (int(h*hf),int(s*sf),int(v*vf)))
        filtered_image = hsv_new_image.convert("RGB")
        if show_intermediate_results:
            self.displayImage6(filtered_image, "hsv_filtered_image -- close window when done viewing")
        return filtered_image

    def connected_components_of_filtered_output(self, argimage, min_brightness_level, min_area_threshold, max_area_threshold, expected_number_of_blobs, blob_shape, show_intermediate_results = True):
        width,height = argimage.size
        mask_size = (height,width) 
        mask_array = numpy.zeros(mask_size, dtype="int")
        for i in range(0, mask_size[0]):
            for j in range(0, mask_size[1]):
                if numpy.linalg.norm(argimage.getpixel((j,i))) > min_brightness_level:
                    mask_array[(i,j)] = 1
        mask_image = Image.new("1", (width,height), 0)
        for i in range(0, height):
            for j in range(0, width):
                if mask_array[(i,j)] == 1:
                    mask_image.putpixel((j,i), 255)
        if show_intermediate_results:
            self.displayImage3(mask_image, "binary mask constructed for filtered image")
        if self.debug:
            for i in range(0, height):
                sys.stdout.write("\n")
                for j in range(0, width):
                    if mask_array[(i,j)] == 1:
                        sys.stdout.write('1')
                    else:
                        sys.stdout.write('0')
            sys.stdout.write('\n\n')        
        self._connected_components_for_binary_array_using_dict_pointers(mask_array, min_area_threshold, max_area_threshold)
        if self.debug:
            print("\n\nblob dictionary prior to shape filtering: ")
            for blob_index in self.blob_dictionary:
                print("%s  ===> %s" % (str(blob_index), str( self.blob_dictionary[blob_index] )))
        colors = {}        
        colorized_mask_image = Image.new("RGB", (width,height), (0,0,0))
        how_many_largest_blobs_to_include, blobs_included = expected_number_of_blobs, 0
        for blob_index in sorted(self.blob_dictionary, key=lambda x: len(self.blob_dictionary[x]), reverse=True):
            if blob_index not in colors:
                colors[blob_index] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
            for (i,j) in self.blob_dictionary[blob_index]:
                colorized_mask_image.putpixel((j,i), colors[blob_index])
            blobs_included += 1
            if blobs_included == how_many_largest_blobs_to_include: break
        if show_intermediate_results:
            self.displayImage3(colorized_mask_image, "prior to shape filtering: binary mask for retained blobs")
        colorized_mask_image.save("colorized_component_labeled.jpg")
        new_mask_image = Image.new("1", (width,height), 0)
        how_many_largest_blobs_to_include, blobs_included = expected_number_of_blobs, 0
        mean_positions_for_detected_shapes = []
        for blob_index in sorted(self.blob_dictionary, key=lambda x: len(self.blob_dictionary[x]), reverse=True):
            if self.debug:      
                print("%s  ===> %s" % (str(blob_index), str( self.blob_dictionary[blob_index] )))
            if blob_shape == "circular":
                test_circular = self.is_blob_circular(self.blob_dictionary[blob_index])
                if test_circular:
                    print("\nblob at index %d was found to be circular" % blob_index)
                    for (i,j) in self.blob_dictionary[blob_index]:
                        new_mask_image.putpixel((j,i), 255)
                    mean_positions_for_detected_shapes.append(test_circular[0])
            else:
                print("\nWARNING: No shape filter applied since none available for %s" % blob_shape)
                for (i,j) in self.blob_dictionary[blob_index]:
                    new_mask_image.putpixel((j,i), 255)
            blobs_included += 1
            if blobs_included == how_many_largest_blobs_to_include: break
        if show_intermediate_results:
            self.displayImage6(new_mask_image, "binary mask for final retained blobs")
        return mean_positions_for_detected_shapes

    def is_blob_circular(self, list_of_pixel_coords):
        '''
        Tests the circularity predicate by taking the ratio of the area of the blob, as measured by the number
        of pixels in the blob, to \pi*r^2 where r is its average radius.  This is obviously much too simple a
        predicate at this time.  However, you can add to its power by incorporating additional logic here.
        '''
        mean_point = [0.0,0.0]
        for (i,j) in list_of_pixel_coords:
            mean_point[0] += j
            mean_point[1] += i
        mean_point = list(map(lambda x: 1.0 * x / len(list_of_pixel_coords), mean_point))
        print("\nmean point: %s" % str(mean_point))
        sum_radius_squared = 0.0
        for (i,j) in list_of_pixel_coords:
            sum_radius_squared += (j - mean_point[0])**2 + (i - mean_point[1])**2
        mean_rad = math.sqrt( 1.0 * sum_radius_squared / len(list_of_pixel_coords)  )
        print("mean radius: %f" % mean_rad)
        expected_area = math.pi * (mean_rad ** 2)
        print("expected_area: %f" % expected_area)
        print("actual area:  %d" % len(list_of_pixel_coords))
        circularity_index = expected_area / len(list_of_pixel_coords)
        mean_point = list(map(lambda x: int(x), mean_point))
        if ((circularity_index < 1.0) and (mean_rad) > 20) or ((circularity_index < 1.0) and (8 < mean_rad < 15)):
            return (mean_point, mean_rad)
        else:
            return False
    
    def extract_data_pixels(self):
        '''
        Gets the binary, grayscale, and color images ready for watershed processing.
        If the images are too large, they are reduced to the size set by the
        constructor.  Color images are converted into grayscale images.
        '''
        if self.binary_or_gray_or_color == 'color':
            if self.padding > 0:
                width,height = self.original_im.size
                padded_im = Image.new('RGB', (width+self.padding,height+self.padding), color=(0,0,0))
                for x in range(self.padding, width):
                    for y in range(self.padding, height):
                        padded_im.putpixel((x,y), self.original_im.getpixel((x-self.padding,y-self.padding)))
                if self.debug:
                    self.displayImage3(padded_im)
                self.original_im = padded_im.copy()
                self.data_im =  padded_im.copy()
            size_for_calculations = self.size_for_calculations
            im = self.data_im.convert("L")
            width,height = im.size            
            scaling = 1.0
            newwidth,newheight = width,height
            if width > height:
                if width > size_for_calculations:
                    scaling = (size_for_calculations * 1.0) / width
                    newwidth,newheight = int(newwidth * scaling),int(newheight * scaling)
            elif height > width:
                if height > size_for_calculations:
                    scaling = (size_for_calculations * 1.0) / height
                    newwidth,newheight = int(newwidth * scaling),int(newheight * scaling)
            im = im.resize((newwidth,newheight), Image.ANTIALIAS)
            self.data_im = im
        elif self.binary_or_gray_or_color == 'gray':
            if self.padding > 0:
                width,height = self.original_im.size
                padded_im = Image.new('L', (width+self.padding,height+self.padding), color=0)
                for x in range(self.padding, width):
                    for y in range(self.padding, height):
                        padded_im.putpixel((x,y), self.original_im.getpixel((x-self.padding,y-self.padding)))
                if self.debug:
                    self.displayImage3(padded_im)
                self.original_im = padded_im.copy()
                self.data_im =  padded_im.copy()
            size_for_calculations = self.size_for_calculations
            im = self.data_im
            width,height = im.size            
            scaling = 1.0
            newwidth,newheight = width,height
            if width > height:
                if width > size_for_calculations:
                    scaling = (size_for_calculations * 1.0) / width
                    newwidth,newheight = int(newwidth * scaling),int(newheight * scaling)
            elif height > width:
                if height > size_for_calculations:
                    scaling = (size_for_calculations * 1.0) / height
                    newwidth,newheight = int(newwidth * scaling),int(newheight * scaling)
            im = im.resize((newwidth,newheight), Image.ANTIALIAS)
            self.data_im = im
        elif self.binary_or_gray_or_color == 'binary':
            # The "L" option, which stands for "luminance" first converts the image 
            # to gray (in case it was color) and then the "1" option converts into
            # a binary image:
            converted = self.data_im.convert("L").convert("1")
            self.data_im = self._return_binarized_image(converted)
        else:
            sys.exit("The image must be declared to be either binary, or gray, or color")

    def extract_image_region_interactively_by_dragging_mouse(self):
        '''
        This is one method you can use to apply watershed segmentation to just a portion of your image.
        This method extract the portion you want.  You click at the upper left corner of the rectangular
        portion of the image you are interested in and you then drag the mouse pointer to the lower 
        right corner.  Make sure that you click on "save" and "exit" after you have delineated the area.
        '''
        global delineator_image
        global delineator_polygon
        print("Drag the mouse pointer to delineate the portion of the image you want to extract:")
        Watershed.image_portion_delineation_coords = []
        mw = Tkinter.Tk() 
        mw.title("Click and then drag the mouse pointer --- THEN CLICK SAVE and EXIT")
        width,height = self.original_im.size
        delineator_image =  self.original_im.copy()
        extracted_image =  self.original_im.copy()
        self.extracted_image_portion_file_name = "image_portion_of_" + self.data_im_name
        mw.configure(height = height, width = width) 
        photo_image = ImageTk.PhotoImage(self.original_im)
        canvasM = Tkinter.Canvas( mw,   
                                  width = width,
                                  height =  height,
                                  cursor = "crosshair" )  
        canvasM.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                        command = lambda: Watershed.extracted_image.save(self.extracted_image_portion_file_name) 
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: mw.destroy()
                      ).pack( side = 'right' )  
        canvasM.bind("<ButtonPress-1>", lambda e: self._start_mouse_motion(e, delineator_image))
        canvasM.bind("<ButtonPress-1>", lambda e: self._start_mouse_motion(e, delineator_image))
        canvasM.bind("<ButtonRelease-1>", lambda e:self._stop_mouse_motion(e, delineator_image))
        canvasM.bind("<B1-Motion>", lambda e: self._on_mouse_motion(e, delineator_image))
        canvasM.create_image( 0,0, anchor=NW, image=photo_image)
        canvasM.pack(fill=BOTH, expand=1)
        mw.mainloop()       
        self.displayImage3(Watershed.extracted_image, "extracted image -- close window when done viewing")
        self.data_im = self.original_im = Watershed.extracted_image

    def extract_image_region_interactively_through_mouse_clicks(self):
        '''
        This method allows a user to use a sequence of mouse clicks in order to specify a region of the 
        input image that should be subject to watershed segmentation.  The mouse clicks taken together 
        define a polygon. The method encloses the polygonal region by a minimum bounding rectangle,
        which then becomes the new input image for the rest of processing.
        '''
        global delineator_image
        global delineator_coordinates
        print("Click mouse in a clockwise fashion to specify the portion you want to extract:")
        Watershed.image_portion_delineation_coords = []
        mw = Tkinter.Tk() 
        mw.title("Place mouse clicks clockwise --- THEN CLICK SAVE and EXIT")
        width,height = self.original_im.size
        delineator_image =  self.original_im.copy()
        Watershed.delineated_portion_file_name = "image_portion_of_" + self.data_im_name
        mw.configure(height = height, width = width) 
        photo_image = ImageTk.PhotoImage(self.original_im)
        canvasM = Tkinter.Canvas( mw,   
                                  width = width,
                                  height =  height,
                                  cursor = "crosshair" )  
        canvasM.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                         command = Watershed._extract_and_save_image_portion_polygonal
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: mw.destroy()
                      ).pack( side = 'right' )  
        canvasM.bind("<Button-1>", lambda e: self._image_portion_delineator(e, delineator_image))
        canvasM.create_image( 0,0, anchor=NW, image=photo_image)
        canvasM.pack(fill=BOTH, expand=1)
        mw.mainloop()       
        self.displayImage3(Watershed.extracted_image, "extracted image -- close window when done viewing")
        self.data_im = self.original_im = Watershed.extracted_image

    def extract_rectangular_masked_segment_of_image(self, horiz_start, horiz_end, vert_start, vert_end):
        '''
        Keep in mind the following convention used in the PIL's Image class: the first
        coordinate in the args supplied to the getpixel() and pupixel() methods is for
        the horizontal axis (the x-axis, if you will) and the second coordinate for the
        vertical axis (the y-axis).  On the other hand, in the args supplied to the
        array and matrix processing functions, the first coordinate is for the row
        index (meaning the vertical) and the second coordinate for the column index
        (meaning the horizontal).  In what follows, I use the index 'i' with its
        positive direction going down for the vertical coordinate and the index 'j'
        with its positive direction going to the right as the horizontal coordinate. 
        The origin is at the upper left corner of the image.
        '''
        masked_image = self.original_im.copy()
        width,height = masked_image.size 
        mask_array = numpy.zeros((height, width), dtype="float")
        for i in range(0, height):
            for j in range(0, width):
                if (vert_start < i < vert_end) and (horiz_start < j < horiz_end):
                    mask_array[(i,j)] = 1
        self._display_and_save_array_as_image( mask_array, "_mask__" )
        for i in range(0, height):
            for j in range(0, width):
                if mask_array[(i,j)] == 0:
                    masked_image.putpixel((j,i), (0,0,0)) 
        self.displayImage3(masked_image, "a segment of the image")

    def compute_gradient_image(self):
        '''
        The Watershed algorithm is applied to the gradient of the input image.  This
        method computes the gradient image.  The gradient calculation is carried out
        after the image is smoothed with a Gaussian kernel whose sigma is set in the
        constructor.
        '''
        gray_image = self.data_im
        width,height = gray_image.size 
        if self.debug:
            print("For the gray-level image:   width: %d    height: %d" % (width,height))
        sigma = self.sigma
        gray_image_as_array = numpy.zeros((height, width), dtype="float")
        for i in range(0, height):
            for j in range(0, width):
                gray_image_as_array[(i,j)] = gray_image.getpixel((j,i))
        self.gray_image_as_array = gray_image_as_array
        smoothing_op = _gaussian(sigma)
        smoothed_image_array = _convolution_2D(gray_image_as_array, smoothing_op)
        if self.debug:
            self._display_image_array_row(smoothed_image_array,32,"smoothed image array")
        gradient_image_array = numpy.zeros((height, width), dtype="float")
        for i in range(1, height):
            for j in range(1, width):
                x_partial = smoothed_image_array[(i,j)] - smoothed_image_array[(i,j-1)]
                y_partial = smoothed_image_array[(i,j)] - smoothed_image_array[(i-1,j)]
                magnitude = math.sqrt( x_partial**2 + y_partial**2 )
                gradient_image_array[(i,j)] = magnitude
        for j in range(1,width):
            gradient_image_array[(0,j)] = gradient_image_array[(1,j)]
        for i in range(1,height):
            gradient_image_array[(i,0)] = gradient_image_array[(i,1)]
        gradient_image_array[(0,0)] = ( gradient_image_array[(0,1)] + gradient_image_array[(1,0)] + gradient_image_array[(1,1)] ) / 3.0
        maxGradientVal = gradient_image_array.max()
        minGradientVal =gradient_image_array.min()
        normalized_grad_image_array = numpy.zeros((height, width), dtype="int")
        for i in range(height):
            for j in range(width):
                newval = int( (gradient_image_array[(i,j)] - minGradientVal) * (255/(maxGradientVal-minGradientVal)) )
                if newval < (255 * self.gradient_threshold_as_fraction):
                    newval = 0 
                normalized_grad_image_array[(i,j)] = newval
        gradient_image_array = normalized_grad_image_array
        self._display_and_save_array_as_image( gradient_image_array, "_gradient__" + str(sigma) )
        self.gradient_image_as_array = gradient_image_array
        maxValOfGradientMag = gradient_image_array.max()
        minValOfGradientMag = gradient_image_array.min() 
        self.max_number_of_levels_in_gradient =  maxValOfGradientMag +1
        self.min_grad_level = minValOfGradientMag 
        self.max_grad_level = int(maxValOfGradientMag * self.max_gradient_to_be_reached_as_fraction)

    def compute_LoG_image(self):
        '''
        This method computes the Laplacian-of-Gaussian (LoG) of an image. The LoG is 
        calculated as the difference of two Gaussian-smoothed versions of the input 
        image at two slightly difference scales.  The LoG itself is NOT used in 
        watershed calculations.
        '''
        sigma = self.sigma
        width,height = self.data_im.size
        gray_image = self.data_im
        gray_image_as_array = numpy.zeros((height, width), dtype="float")
        for i in range(0, height):
            for j in range(0, width):
                gray_image_as_array[(i,j)] = gray_image.getpixel((j,i))
        self.gray_image_as_array = gray_image_as_array
        smoothing_op1 = _gaussian(sigma)
        smoothing_op2 = _gaussian(sigma*1.20)
        smoothed_image_array1 = _convolution_2D(gray_image_as_array, smoothing_op1)
        smoothed_image_array2 = _convolution_2D(gray_image_as_array, smoothing_op2)
        diff_image_array = smoothed_image_array1 - smoothed_image_array2  # DoG
        self._display_and_save_array_as_image( diff_image_array, "_LoG__" + str(sigma) )

    def dilate(self, structuring_element_rad, structuring_ele_shape):
        '''
        This is to just demonstrate the basic idea of dilation of a binary pattern by
        a disk structuring element whose radius is supplied as the first
        argument. The precise shape of the structuring element, which can be either
        "square" or "circular", is supplied through the second argument. This method
        itself is NOT used in the watershed calculations.  For large binary patterns,
        it would be more efficient to carry out the dilations only at the border
        pixels.
        '''
        argimage = self.data_im
        (width,height) = argimage.size
        im_out =  Image.new("1", (width,height), 0)
        a = structuring_element_rad
        if structuring_ele_shape == "circular":
            pixels_to_be_considered = [(k,l) for k in range(-a,a+1) \
                                         for l in range(-a,a+1) if (k**2 + l**2) < a**2]  
        elif structuring_ele_shape == "square":
            pixels_to_be_considered = [(k,l) for k in range(-a,a+1) for l in range(-a,a+1)]
        for j in range(0,height):
            for i in range(0,width):
                if argimage.getpixel((i,j)) != 0:            
                    for pixel in pixels_to_be_considered:
                        if  0 <= j+pixel[1] < height and 0 <= i+pixel[0] < width:
                                im_out.putpixel((i+pixel[0],j+pixel[1]), 255) 
        im_out.save("dilation.jpg")
        self.displayImage3(im_out, "Dilated Pattern  (close window when done viewing)")
        return im_out

    def erode(self, argimage, structuring_element_rad, structuring_ele_shape):
        '''
        This is to just demonstrate the basic idea of erosion of a binary pattern by
        a disk structuring element whose radius is supplied as the first argument.
        The precise shape of the structuring element, which can be either "square" or
        "circular", is supplied through the second argument. This method itself is
        NOT used in the watershed calculations.
        '''
        (width,height) = argimage.size
        erosion_out =  Image.new("1", (width,height), 0)
        a = structuring_element_rad
        if structuring_ele_shape == "circular":
            pixels_to_be_considered = [(k,l) for k in range(-a,a+1) for l in range(-a,a+1) if (k**2 + l**2) < a**2]  
        elif structuring_ele_shape == "square":
            pixels_to_be_considered = [(k,l) for k in range(-a,a+1) for l in range(-a,a+1)]
        for j in range(0,height):
            for i in range(0,width):
                if argimage.getpixel((i,j)) ==255:            
                    image_pixels_at_struct_ele_offsets_all_okay = 1
                    for pixel in pixels_to_be_considered:
                        if  0 <= j+pixel[1] < height and 0 <= i+pixel[0] < width:
                            if argimage.getpixel((i+pixel[0],j+pixel[1])) != 255:  
                                image_pixels_at_struct_ele_offsets_all_okay = 0
                                break
                        if image_pixels_at_struct_ele_offsets_all_okay == 0:
                            break
                    if image_pixels_at_struct_ele_offsets_all_okay == 1:
                        erosion_out.putpixel((i,j), 255) 
                image_pixels_at_struct_ele_offsets_all_okay = 1
        erosion_out.save("erosion.jpg")
        self.displayImage3(erosion_out, "Pattern After Erosion  (close window when done viewing)")
        return erosion_out

    def dilate_mark_in_its_blob(self, mark_index):
        '''
        This method illustrates distance mapping of a blob in a binary image with
        respect to a mark created by clicking at a point within the blob.
        '''
        mark_region = self.marks_dictionary[mark_index]
        relevant_blob_index = self.marks_to_blobs_mapping_dict[mark_index]
        blob = self.blob_dictionary[relevant_blob_index]
        blob_center =  self.blob_center_dict[relevant_blob_index]
        blob_diameter = self.blob_dia_dict[relevant_blob_index]
        print("blob center is: ", blob_center)          # blob always refers to image
        print("blob diameter is: ", blob_diameter)
        print("\n\nImage blob selected by mark:\n")
        _display_portion_of_array_binary( blob, blob_center, blob_diameter )
        print("\n\nOriginal mark:\n")
        _display_portion_of_array_binary( mark_region, blob_center, blob_diameter )
        dilated_mark = \
                self._unit_dilation_of_marker_in_its_blob(mark_region, mark_index, 1)
        if dilated_mark != None:
            print("\n\nDilated mark for dilation of %d:\n" % (1))
            _display_portion_of_array_binary( dilated_mark, blob_center, blob_diameter )
            for i in range(2,40):
                dilated_mark = \
                    self._unit_dilation_of_marker_in_its_blob(dilated_mark, mark_index, i)
                if dilated_mark == None: 
                    print("\n\nMax number of dilations reached at distance %d" % int(i-1))
                    break
                print("\n\nDilated mark for dilation level of %d\n" % (i))
                _display_portion_of_array_binary( dilated_mark, blob_center, blob_diameter )

    def connected_components(self, data_or_marks): 
        '''
        This method is the basic connected components algorithm in the Watershed
        module.  Just for programming convenience related to the I/O from this
        method, I have made a distinction between carrying out a connected-components
        labeling of a binary image and doing the same for a binary pattern that
        contains all of the marks made by the user.
        '''
        if data_or_marks == "data":
            binaryImage = self.data_im
            print("Applying connected components algorithm to the binary pattern")
        elif data_or_marks == "marks":
            binaryImage = self.marker_image_data
            print("Applying connected components algorithm to the marks")
        else:
            sys.exit("Wrong argument supplied to connected_components method")
        equivalences = set()
        width,height = binaryImage.size
        componentID_array = numpy.zeros((height, width), dtype="int")
        markID_data_array = numpy.zeros((height, width), dtype="int")
        current_componentID = 1
        if binaryImage.getpixel((0,0)) ==255:            
            componentID_array[(0,0)] = current_componentID
            current_componentID += 1
        for i in range(1, width):
            if binaryImage.getpixel((i,0)) == 255:
                if componentID_array[(0,i-1)] != 0:
                    componentID_array[(0,i)] = componentID_array[(0,i-1)]
                else:
                    componentID_array[(0,i)] = current_componentID
                    current_componentID += 1
        for j in range(1, height):
            if binaryImage.getpixel((0,j)) == 255:
                if componentID_array[(j-1,0)] != 0:
                    componentID_array[(j,0)] = componentID_array[(j-1,0)]
                else:
                    componentID_array[(j,0)] = current_componentID
                    current_componentID += 1
        for j in range(1, height):
            for i in range(1, width):
                if componentID_array[(j,i-1)] != 0 and componentID_array[(j-1,i)] != 0: 
                    equivalences.add((componentID_array[(j,i-1)], componentID_array[(j-1,i)]))
                if binaryImage.getpixel((i,j)) == 255:            
                    if componentID_array[(j,i-1)] != 0:
                        componentID_array[(j,i)] = componentID_array[(j,i-1)]
                    elif componentID_array[(j-1,i-1)] != 0:
                        componentID_array[(j,i)] = componentID_array[(j-1,i-1)]
                    elif componentID_array[(j-1,i)] != 0:
                        componentID_array[(j,i)] = componentID_array[(j-1,i)]
                    else:
                        componentID_array[(j,i)] = current_componentID
                        current_componentID += 1
        if self.debug:
            print("equivalences: ", equivalences)
        equivalences_as_lists = []
        all_labels_in_equivalences = set()
        for item in equivalences:
            equivalences_as_lists.append(list(item))
            all_labels_in_equivalences  = all_labels_in_equivalences.union(set(item))
        labels_not_in_equivalences = set(range(1,current_componentID)).difference(all_labels_in_equivalences)
        propagated_equivalences = _coalesce(equivalences_as_lists, [] )
        if self.debug:
            print("propagated equivalences: ", propagated_equivalences)
        number_of_components = len( propagated_equivalences )
        if self.debug:
            print("number of components: ", number_of_components)
        if data_or_marks == "data":
            self.number_of_components = number_of_components
        elif data_or_marks == "marks":
            self.number_of_marks = number_of_components
        label_mappings = {}
        mapped_label = 1
        for equiv_list in propagated_equivalences:
            for label in equiv_list:
                label_mappings[label] = mapped_label   
            mapped_label += 1
        for not_yet_mapped_label in list(labels_not_in_equivalences):
            label_mappings[not_yet_mapped_label] = mapped_label       
            mapped_label += 1
        if self.debug:
            print(label_mappings)
        if data_or_marks == "data":
            for j in range(0, height):
                for i in range(0, width):
                    if componentID_array[(i,j)] != 0:
                        componentID_array[(i,j)] = label_mappings[componentID_array[(i,j)]]
            self.componentID_array = componentID_array
            self._make_blob_dictionary()
        elif data_or_marks == "marks":
            for j in range(0, height):
                for i in range(0, width):
                    if componentID_array[(i,j)] != 0:
                        markID_data_array[(i,j)] = label_mappings[componentID_array[(i,j)]]
            self.markID_data_array = markID_data_array
            self._make_marks_dictionary()
        self.number_of_components = mapped_label - 1
            
    def mark_blobs(self, purpose):
        '''
        For demonstrations of distance mapping of a binary blob with respect to a
        marker blob, this method allows a user to both select one or more blobs in a
        binary image for the purpose of distance mapping and to also place marks on
        the blobs.
        '''
        global marker_image
        old_files_with_marks = glob.glob("_mark_for_*.jpg")
        for oldfile in old_files_with_marks:
            os.remove(oldfile)
        old_files_with_mark_blobs = glob.glob("_component_image_for_mark_*.jpg")
        for oldfile in old_files_with_mark_blobs:
            os.remove(oldfile)
        mw = Tkinter.Tk() 
        if purpose == 'influence_zones':
            mw.title("Place two or more marks in one blob (then click SAVE and EXIT)")
        elif purpose == 'distance_mapping':
            mw.title("Click once in a blob (then click SAVE and EXIT)")
        else:
            raise ValueError('''You must set the 'purpose' arg for mark_blobs() to either 'distance_mapping' or 'influence_zones' ''')
        width,height = self.original_im.size
        marker_image =  Image.new("1", (width, height), 0)        
        self.marker_image_file_name = "_mark_for_" + self.data_im_name
        data_image_width, data_image_height = self.data_im.size  
        display_x,display_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            display_x = int(0.5 * screen_width)
            display_y = int(display_x * (height * 1.0 / width))            
        else:
            display_y = int(0.5 * screen_height)
            display_x = int(display_y * (width * 1.0 / height))
        self.display_size = (display_x,display_y)
        mw.configure(height = display_y, width = display_x) 
        mw.resizable( 0, 0 )  
        display_im = self.original_im.copy()
        display_im = display_im.resize((display_x,display_y), Image.ANTIALIAS)
        mark_scale_x = data_image_width / (1.0 * display_x)
        mark_scale_y = data_image_height / (1.0 * display_y)
        # Even though the user will mark an expanded version of the image, the 
        # markers themselves will be stored in images of size the original data
        # image:
        photo_image = ImageTk.PhotoImage(display_im)
        canvasM = Tkinter.Canvas( mw,   
                                  width = display_x,
                                  height =  display_y,
                                  cursor = "crosshair" )  
        canvasM.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                        command = lambda: self._resize_and_save_for_marked_blobs(marker_image,\
                                                        self.marker_image_file_name,width,height) 
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: mw.destroy()
                      ).pack( side = 'right' )  
        canvasM.bind("<Button-1>", lambda e: self._blobmarker(e,mark_scale_x,mark_scale_y)) 
        canvasM.create_image( 0,0, anchor=NW, image=photo_image)
        canvasM.pack(fill=BOTH, expand=1)
        mw.mainloop()       
        self._binarize_marks()

    def mark_blobs_no_image_scale_change(self):
        '''
        For demonstrations of distance mapping of a binary blob with respect to a
        marker blob, this method allows a user to both select one or more blobs in a
        binary image for the purpose of distance mapping and to also place marks on
        the blobs.
        '''
        global marker_image
        old_files_with_marks = glob.glob("_mark_for_*.jpg")
        for oldfile in old_files_with_marks:
            os.remove(oldfile)
        old_files_with_mark_blobs = glob.glob("_component_image_for_mark_*.jpg")
        for oldfile in old_files_with_mark_blobs:
            os.remove(oldfile)
        mw = Tkinter.Tk() 
        mw.title("Mark a blob by clicking (THEN CLICK SAVE and EXIT)")
        width,height = self.data_im.size
        marker_image =  Image.new("1", (width, height), 0)        
        self.marker_image_file_name = "_mark_for_" + self.data_im_name
        mw.configure(height = height, width = width) 
        mw.resizable( 0, 0 )  
        photo_image = ImageTk.PhotoImage(self.data_im)
        canvasM = Tkinter.Canvas( mw,   
                                  width = width,
                                  height =  height,
                                  cursor = "crosshair" )  
        canvasM.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                        command = lambda: marker_image.save(self.marker_image_file_name) 
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: mw.destroy()
                      ).pack( side = 'right' )  
        canvasM.bind("<Button-1>", lambda e: self._blobmarker(e)) 
        canvasM.create_image( 0,0, anchor=NW, image=photo_image)
        canvasM.pack(fill=BOTH, expand=1)
        mw.mainloop()       
        self._binarize_marks()

    def compute_influence_zones_for_marks(self):
        '''
        Calculates the influence zones in a binary blob with respect to the marks
        placed inside the blob.  The method also identifies the pixels at the
        geodesic skeleton formed by the influence zones.
        '''
        width,height = self.data_im.size
        for blob_index in self.blobs_to_marks_mapping_dict.keys():
            blob_center = self.blob_center_dict[blob_index]
            blob_diameter = self.blob_dia_dict[blob_index]
            blob_array = self.blob_dictionary[blob_index]
            set_of_marks_for_blob = set()
            set_of_marks_for_blob.update(self.blobs_to_marks_mapping_dict[blob_index])
            if len(set_of_marks_for_blob) == 0: continue
            print("\n\nHere is the blob you selected for IZ calculation:")
            _display_portion_of_array_binary(blob_array, blob_center, blob_diameter)
            composite_mark_array = numpy.zeros((height, width), dtype="int")
            for mark_index in set_of_marks_for_blob:
                marked_region = self.marks_dictionary[mark_index]
                marked_region *= mark_index
                composite_mark_array += marked_region
            _display_portion_of_array_binary(composite_mark_array, blob_center, blob_diameter)
            dilated_IZ = self._unit_dilation_of_influence_zones(composite_mark_array, blob_array, set_of_marks_for_blob)
            if dilated_IZ != None:
                print("\n\nDilated IZ for dilation of %d:\n" % (1))
                _display_portion_of_array_binary( dilated_IZ, blob_center, blob_diameter )
                for i in range(2,40):
                    dilated_IZ = self._unit_dilation_of_influence_zones(dilated_IZ, blob_array, set_of_marks_for_blob)
                    if dilated_IZ == None: 
                        print("\n\nMax number of dilations reached at distance %d" % (i-1))
                        break
                    print("\n\nDilated IZ for dilation level of %d\n" % (i))
                    _display_portion_of_array_binary(dilated_IZ, blob_center, blob_diameter)

    def compute_Z_level_sets_for_gradient_image(self):
        '''
        For any value of n between 0 and 255, both ends inclusive, a pixel is in the
        set Z_n if the gradient value at that pixel is less than or equal to n.  Note
        that the gradient values are normalized to be between 0 and 255.
        '''
        gradient_image_as_array = self.gradient_image_as_array
        height,width = gradient_image_as_array.shape
        decimation_factor = self.level_decimation_factor
        self.max_grad_level = int(self.max_grad_level / decimation_factor )
        new_Z_levels_dict = {}
        for level in range(self.max_grad_level):
            new_Z_levels_dict[level] = numpy.zeros((height, width), dtype="int")
        for i in range(height):
            for j in range(width):
                for level in range(self.max_grad_level-1):                
                    if gradient_image_as_array[(i,j)] <= level * decimation_factor:
                        new_Z_levels_dict[level][(i,j)] = 1
        new_Z_levels_dict[self.max_grad_level-1] = numpy.ones((height, width), dtype="int")
        self.Z_levels_dict = new_Z_levels_dict

    def propagate_influence_zones_from_bottom_to_top_of_Z_levels(self):
        '''
        Basic to watershed computation is the calculation of influence zones of the
        connected components for one Z level in the connected components in the next
        Z level.  Note that we stop at one level below the max level at which Z sets
        are known.  That is because the last IZ calculation consists of finding the
        influence zones of the Z sets at the 'self.max_grad_level-1' level in the Z
        sets at the 'self.max_grad_level' level.
        '''
        for level in range(self.min_grad_level, self.max_grad_level-1):
            print("Propagating influence zones from level %d to level %d" % (level, level+1))
            self._compute_influence_zone_of_one_Z_level_in_the_next(level)

    def mark_image_regions_for_gradient_mods(self):
        '''
        For watershed segmentation that incorporates user-supplied modifications to
        the image gradients, this method allows a user to demarcate through mouse
        clicks polygonal regions where the gradient can be explicitly set to 0.  For
        each region thus demarcated, the mouse clicks must be supplied in a clockwise
        fashion.
        '''
        files_with_region_marks = glob.glob("_region__*.jpg")
        for oldfile in files_with_region_marks:
            os.remove(oldfile)
        done = 0
        while done == 0:
            region_index = 0
            print("Enter marks for Region 1:")
            Watershed.region_mark_coords[0] = []
            self._get_marks_for_one_region(region_index)
            while 1:
                answer = None
                if sys.version_info[0] == 3:
                    answer = input( "More regions to be marked? Enter 'y' for 'yes' or 'n' for 'no': " )
                else:
                    answer = raw_input( "More regions to be marked? Enter 'y' for 'yes' or 'n' for 'no': ")
                answer = answer.strip()
                if answer == "n": 
                    done = 1
                    self.region_marks_centers = Watershed.region_mark_coords
                    break
                elif answer == "y": 
                    region_index += 1
                    Watershed.region_mark_coords[region_index] = []
                    self._get_marks_for_one_region(region_index)
                else:
                    print("You can only enter 'y' or 'n' for 'yes' and 'no'.  Let's try again.")
        palette = [(255,0,0), (0,255,0), (0,0,255), (255,255,255), (192,68,192)] 
        color_index = 0
        width,height = self.display_size
        # Now place all marks in a single image using different colors:  
        composite_image = self.original_im.copy()
        composite_image = composite_image.resize((width,height), Image.ANTIALIAS)
        if self.binary_or_gray_or_color == "gray":
            new_composite_image = Image.new("RGB", (width,height), (0,0,0))
            for j in range(0, height):
                for i in range(0, width):
                    gray_val = composite_image.getpixel((i,j))
                    new_composite_image.putpixel((i,j), (gray_val,gray_val,gray_val))
            composite_image = new_composite_image
        for region_index in self.region_marks_centers:
            color_index %= len(palette)
            for mark_center in self.region_marks_centers[region_index]:
                for j in range(0, height):
                    for i in range(0, width):
                        if ((i-mark_center[0])**2 + (j-mark_center[1])**2) < 25:
                            composite_image.putpixel((i,j), palette[color_index])
            color_index += 1
        composite_image.save("_composite_image_with_all_marks_" + self.data_im_name)
        self.displayImage6(composite_image, "All_Marks_Entered (close window when done viewing)")
        self._make_new_valleys_from_region_marks()

    def modify_gradients_with_marker_minima(self):
        '''
        After a user has demarcated the regions in which the image gradients can be
        modified, this method carries out the gradient modifications.
        '''
        new_gradient_array =  self.gradient_image_as_array.copy()
        for region_index in self.marked_valley_for_region:
            new_gradient_array *= self.marked_valley_for_region[region_index]
        self.gradient_image_as_array = new_gradient_array
        self._display_and_save_array_as_image(new_gradient_array, "_marker_modified_gradient")

    def extract_watershed_contours_separated(self):
        '''
        This method uses the border following algorithm to extract the watershed
        contours from the final propagation of influences by the propagate_influences
        method.
        '''
        result_componentID_array = self.componentID_array_dict[self.max_grad_level-1]
        height,width = result_componentID_array.shape 
        result_watershed_array = numpy.zeros((height, width), dtype="int")
        for i in range(height):
            for j in range(width):
                if result_componentID_array[(i,j)] == -1:
                    result_watershed_array[(i,j)] = 1
        if self.debug:
            print("\n\nDisplay the watershed pixels as a binary image:\n") 
            _display_portion_of_array(result_watershed_array)
        myarray = result_watershed_array
        height,width = myarray.shape 
        contours = []           #  To allow for multiple contours, each a list of points
        while 1:
            contour = []            #  for one contour
            start_flag = 0    
            # Find first point for starting a contour
            for i in range(height):
                for j in range(width):
                    if myarray[(i,j)] == 1:
                        myarray[(i,j)] = -1
                        start_flag = 1
                        break
                if start_flag == 1: break
            if start_flag == 0:
                if self.debug: 
                    print("\n\nDisplay all contours: ", contours)
                break
            start_i, start_j = i,j
            i,j = start_i,start_j
            contour.append((i,j))
            if self.debug: 
                print("contour starts at: ", (i,j))
            Rpoints = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1)]  # Rpoints_W
            contour_done_flag = 0
            while 1:
                # This inner while loop is for extending a starting point into a complete contour
                contour_extension_flag = 0
                if self.debug:
                    print("\ncontour is: ", contour) 
                    print("Rpoints are: ", Rpoints)    
                for l in range(len(Rpoints)):
                    p,q = Rpoints[l]        
                    if (p,q) == (start_i,start_j): 
                        contour_done_flag = 1
                        break
                    elif p > 0 and p < height and q > 0 and q < width and myarray[(p,q)] == 1:
                        contour_extension_flag = 1
                        if self.debug:
                            print("new point on contour: ", (p,q))
                        contour.append(Rpoints[l])
                        m,n = i,j 
                        i,j = p,q
                        if m == i-1 and n == j-1: 
                            Rpoints = [(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)] # Rpoints_NW
                            break
                        elif m == i-1 and n == j: 
                            Rpoints = [(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1)] # Rpoints_N
                            break 
                        elif m == i-1 and n == j+1: 
                            Rpoints = [(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j)] # Rpoints_NE
                            break
                        elif m == i and n == j+1: 
                            Rpoints = [(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1)] # Rpoints_E
                            break
                        elif m == i+1 and n == j+1: 
                            Rpoints = [(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1)] # Rpoints_SE
                            break
                        elif m == i+1 and n == j: 
                            Rpoints = [(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1)] # Rpoints_S
                            break
                        elif m == i+1 and n == j-1: 
                            Rpoints = [(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j)] # Rpoints_SW
                            break
                        elif m == i and n == j-1: 
                            Rpoints = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1)] # Rpoints_W
                            break 
                    myarray[(i,j)] = -1
                if contour_done_flag == 1: break
                if contour_extension_flag == 0: break
                if self.debug:
                    print("\n\nHere is the contour: ", contour)
                    print(myarray)
            contours.append(contour)
        self.watershed_contours = contours        
        return contours

    def extract_watershed_contours_with_random_sampling(self, num_of_contours, min_length = 20):
        '''
        This method uses the border following algorithm to extract the watershed
        contours from the final propagation of influences by the propagate_influences
        method.
        '''
        result_componentID_array = self.componentID_array_dict[self.max_grad_level-1]
        height,width = result_componentID_array.shape 
        watershed_array = numpy.zeros((height, width), dtype="int")
        for i in range(height):
            for j in range(width):
                if result_componentID_array[(i,j)] == -1:
                    watershed_array[(i,j)] = 1
        if self.debug:
            print("\n\nDisplay the watershed pixels as a binary image:\n") 
            _display_portion_of_array(watershed_array)
        contours = []      
        contours_found = 0
        for trial in range(1000):
            myarray = watershed_array.copy()
            if contours_found == num_of_contours: break
            start_flag = 0
            contour = []
            start_i = start_j = None
            seed = random.randint(0,height-1)
            if self.debug:
                print("\n\nsearching with seed: %d" % seed)
            j_candidates = []
            for j in range(0,width):
                if myarray[(seed,j)] == 1:
                    j_candidates.append(j)
                    start_flag = 1
            if start_flag == 0: continue
            start_i, start_j = seed,random.choice(j_candidates)
            i,j = start_i,start_j
            contour.append((i,j))
            if self.debug: 
                print("contour starts at: ", (i,j))
            Rpoints = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1)]  # Rpoints_W
            contour_done_flag = 0
            while 1:
                # This inner while loop is for extending a starting point into a complete contour
                contour_extension_flag = 0
                if self.debug:
                    print("\ncontour is: ", contour) 
                    print("Rpoints are: ", Rpoints)    
                for l in range(len(Rpoints)):
                    p,q = Rpoints[l]        
                    if (p,q) == (start_i,start_j): 
                        contour_done_flag = 1
                        break
                    elif p > 0 and p < height and q > 0 and q < width and myarray[(p,q)] == 1:
                        contour_extension_flag = 1
                        if self.debug:
                            print("new point on contour: ", (p,q))
                        contour.append(Rpoints[l])
                        m,n = i,j 
                        i,j = p,q
                        if m == i-1 and n == j-1: 
                            Rpoints = [(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)] # Rpoints_NW
                            break
                        elif m == i-1 and n == j: 
                            Rpoints = [(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1)] # Rpoints_N
                            break 
                        elif m == i-1 and n == j+1: 
                            Rpoints = [(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j)] # Rpoints_NE
                            break
                        elif m == i and n == j+1: 
                            Rpoints = [(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1)] # Rpoints_E
                            break
                        elif m == i+1 and n == j+1: 
                            Rpoints = [(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1)] # Rpoints_SE
                            break
                        elif m == i+1 and n == j: 
                            Rpoints = [(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1)] # Rpoints_S
                            break
                        elif m == i+1 and n == j-1: 
                            Rpoints = [(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j)] # Rpoints_SW
                            break
                        elif m == i and n == j-1: 
                            Rpoints = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1)] # Rpoints_W
                            break 
                    myarray[(i,j)] = -1
                if contour_done_flag == 1: break
                if contour_extension_flag == 0: break
            if len(contour) < min_length: continue
            similar_contour_found = 0
            if len(contours) > 0:
                for old_contour in contours:
                    contour_overlap = set(old_contour).intersection(contour)
                    if len(contour_overlap) / len(contour) > 0.8: 
                        similar_contour_found = 1
                        break
            if similar_contour_found: continue             
            contours.append(contour)
            contours_found += 1
        self.watershed_contours = contours        
        return contours

    def extract_segmented_blobs_using_contours(self, min_contour_length = 50):
        '''
        This method uses the inside/outside logic at a point (based on the number of times a
        line through the point intersects the contour) in order to decide whether the point is
        inside a closed contour or outside it.
        '''
        print("\n\nExtracting segmented blobs using contours")
        print("\nYou will see flashes of individual blobs. Finally, all the blobs will be shown together in a composite image.")
        width,height = self.data_im.size
        for contour in sorted(self.watershed_contours, key=lambda x: len(x), reverse=True):
            if len(contour) < min_contour_length: continue
            if self.debug:
                print("\ncontour is: %s" % str(contour))
                print("length of contour: %d" % len(contour))
            array_for_segmented_blob = numpy.zeros((height, width), dtype="int")
            for i in range(0, height):
                for j in range(0, width):
                    number_of_crossings = 0
                    raster_line = (0,j,i,j)
                    for l in range(0,len(contour)-1):
                        line = (contour[l][0],contour[l][1],contour[l+1][0],contour[l+1][1])
                        if _line_intersection(raster_line, line):
                            number_of_crossings += 1
                    last_line = (contour[l+1][0],contour[l+1][1],contour[0][0],contour[0][1])
                    number_of_crossings += _line_intersection(raster_line, last_line)
                    if number_of_crossings % 2 == 1:
                        array_for_segmented_blob[(i,j)] = 255
            self.segmented_regions_as_arrays.append(array_for_segmented_blob)
            mask_image = Image.new("P", (width,height), color=0)
            for i in range(0, height):
                for j in range(0, width):
                    if array_for_segmented_blob[(i,j)] == 255:
                        mask_image.putpixel((j,i), 255)
            mask_image = mask_image.resize(self.original_im.size, Image.ANTIALIAS)
            output_segment = self._extract_masked_segment_of_image(mask_image)
            self.segmented_regions_as_images.append(output_segment)

    def extract_segmented_blobs_using_region_growing(self, num_of_segments, min_area = 50):
        '''
        This method uses region growing to extract segmented blobs.  We start at a pixel
        and grow from there by incorporating other neighboring pixels recursive until we
        hit a watershed ridge.
        '''
        print("\n\nExtracting segmented blobs by region growing")
        print('''\n  You will see flashes of individual blobs.\n''' 
              '''  Finally, all the blobs will be shown together in a composite image.\n\n''')
        result_componentID_array = self.componentID_array_dict[self.max_grad_level-1]
        height,width = result_componentID_array.shape 
        watershed_array = numpy.zeros((height, width), dtype="int")
        for i in range(height):
            for j in range(width):
                if result_componentID_array[(i,j)] == -1:
                    watershed_array[(i,j)] = 1
        if self.debug:
            print("\n\nDisplay the watershed pixels as a binary image:\n") 
            _display_portion_of_array(watershed_array)
        segments_found = 0
        master_mask_array = numpy.zeros((height, width), dtype="int")
        for trial in range(1000):
            sys.stdout.write(".")
            sys.stdout.flush()
            if segments_found == num_of_segments: break
            seed = (random.randint(0,height-1),random.randint(0,width-1))
            if self.debug:
                print("\n\nsearching with seed: %s" % str(seed))
            if master_mask_array[(seed[0],seed[1])] == 1:
                trial += 1
                continue     
            mask_array = numpy.zeros((height, width), dtype="int")
            border_pixel_found = 0
            while True:
                if border_pixel_found == 1: break       
                change_made = 0
                for i in range(0, height):
                    if border_pixel_found: break
                    for j in range(0, width):
                        if border_pixel_found: break
                        if mask_array[(i,j)] == 0:
                            for k in range(i-1,i+2):
                                if border_pixel_found: break
                                for l in range(j-1,j+2):
                                    if (0 <= k < height) and (0 <= l < width):
                                        if watershed_array[(k,l)] == 1: break
                                        elif mask_array[(k,l)] == 1:
                                            if (k == 0) or (k == height-1) or (l == 0) or (l == width-1):
                                                border_pixel_found = 1
                                                break
                                            mask_array[(i,j)] = 1                    
                                            change_made = 1
                                        elif (k == seed[0]) and (l == seed[1]):
                                            mask_array[(i,j)] = 1
                                            change_made = 1
                                        else: continue
                if change_made == 0: break
            for i in range(0, height):
                if (mask_array[(i,0)] == 1) or (mask_array[(i,width-1)] == 1):
                    border_pixel_found = 1
                    break
            for j in range(0, width):
                if (mask_array[(0,j)] == 1) or (mask_array[(height-1,j)] == 1):
                    border_pixel_found = 1
                    break
            if border_pixel_found: continue
            num_pixels_in_mask = overlap_score = 0
            for i in range(0, height):
                for j in range(0, width):
                    if mask_array[(i,j)] == 1: 
                         num_pixels_in_mask += 1
                         if master_mask_array[(i,j)] == mask_array[(i,j)]:
                             overlap_score += 1
            if num_pixels_in_mask < min_area: continue
            if overlap_score / num_pixels_in_mask > 0.5: continue
            for i in range(0, height):
                for j in range(0, width):
                    if mask_array[(i,j)] == 1:
                        master_mask_array[(i,j)] = 1
            if self.debug:
                print("\n\nDisplay region mask as a binary image:\n") 
                _display_portion_of_array(mask_array)
            self.segmented_regions_as_arrays.append(mask_array)
            mask_image = Image.new("P", (width,height), color=0)
            for i in range(0, height):
                for j in range(0, width):
                    if mask_array[(i,j)] == 1:
                        mask_image.putpixel((j,i), 255)
            mask_image = mask_image.resize(self.original_im.size, Image.ANTIALIAS)
            output_segment = self._extract_masked_segment_of_image(mask_image)
            self.segmented_regions_as_images.append(output_segment)
            segments_found += 1
            trial += 1

    def histogram_equalize(self):
        '''
        Carries out contrast enhancement in an image.  If an image is generally too dark or generally too
        bright, you may wish to histogram equalize it before subjecting it to watershed segmentation.
        '''
        width,height = self.original_im.size
        how_many_pixels = width * height
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        hsv_image = self.original_im.copy().convert("HSV")
        hist = {i : 0 for i in range(256)}
        cumu_hist = {i : 0 for i in range(256)}
        Lmax = 0
        for x in range(0, width):        
            for y in range(0, height):
                h,s,v = hsv_image.getpixel((x,y))
                hist[v] += 1
                if v > Lmax: Lmax = v
        hist = {i : float(hist[i]) / how_many_pixels for i in hist}
        cumu_hist[0] = hist[0]
        for i in range(1,256):
            cumu_hist[i] = cumu_hist[i-1] + hist[i]
        i_mapping = {i : int((Lmax - 1) * cumu_hist[i])  for i in range(0,Lmax+1)}
        hsv_new_image = Image.new("HSV", (width,height), (0,0,0))
        for x in range(0, width):        
            for y in range(0, height):
                h,s,v = hsv_image.getpixel((x,y))           
                hsv_new_image.putpixel((x,y), (h,s,i_mapping[v]))
        new_image = hsv_new_image.convert("RGB")
        self.displayImage6(new_image, "histogram_equalized_image -- close window when done viewing")
        self.data_im = self.original_im = new_image

    def apply_otsu_threshold_to_hue(self, polarity=1, area_threshold=0, min_brightness_level=100):
        '''
        Applies the optimum Otsu threshold to hue in order to separate the image into foreground and 
        background.  Regarding the argument 'polarity', if it is '-1', all pixels whose hue is below the 
        optimum Otsu threshold are accepted.  On the other hand, if the polarity is '1', all pixels whole 
        hue is higher than the calculated threshold are accepted.  The 'area_threshold' parameter is
        passed to the method "connected_components_for_binary_array()" for rejecting blobs that are
        smaller than the value supplied through 'area_threshold'.
        '''
        print("\ninvoking apply_otsu_threshold_to_hue")
        assert polarity in [-1,1], "\nThe value of 'polarity' in the call to apply_otsu_threshold_to_hue() must be either -1 or 1 --- aborting"
        self.displayImage6(self.original_im, "input_image -- close window when done viewing")
        width,height = self.original_im.size
        how_many_pixels = width * height
        hsv_image = self.original_im.copy().convert("HSV")
        hist = {i : 0 for i in range(256)}
        Hmax = 0
        Hmin = 255
        for x in range(0, width):        
            for y in range(0, height):
                h,s,v = hsv_image.getpixel((x,y))
                hist[h] += 1
                if h > Hmax: Hmax = h
                if h < Hmin: Hmin = h
        hist = {i : float(hist[i]) / how_many_pixels for i in hist}
        cumu_hist = {i : 0 for i in range(256)}
        cumu_hist[0] = hist[0]
        for i in range(1,256):
            cumu_hist[i] = cumu_hist[i-1] + hist[i]
        sigmaBsquared = {k : None for k in range(Hmin, Hmax+1)}
        for k in range(Hmin, Hmax):
            omega0 = cumu_hist[k]
            omega1 = 1 - omega0
            mu0 = (1.0/omega0) * sum([i * hist[i] for i in range(Hmin,k+1)])                                    
            mu1 = (1.0/omega1) * sum([i * hist[i] for i in range(k+1,Hmax)])                                    
            sigmaBsquared[k] = omega0 * omega1 * (mu1 - mu0) ** 2
        sigmaBsquared = {k : sigmaBsquared[k] for k in range(Hmin, Hmax+1) if sigmaBsquared[k] is not None}
        sorted_hue_thresholds = sorted(sigmaBsquared.items(), key=lambda x: x[1], reverse=True)
        print("\nThe hue threshold discovered by Otsu: %d" % sorted_hue_thresholds[0][0])
        hsv_new_image = Image.new("HSV", (width,height), (0,0,0))
        for x in range(0, width):        
            for y in range(0, height):
                h,s,v = hsv_image.getpixel((x,y))           
                if polarity == -1:
                    if h <= sorted_hue_thresholds[0][0]:
                        hsv_new_image.putpixel((x,y), (h,s,v))
                else:
                    if h > sorted_hue_thresholds[0][0]:
                        hsv_new_image.putpixel((x,y), (h,s,v))
        new_image = hsv_new_image.convert("RGB")
        self.displayImage6(new_image, "hue_thresholded_image -- close window when done viewing")
        self.data_im = self.original_im = new_image
#        hsv_new_image = hsv_new_image.resize((int(width/4),int(height/4)), Image.ANTIALIAS)
        width,height = hsv_new_image.size
        mask_size = (height,width) 
        mask_array = numpy.zeros(mask_size, dtype="int")
        for i in range(0, mask_size[0]):
            for j in range(0, mask_size[1]):
                if numpy.linalg.norm(hsv_new_image.getpixel((j,i))) > min_brightness_level:
                    mask_array[(i,j)] = 1
        mask_image = Image.new("1", (width,height), 0)
        for i in range(0, height):
            for j in range(0, width):
                if mask_array[(i,j)] == 1:
                    mask_image.putpixel((j,i), 255)
        self.displayImage3(mask_image, "binary mask constructed for Otsu segmented output")
        if self.debug:
            for i in range(0, height):
                sys.stdout.write("\n")
                for j in range(0, width):
                    if mask_array[(i,j)] == 1:
                        sys.stdout.write('1')
                    else:
                        sys.stdout.write('0')
            sys.stdout.write('\n\n')        
        self._connected_components_for_binary_array(mask_array, area_threshold)
        if self.debug:
            print("\n\nPrinting out the pixel coordinates in the blobs:")
            for blob_index in self.blob_dictionary:
                 print("%d ===>  %s" % (blob_index, str( self.blob_dictionary[blob_index] )))
        return self.blob_dictionary

    def display_all_segmented_blobs(self):
        if len(self.segmented_regions_as_images) == 0:
            sys.exit("display_all_segmented_blobs() called before blob extraction --- aborting")
        print("\n\nDisplaying all extracted segments in a composite image")
        segmented_regions_as_images = copy.deepcopy(self.segmented_regions_as_images)
        width,height = self.original_im.size
        display_im = Image.new('RGB', (width,height), color=(0,0,0))
        num_of_blobs = len(self.segmented_regions_as_images)
        display_segment_width = int(width/4)
        display_segment_height = int(display_segment_width * (height / float(width)))
        original_im = self.original_im.copy().resize((display_segment_width,display_segment_height),Image.ANTIALIAS)
        segmented_regions_as_images.insert(0, original_im)
        for x in range(width):
            for y in range(height):
                if (x % display_segment_width) == 0 or (y % display_segment_height == 0):
                    display_im.putpixel((x,y), (255,255,255))
        num_of_rows_needed = int(num_of_blobs/4) + 1
        for blob_index in range(len(segmented_regions_as_images)):
            horizontal_index = blob_index % 4
            vertical_index = int(blob_index / 4)
            reduced = segmented_regions_as_images[blob_index].resize((display_segment_width,display_segment_height),Image.ANTIALIAS)
            for x in range(display_segment_width):
                for y in range(display_segment_height):            
                    if (x % display_segment_width) != 0 and (y % display_segment_height != 0):
                        display_im.putpixel((horizontal_index*display_segment_width + x, vertical_index*display_segment_height + y), reduced.getpixel((x,y))) 
#        self.displayImage4(display_im, "A Composite of All Segmented Objects")
        self.displayImage5(display_im, "A Composite of the Segmented Objects")

    def display_data_image(self):
        '''
        This is just a convenience method for displaying the image that you want to
        subject to watershed segmentation.
        '''
        image = self.original_im
        self.displayImage3(image, "Original Image (close window when done viewing)")

    def display_watershed(self):
        '''
        Displays the watershed segmentation of the image in the grayscale mode.  That
        is, the image shown is what the computations are carried out on --- a
        grayscale version of the input image (assuming it was a color image).
        '''
        result_componentID_array = self.componentID_array_dict[self.max_grad_level -1]
        height,width = result_componentID_array.shape
        original_image = self.data_im.copy()
        draw = ImageDraw.Draw(original_image)
        for i in range(0, height):
            for j in range(0, width):
                if result_componentID_array[(i,j)] == -1:
                    draw.point((j,i), 255)
#        self.displayImage3(original_image, "Watershed Segmentation (close window when done viewing)")
        self.displayImage6(original_image, "Watershed_Segmentation (close window when done viewing)")

    def display_watershed_in_color(self):
        '''Displays the watershed segmentation on top of the original color image
        (assuming that the input image was a color image to begin with.)

        To write this result image as a jpeg file to the disk, click on the "save"
        and "exit" buttons at the bottom of the window --- as opposed to just closing
        the window.  You can subsequently display the image from the disk file by
        using, say, the 'display' function from the ImageMagick library.  You can
        create a hardcopy version of the result by sending the jpeg image to a
        printer.
        '''
        im = self.data_im
        im_width,im_height = im.size
        result_componentID_array = self.componentID_array_dict[self.max_grad_level -1]
        watershed_points = []
        for i in range(im_height):
            for j in range(im_width):
                if result_componentID_array[(i,j)] == -1:
                    watershed_points.append((i,j))
        mw = Tkinter.Tk()         
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (im_height * 1.0 / im_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (im_width * 1.0 / im_height))
        original_im = self.original_im.copy()
        original_im = original_im.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title( "Watershed Segmentation (close window when done viewing)" ) 
        mw.configure( height = winsize_y, width = winsize_x )         
        mw.resizable( 0, 0 )                              
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,            
                             width = winsize_x,             
                             cursor = "crosshair" )   
        canvas.pack( side = 'top' )                               
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript( file = "Watershed_point_output.jpg") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        x_scale = winsize_x / (im_width * 1.0)
        y_scale = winsize_y / (im_height * 1.0) 
        photo = ImageTk.PhotoImage( original_im )
        canvas.create_image(winsize_x/2,winsize_y/2,image=photo)
        for point in watershed_points:
            x1 = int(point[1] * x_scale)
            y1 = int(point[0] * y_scale)
            x2 = x1 + 5
            y2 = y1 + 5
            canvas.create_oval(x1,y1,x2,y2, fill='red')
        Tkinter.mainloop()        
        
    def display_watershed_contours_in_color(self):
        '''
        Shows the watershed contours as extracted by the extract_watershed_contours()
        method.

        To write the result image as a jpeg file to the disk, click on the "save"
        and "exit" buttons at the bottom of the window --- as opposed to just closing
        the window.  You can subsequently display the image from the disk file by
        using, say, the 'display' function from the ImageMagick library.  You can
        create a hardcopy version of the result by sending the jpeg image to a
        printer.
        '''
        im = self.data_im
        im_width,im_height = im.size
        if len(self.watershed_contours) == 0:
            sys.exit("You have called display_watershed_contours_in_color() before extracting the contours ... aborting")
        contours = self.watershed_contours
        mw = Tkinter.Tk()         
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (im_height * 1.0 / im_width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (im_width * 1.0 / im_height))
        original_im = self.original_im.copy()
        original_im = original_im.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title( "Watershed Contours (close window when done viewing)" ) 
        mw.configure( height = winsize_y, width = winsize_x )         
        mw.resizable( 0, 0 )                              
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,            
                             width = winsize_x,             
                             cursor = "crosshair" )   
        canvas.pack( side = 'top' )                               
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = "Watershed_contour_output.jpg") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        x_scale = winsize_x / (im_width * 1.0)
        y_scale = winsize_y / (im_height * 1.0) 
        photo = ImageTk.PhotoImage( original_im )
        canvas.create_image(winsize_x/2,winsize_y/2,image=photo)
        for polygon in contours:
            if len(polygon) < 10: continue
            polygon = [(int(item[1]*x_scale), int(item[0]*y_scale)) for item in polygon]
            firstpoint = polygon[0]
            secondpoint = polygon[1]
            lastpoint  = polygon[-1]
            if ((firstpoint[0]-lastpoint[0])**2 + (firstpoint[1]-lastpoint[1])**2) < 8 * (firstpoint[0] - secondpoint[0])**2:
                polygon.append(firstpoint)       
            canvas.create_line(polygon, width=4, fill='red')
        Tkinter.mainloop()        

    def displayImage(self, argimage, title=""):
        '''
        Displays the argument image.  The display stays on for the number of seconds
        that is the first argument in the call to tk.after() divided by 1000.
        '''
        width,height = argimage.size
        winsize_x,winsize_y = width,height
        if width > height:
            winsize_x = 600
            winsize_y = int(600.0 * (height * 1.0 / width))
        else:
            winsize_y = 600
            winsize_x = int(600.0 * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk = Tkinter.Tk()
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.after(1000, self._callback, tk)    # display will stay on for just one second
        tk.mainloop()

    def displayImage2(self, argimage, title=""):
        '''
        Displays the argument image.  The display stays on until the user closes the
        window.  If you want a display that automatically shuts off after a certain
        number of seconds, use the previous method displayImage().
        '''
        width,height = argimage.size
        winsize_x,winsize_y = width,height
        if width > height:
            winsize_x = 600
            winsize_y = int(600.0 * (height * 1.0 / width))
        else:
            winsize_y = 600
            winsize_x = int(600.0 * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk = Tkinter.Tk()
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.mainloop()

    def displayImage3(self, argimage, title=""):
        '''
        Displays the argument image (which must be of type Image) in its actual size.  The 
        display stays on until the user closes the window.  If you want a display that 
        automatically shuts off after a certain number of seconds, use the method 
        displayImage().
        '''
        width,height = argimage.size
        tk = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = tk.winfo_screenwidth(),tk.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( display_image )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.mainloop()

    def displayImage4(self, argimage, title=""):
        '''
        Displays the argument image (which must be of type Image) in its actual size without 
        imposing the constraint that the larger dimension of the image be at most half the 
        corresponding screen dimension.
        '''
        width,height = argimage.size
        tk = Tkinter.Tk()
        tk.title(title)   
        frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH,expand=1)
        photo_image = ImageTk.PhotoImage( argimage )
        label = Tkinter.Label(frame, image=photo_image)
        label.pack(fill=X, expand=1)
        tk.mainloop()

    def displayImage5(self, argimage, title=""):
        '''
        This does the same thing as displayImage4() except that it also provides for
        "save" and "exit" buttons.  This method displays the argument image with more 
        liberal sizing constraints than the previous methods.  This method is 
        recommended for showing a composite of all the segmented objects, with each
        object displayed separately.  Note that 'argimage' must be of type Image.
        '''
        width,height = argimage.size
        winsize_x,winsize_y = None,None
        mw = Tkinter.Tk()
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.8 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.8 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        mw.configure(height = winsize_y, width = winsize_x)         
        mw.title(title)   
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,
                             width = winsize_x,
                             cursor = "crosshair" )   
        canvas.pack( side = 'top' )                               
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = "segmented_objects.jpg") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        photo = ImageTk.PhotoImage(argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS))
        canvas.create_image(winsize_x/2,winsize_y/2,image=photo)
        mw.mainloop()

    def displayImage6(self, argimage, title=""):
        '''
        This does the same thing as displayImage3() except that it also provides for
        "save" and "exit" buttons. Note that 'argimage' must be of type Image.
        '''
        width,height = argimage.size
        mw = Tkinter.Tk()
        winsize_x,winsize_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            winsize_x = int(0.5 * screen_width)
            winsize_y = int(winsize_x * (height * 1.0 / width))            
        else:
            winsize_y = int(0.5 * screen_height)
            winsize_x = int(winsize_y * (width * 1.0 / height))
        display_image = argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS)
        mw.title(title)   
        canvas = Tkinter.Canvas( mw,                         
                             height = winsize_y,
                             width = winsize_x,
                             cursor = "crosshair" )   
        canvas.pack( side = 'top' )                               
        frame = Tkinter.Frame(mw)                            
        frame.pack( side = 'bottom' )                             
        Tkinter.Button( frame,         
                text = 'Save',                                    
                command = lambda: canvas.postscript(file = title.partition(' ')[0] + ".jpg") 
              ).pack( side = 'left' )                             
        Tkinter.Button( frame,                        
                text = 'Exit',                                    
                command = lambda: mw.destroy(),                    
              ).pack( side = 'right' )                            
        photo = ImageTk.PhotoImage(argimage.resize((winsize_x,winsize_y), Image.ANTIALIAS))
        canvas.create_image(winsize_x/2,winsize_y/2,image=photo)
        mw.mainloop()

    # The destructor:
    def __del__(self):                                     
        for filename in glob.glob('_component_image_for_mark*'): os.remove(filename)
        for filename in glob.glob('_gradient__*.jpg'): os.remove(filename)
        for filename in glob.glob('_composite_*.jpg'): os.remove(filename)
        for filename in glob.glob('_binarized_valley_created*'): os.remove(filename)
        for filename in glob.glob('_region__*.jpg'): os.remove(filename)
        for filename in glob.glob('_marker_modified_gradient*'): os.remove(filename)
        for filename in glob.glob('_mark_for_*.jpg'): os.remove(filename)
        for filename in glob.glob('_LoG__*.jpg'): os.remove(filename)

    #______________________________  Static Methods of the Watershed Class ____________________________

    @staticmethod    
    def _start_mouse_motion(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        Watershed.image_portion_delineation_coords.append((markX,markY))
        print("Button pressed at: x=%s  y=%s\n" % (markX, markY)) 
        canvasM.create_oval( markX-5, markY-5, markX+5, markY+5, outline="red", fill="green", width = 2 )  

    @staticmethod    
    def _stop_mouse_motion(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        Watershed.image_portion_delineation_coords.append((markX,markY))
        print("Button pressed at: x=%s  y=%s\n" % (markX, markY))
        points = Watershed.image_portion_delineation_coords
        canvasM.create_rectangle(points[0][0], points[0][1], points[-1][0], points[-1][1], outline="red", fill="green", width = 2 ) 
        Watershed.extracted_image = Watershed._extract_image_portion_rectangular()

    @staticmethod    
    def _on_mouse_motion(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        Watershed.image_portion_delineation_coords.append((markX,markY))
        points = Watershed.image_portion_delineation_coords
        canvasM.create_rectangle(points[0][0], points[0][1], points[-1][0], points[-1][1], outline="red", fill="green", width = 2 ) 

    @staticmethod    
    def _image_portion_delineator(evt, input_image):
        global delineator_image
        display_width, display_height = delineator_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        Watershed.image_portion_delineation_coords.append((markX,markY))
        print("Button pressed at: x=%s  y=%s\n" % (markX, markY)) 
        canvasM.create_oval( markX-10, markY-10, markX+10, markY+10, outline="red", fill="green", width = 2 )  

    @staticmethod    
    def _extract_image_portion_rectangular():
        '''
        This extracts a rectangular region of the image as specified by dragging the mouse pointer
        from the upper left corner of the region to its lower right corner.  After extracting the
        region, it sets the 'original_im' and 'data_im' attributes of the Watershed instance to 
        the region extracted.
        '''
        global delineator_image
        width,height = delineator_image.size
        polygon = Watershed.image_portion_delineation_coords
        extracted_width = polygon[-1][0] - polygon[0][0]
        extracted_height = polygon[-1][1] - polygon[0][1]
        extracted_image = Image.new("RGB", (extracted_width,extracted_height), (0,0,0))
        for x in range(0, extracted_width):        
            for y in range(0, extracted_height):
                extracted_image.putpixel((x,y), delineator_image.getpixel((polygon[0][0]+x, polygon[0][1]+y)))
        return extracted_image

    @staticmethod    
    def _extract_and_save_image_portion_polygonal():
        '''
        This extracts a polygonal region of the image as specified by clicking the mouse in a clockwise
        direction.  After extracting the region, it sets the 'original_im' and 'data_im' attributes of 
        the Watershed instance to the minimum bounding rectangle portion of the original image that 
        encloses the polygonal --- with the pixels outside the polygonal area set to 0.
        '''
        global delineator_image
        width,height = delineator_image.size
        polygon = Watershed.image_portion_delineation_coords
        if len(polygon) <= 2:
            sys.exit("You need MORE THAN TWO mouse clicks (in a clockwise fashion) to extract a region --- aborting!")
        x_min,x_max = min([x for (x,y) in polygon]),max([x for (x,y) in polygon])
        y_min,y_max = min([y for (x,y) in polygon]),max([y for (x,y) in polygon]) 
        extracted_width = x_max - x_min
        extracted_height = y_max - y_min
        extracted_image = Image.new("RGB", (extracted_width,extracted_height), (0,0,0))
        polygon = [(x - x_min, y - y_min) for (x,y) in polygon]
        for x in range(0, extracted_width):        
            for y in range(0, extracted_height):
                number_of_crossings = 0
                raster_line = (0,y,x,y)
                for l in range(0,len(polygon)-1):
                    line = (polygon[l][0],polygon[l][1],polygon[l+1][0],polygon[l+1][1])
                    if _line_intersection(raster_line, line):
                        number_of_crossings += 1
                last_line = (polygon[l+1][0],polygon[l+1][1],polygon[0][0],polygon[0][1])
                number_of_crossings += _line_intersection(raster_line, last_line)
                if number_of_crossings % 2 == 1:
                    extracted_image.putpixel((x,y), delineator_image.getpixel((x+x_min, y + y_min)))
        extracted_image.save(Watershed.delineated_portion_file_name) 
        Watershed.extracted_image = extracted_image

    @staticmethod    
    def _blobmarker(evt, mark_scale_x, mark_scale_y):
        global marker_image
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        print("Button pressed at: x=%s  y=%s\n" % (markX, markY)) 
        canvasM.create_oval( markX-5, markY-5, markX+5, markY+5, outline="red", fill="green", width = 2 )  
        width,height = marker_image.size
        markX *= mark_scale_x
        markY *= mark_scale_y
        for i in range(0, width):
            for j in range(0, height):
                if ((i-markX)**2 + (j-markY)**2) < 25:
                    marker_image.putpixel((i,j), 255)

    @staticmethod
    def _region_marker(evt, region_index, data_image_width, data_image_height):
        global region_marker_image
        display_width, display_height = region_marker_image.size
        canvasM = evt.widget   
        markX, markY = evt.x, evt.y   
        Watershed.region_mark_coords[region_index].append((markX,markY))
        print("For region index %d, Button pressed at: x=%s  y=%s\n" % (region_index, markX, markY)) 
        canvasM.create_oval( markX-5, markY-5, markX+5, markY+5, outline="red", fill="green", width = 2 )  
        display_x,display_y = region_marker_image.size
        for i in range(0, display_x):
            for j in range(0, display_y):
                if ((i-markX)**2 + (j-markY)**2) < 25:
                    region_marker_image.putpixel((i,j), 255)

    @staticmethod
    def _resize_and_save(region_marker_image, width, height, region_marker_image_file_name):
        resized = region_marker_image.resize((width,height), Image.ANTIALIAS)
        resized.save(region_marker_image_file_name)

    @staticmethod
    def _resize_and_save_for_marked_blobs(marked_image,file_name,width,height):
        resized = marker_image.resize((width,height), Image.ANTIALIAS)
        resized.save(file_name)

    @staticmethod
    def make_binary_pic_art_nouveau(under_what_name):
        '''
        Can be used to make "fun" binary images for demonstrating distance mapping of
        binary blobs, calculation of influence zones, etc.  This method is taken from
        Chapter 13 of my book "Scripting with Objects".
        '''
        mw = Tkinter.Tk() 
        mw.title( "Art Nouveau" )   
        mw.configure( height = 650, width = 600 ) 
        mw.resizable( 0, 0 )  
        Watershed.canvas = Tkinter.Canvas( mw,   
                                 height = 600,  
                                 width = 600, 
                                 bg = 'white',
                                 cursor = "crosshair" )  
        Watershed.canvas.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                        command = lambda: Watershed.canvas.postscript( file = under_what_name + \
                                                                               ".ps", colormode="color") 
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: sys.exit(0),   
                      ).pack( side = 'right' )  
        Watershed.canvas.bind( "<Button-1>", lambda e: Watershed._drawingControl( e ) ) 
        mw.mainloop()       

    @staticmethod
    def _drawingControl(evt):              
        '''
        Turn drawing on the canvas on and off with consecutive clicks of the left
        button of the mouse
        '''
        Watershed.drawEnable = (Watershed.drawEnable + 1) % 2   
        if not Watershed.drawEnable:                    
            Watershed.canvas.bind( "<Motion>", lambda e: "break" )   
        else:                 
            Watershed.startX, Watershed.startY = evt.x, evt.y   
            print("Button pressed at: x=%s  y=%s\n" % (Watershed.startX, Watershed.startY)) 
            Watershed.canvas.bind( "<Motion>", lambda e: Watershed._draw( e ) )    

    @staticmethod    
    def _draw(evt):       
        '''
        Event processing for the drawEnable() method
        '''
        canv, x, y = evt.widget, evt.x, evt.y  
        canv.create_arc( Watershed.startX, Watershed.startY, x, y, width = 4, fill = 'black' )  
        Watershed.startX, Watershed.startY = x, y                                 

    @staticmethod
    def gendata( feature, imagesize, position, orientation_or_radius, output_image_name ):
        '''
        This method is useful for generating simple binary patterns for checking the
        validity of the logic used for dilation, erosion, IZ calculation, geodesic
        skeleton calculation, etc.  Note that the permissible values for the
        'feature' parameter are: 'line', 'triangle', 'rectangle', 'broken_rectangle',
        'disk' and 'twin_rect'.  The parameter 'imagesize' is supposed to be a tuple
        (m,n) for the size of the output image desired.  The parameter 'position' is
        supposed to be a tuple (x,y) of pixel coordinates for specifying the position
        of the binary pattern in your image.  The parameter 'orientation_or_radius' is an
        integer value specifying the number of degrees of rotation that should be
        applied to the pattern for a given 'feature' for the case of 'line', 'triangle',
        'rectangle' and 'broken_rectangle'.  The same parameter for the case of 'circle'
        means the radius of the disk.  Note that the x coordinate is along the horizontal 
        direction pointing  to the right and the y coordinate is along vertical direction 
        pointing downwards.  The origin is at the upper left corner.
        '''
        width,height = imagesize
        x=y=theta=radius=sin_theta=cos_theta=tan_theta=None
        if position is not None:
            x,y = position
        if feature == 'circle':
            radius = orientation_or_radius
        else:
            if orientation_or_radius is not None:
                theta = orientation_or_radius
                tan_theta = numpy.tan( theta * numpy.pi / 180 )
                cos_theta =  numpy.cos( theta * numpy.pi / 180 )
                sin_theta =  numpy.sin( theta * numpy.pi / 180 )
        # 'im' is redefined for the case of 'disk'
        im = Image.new( "1", imagesize, 0 )
        draw = ImageDraw.Draw(im)
        if feature == 'line':
            delta =  y / tan_theta
            if delta <= x:
                x1 = x - y / tan_theta
                y1 = 0
            else:
                x1 = 0
                y1 = y - x * tan_theta
            x2 = x1 + height / tan_theta
            y2 = height
            if x2 > width:
                excess = x2 - width
                x2 = width
                y2 = height - excess * tan_theta
            draw.line( (x1,y1,x2,y2), fill=255)
            del draw
            im.save( output_image_name )
        elif feature == "triangle":
            x1 = int(width/2.0)
            y1 = int(0.7*height)
            x2 = x1 -  int(width/4.0)
            y2 = int(height/4.0)
            x3 = x1 +  int(width/4.0)
            y3 = y2
            draw.line( (x1,y1,x2,y2), fill=255 )
            draw.line( (x1,y1,x3,y3), fill=255 )
            draw.line( (x2,y2,x3,y3), fill=255 )
            del draw
            h2 = int(height/2)
            w2 = int(width/2)
            im = im.transform(imagesize, Image.AFFINE, \
              (cos_theta,sin_theta,-x,-sin_theta,cos_theta,-y), Image.BICUBIC )
            im.show()
            im.save( output_image_name )
        elif feature == "rectangle":
            x1 = int(width/3.0)
            y1 = int(height/3.0)
            x2 = int(2.0*width/3.0)
            y2 = y1
            x3 = x2
            y3 = int(2.0*height/3.0)
            x4 = x1
            y4 = y3
            draw.line( (x1,y1,x2,y2), fill=255 )
            draw.line( (x2,y2,x3,y3), fill=255 )
            draw.line( (x3,y3,x4,y4), fill=255 )
            draw.line( (x4,y4,x1,y1), fill=255 )
            del draw
            h2 = int(height/2)
            w2 = int(width/2)
            im = im.transform(imagesize, Image.AFFINE, \
              (cos_theta,sin_theta,-x,-sin_theta,cos_theta,-y), Image.BICUBIC )
            im.save( output_image_name )
        elif feature == "broken_rectangle":
            x1 = int(width/3.0)
            y1 = int(height/3.0)
            x2 = int(2.0*width/3.0)
            y2 = y1
            x3 = x2
            y3 = int(2.0*height/3.0)
            x4 = x1
            y4 = y3
            draw.line( (x1,y1,x1+10,y2), fill=255 )
            draw.line( (x1+15,y1,x2,y2), fill=255 )
            draw.line( (x2,y2,x3,y2+30), fill=255 )
            draw.line( (x2,y2+35,x3,y3), fill=255 )
            draw.line( (x3,y3,x4,y4), fill=255 )
            draw.line( (x4,y4,x1,y1), fill=255 )
            del draw
            h2 = int(height/2)
            w2 = int(width/2)
            im = im.transform(imagesize, Image.AFFINE, \
              (cos_theta,sin_theta,-x,-sin_theta,cos_theta,-y), Image.BICUBIC )
            im.save( output_image_name )
        elif feature == "disk":
            im = Image.new( "RGB", imagesize, (0,0,0) )
            draw = ImageDraw.Draw(im)
            draw.ellipse( (x-10,y-10,x+10,y+10), fill=(255,0,0))
            del draw
            im.save( output_image_name )
        elif feature == "twin_rect":
            im = Image.new( "RGB", imagesize, (0,0,0) )
            draw = ImageDraw.Draw(im)
            x1 = int(width/4.0)
            y1 = int(height/4.0)
            x2 = int(width/2.0) 
            y2 = int(3*height/4.0)
            x3 = int(width/2.0) 
            y3 = int(height/4.0)
            x4 = int(3*width/4.0)
            y4 = int(3*height/4.0)            
            draw.rectangle([x1,y1,x2,y2], fill=(255,0,0))
            draw.rectangle([x3,y3,x4,y4], fill=(0,255,0))
            del draw            
            im.save( output_image_name )
        else:
            sys.exit("unknown feature requested from gendata()")


    #______________________  Private Methods of the Watershed Class  ________________


    def _display_and_save_array_as_color_image(self, array_R, array_G, array_B, what=""):
        '''
        what_type:  just a string that indicated what it is you are trying to display as image
        '''
        import colorsys
        height,width = array_R.shape
        newimage = Image.new("RGB", (width,height), (0,0,0))
        for i in range(0, height):
            for j in range(0, width):
                r,g,b = array_R[i,j], array_G[i,j], array_B[i,j]
                newimage.putpixel((j,i), (r,g,b))
        self.displayImage3(newimage, what + "   (close window when done viewing)")

    def _display_and_save_array_as_image(self, array, what_type):
        height,width = array.shape
        maxVal = array.max()
        minVal = array.min()
        newimage = Image.new("L", (width,height), 0.0)
        for i in range(0, height):
            for j in range(0, width):
                displayVal = int( (array[(i,j)] - minVal) * (255/(maxVal-minVal)) )
                newimage.putpixel((j,i), displayVal)
        self.displayImage3(newimage, what_type + "   (close window when done viewing)")
        image_name = what_type + "_" + self.data_im_name
        newimage.save(image_name)        

    def _display_and_save_binary_array_as_image(self, array, what_type):
        height,width = array.shape
        newimage = Image.new("RGB", (width,height), (0,0,0))
        for i in range(0, height):
            for j in range(0, width):
                if array[(i,j)] == 1:
                    newimage.putpixel((j,i), (255,255,255))
        self.displayImage3(newimage, what_type)
        image_name = what_type + "_" + self.data_im_name
        newimage.save(image_name)        

    def _display_and_save_binary_array_as_image2(self, array, what_type):
        height,width = array.shape
        newimage = Image.new("1", (width,height), 0.0)
        for i in range(0, height):
            for j in range(0, width):
                if array[(i,j)] == 255:
                    newimage.putpixel((j,i), 255)
        self.displayImage3(newimage, what_type)
        image_name = what_type + "_" + self.data_im_name
        newimage.save(image_name)        

    def _display_image_array_row(self, image_array, which_row, type_image='image'):
        print("\nDisplaying row indexed %d for %s:" % (which_row,type_image))
        row = image_array[which_row]
        print("Number of elements in the row: ", len(row)) 
        maxVal = row.max()
        minVal = row.min()
        print("The max and min values are %f %f" % (maxVal, minVal))
        for i in range(len(row)):
            print("%d " % (row[i]),) 
        print("\n\n")

    def _extract_masked_segment_of_image(self, mask_image):
        output_image = self.original_im.copy()
        width,height = output_image.size 
        widthm,heightm = mask_image.size
        if (width != widthm) or (height != heightm):
            sys.exit("\nThe mask image must be of the same size as the input image. Aborting!")
        if self.debug:
            self.displayImage3(mask_image, "Just showing the mask")
        for x in range(width):
            for y in range(height):
                if mask_image.getpixel((x,y)) != 255:
                    output_image.putpixel((x,y), (0,0,0))                
#        self.displayImage3(output_image, "RESULT:  a segment of the image")
        self.displayImage(output_image, "RESULT:  a segment of the image")
        return output_image

    def _compute_influence_zone_of_one_Z_level_in_the_next(self, level):
        '''
        The goal here is the find the SKIZ skeleton in the Z level (i+1) as created by
        the blobs at the level i.  Note that each blob at level i will contained in
        some blob at level i+1.  When 2 or more blobs at at level i are contained in
        the same blob at level i+1, that means the pixels between the level i blobs
        define a watershed since the the level i blobs are the mouths of the valleys
        that merge at level i+1.  When no level i blobs are contained in a given blob
        at level i+1, then the (i+1) blob defines the beginning of a new valley for the
        rising flood as we continue to immerse the topographic relief map in a tub of
        water.  (Note that SKIZ stands for Skeleton formed by Influence Zones.)  The
        blobs at level i are dilated into their corresponding influence zones in the 
        blobs at level i+1.
        '''
        width,height = self.data_im.size
        if level == 0:
            self.start_label_for_labeling_blobs_vs_level[0] = 1
            self._gray_level_connected_components(0,1)
            self.label_pool_at_level[0] = set(range(1,self.level_vs_number_of_components[0]+1))
            self._make_blob_dictionary_at_one_Z_level(0)

        self.start_label_for_labeling_blobs_vs_level[level+1] = \
               self.start_label_for_labeling_blobs_vs_level[level] + self.level_vs_number_of_components[level]
        self._gray_level_connected_components(level+1,self.start_label_for_labeling_blobs_vs_level[level+1])
        self.label_pool_at_level[level+1] = set(range(self.start_label_for_labeling_blobs_vs_level[level+1], 
           self.start_label_for_labeling_blobs_vs_level[level+1] + self.level_vs_number_of_components[level+1] + 1))
        self._make_blob_dictionary_at_one_Z_level(level+1)
        componentID_array_at_current_level = self.componentID_array_dict[level]
        componentID_array_at_next_level = self.componentID_array_dict[level+1]
        current_level_label_mapping_dict = {}
        current_level_labels_used = set()
        next_Z_level_containment = {}
        for i in range(height):
            for j in range(width):
                current_level_label = componentID_array_at_current_level[(i,j)]
                next_level_label = componentID_array_at_next_level[(i,j)]
                if current_level_label > 0 and next_level_label > 0:
                    current_level_label_mapping_dict[current_level_label] = next_level_label
                    if next_level_label not in next_Z_level_containment:
                        next_Z_level_containment[next_level_label] = set([current_level_label])
                    else:
                        next_Z_level_containment[next_level_label].add(current_level_label)
        all_labels_next_level = self.blob_dictionary_by_level_for_Z[level+1].keys()
        if self.debug:
            print("\n\nAt level %d: All labels next level: %s\n" % (level,all_labels_next_level))
        nextlevel = level + 1
        if self.debug:
            for label in next_Z_level_containment:
               print("\nLevel: %d --- blob labeled %d contains lower level blobs labeled %s" 
                                                  %(nextlevel, label, next_Z_level_containment[label]))
            print("Level: %d --- next_Z_level_containment has keys: %s " % (level, next_Z_level_containment.keys()))
            print("keys in the next level blob dictionary: ", self.blob_dictionary_by_level_for_Z[level+1].keys())
            print("componentID array for level ", level)   
            _display_portion_of_array(self.componentID_array_dict[level])
            print("\n\nStarting BIG LOOP\n\n")
        for blob_index in next_Z_level_containment:
            if self.debug:
                print("for next level, we are working with blob index ", blob_index)
            # blob array is the component-labeled blob array for the Z set at that level.  These
            # are produced by the method  compute_Z_level_sets_for_gradient_image() 
            blob_array = self.blob_dictionary_by_level_for_Z[level+1][blob_index]
            lower_level_labels_contained = next_Z_level_containment[blob_index]
            if self.debug:
                print("INSIDE THE BIG LOOP: lower_level_labels_contained: ", lower_level_labels_contained)
            if len(lower_level_labels_contained) == 0: continue
            self.label_pool_at_level[level+1].remove(blob_index)
            self.label_pool_at_level[level+1].update(lower_level_labels_contained)
            self.level_vs_number_of_components[level+1] += len(lower_level_labels_contained) - 1
            composite_mark_array = numpy.zeros((height, width), dtype="int")
            for lower_level_blob_index in next_Z_level_containment[blob_index]:
                marked_region = self.blob_dictionary_by_level_for_Z[level][lower_level_blob_index]
                marked_region *= lower_level_blob_index
                composite_mark_array += marked_region
            self.no_more_dilation_possible = 0  
            dilated_IZ = self._unit_dilation_of_influence_zones2(composite_mark_array, blob_array, lower_level_labels_contained)
            if self.no_more_dilation_possible == 0:
                for i in range(2,40):
                    dilated_IZ = self._unit_dilation_of_influence_zones2(dilated_IZ, blob_array, lower_level_labels_contained)
                    if self.no_more_dilation_possible == 1:
                        if self.debug:
                            print("\n\nMax number of dilations reached at distance %d for blob index %d at level %d" % (i-1, blob_index, level))
                        break
            del self.blob_dictionary_by_level_for_Z[level+1][blob_index]
            sub_blob_dictionary = {}
            for label in lower_level_labels_contained:
                blob_array = numpy.zeros((height, width), dtype="int")
                for i in range(0, height):
                    for j in range(0, width):
                        if dilated_IZ[(i,j)] == label:
                            blob_array[(i,j)] = 1
                        elif dilated_IZ[(i,j)] < 0:
                            componentID_array_at_next_level[(i,j)] = dilated_IZ[(i,j)]
                self.blob_dictionary_by_level_for_Z[level+1][label] = blob_array
        new_componentID_array_at_next_level = numpy.zeros((height, width), dtype="int")
        for i in range(0, height):
            for j in range(0, width):
                if componentID_array_at_next_level[(i,j)] <= 0:
                    new_componentID_array_at_next_level[(i,j)] = componentID_array_at_next_level[(i,j)]
        for blob_index in self.blob_dictionary_by_level_for_Z[level+1].keys():
            blob_array = self.blob_dictionary_by_level_for_Z[level+1][blob_index]
            for i in range(0, height):
                for j in range(0, width):
                    if blob_array[(i,j)] == 1:
                        new_componentID_array_at_next_level[(i,j)] = blob_index 
        if self.debug:
            print("Reconstructed componentID array for level ", level + 1)  
            _display_portion_of_array(new_componentID_array_at_next_level)
        self.componentID_array_dict[level+1] = new_componentID_array_at_next_level
        self._make_blob_dictionary_at_one_Z_level(level+1)

    def _unit_dilation_of_influence_zones2(self, input_array, blob_array, set_of_marks_for_blob):
        '''
        This method dilates the 'input_array' by a unit pixel, the goal being to create the 
        influence zones for the 'input_array' blobs in the blobs of the 'blob_array'.  The 
        'input_array' corresponds to the labeled blobs for the water level at one Z level
        and 'blob_array' the level-set blobs at the next Z level.
        '''
        (width,height) = self.data_im.size
        dilated_array = input_array.copy()
        sorted_mark_labels = sorted(list(set_of_marks_for_blob), reverse=True)
        skiz_label = -1
        change_made = 0
        for i in range(0,height):
            for j in range(0,width):
                if input_array[(i,j)] > 0:
                    if ( ( (j+1) >= 0 and (j+1) < width  )  and input_array[(i,j+1)] == 0 ) or \
                       ( ( (j-1) >= 0 and (j-1) < width  )  and input_array[(i,j-1)] == 0 ) or \
                       ( ( (i-1) >= 0 and (i-1) < height )  and input_array[(i-1,j)] == 0 ) or \
                       ( ( (i+1) >= 0 and (i+1) < height )  and input_array[(i+1,j)] == 0 ):
                        ij_label = input_array[(i,j)]
                        other_labels = set_of_marks_for_blob.difference(set([ij_label]))
                        for k in range(-1,2):
                            for l in range(-1,2):
                                if (0 <= (i+k) < height) and (0 <= (j+l) < width):
                                    if blob_array[(i+k,j+l)] != 0:
                                         if dilated_array[(i+k,j+l)] == 0:
                                             test_bit = 1
                                             for s in range(-1,2):
                                                 for t in range(-1,2):
                                                     if (0 <= (i+k+s) < height) and (0 <= (j+l+t) < width):
                                                         if dilated_array[(i+k+s,j+l+t)] in other_labels:
                                                             test_bit = 0
                                                 if test_bit == 1:
                                                     change_made = 1
                                                     dilated_array[(i+k,j+l)] = dilated_array[(i,j)]
                                                 else:
                                                     dilated_array[(i+k,j+l)] = skiz_label
        if change_made == 0: 
            self.no_more_dilation_possible = 1
        return dilated_array

    def _gray_level_connected_components(self, level, start_label):
        binary_image_array = self.Z_levels_dict[level]
        equivalences = set()           # set of pairs of equivalent labels
        height,width = binary_image_array.shape
        componentID_array = numpy.zeros((height, width), dtype="int")
        current_componentID = 1
        if binary_image_array[(0,0)] == 1:            
            componentID_array[(0,0)] = current_componentID
            current_componentID += 1
        for j in range(1, width):
            if binary_image_array[(0,j)] == 1:
                if binary_image_array[(0,j-1)] == 1:
                    componentID_array[(0,j)] = componentID_array[(0,j-1)]
                else:
                    componentID_array[(0,j)] = current_componentID
                    current_componentID += 1
        for i in range(1, height):
            if binary_image_array[(i,0)] == 1:
                if binary_image_array[(i-1,0)] != 0:
                    componentID_array[(i,0)] = componentID_array[(i-1,0)]
                else:
                    componentID_array[(i,0)] = current_componentID
                    current_componentID += 1
        for i in range(1, height):
            for j in range(1, width):
                if binary_image_array[(i-1,j)] == 1 and binary_image_array[(i,j-1)] == 1: 
                    equivalences.add((componentID_array[(i-1,j)],\
                                                componentID_array[(i,j-1)]))
                if binary_image_array[(i,j)] == 1:            
                    if binary_image_array[(i-1,j)] == 1:
                        componentID_array[(i,j)] = componentID_array[(i-1,j)]
                    elif binary_image_array[(i-1,j-1)] == 1:
                        componentID_array[(i,j)] = componentID_array[(i-1,j-1)]
                    elif binary_image_array[(i,j-1)] ==1:
                        componentID_array[(i,j)] = componentID_array[(i,j-1)]
                    elif (j+1) < width and binary_image_array[(i-1,j+1)] == 1:
                        componentID_array[(i,j)] = componentID_array[(i-1,j+1)]
                    else:
                        componentID_array[(i,j)] = current_componentID
                        current_componentID += 1
        if self.debug:
            print("Inside Component Labeler --- equivalences: ", equivalences)
        equivalences_as_lists = []
        for eachset in equivalences:
            equivalences_as_lists.append(list(eachset))
        propagated_equivalences = _coalesce(equivalences_as_lists, [] )
        if self.debug: 
            print("Inside Component Labeler --- propagated equivalences at level %d: %s" % (level,propagated_equivalences))
        all_labels_in_propagated_equivalences = set()
        for eachlist in propagated_equivalences:
            all_labels_in_propagated_equivalences.update(eachlist)
        all_labels_set = set(range(1,current_componentID))
        labels_not_used_in_equivalences = all_labels_set - all_labels_in_propagated_equivalences
        number_of_components = len( propagated_equivalences ) + len(labels_not_used_in_equivalences)
        if self.debug: 
            print("\nInside Component Labeler --- number of components at level %d: %d " % (level, number_of_components))
        self.level_vs_number_of_components[level] = number_of_components
        label_mappings = {}
        mapped_label = start_label
        for equiv_list in propagated_equivalences:
            for label in equiv_list:
                label_mappings[label] = mapped_label   
            mapped_label += 1
        for label in labels_not_used_in_equivalences:
            label_mappings[label] = mapped_label
            mapped_label += 1         
        for i in range(0, height):
            for j in range(0, width):
                if componentID_array[(i,j)] != 0:
                    componentID_array[(i,j)] = label_mappings[componentID_array[(i,j)]]
            self.componentID_array_dict[level] = componentID_array

    def _make_blob_dictionary_at_one_Z_level(self, level):
        componentID_array = self.componentID_array_dict[level]
        height, width = componentID_array.shape        
        number_of_components = self.level_vs_number_of_components[level]
        self.blob_dictionary_by_level_for_Z[level] = {}
        for blob_index in self.label_pool_at_level[level]:
            blob_array = numpy.zeros((height, width), dtype="int")
            for i in range(0, height):
                for j in range(0, width):
                    if componentID_array[(i,j)] == blob_index:
                        blob_array[(i,j)] = 1
            self.blob_dictionary_by_level_for_Z[level][blob_index] = blob_array

    def _unit_dilation_of_marker_in_its_blob(self, input_array, marker_index, iter_index):
        (width,height) = self.data_im.size
        dilated_array = input_array.copy()
        componentID_array = self.componentID_array
        blob_index_for_marker = self.marks_to_blobs_mapping_dict[marker_index]
        change_made = 0
        for j in range(0,height):
            for i in range(0,width):
                if input_array[(i,j)] != 0:
                    if ( ( (j+1) >= 0 and (j+1) < width  )  and input_array[(i,j+1)] == 0 ) or \
                       ( ( (j-1) >= 0 and (j-1) < width  )  and input_array[(i,j-1)] == 0 ) or \
                       ( ( (i-1) >= 0 and (i-1) < height )  and input_array[(i-1,j)] == 0 ) or \
                       ( ( (i+1) >= 0 and (i+1) < height )  and input_array[(i+1,j)] == 0 ):
                        for l in range(-1,2):
                            for k in range(-1,2):
                                 if componentID_array[(i+k,j+l)] == blob_index_for_marker:
                                     if dilated_array[(i+k,j+l)] == 0:
                                         change_made = 1
                                         dilated_array[(i+k,j+l)] = iter_index
        if change_made == 0: return None
        return dilated_array

    def _unit_erosion_of_marker_in_its_blob(self, input_array, marker_index):
        (width,height) = self.data_im.size
        eroded_array = numpy.zeros((height, width), dtype="int")
        for j in range(0,height):
            for i in range(0,width):
                if ( input_array[(i,j)] == 1 ):            
                    input_pixels_at_unit_ele_offsets_all_okay = 1
                    for l in range(-1,2):
                        for k in range(-1,2):
                            if j+l >= 0 and j+l < width and i+k >= 0 and i+k < height:                            
                                if input_array[(i+k,j+l)] == 0:  
                                    input_pixels_at_unit_ele_offsets_all_okay = 0
                                    break
                        if iinput_pixels_at_unit_ele_offsets_all_okay == 0:
                            break
                if input_pixels_at_struct_ele_offsets_all_okay == 1:
                    eroded_array[(i,j)] = 1
                image_pixels_at_struct_ele_offsets_all_okay = 1
        return eroded_array

    def _make_blob_dictionary(self):
        width,height = self.data_im.size
        componentID_array = self.componentID_array        
        number_of_components = self.number_of_components
        for blob_index in range(1,number_of_components+1):
            blob_array = numpy.zeros((height, width), dtype="int")
            for j in range(0, height):
                for i in range(0, width):
                    if componentID_array[(i,j)] == blob_index:
                        blob_array[(i,j)] = 1
            self.blob_dictionary[blob_index] = blob_array.copy()
        self._compute_center_and_diameter_upper_bound_for_blobs()

    def _make_blob_dictionary_for_binary_arrays(self):
        '''
        This version is meant specifically for the case when a binary pattern is defined
        directly in a numpy array.  Additionally, this method sets a blob to a list of
        pixel coordinates in the blob.
        '''
        componentID_array = self.componentID_array        
        height,width = componentID_array.shape
        number_of_components = self.number_of_components
        for blob_index in range(1,number_of_components+1):
            blob_array = numpy.zeros((height, width), dtype="int")
            blob_pixel_list = []
            for i in range(0, height):
                for j in range(0, width):
                    if componentID_array[(i,j)] == blob_index:
                        blob_pixel_list.append((i,j))
            self.blob_dictionary[blob_index] = blob_pixel_list

    def _make_blob_dictionary_for_binary_arrays_with_component_labels(self):
        '''
        This version is meant specifically for the case when a binary pattern is component
        labeled NOT by the coalesence based _connected_components_for_binary_array() but by
        the dictionary pointer based _connected_components_for_binary_array_using_dict_pointers().
        The former gives consecutively increasing integer labels to the blobs.  On the
        other hand, the latter gives integer labels based on a tree of equivalence pointers ---
        an approach that is a nod to the union-find data data structure.   Note that each 
        blob is a list of pixel coordinates in that blob.
        '''
        componentID_array = self.componentID_array        
        height,width = componentID_array.shape
        number_of_components = self.number_of_components
        for blob_index in self.component_labels:
            blob_array = numpy.zeros((height, width), dtype="int")
            blob_pixel_list = []
            for i in range(0, height):
                for j in range(0, width):
                    if componentID_array[(i,j)] == blob_index:
                        blob_pixel_list.append((i,j))
            self.blob_dictionary[blob_index] = blob_pixel_list

    def _make_marks_dictionary(self):
        width,height = self.data_im.size
        markID_data_array = self.markID_data_array 
        number_of_marks = self.number_of_marks
        for marker_index in range(1,number_of_marks+1):
            marker_array = numpy.zeros((height, width), dtype="int")
            for j in range(0, height):
                for i in range(0, width):
                    if markID_data_array[(i,j)] == marker_index:
                        marker_array[(i,j)] = 1
            self.marks_dictionary[marker_index] = marker_array.copy()
        self._construct_mapping_from_marks_to_blobs()
        self._check_marks_fit_in_blobs()
            
    def _return_binarized_image(self, openedimage):
        argimage = openedimage
        width,height = argimage.size
        output_image =  Image.new("1", (width,height), 0)
        for j in range(0, height):
            for i in range(0, width):
                if argimage.getpixel((i,j)) >= 128:
                    output_image.putpixel((i,j), 255)
                else:
                    output_image.putpixel((i,j), 0)
        return output_image

    def _binarize_marks(self):
        open_marker_image = Image.open(self.marker_image_file_name)
        marker_image_data = open_marker_image.convert("L").convert("1")
        width,height = marker_image_data.size
        output_image =  Image.new("1", (width,height), 0)
        for j in range(0, height):
            for i in range(0, width):
                if marker_image_data.getpixel((i,j)) >= 128:
                    output_image.putpixel((i,j), 255)
                else:
                    output_image.putpixel((i,j), 0)
        self.marker_image_data = output_image
        if self.debug: 
            self.displayImage3(output_image) 

    # Assumes that the connected_components() has already been called
    # on the marks image produced by mark_blobs() method.  So we should
    # already have a numpy array called markID_data_array.
    def _construct_mapping_from_marks_to_blobs(self):
        number_of_components = self.number_of_components
        number_of_marks = self.number_of_marks
        marker_image = self.marker_image_data
        width,height = marker_image.size
        markID_data_array = self.markID_data_array
        indexed_mark_array = numpy.zeros((height, width), dtype="int")
        for mark_index in range(1, number_of_marks+1):
            mark_posX = 0
            mark_posY = 0
            how_many_pixels_in_mark = 0
            for i in range(0, height):
                for j in range(0, width):
                    if markID_data_array[(i,j)] == mark_index:
                        how_many_pixels_in_mark += 1
                        mark_posX += j
                        mark_posY += i
            posX = int(mark_posX)/how_many_pixels_in_mark
            posY = int(mark_posY)/how_many_pixels_in_mark
            componentID_array = self.componentID_array        
            marked_component_index = componentID_array[(posY,posX)]
            if self.debug:
                print("Identity of image blob requested by the mark indexed %d is %d" % (mark_index, marked_component_index))
            self.marks_to_blobs_mapping_dict[mark_index] = marked_component_index
            component_image = Image.new("1", (width,height), 0)        
            for i in range(0, height):
                for j in range(0, width):
                    if componentID_array[(i,j)] == marked_component_index:
                        component_image.putpixel((j,i), 255)
            self.displayImage3(component_image, "Displaying The Blob Selected (close window when done viewing)")
            output_image_name = "_component_image_for_mark_indexed_" + str(mark_index) + ".jpg"
            component_image.save( output_image_name )
        self._construct_mapping_from_blobs_to_marks()

    def _dilate_for_unittest(self, structuring_element_rad):
        argimage = self.data_im
        (width,height) = argimage.size
        im_out =  Image.new("1", (width,height), 0)
        a = structuring_element_rad
        for j in range(0,height):
            for i in range(0,width):
                if argimage.getpixel((i,j)) != 0:            
                    for l in range(-a,a+1):
                        for k in range(-a,a+1):
                            if j+l >= 0 and j+l < width and i+k >= 0 and i+k < height:
                                im_out.putpixel((i+k,j+l), 255) 
        im_out.save("_dilation.jpg")
        self.displayImage(im_out, "Dilated Pattern")
        return im_out

    def _construct_mapping_from_blobs_to_marks(self):
        for blob_index in self.blob_dictionary.keys():
            list_of_marks_for_blob = []
            for mark_index in self.marks_to_blobs_mapping_dict.keys():
                if self.marks_to_blobs_mapping_dict[mark_index] == blob_index:
                    list_of_marks_for_blob.append(mark_index)
            self.blobs_to_marks_mapping_dict[blob_index] = list_of_marks_for_blob

    def _check_marks_fit_in_blobs(self):
        for ii in self.marks_dictionary:
            mark = self.marks_dictionary[ii]
            relevant_blob_index = self.marks_to_blobs_mapping_dict[ii]
            blob = self.blob_dictionary[relevant_blob_index]
            height,width = mark.shape
            for j in range(0,height):
                for i in range(0,width):
                    if blob[(i,j)] == 0:
                        mark[(i,j)] = 0
            self.marks_dictionary[ii] = mark  

    def _callback(self,arg):
        arg.destroy()

    def _get_marks_for_one_region(self, region_index):
        global region_marker_image
        region_marker_index = region_index
        mw = Tkinter.Tk() 
        mw.title("Mark Region " + str(region_index) + " by clicking CLOCKWISE in it  (Must SAVE before Exit)")
        width,height = self.original_im.size
        data_image_width, data_image_height = self.data_im.size  
        display_x,display_y = None,None
        screen_width,screen_height = mw.winfo_screenwidth(),mw.winfo_screenheight()
        if screen_width <= screen_height:
            display_x = int(0.5 * screen_width)
            display_y = int(display_x * (height * 1.0 / width))            
        else:
            display_y = int(0.5 * screen_height)
            display_x = int(display_y * (width * 1.0 / height))
        self.display_size = (display_x,display_y)
        mw.configure(height = display_y, width = display_x) 
        mw.resizable( 0, 0 )  
        display_im = self.original_im.copy()
        display_im = display_im.resize((display_x,display_y), Image.ANTIALIAS)
        mark_scale_x = data_image_width / (1.0 * display_x)
        mark_scale_y = data_image_height / (1.0 * display_y)
        self.marks_scale = (mark_scale_x,mark_scale_y)
        # Even though the user will mark an expanded version of the image, the 
        # markers themselves will be stored in images of size the original data
        # image:
        region_marker_image =  Image.new("1", (display_x, display_y), 0)        
        region_marker_image_file_name = "_region__" + str(region_index) + "__markers_for_" + self.data_im_name
        photo_image = ImageTk.PhotoImage(display_im)
        canvasM = Tkinter.Canvas( mw,   
                                  width = display_x,
                                  height =  display_y,
                                  cursor = "crosshair" )  
        canvasM.pack( side = 'top' )   
        frame = Tkinter.Frame(mw)  
        frame.pack( side = 'bottom' ) 
        Tkinter.Button( frame, 
                        text = 'Save', 
                        command = lambda: self._resize_and_save(region_marker_image, data_image_width, data_image_height, region_marker_image_file_name)
                      ).pack( side = 'left' )  
        Tkinter.Button( frame,  
                        text = 'Exit',
                        command = lambda: mw.destroy()
                      ).pack( side = 'right' )  
        canvasM.bind("<Button-1>", lambda e: self._region_marker(e, region_index, data_image_width, data_image_height)) 
        canvasM.create_image( 0,0, anchor=NW, image=photo_image)
        canvasM.pack(fill=BOTH, expand=1)
        mw.mainloop()       

    def _make_new_valleys_from_region_marks(self):
        width,height = self.data_im.size
        (scale_x,scale_y) = self.marks_scale
        for region_index in self.region_marks_centers:
            list_of_marks = self.region_marks_centers[region_index]
            if self.debug:
                print("\n\nFor region %d the marks before scaling are at: %s" % (region_index, list_of_marks))
            list_of_marks = [(int(item[0]*scale_x), int(item[1]*scale_y)) for item in list_of_marks]
            if self.debug:
                print("For region %d the marks after scaling are at: %s" % (region_index, list_of_marks))
            valley_array_for_region = numpy.ones((height, width), dtype="int")
            for x in range(0, width):
                for y in range(0, height):
                    number_of_crossings = 0
                    raster_line = (0,y,x,y)
                    for l in range(0,len(list_of_marks)-1):
                        line = (list_of_marks[l][0],list_of_marks[l][1],list_of_marks[l+1][0],list_of_marks[l+1][1])
                        if _line_intersection(raster_line, line):
                            number_of_crossings += 1
                    last_line = (list_of_marks[l+1][0],list_of_marks[l+1][1],list_of_marks[0][0],list_of_marks[0][1])
                    number_of_crossings += _line_intersection(raster_line, last_line)
                    if number_of_crossings % 2 == 1:
                        valley_array_for_region[(y,x)] = 0
            self.marked_valley_for_region[region_index] = valley_array_for_region
            self._display_and_save_binary_array_as_image(valley_array_for_region, "_binarized_valley_created_by_user_" + str(region_index) + "  (close window when done viewing)")

    def _compute_center_and_diameter_upper_bound_for_blobs(self):
        width,height = self.data_im.size
        for blob_index in self.blob_dictionary.keys():
            blob = self.blob_dictionary[blob_index]
            xmin,xmax = width,0
            ymin,ymax = height,0
            for j in range(0,height):
                for i in range(0,width):
                    if blob[(i,j)] == 1:
                        if i < xmin: xmin = i
                        if i > xmax: xmax = i
                        if j < ymin: ymin = j
                        if j > ymax: ymax = j
            dia = int(math.sqrt( (xmax - xmin)**2 + (ymax - ymin)**2 ))
            xavg = xmin + int( (xmax - xmin) / 2.0 )
            yavg = ymin + int( (ymax - ymin) / 2.0 )
            self.blob_center_dict[blob_index] = (xavg,yavg)
            self.blob_dia_dict[blob_index] = dia

    def _unit_dilation_of_influence_zones(self, input_array, blob_array, set_of_marks_for_blob):
        '''
        This method dilates the 'input_array' by a unit pixel, the goal being to create the 
        influence zones for the 'input_array' blobs in the blobs of the 'blob_array'.  The 
        'input_array' corresponds to the labeled blobs for the water level at one Z level
        and 'blob_array' the level-set blobs at the next Z level.
        '''
        (width,height) = self.data_im.size
        dilated_array = input_array.copy()
        sorted_mark_labels = sorted(list(set_of_marks_for_blob), reverse=True)
        skiz_label = sorted_mark_labels[0] + 1
        change_made = 0
        for i in range(0,height):
            for j in range(0,width):
                if input_array[(i,j)] != 0:
                    if ( ( (j+1) >= 0 and (j+1) < width  )  and input_array[(i,j+1)] == 0 ) or \
                       ( ( (j-1) >= 0 and (j-1) < width  )  and input_array[(i,j-1)] == 0 ) or \
                       ( ( (i-1) >= 0 and (i-1) < height )  and input_array[(i-1,j)] == 0 ) or \
                       ( ( (i+1) >= 0 and (i+1) < height )  and input_array[(i+1,j)] == 0 ):
                        ij_label = input_array[(i,j)]
                        other_labels = set_of_marks_for_blob.difference(set([ij_label]))
                        for k in range(-1,2):
                            for l in range(-1,2):
                                 if blob_array[(i+k,j+l)] != 0:
                                     if dilated_array[(i+k,j+l)] == 0:
                                         test_bit = 1
                                         for s in range(-1,2):
                                             for t in range(-1,2):                                     
                                                 if dilated_array[(i+k+s,j+l+t)] in other_labels:
                                                     test_bit = 0
                                         if test_bit == 1:
                                             change_made = 1
                                             dilated_array[(i+k,j+l)] = dilated_array[(i,j)]
                                         else:
                                             dilated_array[(i+k,j+l)] = skiz_label
        if change_made == 0: return None
        return dilated_array

    def _connected_components_for_binary_array(self, array, area_threshold): 
        '''
        This connected components labeling implementation is meant specifically for binary patterns
        defined directly as numpy arrays.  The first parameter, 'array', must be a numpy array of
        binary blobs.  And the second and the third parameters, 'min_area_threshold' and 
        'max_area_threshold', are used to reject the blobs whose sizes are outside this range
        dictated by these two parameters.  The method returns the total number of blobs 
        meeting the area threshold condition.
        '''
        equivalences = set()
        height,width = array.shape
        componentID_array = numpy.zeros((height, width), dtype="int")
        markID_data_array = numpy.zeros((height, width), dtype="int")
        current_componentID = 1
        if array[(0,0)] == 1:            
            componentID_array[(0,0)] = current_componentID
            current_componentID += 1
        for i in range(1, width):
            if array[(0,i)] == 1:
                if componentID_array[(0,i-1)] != 0:
                    componentID_array[(0,i)] = componentID_array[(0,i-1)]
                else:
                    componentID_array[(0,i)] = current_componentID
                    current_componentID += 1
        for j in range(1, height):
            if array[(j,0)] == 1:
                if componentID_array[(j-1,0)] != 0:
                    componentID_array[(j,0)] = componentID_array[(j-1,0)]
                else:
                    componentID_array[(j,0)] = current_componentID
                    current_componentID += 1
        for i in range(1, height):
            for j in range(1, width):
                if componentID_array[(i-1,j)] != 0 and componentID_array[(i,j-1)] != 0: 
                    equivalences.add((componentID_array[(i-1,j)], componentID_array[(i,j-1)]))
                if array[(i,j)] == 1:            
                    if componentID_array[(i-1,j)] != 0:
                        componentID_array[(i,j)] = componentID_array[(i-1,j)]
                    elif componentID_array[(i-1,j-1)] != 0:
                        componentID_array[(i,j)] = componentID_array[(i-1,j-1)]
                    elif componentID_array[(i,j-1)] != 0:
                        componentID_array[(i,j)] = componentID_array[(i,j-1)]
                    else:
                        componentID_array[(i,j)] = current_componentID
                        current_componentID += 1
        if self.debug:
            print("\ncurrent_componentID: %d" % current_componentID)
            print("\nequivalences: %s" % str(equivalences))
        equivalences_as_lists = []
        all_labels_in_equivalences = set()
        for item in equivalences:
            equivalences_as_lists.append(item)
            all_labels_in_equivalences  = all_labels_in_equivalences.union(set(item))
        labels_not_in_equivalences = set(range(1,current_componentID)).difference(all_labels_in_equivalences)
        propagated_equivalences = _coalesce(equivalences_as_lists, [] )
        if self.debug:
            print("\npropagated equivalences: %s" % str(propagated_equivalences))
        number_of_components = len( propagated_equivalences )
        if self.debug:
            print("\nnumber of components from equivalences: %d" % number_of_components)
        label_mappings = {}
        mapped_label = 1
        for equiv_list in propagated_equivalences:
            for label in equiv_list:
                label_mappings[label] = mapped_label   
            mapped_label += 1
        for not_yet_mapped_label in list(labels_not_in_equivalences):
            label_mappings[not_yet_mapped_label] = mapped_label       
            mapped_label += 1
        if self.debug:
            print("Label mappings: %s" % str(label_mappings))
        for i in range(0, height):
            for j in range(0, width):
                if componentID_array[(i,j)] != 0:
                    componentID_array[(i,j)] = label_mappings[componentID_array[(i,j)]]
        self.number_of_components = mapped_label - 1
        if self.debug:
            print("\nModule: Number of components: %d" % (mapped_label - 1))
        self.componentID_array = componentID_array
        self._make_blob_dictionary_for_binary_arrays()
        blob_sizes = [len(self.blob_dictionary[x]) for x in self.blob_dictionary]
        if self.debug:
            print("\nblob sizes: %s" % str(sorted(blob_sizes, reverse=True)))
        new_blob_dictionary = {x : self.blob_dictionary[x] for x in self.blob_dictionary 
                                               if len(self.blob_dictionary[x]) > area_threshold}
        self.blob_dictionary = new_blob_dictionary
        num_retained_components = len(self.blob_dictionary)
        print("\nModule: Number of retained components: %d" % num_retained_components)
        return num_retained_components

    def _connected_components_for_binary_array_using_dict_pointers(self, array, min_area_threshold, max_area_threshold): 
        '''
        Whereas the previous version of the component labeling method uses the recursive coalescence
        algorithm for what is usually accomplished with a union-find data structure in component labeling,
        this version does the same with a much faster algorithm based on maintaining equivalence pointers
        stored in Python dictionary.  As in the previous method, this connected components labeling 
        implementation is meant specifically for binary patterns defined directly as numpy arrays.  The 
        first parameter, 'array', must be a numpy array of binary blobs.  And the second parameter, 
        'area_threshold', is used to reject the blobs when the blob area is less than this threshold.  
        The method returns the total number of blobs meeting the area threshold condition.
        '''
        equiv_tree = {}
        def find_root_in_euiv_tree(label):
            next_label = None
            while next_label is not -1:
                next_label = equiv_tree[label]
                prev_label = label
                label = next_label
            return prev_label
        height,width = array.shape
        componentID_array = numpy.zeros((height, width), dtype="int")
        markID_data_array = numpy.zeros((height, width), dtype="int")
        current_componentID = 1
        if array[(0,0)] == 1:            
            componentID_array[(0,0)] = current_componentID
            equiv_tree[current_componentID] = -1
            current_componentID += 1
        for i in range(1, width):
            if array[(0,i)] == 1:
                if componentID_array[(0,i-1)] != 0:
                    componentID_array[(0,i)] = componentID_array[(0,i-1)]
                else:
                    componentID_array[(0,i)] = current_componentID
                    equiv_tree[current_componentID] = -1
                    current_componentID += 1
        for j in range(1, height):
            if array[(j,0)] == 1:
                if componentID_array[(j-1,0)] != 0:
                    componentID_array[(j,0)] = componentID_array[(j-1,0)]
                else:
                    componentID_array[(j,0)] = current_componentID
                    equiv_tree[current_componentID] = -1
                    current_componentID += 1
        for i in range(1, height):
            for j in range(1, width):
                if componentID_array[(i-1,j)] != 0 and componentID_array[(i,j-1)] != 0: 
                    root1 = find_root_in_euiv_tree(componentID_array[(i-1,j)])
                    root2 = find_root_in_euiv_tree(componentID_array[(i,j-1)])
                    if root1 < root2:
                        equiv_tree[root2] = root1
                    elif root2 < root1:
                        equiv_tree[root1] = root2
                if array[(i,j)] == 1:            
                    if componentID_array[(i-1,j)] != 0:
                        componentID_array[(i,j)] = componentID_array[(i-1,j)]
                    elif componentID_array[(i-1,j-1)] != 0:
                        componentID_array[(i,j)] = componentID_array[(i-1,j-1)]
                    elif componentID_array[(i,j-1)] != 0:
                        componentID_array[(i,j)] = componentID_array[(i,j-1)]
                    else:
                        componentID_array[(i,j)] = current_componentID
                        equiv_tree[current_componentID] = -1
                        current_componentID += 1
        if self.debug:
            print("\ncurrent_componentID: %d" % current_componentID)
            print("equiv tree: %s" % str(equiv_tree))
            def check_equiv_tree():
                for i in range(1,current_componentID):
                    if not i in equiv_tree:
                        print("label %d does not exist in equiv_tree" % i)
                        sys.exit("we don't have all labels in equiv_tree of labels --- aborting")
            check_equiv_tree()        
            def check_equiv_tree2():
                for i in range(1,current_componentID):
                    if equiv_tree[find_root_in_euiv_tree(i)] != -1:
                        print("label %d does not exist in equiv_tree" % i)
                        sys.exit("we don't have all labels in equiv_tree of labels --- aborting")
            check_equiv_tree2()
        # Note that root labels, these are labels that point to -1 in equiv_tree, will be mapped to themselves 
        # in the mapped_labels dictionary:
        mapped_labels = {}
        for key in equiv_tree:
            mapped_labels[key] = find_root_in_euiv_tree(key)
        for i in range(0, height):
            for j in range(0, width):
                if componentID_array[(i,j)] != 0:
                    componentID_array[(i,j)] = mapped_labels[componentID_array[(i,j)]]
        self.component_labels = set(mapped_labels.values())
        self.number_of_components = len(self.component_labels)
        self.componentID_array = componentID_array
        self._make_blob_dictionary_for_binary_arrays_with_component_labels()
        blob_sizes = [len(self.blob_dictionary[x]) for x in self.blob_dictionary]
        if self.debug:
            print("\nblob sizes: %s" % str(sorted(blob_sizes, reverse=True)))
        new_blob_dictionary = {x : self.blob_dictionary[x] for x in self.blob_dictionary 
                             if (min_area_threshold < len(self.blob_dictionary[x]) < max_area_threshold)}
        self.blob_dictionary = new_blob_dictionary
        num_large_components = len(self.blob_dictionary)
        print("\nModule: Number of large components: %d" % num_large_components)
        return num_large_components


#_________________________  End of Watershed Class Definition ___________________________



#______________________________    Test code follows    _________________________________

if __name__ == '__main__': 

#    Watershed.gendata( "broken_rectangle", (200,200), (0,0), 0, "broken_rectangle1.jpg" )


    wtrshd = Watershed( 
#               data_image = "triangle1.jpg",
#               data_image = "rectangle1.jpg",
#               data_image = "broken_rectangle1.jpg",
#               data_image = "artpic3.jpg",
#               binary_or_gray_or_color = "binary",

               data_image = "orchid0001.jpg",
#               binary_or_gray_or_color = "gray",
               binary_or_gray_or_color = "color",
               size_for_calculations = 128,
               sigma = 1,
               level_decimation_factor = 16,   # Number of grad levels: 256 / this_factor
               gradient_threshold_as_fraction = 0.1,
               max_gradient_to_be_reached_as_fraction = 1.0,


#               data_image = "orchid0001.jpg",
#               binary_or_gray_or_color = "color",
#               size_for_calculations = 128,
#               sigma = 1,
#               level_decimation_factor = 16,   # Number of grad levels: 256 / this_factor
#               gradient_threshold_as_fraction = 0.1,
#               max_gradient_to_be_reached_as_fraction = 1.0,
#

               )


    wtrshd.extract_data_pixels()           
    print("Displaying the original image:")
    wtrshd.display_data_image()

    '''
    masked_segment_of_image = wtrshd.extract_rectangular_masked_segment_of_image(400, 1200, 300, 600)
    '''

    '''
    # This is a good demo of the LoG of an image calculated as the DoG.
    # The function compute_LoG_image() smooths the image with two 
    # Gaussians, one at sigma and the other at 1.20*sigma.  The difference
    # of the two is shown as the LoG of the image. 
    wtrshd.compute_LoG_image()
    '''

    '''
    # For demonstrating pure dilation and erosion of a binary image.
    dilated_image = wtrshd.dilate(5)
    wtrshd.erode(dilated_image, 5)
    '''


    '''
    # This is a demonstration of how dilations and erosions can be used to repair
    # small breaks in contours.
    dilated_image = wtrshd.dilation(wtrshd.data_im, 5)
    wtrshd.erosion( dilated_image, 5 )
    '''

    '''
    # For illustrating distance transformation vis-a-vis a set of marks
    # made by the user.
    wtrshd.connected_components("data")
    wtrshd.mark_blobs()
    wtrshd.connected_components("marks")
    print "\n\nStart dilating marked blob:\n\n"
    wtrshd.dilate_mark_in_its_blob(1)
    '''

    '''    
    # For illustrating the computation of Influence Zones (IZ) and the
    # the geodesic skeletons (SKIZ) where SKIZ stands for Skeleton by Zones
    # of Influence.  The SKIZ skeleton is a by-product of the call to the
    # last call shown below --- the call to compute_influence_zones_for_marks.
    # The SKIZ skeleton is shown with a pixel label that is one larger than the
    # number of marks inside an image blob.
    wtrshd.connected_components("data")
    wtrshd.mark_blobs()
    wtrshd.connected_components("marks")
    wtrshd.compute_influence_zones_for_marks()
    '''

    '''
    # For demonstrating MARKERLESS watersheds:
    print "Calculating the gradient image"
    wtrshd.compute_gradient_image()
    print "Computing Z levels in the gradient image"
    wtrshd.compute_Z_level_sets_for_gradient_image()
    print "Propagating influences:"
    wtrshd.propagate_influence_zones_from_bottom_to_top_of_Z_levels()
    wtrshd.display_watershed()
    wtrshd.extract_watershed_contours()
    wtrshd.display_watershed_in_color()
    wtrshd.display_watershed_contours_in_color()
    wtrshd.extract_segmented_blobs()
    '''


    '''
    # For demonstrating MARKER-BASED watersheds:
    wtrshd.mark_image_regions_for_gradient_mods()
    wtrshd.compute_gradient_image()
    wtrshd.modify_gradients_with_marker_minima()
    print("Computing Z levels in the gradient image")
    wtrshd.compute_Z_level_sets_for_gradient_image()
    print("Propagating influences:")
    wtrshd.propagate_influence_zones_from_bottom_to_top_of_Z_levels()
    wtrshd.display_watershed()
    wtrshd.display_watershed_in_color()
    wtrshd.extract_watershed_contours()
    wtrshd.display_watershed_contours_in_color()
    '''

