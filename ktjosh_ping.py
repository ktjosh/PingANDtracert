"""
file : ksj4205_ping.py

Author : Ketan Joshi ksj4205

The program implements Ping (packet internet groper)
by ending ICMP echo request packet to test host reachability
"""
import socket
import struct
import time
import random
import sys




def ksj4205_ping(hostname,count,wait,datassize,timeout):
    """
    Function sends ICMP echo request to hosts, listenes reply ICMP packet from hosts
    and read it.
    :param   hostname : domain name of the host
    :param      count : count of how many echo request packets to be sent
    :param       wait : param to wait between sending between consecutive icmp packets.
    :param datassize : Specfies the size of the data to be sent
    :param    timeout : specifies the timeout for the echo request, after timeout it will stop sending echo request
    """
    #values initialized
    min_RTT=99999
    max_RTT=0
    sum_RTT=0
    success_count=0
    lost_count=0
    addr=""
    #set protocol name
    icmp_protocol = socket.getprotobyname("icmp")
    #created raw socket with protocol type ICMP
    ksj4205socket = socket.socket(socket.AF_INET ,socket.SOCK_RAW,icmp_protocol)

    addr = socket.gethostbyname(hostname)


    ip =addr


    #output
    print('\nPinging '+str(hostname)+" ["+str(ip)+ "]"+" with "+str(datassize)+" bytes of data:")
    #variable for global timeout
    global_time = time.time()
    #index initialized
    index=0
    try:
        while index<count:
            if time.time()-global_time>timeout:
                break
            Icmp_packet = getksj4205_icmpPacket(datassize)
            ksj4205socket.settimeout(3)
            ksj4205socket.sendto(Icmp_packet,(addr,5000))
            starttime = time.time()
            try:
                packet,receieve_addr = ksj4205socket.recvfrom(2048)
                RTT = round((time.time() - starttime)*1000)
                if(min_RTT>RTT):
                    min_RTT = RTT
                if(max_RTT<RTT):
                    max_RTT = RTT
                sum_RTT+= RTT
                #output
                print("Reply from "+ str(addr) + ": bytes=" +str(datassize)+ " time="+str(RTT)+ "ms TTL=" + str(packet[8]))
                success_count+=1
            except:
                print("Request timed out.")
                lost_count+= 1
                index+= 1
                continue

            index+= 1
            time.sleep(wait)

    except KeyboardInterrupt:
        pass
    percent = round( lost_count / ( lost_count + success_count ) * 100 )
    try:
        avg_RTT = round(  sum_RTT / success_count )
    except ZeroDivisionError:
        avg_RTT = 0
    #output
    print("\nPing statistics for "+str(addr))
    print("   Packets: Sent = "+str(lost_count+success_count)+", Received = "+str(success_count),end ="")
    print(", Lost = "+str(lost_count)+" ("+str(percent)+"% loss),")
    print("Approximate round trip times in milli-seconds:")
    print("   Minimum ="+str(min_RTT)+" ms, Maximum = "+str(max_RTT)+" ms, Average="+str(avg_RTT)+" ms")
    ksj4205socket.close()




def getksj4205_icmpPacket(datasize):
    """
    Function creates an ICMP packet with argument passed as a size of the data

    :param datasize: specifies the size of the data to be send
    :return: returns the icmp packet created
    """
    type = 8 #ICMP echo request

    code = 0
    headerchecksum = 0
    identifier =random.randint(0,65534)
    seq_num = 1
    data = "X" * datasize #default 56 bytes
    icmp_data = bytes(data,'utf-8')
    #struct creates a byte stream pf specified argument values
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
    #each byte is an octet so if we have odd numbers of octet then we will not have all exact 16 but pieces
    if(len(packet_string)%2==1):
        odd_size = True
        loop_limit = len(packet_string) -1
    index =0
    sixteen_bit_data_add = 0
    #sixeteen  but addition
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
    main function that calls the ping function
    :return:
    """
    #defualt values of the fields
    count = 1000000000
    wait = 1
    datasize = 56
    timeout = 10000000000

    if len(sys.argv)>2:
        i=1
        try:
            while i< len(sys.argv)-1:
                if sys.argv[i] == "-c":
                    count = int(sys.argv[i+1])
                elif sys.argv[i] == "-i":
                    wait = int(sys.argv[i+1])
                elif sys.argv[i] == "-s":
                    datasize = int(sys.argv[i+1])
                elif sys.argv[i] == "-t":
                    timeout = int(sys.argv[i+1])
                else:
                    print("please select valid options")
                    sys.exit(1)
                i+=2
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

    ksj4205_ping(hostname,count,wait,datasize,timeout)


main()
