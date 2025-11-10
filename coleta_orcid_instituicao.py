import os
import csv

final = [name for name in os.listdir('./csvs/') if name.startswith('final_')]

orcids = []
names = []
for name in final:
	with open(f'./csvs/'+name, 'r') as f:
		print(name)
		reader = csv.reader(f)
		first = True
		for entry in reader:
			if first:
				first = False
				orcid_ids = [entry.index('orientador')]
				for i in range(8):
					if f'avaliador{i+1}' in entry:
						orcid_ids.append(entry.index(f'avaliador{i+1}'))
				names_ids = [entry.index('orientador_filiação')]
				for i in range(8):
					if f'avaliador{i+1}_filiação' in entry:
						names_ids.append(entry.index(f'avaliador{i+1}_filiação'))
			else:
				orcids.extend([entry[idx] for idx in orcid_ids])
				names.extend([entry[idx] for idx in names_ids])
orcid_clean = []
names_clean = []
for i in range(len(orcids)):
	if not orcids[i] in orcid_clean:
		orcid_clean.append(orcids[i])
		names_clean.append(names[i])

with open('filiacao.csv', 'w') as f:
	f.write('orcid, filiacao\n')
	for orcid, name in zip(orcid_clean, names_clean):
		f.write(f'{orcid}, {name}\n')
	
