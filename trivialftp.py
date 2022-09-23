
import argparse, build_packet, read_file, write_file


PARSER = argparse.ArgumentParser(description= "parse TFTP header data")

##################################################
#error handling for port, 5000<=vlaue<=65535
#Inputs:
#-p flagged value from argparser
#
#Outputs:
#error message if port number out of range
#####################################################
def check_range (arg):
    try:
        value = int(arg)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error))

    if value < 5000 or value > 65535:
        message = "Port Number out of range: Acceptable range = (5000 <= Value <= 65535)".format(value)
        raise argparse.ArgumentTypeError(message)

    return str(value)

#####################################################
#error handling  for mode, only 'r' and 'w' accepted
#Inputs:
#-m flagged value from argparser
#
#Outputs:
#error message if mode is not 'r' (read) or 'w' (write)
#####################################################
def check_val (arg):
    try:
        value = str(arg)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error))

    if value != 'r' and value != 'w':
        message = "Invalid mode: Acceptable mode: 'r' or 'w'".format(value)
        raise argparse.ArgumentTypeError(message)
    return str(value)




def main ():
    #mode is always netascii
    mode = 'netascii'

    ##################################################
    #parse the argument, check for valid input
    #check_range and check_val methods ensure valid inputs
    #dest = assigns variable names to flagged inouts
    ##################################################
    PARSER.add_argument('-a',dest = 'IP_ADDRESS', required=True)
    PARSER.add_argument('-sp',dest = 'SERVER_PORT', required=True)
    PARSER.add_argument('-f',dest = 'FILE_NAME', required=True)
    PARSER.add_argument('-p',dest = 'PORT_NUMBER', type=check_range, required=True)
    PARSER.add_argument('-m',dest = 'OPCODE', type=check_val, required=True)
    args = PARSER.parse_args()

    
    #######################################################
    #build rrq, pass rrq packet to read_file() method
    #Inputs:
    #args variables for filename, ip address, adn server port number
    #recieves contstructed RRQ packet from build_packet.py
    #sends packet to read_file.py to handle entire read request from server
    ######################################################## 
    if args.OPCODE == 'r':
        packet = build_packet.make_RRQ(args.FILE_NAME, mode)
        read_file.read_file(packet, args.FILE_NAME, str(args.IP_ADDRESS), int(args.SERVER_PORT))



    #######################################################
    #build wrq pass packet to write_file() method
    #Inputs:
    #args variables for filename, ip address, adn server port number
    #recieves contstructed WRQ packet from build_packet.py
    #sends packet to write_file.py to handle entire write request from server
    ######################################################## 
    else: 
        packet = build_packet.make_WRQ(args.FILE_NAME, mode)
        write_file.write_file(packet, args.FILE_NAME, str(args.IP_ADDRESS), int(args.SERVER_PORT))

  
if __name__ == '__main__':
    main()

