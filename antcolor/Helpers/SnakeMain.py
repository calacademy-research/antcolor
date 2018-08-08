from Helpers import SnakeObj
import sys
import math
import numpy as np
import cv2

class SnakeMain(object):
    snake = SnakeObj
    progress = 0
    points = np.zeros
    visualize = False
    def load_image(self, file_to_load, visualizebool):
        # Loads the desired image
        # image = cv2.imread( file_to_load, cv2.IMREAD_COLOR )
        image = file_to_load
        # Creates the snake
        snake = SnakeObj.SnakeObj( image, closed = True )
        visualize = visualizebool

        # Window, window name and trackbars
        if(visualize):
            snake_window_name = "Snakes"
            controls_window_name = "Controls"
            cv2.namedWindow( snake_window_name )
            cv2.namedWindow( controls_window_name )
            cv2.createTrackbar( "Alpha", controls_window_name, math.floor( snake.alpha * 100 ), 100, snake.set_alpha )
            cv2.createTrackbar( "Beta",  controls_window_name, math.floor( snake.beta * 100 ), 100, snake.set_beta )
            cv2.createTrackbar( "Delta", controls_window_name, math.floor( snake.delta * 100 ), 100, snake.set_delta )
            cv2.createTrackbar( "W Line", controls_window_name, math.floor( snake.w_line * 100 ), 100, snake.set_w_line )
            cv2.createTrackbar( "W Edge", controls_window_name, math.floor( snake.w_edge * 100 ), 100, snake.set_w_edge )
            cv2.createTrackbar( "W Term", controls_window_name, math.floor( snake.w_term * 100 ), 100, snake.set_w_term )

        # Core loop
        while( True ):

            if(visualize):
                # Gets an image of the current state of the snake
                snakeImg = snake.visualize()
                # Shows the image
                cv2.imshow( snake_window_name, snakeImg )
            # Processes a snake step
            snake_changed = snake.step()
            self.progress+=1
            # Stops looping when ESC pressed
            k = cv2.waitKey(33)
            self.points = snake.points
            if self.progress > 30:
                break


        cv2.destroyAllWindows()
