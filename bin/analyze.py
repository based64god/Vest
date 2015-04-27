def unweighted_ranking(victims_dict):
	
	'''
	Parameters
	----------
	Dictionary that maps a victim's name to their list of friends

	Function
	--------
	Compares friend lists to find the frequency at which each name occurs

	Returns
	-------
	List of lists containing the ids with the most friends who are victims

	'''

	all_ids = []
	for v in victims_dict.keys(): #add all of the ids to a big list
		for _id in victims_dict[v]:
			all_ids.append(_id)
	all_ids = sorted(all_ids) #sort that list to count the occurances

	ranked_list = [] #list of lists that contain the ids that occur at a given frequency
	#i.e. ranked_list[1] = the ids that occur once
	#	  ranked_list[4] = the ids that occur 4 times

	#append empty lists to the ranking so that it can hold all of the occurances
	#	it must be the length of the number of victims because that is the most times an _id can appear
	while len(ranked_list)-1 < len(victims_dict.keys()): 
		ranked_list.append( [] )

	current_id = ""
	current_id_count = 0
	for _id in all_ids:
		if current_id != _id:
			ranked_list[ current_id_count ].append(current_id)
			current_id = _id
			current_id_count = 1
		else:
			current_id_count += 1

	return ranked_list
					


if __name__ == "__main__":
	print ("[!] This file has no main, use main.py")