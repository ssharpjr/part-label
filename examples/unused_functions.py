# Removed functions.  Saving them for reference

# def get_press_id():
#     # Get PRESS_ID from /boot/PRESS_ID file
#     # Close the program if no PRESS_ID is found
#     if DEBUG:
#         print("Setting Press ID...")
#     try:
#         with open(press_id_file) as f:
#             PRESS_ID = f.read().replace('\n', '')
#             if len(PRESS_ID) >= 3:
#                 return PRESS_ID
#             else:
#                 raise ValueError("PRESS_ID is Not Assigned!"
#                                  "Run 'sh deployments/setup.sh'\nExiting")
#                 sys.exit()
#     except IOError:
#         print(press_id_file + " Not Found!\nExiting")
#         sys.exit()
#     except BaseException as e:
#         print(e)
#         sys.exit()


# def set_printer_usb():
#     label_printer = "zplprinter"
#     check_label_printer = check_output("lpstat -p | grep " + label_printer +
#                                        "; exit 0",
#                                        stderr=STDOUT, shell=True)
#     if not len(check_label_printer) > 0:
#         print("Label printer not detected! \n Exiting")
#         # Cannot print labels without a label printer.
#         run_or_exit_program('exit')
#     # Setup printer options
#     set_default_printer_cmd = "lpoptions -d " + label_printer +\
#                               "> /dev/null 2>&1"
#     set_cups_cmd = "lpadmin -p " + label_printer +\
#                    " -o usb-no-reattach-default=false > /dev/null 2>&1"
#     restart_cups_cmd = "sudo /etc/init.d/cups restart > /dev/null 2>&1"
#     os.system(set_default_printer_cmd)
#     os.system(set_cups_cmd)
#     os.system(restart_cups_cmd)
#     if DEBUG:
#         print("Printer: " + label_printer)
#     return label_printer


# def set_part_number(press_id):
#     if DEBUG:
#         print("Getting Part Number from IQ...")
#     # Get Part Number from IQ API
#     # Part Number is ITEMNO from IQ
#     part_number = press_api_request_pn_only(press_id)
#     # Must be 15-digits.  Pad with zeros as needed.
#     part_number = str(part_number)
#     return part_number


# def print_label_usb(label_printer):
#     if DEBUG:
#         print("Printing label")
#     print_cmd = "lpr -P " + label_printer + " -l " + label_file
#     os.system(print_cmd)

