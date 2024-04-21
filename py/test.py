from dfo.algo import DFO
import cv2 as cv

img = cv.imread('gaussian.png')
# Convert the image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# def fitness_function(x):
#     return sum([i**2 for i in x])

# dfo = DFO(fitness_func=fitness_function, dims_range=[30,30,30], max_iter =1500, fitness_type='min')
dfo = DFO(fitness_matrix=gray)

dominant = dfo.run()
print(dominant)