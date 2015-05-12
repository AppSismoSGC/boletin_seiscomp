#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#v(1) -- 03/20/2015

import sys
import os

if len(sys.argv)<2:
	print 'No input files'
	sys.exit()

begin = sys.argv[1]+' '+sys.argv[2]
end = sys.argv[3]+' '+sys.argv[4]

def event_sc(eventId, bul_type):
	os.system('scbulletin -d mysql://sysop:sysop@10.100.100.232/seiscomp3 -E '+eventId+' '+str(bul_type)+' > bull.txt')
	bulletin = open('bull.txt','rU')
	lines = bulletin.readlines()
	if bul_type == -3:
		Date = lines[5][27:37]
		Time = lines[6][27:37]
		ErrorTime = float(lines[6][44:47])
		Lat = float(lines[7][25:33])
		ErrorLat = float(lines[7][42:47]) 
		Lon = float(lines[8][25:33])
		ErrorLon = float(lines[8][42:47])
		Depth = float(lines[9][25:33])
		if len(lines[9][42:47]) == 0:
			ErrorDepth = 'Fixed'
		else:
			ErrorDepth = float(lines[9][42:47])
		Gap = float(lines[14][25:33])
		RMS = float(lines[13][25:35])
		for line in lines:
			if "preferred" in line:
				M = line[13:18]
		print Date, Time, ErrorTime, Lat, ErrorLat, Lon, ErrorLon, Depth, ErrorDepth, Gap, RMS, M
		event_dict = {'Date':Date,'Time':Time,'ErrorTime':ErrorTime,'Lat':Lat,'ErrorLat':ErrorLat,'Lon':Lon,'ErrorLon':ErrorLon,'Depth':Depth,'ErrorDepth':ErrorDepth,'Gap':Gap,'RMS':RMS,'M':M}
	bulletin.close()
	return event_dict

def list_sc(begin, end):
	lista = []
	os.system("scevtls -d mysql://sysop:sysop@10.100.100.232/seiscomp3 --begin \'"+begin+"\' --end \'"+end+"\' > list.txt")
	list_file = open('list.txt', 'rU')
	for line in list_file.readlines():
		lista.append(line.strip())
	print lista
	list_file.close()
	return lista
#ejemplo-----
report = open('reportSC.out','w+')
list_ID = list_sc(begin, end)
#print >> report, "  Date \t\t   Time \tET(s)   Lat(°)   Error(km)   Lon(°)  Error(km)  Depth(km)  Error(km)   Mag   Gap(°)   RMS"
for eventID in list_ID:
	event = event_sc(eventID, -3)
	print >> report, event['Date']+'\t'+event['Time']+'\t'+str(event['ErrorTime'])+'\t'+str(event['Lat'])+'\t'+str(event['ErrorLat'])+'\t'+str(event['Lon'])+'\t'+str(event['ErrorLon'])+'\t'+ str(event['Depth'])+'\t'+str(event['ErrorDepth'])+'\t'+str(event['M'])+'\t'+str(event['Gap'])+'\t'+str(event['RMS'])+'\t'+eventID  

report.close()

#event = event_sc('SGC2015dmpq', -3)
#print event
