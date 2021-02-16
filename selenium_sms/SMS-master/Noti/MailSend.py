# -*- coding: utf-8 -*-
#!/usr/bin python

import datetime
import sys
import os
import re

import Mobigen.Common.Log as Log
from socket import *
import time
#import ConfigParser
import struct

IDX_IP = 0
IDX_PORT = 1

IDX_VALUE = 0
IDX_DESC = 1

IDX_IRIS_NODEID = 0
IDX_IRIS_SYS_STATUS = 1
IDX_IRIS_ADM_STATUS = 2
IDX_IRIS_UPDATE_TIME = 3
IDX_IRIS_CPU = 4
IDX_IRIS_LOADAVG = 5
IDX_IRIS_MEMP = 6
IDX_IRIS_MEMF = 7
IDX_IRIS_DISK = 8

IDX_MEMORY_TOTAL = 0
IDX_MEMORY_USED = 1
IDX_MEMORY_AVAILABE = 2
IDX_MEMORY_USE_PER = 3

IDX_DISK_MOUNT = 0
IDX_DISK_1MBLOCKS = 1
IDX_DISK_USED = 2
IDX_DISK_AVAILABLE = 3
IDX_DISK_USE_PER = 4

IDX_LOG_DATE = 0
IDX_LOG_VALUE = 1
IDX_FILE_VALUE =1 

class SMSSend() :
	#제목 / 통신사 정보 Dict / 전화번호 정보 Dict / 값 Dict
	def __init__(self, _Parser, _ValueDict,collect) :
		self.ValueDict = _ValueDict
		self.PARSER = _Parser
		self.Collect = collect
		
		self.GetConfig()

	def GetConfig(self) :
		try :
			self.Title 			= self.PARSER.get('SMS', 'TITLE')
			self.fromNumber 	= self.PARSER.get('SMS', 'FROM_Number')
			self.toNumberList	= self.PARSER.get('SMS', 'TO_NUMBER').split(',')
		
		except :
			__LOG__.Exception()

	def run(self) :
		try :
			#Make Msg List
			MsgList = []
			mailStr	= ''
#			mailFile = open('/home/eva/user/kimjw/SMS-master/mail.txt', 'w')	
#			MsgList.append('test')
			for Server in self.ValueDict.keys() :
				HostName = self.ValueDict[Server]['HOSTNAME']['VALUE'][0]
				mailStr += '-----------%s (%s)-----------------------\n' % (HostName, Server)
				for Type in self.ValueDict[Server].keys() :
					__LOG__.Trace(Type)

					# UTF-8 로 바꿀 필요성
					if type(HostName)==unicode : 
						HostName = HostName.encode('cp949')

					#Connected Fail
					if (Type == 'STATUS' and self.ValueDict[Server][Type] == 'NOK') : 
						Msg = '[%s] | %s | (%s) | Connected Fail' % (self.Title, Server,HostName) # SSH 자체 Connection Error
						Msg = Msg.decode('utf-8')
						MsgList.append(Msg)
						continue
					elif Type == 'IRIS' :
						mailStr += '[%s]\n%s\n\n' %(Type, self.ValueDict[Server][Type]['VALUE'][IDX_IRIS_SYS_STATUS] + '/' + self.ValueDict[Server][Type]['VALUE'][IDX_IRIS_UPDATE_TIME] ) 
						__LOG__.Trace(self.ValueDict[Server][Type])
						if self.ValueDict[Server][Type]['STATUS'] == 'NOK' : 
							Desc = self.ValueDict[Server][Type]['VALUE'][IDX_IRIS_SYS_STATUS] + '/' + self.ValueDict[Server][Type]['VALUE'][IDX_IRIS_UPDATE_TIME]
							Msg = '[%s]  | %s (%s) | %s | %s' % (self.Title, Server, HostName, Type, Desc) # IRIS Error
						
							Msg = Msg.decode('utf-8')
							MsgList.append(Msg)
						continue
						#	Msg = Msg.decode('utf-8')

					elif Type == 'MEMORY' or Type == 'SWAP' :
						mailStr += '[%s]\n%s(%%)\n\n' %(Type, self.ValueDict[Server][Type]['VALUE'][IDX_MEMORY_USE_PER])
						#__LOG__.Trace(self.ValueDict[Server][Type]['VALUE'][IDX_MEMORY_USE_PER])
						if self.ValueDict[Server][Type]['STATUS'] == 'NOK' : 
							Msg = '[%s] | %s | (%s) | %s(%%)' % (Type, Server, HostName, self.ValueDict[Server][Type]['VALUE'][IDX_MEMORY_USE_PER])

							Msg = Msg.decode('utf-8')
							MsgList.append(Msg)
						continue
																						# 사용 메모리 * 100 / total 메모리 [total 메모리 = used + free 
					elif Type == 'LOAD_AVG' :
						mailStr += '[%s]\n%s\n\n' % ( Type, '/'.join(self.ValueDict[Server][Type]['VALUE'])) 
						if self.ValueDict[Server][Type]['STATUS'] == 'NOK' : 
							Msg = '[%s] | %s | (%s) | %s' % (self.Title, Server, HostName, Type, '/'.join(self.ValueDict[Server][Type]['VALUE']))
																						# 1분 시스템 평균 부하율 / 5분 .. / 15분 ..
							Msg = Msg.decode('utf-8')
							MsgList.append(Msg)
						continue
					elif Type == 'DISK' :
						for Disk in self.ValueDict[Server][Type] :
							mailStr += '[%s]\n%s : %s(%%)\n\n' % ( Type, Disk['VALUE'][IDX_DISK_MOUNT], Disk['VALUE'][IDX_DISK_USE_PER])
							#__LOG__.Trace(Disk)
							if Disk['STATUS'] == 'NOK' : 

################################# 임시 추가 #######################
								if (HostName == 'Koti-Chain-01' or HostName == 'Koti-Chain-02') and ('/snap/core/8592' == Disk['VALUE'][IDX_DISK_MOUNT] or '/snap/core/8689' ==  Disk['VALUE'][IDX_DISK_MOUNT] ) :
									continue
##################################################################
								else :
									Msg = '[%s] | %s | (%s) | %s | %s | %s(%%)' % (self.Title, Server, HostName, Type, Disk['VALUE'][IDX_DISK_MOUNT], Disk['VALUE'][IDX_DISK_USE_PER])
																									# mount 위치, 디스크 사용 퍼센트	
									Msg = Msg.decode('utf-8')
									MsgList.append(Msg)

					elif Type == 'IRIS_OPENLAB' :
						mailStr += 'IRIS OPENLAB RESULT : %s \n\n' % self.ValueDict[Server][Type]['VALUE']
						__LOG__.Trace(self.ValueDict[Server][Type]['VALUE'])
						if self.ValueDict[Server][Type]['STATUS'] == 'NOK' :
							__LOG__.Trace(self.ValueDict[Server][Type]['VALUE'])
							MSG = '[%s] | %s (%s) | %s' % (self.Title, Server, HostName, self.ValueDict[Server][Type]['VALUE'])
							Msg = Msg.decode('utf-8')
							MsgList.append(Msg)
						continue

					else : pass
			#Msg 전송 = 한 Connection 당 한 Number 메시지 전송
			if MsgList :
				for Msg in MsgList :
					__LOG__.Trace('\n'+Msg)
					for toNumber in self.toNumberList : # 전화번호
						__LOG__.Trace('TO Number[%s]' % toNumber)
#						__LOG__.Trace("/home/eva/SMS-master/smsTransfer.p %s %s '%s'" %(self.fromNumber, toNumber, Msg) )
					#	os.system("/home/eva/SMS-master/smsTransfer.p %s %s '%s'" %(self.fromNumber, toNumber, Msg) ) 
						time.sleep(2) #빨리 보내면 안감 , 그래서 Sleep 줌
			else :
				__LOG__.Trace('이상 없음')
		except :
			__LOG__.Exception()

		return mailStr, len(MsgList)
