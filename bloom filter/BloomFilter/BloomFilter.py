import mmh3, math, bitarray, copy

class InputException(Exception):
    def __init__(self, message):
        self.message = message

class bloomfilter(object):
    """
    Introduction:
    A Bloom filter is a space-efficient probabilistic data structure, conceived by Burton Howard Bloom in 1970, that is used to test whether an element is a member of a set.

    -------------------------

    property description:
        param n: input and property, Estimated number of elements in the set

        param k: input and property, number of hash functions, default best k (is bln2, where b is introduced later)

        param m: property, bit array size

        param b: property, computed by m / n, best b is -(ln(ε) / (ln(2))^2)

        param actual_epsilon: property, bloom filter actual ε, when size of samples is near to n, actual ε is near to pre-defined ε

    -------------------------
    """
    def __init__(self, n=1e5, samples=None, epsilon=1e-3, k=0):
        """
        :param n: input and property, Estimated number of elements in the set
        :param samples: input, elements used for initializing the set, can be empty
        :param epsilon: input, pre-defined probability that the element is not present in the set but return true
        :param k: input and property, number of hash functions, default best k (is bln2, where b is introduced later)
        :param m: property, bit array size
        :param b: property, computed by m / n, best b is -(ln(ε) / (ln(2))^2)
        :param actual_epsilon: property, bloom filter actual ε, when size of samples is near to n, actual ε is near to pre-defined ε
        """
        # check input
        if samples is None:
            samples = []
        if n <= 0:
            raise InputException("n should be positive")
        if epsilon <=0 or epsilon >= 1:
            raise InputException("ε range should be (0, 1)")

        # initialize
        self.b = - math.log(epsilon) / (math.log(2)) ** 2
        self.k = math.ceil(self.b * math.log(2)) if k==0 else k
        self.n = n
        self.m = math.ceil(self.n * self.b)
        self.__bitarray = bitarray.bitarray('0' * self.m)
        self.__size = len(samples)

        # construct Bloom Filter
        for sample in samples:
            for seed in range(self.k):
                self.__bitarray[mmh3.hash(str(sample), seed=seed) % self.m] = 1

    def __add__(self, other):
        """
        :param other: add bloomfilter with other, e.g. bloomfilter + other
        :return: result
        """
        if isinstance(other, bloomfilter):
            # check input
            if other.k != self.k:
                raise InputException("bloom filters which have different hash functions cannot be added.")
            if other.m != self.m:
                raise InputException("bloom filters which have different size cannot be added.")


            # merge 2 different bloom filter and return
            tmp = copy.deepcopy(self)
            tmp.__size += other.__size
            for i in range(tmp.m):
                tmp.__bitarray[i] |= other.__bitarray[i]
            return tmp

        else:
            # add new element into bloom filter
            tmp = copy.deepcopy(self)
            tmp.__size += 1
            for seed in range(tmp.k):
                tmp.__bitarray[mmh3.hash(str(other), seed=seed) % tmp.m] = 1
            return tmp

    def __radd__(self, other):
        """
        :param other: add other with bloomfilter, e.g. other + bloomfilter
        :return: add result
        """
        return self.__add__(other)

    def __call__(self, samples=None):
        """
        :param samples: elements used for initializing
        :return: None
        """
        if samples is None:
            samples = []
        if self.__bitarray.any():
            raise InputException("Some elements have already been in this bloom filter. "
                                 "If user want to add elements into this bloom filter, "
                                 "please create a new one and add them together.")
        else:
            self.__size += len(samples)
            for sample in samples:
                for seed in range(self.k):
                    self.__bitarray[mmh3.hash(str(sample), seed=seed) % self.m] = 1

    def __contains__(self, item) -> bool:
        """
        :param item: element to be checked
        :return: true if the element is in the set, else false
        """
        for seed in range(self.k):
            if self.__bitarray[mmh3.hash(str(item), seed=seed) % self.m] == 0:
                return False
        return True

    def __len__(self) -> int:
        """
        :return: number of elements
        """
        return self.__size

    @property
    def actual_epsilon(self) -> float:
        """
        :return: The actual epsilon of current set, which is related to size of bitarray and number of elements
        """
        return 0.5 ** ((self.m / self.__size) * math.log(2)) if self.__size != 0 else 0

    def show(self):
        """
        :return: bit array in list form (e.g. [0, 1, 1, 1, 0, 0, ...])
        """
        return self.__bitarray.tolist()

if __name__=="__main__":
    bf1 = bloomfilter()
    help(bf1)

    """below are test code"""
# if __name__=="__main__":
#     # don't need to read this part of code, directly run it
#     print("-----start test1: basic-----")
#     n, sample_num, epsilon = 1e5, 1e5, 1e-3
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples = [random.randint(sample_low, int(sample_high)) for _ in range(int(sample_num))]
#     bf1 = bloomfilter(samples=samples)
#     print(f"bloom filter parameters: n: {bf1.n}, m: {bf1.m}, k: {bf1.k}, b: {bf1.b}")
#     print(f"element features: size: {len(bf1)}, range: {sample_low}~{sample_high}")
#     print(f"actual ε: {bf1.actual_epsilon}")
#     print(f"test contain: \n\tinput elements{samples[0:5]}")
#     for i in range(5):
#         print(f"\telement {samples[i]} is{'' if samples[i] in bf1 else ' not'} in bloom filter1")
#     test_elements = [random.randint(int(sample_high+1), 2*int(sample_high)) for _ in range(10)]
#     print(f"test not contain:\n\telements{test_elements}")
#     for i in range(5):
#         print(f"\telement {test_elements[i]} is{'' if test_elements[i] in bf1 else ' not'} in bloom filter1")
#
#     print("\n-----start test2: lower n-----")
#     n, sample_num, epsilon = 1e3, 1e5, 1e-3
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples = [random.randint(sample_low, int(sample_high)) for _ in range(int(sample_num))]
#     bf1 = bloomfilter(n=n, samples=samples)
#     print(f"bloom filter parameters: n: {bf1.n}, m: {bf1.m}, k: {bf1.k}, b: {bf1.b}")
#     print(f"element features: size: {len(bf1)}, range: {sample_low}~{sample_high}")
#     print(f"actual ε: {bf1.actual_epsilon}")
#     print(f"test contain: \n\tinput elements{samples[0:5]}")
#     for i in range(5):
#         print(f"\telement {samples[i]} is{'' if samples[i] in bf1 else ' not'} in bloom filter2")
#     test_elements = [random.randint(int(sample_high + 1), 2 * int(sample_high)) for _ in range(10)]
#     print(f"test not contain:\n\telements{test_elements}")
#     for i in range(5):
#         print(f"\telement {test_elements[i]} is{'' if test_elements[i] in bf1 else ' not'} in bloom filter2")
#
#     print("\n-----start test3: higher n-----")
#     n, sample_num, epsilon = 1e7, 1e5, 1e-3
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples = [random.randint(sample_low, int(sample_high)) for _ in range(int(sample_num))]
#     bf1 = bloomfilter(n=n, samples=samples)
#     print(f"bloom filter parameters: n: {bf1.n}, m: {bf1.m}, k: {bf1.k}, b: {bf1.b}")
#     print(f"element features: size: {len(bf1)}, range: {sample_low}~{sample_high}")
#     print(f"actual ε: {bf1.actual_epsilon}")
#     print(f"test contain: \n\tinput elements{samples[0:5]}")
#     for i in range(5):
#         print(f"\telement {samples[i]} is{'' if samples[i] in bf1 else ' not'} in bloom filter3")
#     test_elements = [random.randint(int(sample_high + 1), 2 * int(sample_high)) for _ in range(10)]
#     print(f"test not contain:\n\telements{test_elements}")
#     for i in range(5):
#         print(f"\telement {test_elements[i]} is{'' if test_elements[i] in bf1 else ' not'} in bloom filter3")
#
#     print("\n-----start test4: higher epsilon-----")
#     n, sample_num, epsilon = 1e5, 1e5, 1e-2
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples = [random.randint(sample_low, int(sample_high)) for _ in range(int(sample_num))]
#     bf1 = bloomfilter(samples=samples, epsilon=epsilon)
#     print(f"bloom filter parameters: n: {bf1.n}, m: {bf1.m}, k: {bf1.k}, b: {bf1.b}")
#     print(f"element features: size: {len(bf1)}, range: {sample_low}~{sample_high}")
#     print(f"actual ε: {bf1.actual_epsilon}")
#     print(f"test contain: \n\tinput elements{samples[0:5]}")
#     for i in range(5):
#         print(f"\telement {samples[i]} is{'' if samples[i] in bf1 else ' not'} in bloom filter4")
#     test_elements = [random.randint(int(sample_high + 1), 2 * int(sample_high)) for _ in range(10)]
#     print(f"test not contain:\n\telements{test_elements}")
#     for i in range(5):
#         print(f"\telement {test_elements[i]} is{'' if test_elements[i] in bf1 else ' not'} in bloom filter4")
#
#     print("\n-----start test5: lower epsilon-----")
#     n, sample_num, epsilon = 1e5, 1e5, 1e-4
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples = [random.randint(sample_low, int(sample_high)) for _ in range(int(sample_num))]
#     bf1 = bloomfilter(samples=samples, epsilon=epsilon)
#     print(f"bloom filter parameters: n: {bf1.n}, m: {bf1.m}, k: {bf1.k}, b: {bf1.b}")
#     print(f"element features: size: {len(bf1)}, range: {sample_low}~{sample_high}")
#     print(f"actual ε: {bf1.actual_epsilon}")
#     print(f"test contain: \n\tinput elements{samples[0:5]}")
#     for i in range(5):
#         print(f"\telement {samples[i]} is{'' if samples[i] in bf1 else ' not'} in bloom filter5")
#     test_elements = [random.randint(int(sample_high + 1), 2 * int(sample_high)) for _ in range(10)]
#     print(f"test not contain:\n\telements{test_elements}")
#     for i in range(5):
#         print(f"\telement {test_elements[i]} is{'' if test_elements[i] in bf1 else ' not'} in bloom filter5")
#
#     print("\n-----start test6: later initialization-----")
#     n, sample_num, epsilon = 1e5, 1e5, 1e-3
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples = [random.randint(sample_low, int(sample_high)) for _ in range(int(sample_num))]
#     bf1 = bloomfilter()
#     print(f"bloom filter parameters: n: {bf1.n}, m: {bf1.m}, k: {bf1.k}, b: {bf1.b}")
#     print(f"element features: size: {len(bf1)}, range: {sample_low}~{sample_high}")
#     print(f"initial empty bloom filter(first 20): {bf1.show()[0:20]}")
#     bf1(samples=[])
#     print(f"call and add 0 element bloom filter(first 20): {bf1.show()[0:20]}")
#     bf1(samples=samples)
#     print(f"call and add {sample_num} elements bloom filter(first 20): {bf1.show()[0:20]}")
#     try:
#         print("add again:")
#         bf1(samples=samples)
#     except InputException as e:
#         print(f"\t{e.message}")
#
#     print("\n-----start test7: merge-----")
#     n, sample_num, epsilon = 1e5, 1e5, 1e-3
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples1 = [random.randint(sample_low, int(sample_high / 3)) for _ in range(int(sample_num / 3))]
#     samples2 = [random.randint(int(sample_high / 3) + 1, int(2 * sample_high / 3)) for _ in range(int(sample_num / 3))]
#     samples3 = [random.randint(int(2 * sample_high / 3) + 1, int(sample_high)) for _ in range(int(sample_num / 3))]
#     bf1 = bloomfilter(samples=samples1)
#     bf2 = bloomfilter(samples=samples2)
#     try:
#         print("merge different k:")
#         bf3 = bloomfilter(samples=samples1, epsilon=0.1*epsilon)
#         bf1 = bf1 + bf3
#     except InputException as e:
#         print(f"\t{e.message}")
#     try:
#         print("merge different m:")
#         bf4 = bloomfilter(n=10*n, samples=samples1)
#         bf1 = bf4 + bf1
#     except InputException as e:
#         print(f"\t{e.message}")
#     bf5 = bloomfilter(samples=samples3)
#     bf6 = bf1 + bf2 + bf5
#     bf6 += bf2
#     print("successfully execute sequetial add & self add")
#     print(f"merged bloom filter parameters: n: {bf6.n}, m: {bf6.m}, k: {bf6.k}, b: {bf6.b}")
#     print(f"element features: size: {len(bf6)}, range: {sample_low}~{sample_high}")
#     print(f"actual ε: {bf6.actual_epsilon}")
#     tmp_sample = samples1[0:5] + samples2[0:5] + samples3[0:5]
#     print(f"test contain: \n\tinput elements{tmp_sample}")
#     for i in range(15):
#         print(f"\telement {tmp_sample[i]} is{'' if tmp_sample[i] in bf6 else ' not'} in bloom filter7")
#     print(f"test contain in 7 not in 1:\n\telements{samples2[0:5]}")
#     for i in range(5):
#         print(f"\telement {samples2[i]} is{'' if samples2[i] in bf6 else ' not'} in bloom filter7")
#         print(f"\telement {samples2[i]} is{'' if samples2[i] in bf1 else ' not'} in bloom filter1")
#
#     print("\n-----start test8: add new element-----")
#     n, sample_num, epsilon = 1e5, 1e5, 1e-3
#     sample_low, sample_high = 0, 1e5
#     print(f"create randomly n: {n}, samples number: {sample_num}, ε:{epsilon}")
#     samples1 = [random.randint(sample_low, int(sample_high)) for _ in range(int(sample_num))]
#     bf1 = bloomfilter(samples=samples1)
#     add = 1e7
#     print(f"bloom filter parameters: n: {bf1.n}, m: {bf1.m}, k: {bf1.k}, b: {bf1.b}")
#     print(f"element features: size: {len(bf1)}, range: {sample_low}~{sample_high}")
#     print(f"actual ε: {bf1.actual_epsilon}")
#     print(f"\telement {add} is{'' if add in bf1 else ' not'} in bloom filter8")
#     print(f"after add new element: ")
#     bf2 = bf1 + add
#     print(f"\telement {add} is{'' if add in bf2 else ' not'} in bloom filter8")
