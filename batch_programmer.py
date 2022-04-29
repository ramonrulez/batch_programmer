import os

#	Welcome--------------------------------------------------------------
print("\n -------------------------------------")
print("| Welcome to the repeated programmer! |")
print(" -------------------------------------\n")

#	Initialization-------------------------------------------------------
PATH = os.getcwd()

User = os.getlogin()
BUILD_PATH = "C:/Users/" +User+ "/Documents/Arduino/Builds"

my_programmer = "usbtiny"
my_mcu = "t85"

#	Functions------------------------------------------------------------
#	This function returns how much chips you choose to program
def choose_quantity():
	while 1:
		while 1:
			count = input("How much do you want? : ")			
			try:
				count = int(count)
				break
			except ValueError:
				print("This is not a number")		
		print("You choose", count,"!")
		choise = input("Are you sure you need this much? (y/N) :")
		match choise:
			case "Y" | "y":
				break
	return count


#	Programming routine of the chips
def programming_routine(counter):
	hex_file = file_find()	#	Find the file first
	while counter > 0:	
		exit_status = programmer(hex_file)	#	Program each microcontroller independently
		match exit_status:
			case 0:
				counter -= 1
				input("OK.Press any key to continue!")
			case _:
				input("Something gone wrong :(")
		
		
#	The actual programming of each chip
def programmer(file):
	os.chdir(BUILD_PATH)	# Change to the build directory
	command = "avrdude -p "+my_mcu+" -c "+my_programmer+" -U lfuse:w:0xE2:m -U flash:w:"+file 
	print("Programming...")
	exit_status = os.system(command)
	return exit_status


#	Find the build file
def file_find():
	file = [x for x in os.listdir(BUILD_PATH) if x.endswith('.ino.hex')]
	return file[0]


#	Utility function that take each kind of memory from the mcu and copies it to a folder
def mcu_backup(where):	
	os.chdir(where)	#	In which folder you want to save the results 
	mem_type = ["eeprom", "flash", "signature", "lfuse", "hfuse", "efuse"]
	for m in mem_type:
		command = "avrdude -p "+my_mcu+" -c "+my_programmer+" -v -n -U "+m+":r:"+m+".hex:i"
		os.system(command)
	return 0
		
		
#	Write the MCU's	default state in the MCU	
def mcu_restore(default_folder):
	os.chdir(default_folder)	#	In which folder you want to save the results 
	mem_type = ["eeprom", "flash", "lfuse", "hfuse", "efuse"]
	for m in mem_type:
		command = "avrdude -p "+my_mcu+" -c "+my_programmer+" -v -U "+m+":w:"+m+".hex"
		os.system(command)
	return 0
	
	
#	Main-----------------------------------------------------------------


# programming_routine(choose_quantity())