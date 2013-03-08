# Back-Propagation Neural Networks
# 
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Neil Schemenauer <nas@arctrix.com>

import math
import random
import string
import data
import pprint
random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1 # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no
        
        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum   
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        # output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns):
		results = []
		for p in patterns:
			results.append((p[0], self.update(p[0])))
		return results

    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('Output weights:')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=300, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        last_error = 0
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 100 == 0:
                print(error)
            if last_error == error:
				print('Error hasn\'t changed - breaking.')
				break
            last_error = error
			
def demo():
cube = data.load(['SPY', 'QQQ'], '20100101', '20130204')

spy_px = [cube.data[('SPY', 'adjclose')][dt] for dt in cube.get_dates()]
qqq_px = [cube.data[('QQQ', 'adjclose')][dt] for dt in cube.get_dates()]
minspy = min(spy_px)
maxspy = max(spy_px)
minqqq = min(qqq_px)
maxqqq = max(qqq_px)
spy_px = [(px - minspy) / (maxspy - minspy) for px in spy_px]
qqq_px = [(px - minqqq) / (maxqqq - minqqq) for px in qqq_px]

spy_inp = [[spy_px[j-i] for i in range(10, 0, -1)] for j in range(10, len(spy_px))]
spy_tar = [spy_px[i] for i in range(10, len(spy_px))]
qqq_inp = [[qqq_px[j-i] for i in range(10, 0, -1)] for j in range(10, len(qqq_px))]
qqq_tar = [qqq_px[i] for i in range(10, len(qqq_px))]
inp = np.array([z[0] + z[1] for z in zip(spy_inp, qqq_inp)])
tar = np.array([[z[0]] + [z[1]] for z in zip(spy_tar, qqq_tar)])
net = nl.net.newff([[0,1]]*20, [41,40,2])
#inp = np.array(spy_inp)
#tar = np.array([spy_tar]).reshape(len(inp), 1)
#net = nl.net.newff([[0,1]]*10, [51,2,1])
error = net.train(inp,tar,epochs=500, show=100, goal=0.02)
	
	
	returns = {}	
	for dt in cube.get_dates()[1:]:
		yesterday = cube.go_back(dt, 1)
		px_T = cube.data[('SPY', 'adjclose')][dt]
		px_Tm1 = cube.data[('SPY', 'adjclose')][yesterday]
		r = px_T / px_Tm1
		returns[dt] = px_T	
	maxreturn = max(returns.values())
	minreturn = min(returns.values())
	for k, v in returns.items():
		returns[k] = (v - minreturn) / (maxreturn - minreturn)
	
	xs = []
	ys = []
	pat = []
	dates = cube.get_dates()
	for dt in dates[11:]:		
		contents = [returns[cube.go_back(dt, x)] for x in range(10, 0, -1)]
		target = returns[dt]
		xs.append(contents)
		ys.append([target])
		pat.append([contents, [target]])
	
	import neurolab as nl
	import numpy as np	
	inp = np.array(xs)

	tar = np.array(ys)
	
	net = nl.net.newp([[-1,1],[-1,1],[-1,1],[-1,1],[-1,1],[-1,1],[-1,1],[-1,1],[-1,1],[-1,1]],1)	
	error = net.train(inp, tar, epochs=500, show=100)
	print 'error', error
	
	out = net.sim([inp[-1]])
	print 'out', out
	
	
if __name__ == '__main__':
    demo()