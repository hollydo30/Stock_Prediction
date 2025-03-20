"""
COMP 614
Homework 3: Stock Prediction
"""

import comp614_module3 as stocks
import random


def markov_chain(data, order):
    """
    Creates and returns a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the Markov chain

    returns: a dictionary that represents the Markov chain
    """
    markov_list = {}  
    
    tuple_list = []
    
    for index in range(len(data)-order):
        tuple1 = tuple ( data[index : index + order] )
        if tuple1 not in tuple_list:
            tuple_list.append(tuple1)  
    
    value_list = []

    for index in range(len(data)):
        if data[index] not in value_list:
            value_list.append(data[index]) 
    
    for tup in tuple_list:
        sum_count = 0  

        prop_list = {} 
        
        for index in range(len(data) - order):
            if data[index:(index+order)] == list(tup):
                sum_count += 1 
        
        for value in value_list:
            count = 0 
            for index in range(len(data) - order):
                if data[index:(index+order)] == list(tup) and data[index + order] == value:
                    count += 1
        
            if sum_count>0 and count > 0:  
                prop_list[value] = count / sum_count
                
        markov_list[tup] = prop_list 

    return markov_list    


def predict(model, last, num):
    """
    Predicts the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    predictions = []
    last_tuple = tuple(last)
    
    for dummy in range(num):
        if last_tuple in model:
            next_val = 0
            
            rand = random.random()
            cum_val = 0
            
            for item, val in model[last_tuple].items():
                cum_val = val + cum_val
                if rand < cum_val:
                    next_val = item
                    break
        else:
            next_val = random.randint(0,3)
            
        predictions.append(next_val)
        
        last_tuple = last_tuple + (next_val, ) 
        
        last_tuple = last_tuple[1:]
     
    return predictions


def mse(result, expected):
    """
    Calculates the mean squared error between two data sets. Assumes that the 
    two data sets have the same length.
    
    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    square_error = 0.0
    count = 0
    mean_square_error = 0.0
    sum_square = 0.0
    expected_list = []
    
    if isinstance(expected, dict):
        expected_list = list(expected.values())
    elif isinstance(expected, list):
        expected_list = expected
    else:
        expected_list = [expected]
    
    for index in range(len(result)):
        if not result or not expected_list or len(result) != len(expected_list):
            return 0.0
        else:
            error = result[index] - expected_list[index]
            square_error = error**2
            sum_square += square_error
            count += 1
            
    if len(result) > 0 and count > 0:
        mean_square_error = sum_square/count
        return mean_square_error
    else:
        return 0.0


def run_experiment(train, order, test, future, actual, trials):
    """
    Runs an experiment to predict the future of the test data based on the
    given training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    model = markov_chain(train, order)
    total = 0.0
    for dummy in range(trials):
        future1 = predict(model, test, future)
        total += mse(actual, future1)
    average = total/trials
        
    return average

    
def run():
    """
    Runs the stock prediction application. You should not modify this function!
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Load the training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Load the test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

        
# You may want to keep this call commented out while you're writing & testing
# your code. Uncomment it when you're ready to run the experiments.
run()
