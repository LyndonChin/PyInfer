# Note: Python 2.x only
# using a non-generator

sum_of_first_n = sum(range(1000000))
print(sum_of_first_n)

# using a generator
sum_of_first_n = sum(xrange(1000000))
print(sum_of_first_n)
