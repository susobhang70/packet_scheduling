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
	a = [] 							# input port pointers
	g = []							# output port pointers
	final_answer = []				# to store final answer

	for i in range(N):
		O.append([])				# empty lists for each input port
		final_answer.append([])		# empty lists for each input port for final answer
		a.append(1)					# input  port pointers initialized to 1st output port
		g.append(1)					# output port pointers initialized to 1st input  port

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
			print tabulate(([i+1, a[i], req[i], g[i]] for i in range(N)), 
					headers=['I/P Ports', 'I/P Pointers', 'O/P Ports', 'O/P Pointers'], tablefmt='fancy_grid')
			
			# Grant phase
			for i in range(N):
				for op in req[i]:
					accept[op - 1].append(i + 1)

			print
			print "Grant Phase"
			print tabulate(([i+1, g[i], accept[i], a[i]] for i in range(N)),
					headers=['O/P Ports', 'O/P Pointers', 'I/P Ports', 'I/P Pointers'], tablefmt='fancy_grid')

			# randomly pick from the input port requests
			for i in range(N):
				if accept[i]:
					try:
						accept[i] = sorted(p for p in accept[i] if p >= g[i])[0]
					except:
						accept[i] = min(accept[i])
					grant[accept[i] - 1].append(i + 1)

			print tabulate(([i+1, g[i], accept[i], a[i]] for i in range(N)),
					headers=['O/P Ports', 'O/P Pointers', 'I/P Ports', 'I/P Pointers'], tablefmt='fancy_grid')

			print
			print "Accept Phase"
			print tabulate(([i+1, a[i], grant[i], g[i]] for i in range(N)),
					headers=['I/P Ports', 'I/P Pointers', 'O/P Ports', 'O/P Pointers'], tablefmt='fancy_grid')

			# randomly pick from the input port requests
			for i in range(N):
				if grant[i]:
					try:
						grant[i] = sorted(p for p in grant[i] if p >= a[i])[0]
					except:
						grant[i] = min(grant[i])
					a[i] = (grant[i] % N) + 1			# update input port o/p pointer
					g[grant[i] - 1] = ((i + 1) % N) + 1 # update output port i/p pointer

					occupied_ports.append(grant[i])
					final_answer[i].append(grant[i])
					O[i].remove(grant[i])
					req[i] = []

			# remove occupied ports from the request list for the current round
			for i in range(N):
				for j in occupied_ports:
					try:
						req[i].remove(j)
					except:
						pass

			print tabulate(([i+1, a[i], grant[i], g[i]] for i in range(N)),
					headers=['I/P Ports', 'I/P Pointers', 'O/P Ports', 'O/P Pointers'], tablefmt='fancy_grid')

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