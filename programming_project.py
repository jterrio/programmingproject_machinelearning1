import xlrd
import json
from pprint import pprint







def error(b, m, data):
    error = 0;
    for i in range(0, len(data)):
        x = data[i].sqft
        y = data[i].price
        error += (y- (m*x+b)) ** 2
    return error / float(len(data))




def step(data, b, m, learning_rate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(data))
    for i in range(0, len(data)):
        x = data[i].sqft
        y = data[i].price
        b_gradient += -(2/N) * (y - ((m * x) + b)) #update b
        m_gradient += -(2/N) * x * (y - ((m * x) + b)) #update m
    b -= (learning_rate * b_gradient) #update b
    m -= (m) - (learning_rate * m_gradient) #update m
    return [b, m] #return to either send back or retrain


def gradient_descent_runner(data, init_b, init_m, learning_rate, num_iterations):
    b = init_b
    m = init_m
    for i in range(num_iterations):
        [b, m] = step(data, b, m, learning_rate) #train 1000 times
    return [b, m]



class House:

    def __init__(self, sqft, price, city, bedrooms, baths):
        self.sqft = sqft
        self.price = price
        self.city = city
        self.bedrooms = bedrooms
        self.baths = baths





def main():
    print("Opening file...") 
    workbook = xlrd.open_workbook("housing prices.xlsx") #Open the file
    sheet = workbook.sheet_by_index(0)
    print("Making houses...")
    houses = []
    for i in range(83): #create each object with the data by row
        houses.append(House(sheet.cell_value(i+1, 0), sheet.cell_value(i+1, 1), sheet.cell_value(i+1, 2), sheet.cell_value(i+1, 3), sheet.cell_value(i+1, 4)))
    learning_rate = 0.0001 #set learning rate
    init_b = 0 #y = mx + b - initial variables
    init_m = 0 #y = mx + b
    num_iterations = 1000 #how many times we want to iterate
    print("Doing Gradient Descent...")
    [b, m] = gradient_descent_runner(houses, init_b, init_m, learning_rate, num_iterations) #train
    print("After " + str(num_iterations) + " iterations, b = " + str(b) + ", m = " + str(m) + ".")
    
    


main()
