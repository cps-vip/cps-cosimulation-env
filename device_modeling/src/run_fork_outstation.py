import os
import logging


from time import sleep
# from devices.outstation import Outstation
# from devices.master import Master
from dnp3.devices.outstation import Outstation
from dnp3.devices.master import Master


logging.basicConfig(filename="simulation.log", level=logging.INFO, filemode="w+")
logger = logging.getLogger(__name__)




if __name__ == '__main__':
   master_dnp3_addr = 1
   outstation1_addr = (1024, "127.0.0.1:20000")
   outstation2_addr = (1025, "127.0.0.1:20001")


   pid = os.fork()
   if pid == 0:
       outstation1 = Outstation("Outstation 1",
                                outstation1_addr[0],
                                master_dnp3_addr,
                                outstation1_addr[1])
       outstation1.activate()


    #    print('Input "b" to update the binary input and "q" to quit and "a" for the double bit binary transaction and "3" for binary_output_status_transaction2 and "4" for counter_transaction2 and "5" for frozen_counter_transaction2 and "6" for analog_transaction2 and "7" for analog_output_status_transaction2 and "octet" for octet_string_transaction2')
       print('Update database values by typing binary_input, double_bit_binary, binary_output_status, counter, frozen_counter, analog, analog_output_status, and octet. Type q to quit')
       while True:
           x = input()
           if (x == 'binary_input'):
               outstation1.binary2_input_transaction()
           elif (x == 'double_bit_binary'):
               outstation1.double_bit_binary_transaction2()
           elif (x == 'binary_output_status'):
               outstation1.binary_output_status_transaction2()
           elif (x == 'counter'):
               outstation1.counter_transaction2()
           elif (x == 'frozen_counter'):
               outstation1.frozen_counter_transaction2()
           elif (x == 'analog'):
               outstation1.analog_transaction2()
           elif (x == 'analog_output_status'):
               val = float(input("Enter analog output status value: "))
               outstation1.analog_output_status_transaction2(val)

        #    elif (x == '7'):
        #        outstation1.analog_output_status_transaction2()
        #    elif (x == 'octet'):
        #        outstation1.octet_string_transaction2()
           elif x == 'octet':
                text = input("Enter octet string to write at index 7: ")
                outstation1.octet_string_transaction2(text)
           elif (x == 'q'):
               break
   #    outstation1._tcpserver.log_stuff()
   #    logger.info("Activated outstation 1")


  #     outstation2 = Outstation("Outstation 2",
    #                            outstation2_addr[0],
    #                            master_dnp3_addr,
   #                             outstation2_addr[1])
 #     outstation2.activate()
  #     logger.info("Activated outstation 2")
  #     sleep(5)


       logger.info("Deactivating outstation 1")
       outstation1.deactivate()
       outstation1.destroy()


       # logger.info("Deactivating outstation 2")
       # outstation2.deactivate()
       # outstation2.destroy()
   else:
       master = Master("Master", master_dnp3_addr)
       # master.add_outstations([outstation1, outstation2])
       master.create_channel(outstation1_addr[0], outstation1_addr[1])
 #      master.create_channel(outstation2_addr[0], outstation2_addr[1])
       master.activate()
       logger.info("Activated master station")
       os.waitpid(pid, 0)


       logger.info("Deactivating master station")
       master.deactivate()
       master.destroy()





