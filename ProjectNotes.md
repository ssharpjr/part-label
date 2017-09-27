# PLC-Triggered Part-Level Label Printing Project
Print a part label using a PLC trigger, a Raspberry Pi SBC and a Zebra ZPL printer.

### Project Notes - Logical Process Flow
* PLC output sends a signal to RPI GPIO input.
* RPI monitors GPIO input.
  * __DESIGN QUESTION__: Interrupt or loop to monitor input?
* RPI gets the Part Number for the label.
  * __PROJECT QUESTION__: What is the Part Number source (IQAPI, Manual input)?
* RPI assigns the Part Number to the label data.
* RPI generates a Serial Number based on the current Time/Date and assigns to label data.
* RPI builds ZPL file from label data variables.
* RPI sends ZPL file to printer via lpr raw command.


### Possible Technologies to Use
__Raspberry Pi__
* Pros:
  * Python programming, native Linux OS, USB printer interface,
  * Current experience based on previous projects.
* Cons:
  * No native RTC (would need addon or use printer RTC), 
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

__Arduino__
* Pros:
  * Ethernet/Wifi and serial interfaces (with addon shields)
* Cons:
  * Not proven connectivity with IQ API or serial printer.


### Problematics
* The Press Number cannot be hardcoded.  What if the PLC/RPI device is moved to another press?  How does it know where it is?

