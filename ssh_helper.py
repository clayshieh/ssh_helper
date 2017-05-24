import os
import sys

user_home_path = os.path.expanduser("~")
config_path = user_home_path + "/.ssh/config"
parameter_names = ["HostName", "User", "Port"]

print "ssh config path: " + config_path
print

def preamble():
	if not os.path.isfile(config_path):
		print "Config file does not exist at" + config_path + " !"
		response = raw_input("Create now? (y/n) : ")
		if response.lower() == "n":
			sys.exit(0)

def find_exitsing_configs():
	existing_configs = {}
	with open(config_path, "r") as f:
		cur_host_name = None
		cur_host = {}
		for line in f:
			line = line.strip()
			#ignoring comments for now
			if line.startswith("#"):
				continue
			if (line.startswith("Host") and not line.startswith("HostName")):
				if not cur_host_name:
					cur_host_name = line.split()[1]
				else:
					existing_configs[cur_host_name] = cur_host
					cur_host_name = line.split()[1]
					cur_host = {}
			else:
				data = line.split()
				#last line is just a new line
				if len(data) == 2:
					cur_host[data[0]] = data[1]
	if len(existing_configs.keys()) == 0:
		if raw_input("No existing configs found, is this expected? (y/n) : ").lower() == "n":
			print ("Please check your config file format here: " + config_path)
			sys.exit(0)
	return existing_configs

def configs_available_comma(configs):
	ret = ""
	for config in configs:
		ret += " " + config + ","
	return ret[1:-1]

def configs_available_line(configs):
	ret = ""
	for config in configs:
		ret += config + " | "
	return ret[:-3]

def add_config(configs):
	print
	print "Please follow the prompts, enter \".\" when prompted for Host to stop. Leave parameter empty if not needed."
	
	host_name = raw_input("Host: ")
	while host_name != ".":
		if host_name in configs:
			if raw_input("Host already exists in config, delete and overwrite? (y/n) : ").lower() == "n":
				print
				continue
		host_parameters = {}
		for param in parameter_names:
			param_val = raw_input(param + ": ").strip()
			if param_val:
				host_parameters[param] = param_val
		configs[host_name] = host_parameters
		print
		host_name = raw_input("Host: ")

def edit_config(configs):
	print
	print "Configs available: " + configs_available_comma(configs)
	config_name = raw_input("Which config do you want to edit? (Type \".\" to quit) : ").strip()
	while config_name not in configs:
		print "Config name provided does not exist, please enter valid config name."
		config_name = raw_input("Which config do you want to edit? (Type \".\" to quit) : ").strip()
	config = configs[config_name]
	print
	print "Edit parameters, original are in square brackets, type nothing to keep the same: "
	for param in config:
		change = raw_input(param + " [" + config[param] + "] : ").strip()
		if change:
			config[param] = change
	print
	print "New config"
	for param in config:
		print param + " : " + config[param]
	print 
	accept = raw_input("Make changes? (y/n) : ").strip()
	if accept.lower() == "y":
		configs[config_name] = config

def delete_config(configs):
	print
	print "Configs available: " + configs_available_comma(configs)
	config_name = raw_input("Which config do you want to delete? (Type \".\" to quit) : ").strip()
	while config_name not in configs:
		print "Config name provided does not exist, please enter valid config name."
		config_name = raw_input("Which config do you want to delete? (Type \".\" to quit) : ").strip()
	del configs[config_name]

def write_config(configs):
	with open(config_path, "w") as f:
		for host in configs:
			f.write("Host " + host + "\n")
			for param in configs[host]:
				f.write("\t" + param + " " + configs[host][param] + "\n")
	print "Finished writing config file at " + config_path

def prompter(configs):
	response = raw_input("What do you want to do? Show configs available (s), add config (a), edit config (e), delete config (d), write configs (w), quit (.) : ").strip().lower()
	written = False
	while response != ".":
		if response == "s":
			print configs_available_line(configs)
		elif response == "a":
			add_config(configs)
		elif response == "e":
			edit_config(configs)
		elif response == "d":
			delete_config(configs)
		elif response == "w":
			# write_config(configs)
			written = True
		else:
			print "Please enter a valid command as denoted by the character in paranthesis"
		print
		response = raw_input("What do you want to do? Show configs available (s), add config (a), edit config (e), delete config (d), write configs (w), quit (.) : ").strip().lower()
	
	if not written:
		print
		if len(configs):
			response = raw_input("New/old configs have not been written, are you sure you want to exit? (y/n) : ").strip().lower()
		if response == "n":
			print
			return False
	return True

def main():
	preamble()
	configs = find_exitsing_configs()
	while not prompter(configs):
		prompter(configs)



if __name__ == '__main__':
	main()

