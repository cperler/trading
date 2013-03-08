from math import tanh

def dtanh(y):
	return 1.0 - y * s
	
class NN:
	def __init__(self, topography):
		self.topography = topography		
		self.nodes_per_layer = {}
		for layer, num_nodes in enumerate(self.topography):
			self.nodes_per_layer[layer] = [1.0] * num_nodes
		self.strengths={}
		for layer in range(0, len(self.topography)-1):
			for node_from in range(0, len(self.nodes_per_layer[layer])):
				for node_to in range(0, len(self.nodes_per_layer[layer+1])):
					if layer+1 == len(self.topography)-1:
						self.strengths[((layer, node_from), (layer+1, node_to))] = 0.1
					else:
						self.strengths[((layer, node_from), (layer+1, node_to))] = 1.0
						
	def feedforward(self):
		

sample_data = [100 + i for i in range(0, 50)]
			
def main():
	
	
		
if __name__ == '__main__':
	main()