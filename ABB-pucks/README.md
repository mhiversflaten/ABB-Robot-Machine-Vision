# ABB-pucks
Complete code for localizing and picking pucks with an IRB 140 robot arm. Image processing in Python and Rest API to communicate between Python and RobotWare.

### class RAPID;

**\_\_init\_\_:**  
Initializes base url, username and password

**def set\_rapid\_variable:**  
POST request to update variables in RAPID  
Requires name of variable and value  
returns nothing

**def get\_rapid\_variable:**  
GET request to get value from variable in RAPID  
Requires name of variable  
returns the value of the specified variable

**set\_robtarget\_variables:**  
Calls the function *set\_rapid\_variable*, manipulated to be able to update robtargets  
Requires name of variable and \[x, y, z\] coordinates  
returns nothing

**get\_robtarget\_variables:**  
GET request to get value from robtarget in RAPID  
Requires name of robtarget  
returns translation\[x, y, z\] and rotation[C, X\*S, Y\*S, Z\*S]  

**set\_offset\_variables:**  
Calls the function *set\_rapid\_variable*, manipulated to be able to update an offset array  
Requires name of variable and \[x, y\] array  
returns nothing

**wait\_for\_rapid:**  
Calls the function *get\_rapid\_variable* to get the **'ready\_flag'** variabel  
A while loop checks on **'ready\_flag'** with a certain interval  
Sets **'ready\_flag'** to *FALSE* when the check is completed  
returns nothing


## HOW THE PROGRAM SHOULD WORK (in progress)
###### !!!! TODO: Make GUI which will function much like the program does up until now (not very important, but something that can be done at a later stage)

	A session gets created:
 
	- session = RAPID()

	Initialize requried variables

	- angles array
	- positions array
	- table_height
	- WRD ("what RAPID does")

Infinite loop is now placed around this main program. Reason being we want to be able to make choices over and over again without restarting the script all the time
	
	while loop that waits for RAPID

	**** changes needs to be done here **** 
	
	- the user gets several options:
		1. Picture from above (needs to be done to find the pucks)
		2. Move a puck to the middle
		3. Stack pucks
		4. Rotate pucks
		5. Quit

	- using an if-loop to run whatever the user chooses

	- option 1:
		1. set WPW ('what Python wants) to 1 -> run CASE 1 in RAPID
		2. run "wait_for_rapid" function to be sure camera is in position
		3. take picture and scan for QR-codes
		4. get [x, y] positions and angles (from QR-codes function)
		5. convert pixel positions to mm (might be done in QR-code function)
		6. calculate how many pucks there are on the table (from QR-code function)
		7. append "table_height" in the [x, y] positions so they can be used to 
		   update robtargets
		8. update the array with robtargets with all the current puck positions
		9. do the same for all the angles

	- option 2:
		1. user is asked which puck he wants to move to the middle
		2. depending on which puck that gets picked the robtarget gets updated
		3. the same applies to the angle of the puck which is also updated
		4. everything is now updated and ready to run, setting WPW ('what
		   Python wants') to 2 -> run CASE 2 in RAPID
		5. run "wait_for_rapid" function to make sure camera is in position
		6. take a new picture and scan for QR-code (now more precise because
		   closer to the puck)
		7. function to calculate how much the offset is to make sure we can pick
		   up the puck safely without missing
		8. the angle can also be updated, but should be pretty accurate from 
		   first reading
		9. update the offset array, and use this to skew the already created
		   robtarget	   
		10.sending 'image_processed:=TRUE' to RAPID to make sure the processing
		   of the image gets done before we continue on with the RAPID program 
	
	- option 3:
		1. update the variable "numberOfPucks", because this is used in the 
		   stackPuck function in RAPID
		2. set WPW ('what Python wants') to 3 -> run CASE 3 in RAPID
		3. the function "stackPucks()" in RAPID has to wait every time we are 
		   going to take a new picture in "safe_position" over the puck
		4. take a new picture and scan for QR-code (now more precise because we 
		   are closer to the puck)
		5. function to calculate how much the offset is to make sure we can pick
		   up the puck safely without missing
		6. the angle can also be updated, but should be pretty accurate from 
		   first reading
		7. update the offset array, and use this to skew the already created
		   robtarget	   
		8. sending 'image_processed:=TRUE' to RAPID to make sure the processing
		   of the image gets done before we continue on with the RAPID program
		9. the function will then pick up the specific pucks and place them in 
		   the middle
		10.this will be repeated for every puck that was identified
	
