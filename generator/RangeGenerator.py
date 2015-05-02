
def irange(num):
    i = 0
    while i < num:
        yield i
        i = i + 1

#the for loop will generate each i (i.e. 1,2,3,4,5, ...), add it to total, and throw it away
#before the next i is generated. This is opposed to iterating through range(...), which creates
#a potentially massive list and then iterates through it.
total = 0
for i in irange(100000):
    total += i
print(total)
