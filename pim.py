#!/usr/bin/env python

import copy
from sys import exit
from tabulate import tabulate
from random import choice

def empty_list(input_list):
    """Recursively iterate through values in nested lists."""
    for item in input_list:
        if not isinstance(item, list) or not empty_list(item):
             return False
    return True

def main():
	'''Main'''
	print "Number of Input/Output ports (N):",
	N = int(input())				# N x N switch, number of i/p or o/p ports
	print "I/P Port (1-based index) \t [O/P Ports (space separated)]"

	O = []							# to store the output ports
	final_answer = []
	for i in range(N):
		O.append([])				# empty lists for each input port
		final_answer.append([])		# empty lists for each input port for final answer

	for i in range(N):
		# remove formatting
		raw = raw_input().lstrip().rstrip()
		input_port, raw = raw.split(' ', 1)
		raw = raw.lstrip('[').rstrip(']').lstrip().rstrip()
		input_port = int(input_port) # get the input port, which is the first of the line

		# check if the input port given is higher than the ports in the system
		if input_port > N:
			print "Input Port Number greater than number of I/P Ports"
			exit(0)

		output_ports = map(int, raw.split()) # take the space separated output ports for the corresponding i/p port

		# if all the output ports given is less than the number of output ports
		if not all(1 <= i <= N for i in output_ports):
			print "Output Port Number greater than number of O/P Ports"

		O[input_port - 1] = O[input_port - 1] + output_ports
	
	print
	print

	# Setting round counter to 1
	rounds = 1
	iteration_count = []

	while(1):

		# Setting iteration counter to 1
		iteration = 1

		occupied_ports = []

		req = copy.deepcopy(O)

		while(1):
			# Initialize accept and grant lists
			accept = []
			grant = []
			for i in range(N):
				grant.append([])
				accept.append([])

			print "------------------------------------------"
			print "Round %d Iteration %d" %(rounds, iteration)
			print "Request Phase"
			print tabulate(([i+1, req[i]] for i in range(N)), 
					headers=['I/P Ports', 'O/P Ports'], tablefmt='fancy_grid')
			
			# Grant phase
			for i in range(N):
				for op in req[i]:
					accept[op - 1].append(i + 1)

			print
			print "Grant Phase"
			print tabulate(([i+1, accept[i]] for i in range(N)),
					headers=['O/P Ports', 'I/P Ports'], tablefmt='fancy_grid')

			# randomly pick from the input port requests
			for i in range(N):
				try:
					accept[i] = choice(accept[i])
					grant[accept[i] - 1].append(i + 1)
				except:
					pass

			print tabulate(([i+1, accept[i]] for i in range(N)),
					headers=['O/P Ports', 'I/P Ports'], tablefmt='fancy_grid')

			print
			print "Accept Phase"
			print tabulate(([i+1, grant[i]] for i in range(N)),
					headers=['I/P Ports', 'O/P Ports'], tablefmt='fancy_grid')

			# randomly pick from the input port requests
			for i in range(N):
				try:
					grant[i] = choice(grant[i])
					occupied_ports.append(grant[i])
					final_answer[i].append(grant[i])
					O[i].remove(grant[i])
					req[i] = []
				except:
					pass

			for i in range(N):
				for j in occupied_ports:
					try:
						req[i].remove(j)
					except:
						pass

			print tabulate(([i+1, grant[i]] for i in range(N)),
					headers=['I/P Ports', 'O/P Ports'], tablefmt='fancy_grid')

			# check if requests are empty
			if empty_list(req):
				break

			iteration += 1

		iteration_count.append(iteration)
		
		# check if the solution has been reached
		if empty_list(O):
			break
		rounds += 1

	print
	print "-------------------------------------"
	print "Total Rounds:", rounds
	print tabulate(([i+1, iteration_count[i]] for i in range(len(iteration_count))),
			headers=['Rounds', 'Iterations'], tablefmt='fancy_grid')

if __name__ == '__main__':
	main()