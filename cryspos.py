from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations
from sympy import Symbol,N

import numpy as np
import os

class cryspos:
	def __init__(self):
		if os.path.isdir('../cryspos_storage'):
			pass
		else:
			print("Running collector.sh")
			os.system("chmod +x collector.sh")
			os.system("./collector.sh")


	def space_group_to_positions(self,space_group,wyckoff_number,a=0,b=0,c=0):
		'''This function takes the space group and the designated wyckoff number to give the atomic positions using crystal units as placements'''
		group_file = self.gather_pos(space_group,wyckoff_number)

		transformations = standard_transformations
		x = Symbol("x")
		y = Symbol("y")
		z = Symbol("z")

		for i in group_file:
			pos = i.split(', ')
			counter = 0
			for j in pos:
				eq = parse_expr(j, transformations=transformations)
				if 'x' in j:
					pos[counter] = float(eq.subs(x,a))
				elif 'y' in j:
					pos[counter] = float(eq.subs(y,b))
				elif 'z' in j:
					pos[counter] = float(eq.subs(z,c))
				else:
					pos[counter] = N(pos[counter])

				counter+=1
			pos = self.recursive_boundaries(pos)
			print(pos)


	def recursive_boundaries(self,positions):
		'''If an atomic position is more than one, it will return that within the boundary'''
		for i in np.arange(0,len(positions)):
			if positions[i]>=1:
				positions[i]=positions[i]-1
			elif positions[i]<0:
				positions[i]=positions[i]+1

		return positions


	def gather_pos(self,space_group,wyckoff_number):
		'''Goes into the proper directory and takes the file information'''
		space_group_file = np.loadtxt('../cryspos_storage/{}.txt'.format(space_group),dtype=str,delimiter='/n',skiprows=18)
		wyckoff_group_file = []

		for i in space_group_file:
			if i[0].isalnum() and len(wyckoff_group_file):
				break

			if wyckoff_number in i or len(wyckoff_group_file):
				wyckoff_group_file.append(i.strip())
			
		return wyckoff_group_file[1:]


	def position_to_space_group(self,positions,tolerance):
		'''Given a set of atomic positions, this function will look through each space group and see if it fits given a tolerance'''
		pass
