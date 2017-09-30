# PLC-Triggered Part-Level Label Printing Project

___
##### Project Goal:
Print a part label using a PLC trigger, a Raspberry Pi SBC and a Zebra ZPL printer.
___


### Project Notes - Logical Process Flow
* PLC output sends a signal to RPI GPIO input.
* RPI monitors GPIO input using edge detection.
* RPI gets the Part Number for the label from IQ API.
* RPI assigns the Part Number to a variable (15-digit padded for Barcode).
* RPI generates date based on 2-digit year and 3-digit (Julian) day and assigns it to a variable.
* RPI generates a 4-digit Serial Number counter and assigns it to a variable (4-digit padded for Barcode).
* RPI stores both the Date and next Serial Number in files in case of system failure.
* RPI resets the Serial Number when it reaches the 4-digit limit (9999).
  -  Cycle times are greater than 9 seconds so this is not an issue.
* RPI builds ZPL file from label template and variables.
* RPI sends ZPL file to printer via lpr raw command.
* RPI increments the Serial Number and stores it in a file.


### Possible Technologies to Use
__Raspberry Pi__
* Pros:
  * Python programming, native Linux OS, USB printer interface,
  * Current experience based on previous projects.
* Cons:
  * No native RTC (would need add-on hat, network time, or use printer RTC add-on), 
  * Custom solution that requires IT support.

__Android__
* Pros:
  * Tablet-based user interface, USB printer interface, Zebra Link-OS SDK available with examples,
  * Native RTC.
* Cons:
  * Limited Java/Android programming knowledge, new Zebra SDK to learn and implement, 
  * Custom solution that requires IT support.

__Programmable Logic Controller (PLC)__
* Pros:
  * Familiar hardware for Engineering, HMI interface, ASCII output via serial interface.
* Cons:
  * No IT knowledge of PLC/HMI programming, Not proven if IQ API access is possible, potential cost.
  * Automation direct has a database connector server software for $800.

__Arduino__
* Pros:
  * Ethernet/Wifi and serial interfaces (with add-on shields)
* Cons:
  * Not proven connectivity with IQ API or serial printer.


### Problematics
* The Press Number cannot be hardcoded.  What if the PLC/RPI device is moved to another press?  How does it know where it is?
