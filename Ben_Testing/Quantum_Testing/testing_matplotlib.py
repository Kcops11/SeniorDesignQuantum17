import matplotlib.pyplot as plt
import numpy as np

def make_plot(slope):
    x = np.arange(1,10)
    y = slope*x+3
    plt.figure()
    plt.plot(x,y)

make_plot(2)
make_plot(3)



plt.figure()
# Generate plot1
plt.plot(range(10, 20))
# Show the plot in non-blocking mode
plt.show(block=False)

# create figure (will only create new window if needed)
plt.figure()
# Generate plot2
plt.plot(range(10, 20))
# Show the plot in non-blocking mode
plt.show(block=False)

...

# Finally block main thread until all plots are closed
plt.show()