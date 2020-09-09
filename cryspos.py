import numpy as np
import os

class cryspos:
	def __init__(self):
	
		print("yo, we doin this\n")

		if os.path.isdir('../cryspos_storage'):
			print("You're good")
		else:
			print("You need to run collector.sh")
			os.system("chmod +x collector.sh")
			os.system("./collector.sh")


	def space_group_to_positions(self,space_group,wyckoff_number):
		'''This function takes the space group and the designated wyckoff number to give the atomic positions using crystal units as placements'''

		pass


	def gather_pos(self,space_group,wyckoff_number):
		'''Goes into the proper directory and takes the file information'''

		pass


	def position_to_space_group(self,positions,tolerance):
		'''Given a set of atomic positions, this'''
