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

	ranks = {}
	for v in victims_dict.keys():
		for _id in victims_dict[v]:
			if _id in ranks.keys():
				ranks[_id] += 1
			else:
				ranks[_id] = 1
	ranked_list = [] #list of lists that contain the _ids that occur at a given frequency
	#i.e. ranked_list[1] = the ids that occur once
	#	  ranked_list[4] = the ids that occur 4 times
	while len(ranked_list)-1 < len(victims_dict.keys()):
		ranked_list.append( [] )
	for _id in ranks.keys():
		ranked_list[ ranks[_id] ].append(_id)

	return ranked_list
					


if __name__ == "__main__":
	print ("[!] This class has no main, use main.py")