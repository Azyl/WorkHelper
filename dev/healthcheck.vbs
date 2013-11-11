REM ###############################################################################################################################
REM # Author			 - Tataru Andrei, Sorin Pop
REM # Batch file name    - disc_usage.vbs
REM # Batch role         - Logs the disk usage of the local drives
REM # Batch version      - 0.0003
REM # Batch requirements - Elevated privileges required
REM ###############################################################################################################################
REM # v - 0.0002         - added Total Space and Free percentage to the log, automatic Server name and address
REM # v - 0.0003         - added Control logic for sending emails, also added the log as an attachment
REM ###############################################################################################################################
'----------------------------------------------------------------------------------------------------------------------------------
' Parameters


hostname="Lemet DB Prod"

'log_directory = "C:\TEMP\disc_usage\logs"
log_directory = ""
cumulative_log_file = "Check.sql"
warning_th=20
critical_th=10

Const HARD_DISK = 3 'Const Unknown = 0 Const Removable = 1 Const Fixed = 2 Const Remote = 3 Const CDROM = 4 Const RAMDisk = 5


strComputer = "."
warning_level = 0

'----------------------------------------------------------------------------------------------------------------------------------
' File configuration
Set objFSO=CreateObject("Scripting.FileSystemObject")
Const ForReading = 1, ForWriting = 2, ForAppending = 8
outFile = log_directory & cumulative_log_file
Set objFile = objFSO.OpenTextFile(outFile,ForWriting,True)
'==End file configuration section==
'----------------------------------------------------------------------------------------------------------------------------------


'----------------------------------------------------------------------------------------------------------------------------------
' Get Computer name and IP
Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")

Set colSettings = objWMIService.ExecQuery _
    ("Select * from Win32_ComputerSystem")
For Each objComputer in colSettings 
    serverC_name = objComputer.Name
Next
	
Set colItems = objWMIService.ExecQuery _
    ("Select * From Win32_NetworkAdapterConfiguration Where IPEnabled = True")
   
strCount = 1
For Each objitem in colItems
    If strCount = 1 Then
        ActiveDHCPIPAddress = objitem.IPAddress(0)
        'FullAddress = Join(objitem.IPAddress, ",") ' If the MAC address is also required
        IP=ActiveDHCPIPAddress
        strCount = strCount + 1
        serverC_name = serverC_name & " on: " & IP
    Else
    End If
next
'==End get computer name and IP section==
'----------------------------------------------------------------------------------------------------------------------------------

'----------------------------------------------------------------------------------------------------------------------------------
' Get Disk usage ,write into log files	



Set colDisks = objWMIService.ExecQuery _
    ("Select * from Win32_LogicalDisk Where DriveType = " & HARD_DISK & "")
	

ss="<table>"   & _
"<caption>Table 14 : Disk Usage </caption> "   & _
"<tr>"   & _
"<th>Drive Letter</th>"   & _
"<th>Total Space MB</th>"   & _
"<th>Free Space MB</th> "  & _
"<th>Free Percentage %</th>"   & _
"</tr>"  	


i=0
For Each objDisk in colDisks
	i=i+1
	
	TotSpace=Round(((objDisk.Size)/1073741824),1)
    FrSpace=Round(objDisk.FreeSpace/1073741824,1)
    FrPercent=Round((FrSpace / TotSpace)*100,2)
	
	
	
	
	if FrPercent < warning_th then
		ss=ss & "<tr class=''alterr''>"  
	else
		if i mod 2 = 0 then
			ss=ss & "<tr class=''alt''>"  
		else
			ss=ss & "<tr>"  
		end if
	end if
	
	ss=ss & "<td>" & objDisk.DeviceID & "</td>"
	ss=ss & "<td>" & TotSpace & "</td>" 
	ss=ss & "<td>" & FrSpace & "</td>" 
	ss=ss & "<td>" & FrPercent & "</td>" 
	ss=ss & "</tr>"  

Next

ss=ss & "<br><br><br>"


s="exec Crisoftadmin.Crisoftadm.Health_Check('" & ss & "','"& hostname &"');"


objFile.Write s
objFile.Close



strCommandLine="C:\Programs\instantclient_11_2\sqlplus.exe CrisoftAdmin/manu123@LEMETTEST.CRISOFT.RO @Check.sql"
Set oShell = CreateObject("WScript.Shell")
oShell.Run strCommandLine, 1, True
Set oShell = Nothing


'----------------------------------------------------------------------------------------------------------------------------------



