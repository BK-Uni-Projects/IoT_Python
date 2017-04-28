from time import sleep
import mcp3008_2

while True:
    m = mcp3008_2.readadc(5)
    print "Moisture level: {:>5} ".format(m)
    sleep(.5)
