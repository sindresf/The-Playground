#use numpy built-ins for this, gotta be some
def total_compare_error(array1,array2):
    error = 0.0
    for i,j in zip(array1,array2):
        error += abs(i - j)
    return error

def avg_compare_error(array1,array2):
    tot_error = total_compare_error(array1,array2)
    return tot_error / len(array1)

def total_squared_compare_error(array1,array2):
    error = 0.0
    for i,j in zip(array1,array2):
        error += abs(i - j) ** 2
    return error

def avg_squared_compare_error(array1,array2):
    tot_error = total_squared_compare_error(array1,array2)
    return tot_error / len(array1)