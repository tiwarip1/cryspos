from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations
from sympy import Symbol,N

import numpy as np
import os

class cryspos:
	def __init__(self):
		#Checks if you have the proper space groups stored, if not it gets it for you
		if os.path.isdir('../cryspos_storage'):
			pass
		else:
			print("Running collector.sh")
			os.system("chmod +x collector.sh")
			os.system("./collector.sh")


	def space_group_to_positions(self,space_group,wyckoff_number,x=0,y=0,z=0):
		'''This function takes the space group and the designated wyckoff number to give the atomic positions using crystal units as placements'''
		group_file = self.gather_pos(space_group,wyckoff_number)
		#Defining symbols and addition rules
		transformations = standard_transformations
		x1 = Symbol("x")
		y1 = Symbol("y")
		z1 = Symbol("z")

		result = []
		#Parses atomic positions with variables and turns them into numbers
		for i in group_file:
			pos = i.split(', ')
			counter = 0
			for j in pos:
				eq = parse_expr(j, transformations=transformations)
				if 'x' in j:
					pos[counter] = float(eq.subs(x1,x))
				elif 'y' in j:
					pos[counter] = float(eq.subs(y1,y))
				elif 'z' in j:
					pos[counter] = float(eq.subs(z1,z))
				else:
					pos[counter] = N(pos[counter],3)

				counter+=1
			pos = self.recursive_boundaries(pos)
			#print(pos)
			result.append(pos)

		return result


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

	
	def give_wyckoff_numbers(self,space_group):
		'''Reads a given files and tells you the wyckoff numbers associated with that space group from the file itself'''
		df = space_group_file = np.loadtxt('../cryspos_storage/{}.txt'.format(space_group),dtype=str,delimiter='/n',skiprows=18)
		
		wyckoff_list = []
		for i in df:
			if i[0].isnumeric():
				wyckoff_list.append(i[:i.find(' ')])

		return wyckoff_list


	def position_to_space_group(self,filepath,tolerance,file_type,x,y,z):
		'''Given a set of atomic positions, this function will look through each space group and see if it fits given a tolerance'''
		df = np.loadtxt(filepath,delimiter='/n',dtype=str)
		data = []
		#Only looks at real space unit cell in units of angstroms
		for i in df:
			if 'RECIP-PRIMVEC' in i:
				break
			elif 'CONVCOORD' in i or len(data):
				data.append(list(filter(None,i.split(' '))))
		
		#Identifies how many of each atom there are and goes from angstoms to crystals vectors
		atomic_numbers = {}
		transformed_data = []

		for i in data[2:]:
			#print(i)
			j = [float(item) for item in i]
			j[1]=N(j[1]/x,4)
			j[2]=N(j[2]/y,4)
			j[3]=N(j[3]/z,4)
			transformed_data.append(j)
			
			if i[0] not in atomic_numbers.keys():
				atomic_numbers[i[0]]=1
			else:
				atomic_numbers[i[0]]+=1

		#Finds all space group position files stored and iterates over them
		space_group_files = [f for f in os.listdir('../cryspos_storage/') if os.path.isfile(os.path.join('../cryspos_storage/', f))]

		for i in space_group_files:
			space_group = i[:i.find('.')]
			wyckoff_list = self.give_wyckoff_numbers(space_group)
			for j in wyckoff_list:
				for k in atomic_numbers.keys():
					if int(j[:-1])==int(k) or int(j[:-1])==int(k)*2 or int(j[:-1])==int(k)*3:
						print('it happened {} {}'.format(space_group,j))
						#pos = self.space_group_to_positions(space_group,j)

						
