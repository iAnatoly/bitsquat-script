#!/usr/bin/env python
# contact me: artem [at] dinaburg [dot] org
import sys
import socket
import whois

def bitflip(num, pos):
    shiftval = 1 << pos
    return num ^ shiftval

def is_valid(charnum):
    return ((charnum >= ord('0') and charnum <= ord('9')) or
            (charnum >= ord('a') and charnum <= ord('z')) or
            (charnum >= ord('A') and charnum <= ord('Z')) or
             charnum == ord('-'))

def usage():
    print "Usage:"
    print "bitsquat.py <domain name> <extension>"
    print ""
    print "example:"
    print "bitsquat.py google .com"
    print ""

if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()
        sys.exit()

    name = sys.argv[1]
    suffix = sys.argv[2]

    for i in range(0, len(name)):
        val = name[i]
        for bit in range(0,8):
            newval = bitflip(ord(val), bit)
            if is_valid(newval) and val.lower() != chr(newval).lower():
                newname = name[:i] + chr(newval) + name[i+1:]
                fullname = newname + suffix
                try:
                    ipaddr = socket.gethostbyname(fullname)
                    sys.stdout.write('%s: is taken (%s)\n' % (fullname, ipaddr,))
                except:
                    domain = whois.query(fullname)
                    # print(domain.__dict__)
                    if domain.registrar is None:
                        sys.stdout.write('%s might be available!\n' % (fullname, ))
                    else:
                        sys.stdout.write('%s: is taken since %s\n' % (fullname, domain.creation_date,))
    


