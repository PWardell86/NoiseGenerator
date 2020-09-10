from random import randint
from math import sqrt
from pyglet import shapes
class Noise:
    """
    Must specify the resolution, which is the size of each "pixel" or block that is drawn \n
    Must specify how many random points to generate \n
    Must specify the bounds of where to generate the random points \n
    Must specify the reach or max radius of each bubble. Goes from 0 to 255 / -1 \n
    Must specify the weight of each colour value. Values range from 0 to 1 \n
    Must specify the batch to draw the "pixels" to \n
    """
    def __init__(self, resolution: int, numOfPoints: int, windowDimensions: tuple, reach: int, RGB: tuple, batch):
        self._batch = batch
        self._width = windowDimensions[0]
        self._heightY = windowDimensions[1]
        self._heightZ = windowDimensions[2]
        self._points = []
        self._pixels = []
        self._RGB = RGB
        for point in range(0, numOfPoints):
            x = randint(0, self._width)
            y = randint(0, self._heightY)
            z = randint(0, self._heightZ)
            self._points.append([x, y, z])

        self._resolution = resolution
        self._reach = reach

    def clearPixels(self):
        """
        Clears the pixels from the internal list and deletes each "pixel" that was drawn to the screen
        """
        for pixel in self._pixels:
            pixel.delete()
        self._pixels.clear()

    def generatePixels(self, layer: int):
        """
        Generates the pixels based on the layer given. Calculates the distances and proper colour for the pixel
        """
        self.clearPixels()
        for x in range(0, self._width // self._resolution):
            for z in range(0, self._heightZ // self._resolution):
                colour = self.getPixelColour((x * self._resolution, layer, z * self._resolution))
                self._pixels.append(shapes.Rectangle(x * self._resolution, z * self._resolution, self._resolution, self._resolution, 
                                                    (int(colour * self._RGB[0]), int(colour * self._RGB[1]), int(colour * self._RGB[2])), 
                                                    self._batch))
        return self._pixels
        
    def generatePixels2D(self, layer: int):
        self.clearPixels()
        for x in range(0, self._width // self._resolution):
            colour = self.getPixelColour((x * self._resolution, layer))
            self._pixels.append(shapes.Rectangle(x * self._resolution, layer, self._resolution, self._resolution, 
                                (int(colour * self._RGB[0]), int(colour * self._RGB[1]), int(colour * self._RGB[2])), 
                                self._batch))

    def generatePixelData2D(self, layer: int):
        data = []
        for x in range(0, self._width // self._resolution):
            colour = self.getPixelColour((x * self._resolution, layer))
            data.append(colour)
        return data

    def distToClosestPoint(self, pixel: tuple):
        """
        Finds the distance from the specified pixel to the nearest point
        """
        if len(pixel) == 3:
            distance = self._width * self._heightZ
            for point in self._points:
                dX = pixel[0] - point[0]
                dY = pixel[1] - point[1]
                dZ = pixel[2] - point[2]
                distance = min(distance, sqrt(dX ** 2 + dZ ** 2 + dY ** 2))      
        else:
            distance = self._width * self._heightZ
            for point in self._points:
                dX = pixel[0] - point[0]
                dZ = pixel[1] - point[2]
                distance = min(distance, sqrt(dX ** 2 + dZ ** 2))
        return int(distance)            

    def getPixelColour(self, pixel: tuple):
        """
        Uses the distance to the closest point to colour the pixel
        """
        if len(pixel) == 3:
            distance = self.distToClosestPoint(pixel)
            colour = max(0, 255 - min(255 - self._reach, distance) - self._reach)
        
        else:
            distance = self.distToClosestPoint(pixel)
            colour = max(0, 255 - min(255 - self._reach, distance) - self._reach)
        return int(colour)