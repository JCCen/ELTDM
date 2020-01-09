import timeit
num_terations = 500
t = timeit.Timer(stmt="kcore_function.naive_core_dec(kcore_function.g, False)", setup="import kcore_function").timeit(number=num_terations)
print(t)