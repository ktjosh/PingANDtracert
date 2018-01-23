"""
file : ksj4205_traceroute.py

Author : Ketan Joshi ksj4205

The program finds all the intermediate nodes to reach the host by sending ICMP echo request to each of the intermediate
nodes
"""
import socket
import sys
import time
import struct
import random

def ksj4205_traceroute(hostname,addressname_flag,probe_count,summary_flag):
    """
    Function sends sepecified probes (echo request) to every node that is in the path to reach the specifed host
    and displayes information about each node. It does so by increasing the time to live (hops it can cover) to reach
    the destination.

    :param         hostname : the domain name of the host
    :param addressname_flag : flag that if set displays the domain name of each intermediate node
    :param      probe_count : sets the number of probes to be sent for each hop
    :param     summary_flag : flag if set displays the summary for each hop
    :return:
    """
    #set protocol by name
    icmp_protocol = socket.getprotobyname("icmp")
    #created raw socket
    ksj4205socket = socket.socket(socket.AF_INET ,socket.SOCK_RAW,icmp_protocol)
    #intiailized time to live
    ttl=0
    #dns lookup to find the ip of the host

    addr = socket.gethostbyname(hostname)
    ipaddress =""
    #output
    print("\nTracing route to "+str(hostname)+ "["+str(addr)+"]")
    print("over a maximum of 30 hops:\n")

    try:
        #It will keep on find till it finds the address of the host
        while ipaddress!=addr:
            ipaddress = ""

            if(ttl>=30):
                break
            #initialize variable
            min_RTT = 99999
            max_RTT = 0
            sum_RTT = 0
            success_count = 0
            lost_count = 0
            #increasing time to live
            ttl+=1
            Icmp_packet = getksj4205_icmpPacket()

            ksj4205socket.settimeout(3)
            ksj4205socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            #output
            print(str(ttl)+"\t",end="")
            #send specified number of probes
            for j in range (probe_count):
                ksj4205socket.sendto(Icmp_packet, (addr, 5000))

                starttime = time.time()
                try:
                    packet, receieve_addr = ksj4205socket.recvfrom(2048)
                    RTT = round((time.time() - starttime) * 1000)
                    if min_RTT>RTT:
                        min_RTT = RTT
                    if max_RTT<RTT:
                        max_RTT = RTT
                    sum_RTT+= RTT
                    if RTT<1:
                        RTT="<1"
                    elif RTT<10:
                        RTT = " "+str(RTT)
                    #output
                    print(str(RTT)+" ms \t",end="")
                    ipaddress = receieve_addr[0]
                    success_count+=1
                except socket.timeout :
                    lost_count+=1
                    print(" *"+"\t",end="")

                    continue
            try:
                if addressname_flag:
                    if success_count!=0:
                        name = socket.gethostbyaddr(ipaddress)
                        print(str(name[0]),end ="")
                if success_count == 0:
                    print("Request timed out.")
                if success_count!=0:
                    print("  ["+str(ipaddress)+"]")

            except socket.herror:
                print(str(ipaddress))
            if summary_flag:
                percent = round( lost_count / ( lost_count + success_count ) * 100 )
                try:
                    avg_RTT = round( sum_RTT / success_count )
                except ZeroDivisionError:
                    avg_RTT = 0
                if( success_count==0 ):
                    min_RTT=0
                    max_RTT=0
                #output statistics
                print("\n statistics for " + str(ipaddress))
                print("   Packets: Sent = " + str(lost_count + success_count) + ", Received = " + str(success_count),
                      end="")
                print(", Lost = " + str(lost_count) + " (" + str(percent) + "% loss),")
                print("Approximate round trip times in milli-seconds:")
                print("   Minimum =" + str(min_RTT) + " ms, Maximum = " + str(max_RTT) + " ms, Average=" + str(
                    avg_RTT) + " ms\n")
    except KeyboardInterrupt:
        pass



    print("\nTrace complete.\n")
    ksj4205socket.close()





def getksj4205_icmpPacket():
    """
    Function creates an ICMP packet with argument passed as a size of the data

    :param packetsize: specifies the size of the data to be send
    :return: returns the icmp packet created
    """
    type = 8 #ICMP echo request
    #type,code,headerchecksum,identifier,seq_num
    code = 0
    headerchecksum = 0
    identifier =random.randint(0,65534)
    seq_num = 1
    data = "X" * 56 #default 56 bytes
    icmp_data = bytes(data,'utf-8')
    # struct creates a byte stream pf specified argument values
    icmp_header = struct.pack("!BBHHH",type,code,headerchecksum,identifier,seq_num)
    headerchecksum = get_icmp_checksum(icmp_header + icmp_data)
    icmp_header = struct.pack("!BBHHH", type, code, headerchecksum, identifier, seq_num)
    icmp_packet = icmp_header + icmp_data

    return  icmp_packet


def get_icmp_checksum(packet_string):
    """
    Function calculates icmp checksum and returns it

    The checksum is calculated  by dicing the packet into 16 bits pieces adding all the pieces and the computing the
    one's compliment of it, which is the checksum

    :param packet_string: It is the packet i.e. Header + data
    :return: returns checksum calculayed
    """

    loop_limit = len(packet_string)
    odd_size = False
    # each byte is an octet so if we have odd numbers of octet then we will not have all exact 16 but pieces
    if(len(packet_string)%2==1):
        odd_size = True
        loop_limit = len(packet_string) -1
    index =0
    sixteen_bit_data_add = 0
    while index<loop_limit:
        sixteen_bit_data_add = sixteen_bit_data_add + ( ( packet_string[index]<<8 ) + packet_string[index+1] )
        carry_bit = sixteen_bit_data_add>>16 #17th bit will be carry so right shift 16
        sixteen_bit_data_add = sixteen_bit_data_add & 0xFFFF # to remove the 17th bit
        sixteen_bit_data_add = sixteen_bit_data_add + (carry_bit & 0xFFFF)
        index = index +2
    if odd_size:
        last_octet = packet_string[loop_limit]<<8
        sixteen_bit_data_add = sixteen_bit_data_add + last_octet
        carry_bit = sixteen_bit_data_add >> 16  # 17th bit will be carry so right shift 16
        sixteen_bit_data_add = sixteen_bit_data_add & 0xFFFF  # to remove the 17th bit
        sixteen_bit_data_add = sixteen_bit_data_add + (carry_bit & 0xFFFF)

    final_checksum = (~sixteen_bit_data_add)
    return final_checksum & 0xFFFF


def main():
    """
    Main function
    :return:
    """
    #initialized variabeles
    addressname_flag = True
    probe_count =3
    summary_flag=False
    if len(sys.argv)>2:
        i=1
        try:
            while i< len(sys.argv)-1:
                if sys.argv[i] == "-n":
                    addressname_flag = False
                    i+=1
                elif sys.argv[i] == "-q":
                    probe_count = int(sys.argv[i+1])
                    i+=2
                elif sys.argv[i] == "-S":
                    summary_flag = True
                    i+=1
                else:
                    print("please select valid options")
                    sys.exit(1)

            hostname = sys.argv[len(sys.argv)-1]
        except ValueError:
            print("Please put numerical value")
            sys.exit(0)
    else:
        hostname = sys.argv[len(sys.argv)-1]

    try:
        addr = socket.gethostbyname(hostname)
    except:
        print("Ping request could not find host '"+str(hostname)+"' Please check the name and try again.")
        sys.exit(0)

    ksj4205_traceroute(hostname,addressname_flag,probe_count,summary_flag)



main()

