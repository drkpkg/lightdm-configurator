from configobj import ConfigObj

class lightdm_reader:
	def __init__(self):
		
		self.ldm = ConfigObj()
		self.ldm['SeatDefaults'] = {}
			
		self.gtr = ConfigObj()
		self.gtr['greeter'] = {}
		
#---------------------------------------------------------------------------
	def set_config(self, archive):
		self.lightdm_config = ConfigObj(archive)
		self.ldm_archive = archive
				
	def set_greeter(self, archive):
		self.greeter = ConfigObj(archive)
		self.greeter_archive = archive

	def set_background(self, background):
		if(background!=""):
			self.gtr['greeter']['background'] = background
		else:
			print "Fondo no cargado."

	def set_logo(self, logo):
		try:
			if(logo!=""):
				self.gtr['greeter']['logo'] = logo
			else:
				print "Logo no cargado."
		except:
			print "Logo don't exist"

	def set_font(self, font):
		self.gtr['greeter']['font-name'] = font

	def set_theme(self, theme):
		self.gtr['greeter']['theme-name'] = theme

	def set_icon_theme(self, icontheme):
		self.gtr['greeter']['icon-theme-name'] = icontheme

	def set_antialias(self, switch):
		if(switch==True):
			self.gtr['greeter']['xft-antialias'] = "true"
		else:
			self.gtr['greeter']['xft-antialias'] = "False"

	def set_dpi(self, dpi):
		self.gtr['greeter']['xft-dpi'] = dpi
#---------------------------------------------------------------------------
	def set_active_guest(self, switch):
		if(switch==True):
			self.ldm['SeatDefaults']['autologin-guest'] = "true"
			self.ldm['SeatDefaults']['autologin-session'] = "lightdm-autologin"
		else:
			self.ldm['SeatDefaults']['autologin-guest'] = "false"

	def set_active_autologin(self, user, time):
		if(user!=""):
			self.ldm['SeatDefaults']['autologin-user'] = user
			self.ldm['SeatDefaults']['autologin-session'] = "lightdm-autologin"
			self.ldm['SeatDefaults']['autologin-user-time'] = time

#	def set_wait_autologin(self, time):
		
#---------------------------------------------------------------------------
	def get_background(self):
		try:
			return self.greeter['greeter']['background']
		except:
			return 0
	
	def get_config(self):
		return self.lightdm_config
	
	def get_config_greeter(self):
		return self.greeter
	
	def get_greeter(self):
		return self.lightdm_config['SeatDefaults']['greeter-session']
		
	def get_logo(self):
		try:
			return self.greeter['greeter']['logo']
		except:
			return 0
	
	def get_font(self):
		return self.greeter['greeter']['font-name']
		
	def get_theme(self):
		return self.greeter['greeter']['theme-name']
		
	def get_icon_theme(self):
		return self.greeter['greeter']['icon-theme-name']
#---------------------------------------------------------------------------
	def get_active_guest(self):
		try:
			if(self.lightdm_config['SeatDefaults']['autologin-guest']=='false'):
				return 0
			else:
				return 1
		except:
			return 0
	
	def get_active_autologin(self):
		try:
			return self.lightdm_config['SeatDefaults']['autologin-user']
		except:
			return 0
		
	def get_wait_autologin(self):
		try:
			return self.lightdm_config['SeatDefaults']['autologin-user-timeout']
		except:
			return 0
	
	def view_new_config_lightdm(self):
		return self.ldm
	
	def view_new_config_greeter(self):
		return self.gtr
#---------------------------------------------------------------------------
	def write_config(self):
					
		try:			
			self.ldm.filename = self.ldm_archive
			self.ldm['SeatDefaults']['greeter-session'] = self.lightdm_config['SeatDefaults']['greeter-session']
			self.ldm['SeatDefaults']['user-session'] = self.lightdm_config['SeatDefaults']['user-session']
			self.ldm.write()
		
			self.gtr.filename = self.greeter_archive
			self.gtr['greeter']['xft-hintstyle'] = 'hintslight'
			self.gtr['greeter']['xft-rgba'] = 'rgb'
			self.gtr.write()
			
			return 0
		except:
			print "No effects."
			return -1
	
		
	def write_config_in_other_file(self, ldmconf, grtconf):
		self.ldm_archive = ldmconf
		self.greeter_archive = grtconf
		self.write_config()
	
#if __name__ == "__main__":
	
	'''background=/usr/share/backgrounds/warty-final-ubuntu.png
	logo=/usr/share/unity-greeter/logo.png
	theme-name=Ambiance
	icon-theme-name=ubuntu-mono-dark
	font-name=Ubuntu 11
	xft-antialias=true
	xft-dpi=96
	xft-hintstyle=hintslight
	xft-rgba=rgb'''
	
	'''autologin-guest=false
	autologin-user=drkpkg
	autologin-user-timeout=0
	autologin-session=lightdm-autologin
	greeter-session=unity-greeter
	user-session=ubuntu'''
	
	'''l = lightdm_reader()
	l.set_config("/etc/lightdm/lightdm.conf")
	l.set_greeter("/etc/lightdm/unity-greeter.conf")
	l.set_background("/usr/share/backgrounds/warty-final-ubuntu.png")
	l.set_logo("/usr/share/unity-greeter/logo.png")
	l.set_theme("Ambiance")
	l.set_icon_theme("ubuntu-mono-dark")
	l.set_font("Ubuntu 11")
	l.set_antialias(True)
	l.set_dpi(96)
	
	l.set_active_autologin("drkpkg")
	l.set_active_guest(False)
	l.set_wait_autologin(0)
	
	print l.view_new_config_lightdm() 
	print "\n"
	print l.view_new_config_greeter() 
	print "\n"
	print l.get_config() 
	print "\n"
	print l.get_greeter() 
	print "\n"

	l.write_config()'''
	
	'''print l.get_config()
	print l.get_greeter()
	print l.get_active_autologin()
	print l.get_active_guest()
	print l.get_background()
	print l.get_font()
	print l.get_icon_theme()
	print l.get_logo()
	print l.get_theme()
	print l.get_wait_autologin()'''
	

