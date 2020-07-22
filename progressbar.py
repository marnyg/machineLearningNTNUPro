import time as t
import os
class ProgressBar:
    def __init__(self, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", eta = False):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd
        self.eta = eta
        self.starting_time = None
        self.current_time = None
        self.elapsed_time = None
        rows, columns = os.popen('stty size', 'r').read().split()
        self.length = int((int(columns) - len(self.suffix) - len(self.prefix) - len(self.printEnd)) * 3 / 4)
    
    def show(self, iteration):
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.total)))
        filledLength = int(self.length * iteration // self.total)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        if self.eta == True:
            self.show_eta(iteration)
        print('\r%s |%s| %s%% %s' % (self.prefix, bar, percent, self.suffix), end = self.printEnd)
        if iteration == self.total: 
            print()
    
    def set_suffix(self, suffix):
        self.suffix = suffix
        
    def show_eta(self, iteration):
        if iteration == 0:
            self.starting_time = t.time()
            self.suffix = '0 seconds'
        else:
            self.current_time = t.time()
            self.elapsed_time = self.current_time - self.starting_time
            
            avrg_time_per_iteration = self.elapsed_time / (iteration + 1)
            remaining_iterations = self.total - iteration
            #self.suffix = 'Average time per iteration: ' + str(avrg_time_per_iteration) + ' Remaining iterations: ' + str(remaining_iterations)
            remaining_time = remaining_iterations * avrg_time_per_iteration
            if remaining_time >= 0:
                minutes = int(remaining_time / 60)
                seconds = int(remaining_time % 60)
                self.suffix = str(minutes) + ' minutes ' + str(seconds) + ' seconds'
            else: 
                seconds = int(remaining_time % 60)
                self.suffix = str(seconds) + ' seconds'




