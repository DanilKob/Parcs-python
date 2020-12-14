from Pyro4 import expose
import random


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n = self.read_input()

        # map

        a = []
        for i in range(n):
            a.append(random.randint(1, 1000000))

        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].convert_to_binary( a))

        # reduce
        reduced = self.myreduce(mapped)

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def convert_to_binary(array):

        N = len(array)
        result = []
        for i in range(N - 1):
            num = array[i]
            b = ""
            while num > 0:
                b = str(num % 2) + b
                num = num // 2
            result.append(b)

        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        return mapped[len(mapped) - 1].value

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
