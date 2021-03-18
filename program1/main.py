class domino:
	def __init__(self, top, bottom):
		self.top = top
		self.bottom = bottom
		can_lead = False
		if len(self.top) <= len(self.bottom):
			for i in range(0,len(self.top)):
				if self.top[i] == self.bottom[i]:
					can_lead = True
				else:
					can_lead = False
					break
		else:
			for i in range(0,len(self.bottom)):
				if self.bottom[i] == self.top[i]:
					can_lead = True
				else:
					can_lead = False
					break
		
		self.can_lead = can_lead

def init(domino_list):
	for k, v in domino_list.items():
		if v.can_lead:
			frontier[k] = v
			explored[k] = v
			ts = find_trailing(v)
			if ts[1] and output_form:
				print("ADDING STATE: +"+ts[0]+" to the Frontier\n")
			elif output_form:
				print("ADDING STATE: -"+ts[0]+" to the Frontier\n")
			
			
def goal_state(domino):
	if len(domino.top) == len(domino.bottom):
		for i in range(0,len(domino.top)):
			if domino.top[i] != domino.bottom[i]:
				return False
		return True
	else:
		return False

def get_next_dominos(domino_kv,domino_list):

	domino = domino_kv[1]
	result = find_trailing(domino)
	trailing_string = result[0]
	top_flag = result[1]
	next_list = []
	
	for k,v in domino_list.items():
		usable = True
		if top_flag and len(v.bottom) < len(trailing_string):
			length = len(v.bottom)
		elif not top_flag and len(v.top) < len(trailing_string):
			length = len(v.top)
		else:
			length = len(trailing_string)
		
		for i in range(0,length):
			if top_flag:
				if trailing_string[i] != v.bottom[i]:
					usable = False
					break
			else:
				if trailing_string[i] != v.top[i]:
					usable = False
					break
		if usable:
			next_list.append({k:v})		
	return next_list

def find_trailing(domino):
	trailing = ""
	
	if len(domino.top) <= len(domino.bottom):
		for i in range(len(domino.top),len(domino.bottom)):
			trailing = trailing + domino.bottom[i]
		return [trailing, 0]
	else:
		for i in range(len(domino.bottom), len(domino.top)):
			trailing = trailing + domino.top[i]
		return [trailing, 1]		
		
def get_child_node(currNode_kv, nextNode_kv):
	curdomino_name = currNode_kv[0]
	curdomino = currNode_kv[1]
	nextdomino_name = list(nextNode_kv.keys())[0]
	nextdomino = list(nextNode_kv.values())[0]
	top = curdomino.top + nextdomino.top
	bottom = curdomino.bottom + nextdomino.bottom
	child_v = domino(top,bottom)
	child_k = str(curdomino_name) + str(nextdomino_name)
	
	return [child_k, child_v]
	
def check_validity(domino):
	if len(domino.top) <= len(domino.bottom):
		for i in range(0,len(domino.top)):
			if domino.top[i] == domino.bottom[i]:
				valid = True
			else:
				valid = False
				break
	else:
		for i in range(0,len(domino.bottom)):
			if domino.bottom[i] == domino.top[i]:
				valid = True
			else:
				valid = False
				break
	return valid

def depth_limited_search(node, limit, domino_list):
	return recursive_dls(node,limit, domino_list)
	
def recursive_dls(node, limit,domino_list):
	limit_reached = False
	if goal_state(node[1]):
		return node
	if limit > maximum_states:
		#limit_reached = True
		return None
	else:
		#print(node[0])
		ts = find_trailing(node[1])
		if ts[1] and output_form:
			print("POPPING STATE: +"+ts[0]+"\n")
		elif output_form:
			print("POPPING STATE: -"+ts[0]+"\n")
		next_dominos = []
		next_dominos = get_next_dominos(node, domino_list)
		for x in next_dominos:
			childNode_kv = get_child_node(node, x)
			child_name = childNode_kv[0]
			child_domino = childNode_kv[1]
			if not check_validity(child_domino):
				continue
			if child_domino not in explored.values():
				explored[child_name] = child_domino
			#print(child_name)
			result = recursive_dls(childNode_kv, limit+1, domino_list)
			if not result:
				limit_reached = True
			elif result:
				return result
		if limit_reached:
			return None
		else:
			#no_solution
			return None

def iterative_deepening(frontier, limit, domino_list):
	goal_found = False
	limit_reached = False
	for node in frontier.items():
		ts = find_trailing(node[1])
		if ts[1] and output_form:
			print("STARTING STATE: +"+ts[0]+"\n")
		elif output_form:
			print("STARTING STATE: -"+ts[0]+"\n")
		result = depth_limited_search(node, limit, domino_list)
		if result:
			goal_found = True
			break
		else:
			limit_reached = True
	if goal_found:
		print("GOAL FOUND IN DFS")
		child_name = result[0]
		child_domino = result[1]
		solution_sequence = ""
		temp = child_name.split("D")
		for num in temp:
			if num == "":
				continue
			num = "D" + num + " "
			solution_sequence = solution_sequence + num
		print("Domino Sequence:")
		print(solution_sequence)
		print("String Produced:")
		print(child_domino.top)
		print(child_domino.bottom)
	elif limit_reached:
		print("limit reached")
	else:
		print("no solution")
	
	


maximum_size = int(input("Enter Max Size of Frontier:\n"))
maximum_states = int(input("Enter Max Number of States:\n"))
output_form = int(input("Output State Space? 1 or 0\n"))
number_of_dominos = int(input("Enter Number of Dominos:\n"))

domino_list = {}
frontier = {}
explored = {}
state_list = []

for i in range(0,number_of_dominos):
	domino_string = input("Enter Domino EX: 1. ab ba\n")
	domino_sides = domino_string.split(" ")
	D = domino(domino_sides[1], domino_sides[2])
	key = domino_sides[0]
	key = key.replace(".","")
	key = "D"+key
	domino_list[key] = D		

print("==============================================================")
print("Starting Breadth-First search")
print("==============================================================")
init(domino_list)
states = len(frontier)
goal_found = False
no_solution = False
limit_reached = False
frontier_full = False
while len(frontier) < maximum_size and states < maximum_states:
	if not frontier:
		print("Frontier Empty")
		no_solution = True
		break
	currNode = list(frontier.items())[0]
	del frontier[currNode[0]]
	ts = find_trailing(currNode[1])
	if ts[1] and output_form:
		print("REMOVING STATE: +"+ts[0]+" from the Frontier\n")
	elif output_form:
		print("REMOVING STATE: -"+ts[0]+" from the Frontier\n")
	next_dominos = []
	next_dominos = get_next_dominos(currNode,domino_list)
	for x in next_dominos:
		childNode_kv = get_child_node(currNode, x)
		child_name = childNode_kv[0]
		child_domino = childNode_kv[1]
		if not check_validity(child_domino):
			continue
		if child_domino not in explored.values() and child_domino not in frontier.values():
			if goal_state(child_domino):
				print("GOAL FOUND IN BFS")
				goal_found = True
				break
			states = states + 1
			explored[child_name] = child_domino
			frontier[child_name] = child_domino
			ts = find_trailing(child_domino)
			if ts[1] and output_form:
				print("ADDING STATE: +"+ts[0]+" to the Frontier\n")
			elif output_form:
				print("ADDING STATE: -"+ts[0]+" to the Frontier\n")

			if (len(frontier)) >= maximum_size:
				frontier_full = True;
				break
	if frontier_full:
		break
	if goal_found:
		break
if goal_found:
	solution_sequence = ""
	temp = child_name.split("D")
	for num in temp:
		if num == "":
			continue
		num = "D" + num + " "
		solution_sequence = solution_sequence + num
	print("Domino Sequence:")
	print(solution_sequence)
	print("String Produced:")
	print(child_domino.top)
	print(child_domino.bottom)
if no_solution:
	print("No Solution Possbile")
if states >= maximum_states:
	print("Maximum Number of States Reached")
if len(frontier) >= maximum_size:
	print("==============================================================")
	print("Maximum Frontier Size Reached. Moving to Depth-First search")
	print("==============================================================")
	iterative_deepening(frontier, states, domino_list)
