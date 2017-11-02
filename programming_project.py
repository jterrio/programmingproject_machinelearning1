import xlrd
import json
from pprint import pprint







def error(pred_y, actual_y):
    return (pred_y - actual_y) ** 2




def step(data, W, learning_rate):
    y = 0
    for i in range(58):
        a = data[i].sqft * W[0]
        b = data[i].city * W[1]
        c = data[i].bedrooms * W[2]
        d = data[i].baths * W[3]
        pred_y = a + b + c + d
        diff_y = data[i].price - pred_y
        if diff_y >= 0: #check to see if we need to step up or step down
            y = 1
        else:
            y = -1
        #check to see if we are within 5% of the actual, if not: step
        if((pred_y < (data[i].price - (data[i].price * 0.05))) or (pred_y > (data[i].price + (data[i].price * 0.05))) ):
            W[1] = W[1] +  y * data[i].city * learning_rate
            W[2] = W[2] + y * data[i].bedrooms * learning_rate
            W[0] = W[0] + y * data[i].sqft * learning_rate
            W[3] = W[3] + y * data[i].baths * learning_rate
    return W
        


def gradient_descent_runner(data, init_b, init_m, learning_rate, num_iterations):
    W = [0, 0, 0, 0]
    for i in range(num_iterations):
        W = step(data, W, learning_rate) #train x number of times
    return W



class House:

    def __init__(self, sqft, price, city, bedrooms, baths):
        self.sqft = sqft
        self.price = price
        self.city = city
        self.bedrooms = bedrooms
        self.baths = baths



def test(data, W):
    mse = 0
    for i in range(25): #sum our error
        i = i + 58
        pred_y = (W[0] * data[i].sqft) + (W[1] * data[i].city) * (W[2] * data[i].bedrooms) * (W[3] * data[i].baths)
        mse += error(pred_y, data[i].price)
    return ((mse/25) ** (1/2))

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
    W = gradient_descent_runner(houses, init_b, init_m, learning_rate, num_iterations) #train
    print("After " + str(num_iterations) + " iterations, weights are: " + str(W[0]) + " " + str(W[1]) + " " + str(W[2]) + " " + str(W[3]))
    print("Testing...")
    mse = test(houses, W)
    print("Mean squared error = " + str(mse))

    #See how model classifies expensive and cheap houses vs reality
    exp_houses = 0
    chp_houses = 0
    for i in range(83):
        if houses[i].price > 500000:
            exp_houses += 1
        else:
            chp_houses += 1
    print("For threshold T of 500,000; " + str(exp_houses) + " expensive houses and " + str(chp_houses) + " cheap houses.")
    m_exp_houses = 0
    m_chp_houses = 0
    for i in range(83):
        pred_y = (W[0] * houses[i].sqft) + (W[1] * houses[i].city) * (W[2] * houses[i].bedrooms) * (W[3] * houses[i].baths)
        if(pred_y > 500000):
            m_exp_houses += 1
        else:
            m_chp_houses += 1
    print("Model predicts: " + str(m_exp_houses) + " expensive houses and " + str(m_chp_houses) + " cheap houses.")
    #calculate mean squared error
    mse = (((m_exp_houses - exp_houses) ** 2) + ((m_chp_houses - chp_houses) ** 2)) ** (1/2)
    print("Mean squared error = " + str(mse))
main()
