import math
import time

# Fast inverse square root approximation
def fast_inverse_sqrt(x):
#    threehalfs = 1.5
#    x2 = x * 0.5
#    i = int(x)
#    y = float(x).hex() # Convert float to hexadecimal string
#    i = int(y, 16)  # Convert hex string to integer
    return 0x5f3759df - (int(x) >> 1)
#    y = float.fromhex(hex(i))
#    y = y * (threehalfs - (x2 * y * y))
#    return y

# Native math function method
def native_inverse_sqrt(x):
    return 1 / math.sqrt(x)

def speed_test(func, num_iterations=1000000):
    start_time = time.time()
    for _ in range(num_iterations):
        func(12345.6)
    end_time = time.time()
    return end_time - start_time

# Run the test
num_iterations = 1000000
fast_time = speed_test(fast_inverse_sqrt, num_iterations)
native_time = speed_test(native_inverse_sqrt, num_iterations)

print(f"Fast inverse square root took {fast_time:.6f} seconds for {num_iterations} iterations")
print(f"Native inverse square root took {native_time:.6f} seconds for {num_iterations} iterations")
