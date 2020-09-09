mkdir ../cryspos_storage

for i in {1..230};
do
	pyxtal_symmetry.py -s ${i} > ../cryspos_storage/${i}.txt;
done
