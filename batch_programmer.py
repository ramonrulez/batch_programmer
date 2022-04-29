import os
import glob

#	Welcome--------------------------------------------------------------
print("\n -------------------------------------")
print("| Welcome to the repeated programmer! |")
print(" -------------------------------------\n")

#	Initialization-------------------------------------------------------
User=os.getlogin()
BUILD_FOLDER="C:/Users/" +User+ "/Documents/Arduino/Builds"


#	Functions------------------------------------------------------------
#	Quantity menu with checks
def choose_quantity_menu():
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


#	The actual programming of the chip
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
		
		
def programmer(file):
	# avrdude -c usbtiny -p t85 -v -U flash:w:SRE_100_PROGRAM_V7_8Mhz.ino.hex -U lfuse:w:0xE2:m
	command = "avrdude -c usbtiny -p t85 " +file
	print("Programming...")
	exit_status = os.system(command)
	return exit_status
	
def file_find():
	os.chdir(BUILD_FOLDER)	# Change to the build directory
	file = "to_file"	#	DELETE THIS
	
	#
	#
	#	The actual code to find the right file
	#
	#
	return file

def microcontroller_backup(where):	
	os.chdir(where)

	mem_type = ["eeprom", "flash", "signature", "lfuse", "hfuse", "efuse", "calibration"]
	for m in mem_type:
		command = "avrdude -c usbtiny -p t85 -v -n -U " +m+ ":r:" +m+ ".hex:h"
		os.system(command)
		

#	Main-----------------------------------------------------------------

# microcontroller_backup("new")

# programming_routine(choose_quantity_menu())

os.chdir(BUILD_FOLDER)
file = glob.glob("*.ino.hex")
print(file)