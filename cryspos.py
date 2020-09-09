import numpy as np
import os

class cryspos:
	def __init__(self):
	
		print("yo, we doin this\n")

		if os.path.isdir('../cryspos_storage'):
			pass
		else:
			print("Running collector.sh")
			os.system("chmod +x collector.sh")
			os.system("./collector.sh")


	def space_group_to_positions(self,space_group,wyckoff_number):
		'''This function takes the space group and the designated wyckoff number to give the atomic positions using crystal units as placements'''

		pass


	def gather_pos(self,space_group,wyckoff_number=False):
		'''Goes into the proper directory and takes the file information'''

		space_group_file = np.loadtxt('../cryspos_storage/{}.txt'.format(space_group),dtype=str,delimiter='/n',skiprows=18)
		wyckoff_group_file = []

		if not wyckoff_number:
			return space_group_file

		for i in space_group_file:
			if i[0].isalnum() and len(wyckoff_group_file):
				break

			if wyckoff_number in i or len(wyckoff_group_file):
				wyckoff_group_file.append(i.strip())
			
		return wyckoff_group_file[1:]


	def position_to_space_group(self,positions,tolerance):
		'''Given a set of atomic positions, this function will look through each space group and see if it fits given a tolerance'''

		pass
