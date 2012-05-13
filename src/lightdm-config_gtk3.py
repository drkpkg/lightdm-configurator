#/usr/bin/env python
# -*- coding: utf-8 -*-
import os, commands
from gi.repository import Gtk, Gio, GdkPixbuf
from lightdm_reader import lightdm_reader

class MainWindow():
	
	def __init__(self):	
		self.Builder = Gtk.Builder()
		
		try:
			self.Builder.add_from_file("interface_gtk.glade")
			self.Window = self.Builder.get_object("main_window")
			self.Window.set_icon("data/logo.png")
		except:
			self.Builder.add_from_file("/usr/share/lightdm-configurator/interface_gtk.glade")
			self.Window = self.Builder.get_object("main_window")
			self.Window.set_icon_from_file("/usr/share/lightdm-configurator/data/logo.png")
		
		self.Window.set_title("Configura Lightdm")
		
		#Creando instancia reader
		self.lightdm = lightdm_reader()
		self.lightdm.set_config("/etc/lightdm/lightdm.conf")
		self.lightdm.set_greeter("/etc/lightdm/"+self.lightdm.get_greeter()+".conf")
		
#Hacer la miniaturas para los botones
	#Para el wallpaper
		self.wall = self.lightdm.get_background()
		background = GdkPixbuf.Pixbuf.new_from_file_at_size(self.wall,100,50)
		self.image_background = Gtk.Image()
		self.image_background.set_from_pixbuf(background)
		self.Builder.get_object("Bimagen").set_image(self.image_background)

#Para el logo
		try:
			self.logo = self.lightdm.get_logo()
			logo = GdkPixbuf.Pixbuf.new_from_file_at_size(self.logo,100,50)
			self.image_logo = Gtk.Image()
			self.image_logo.set_from_pixbuf(logo)
			self.Builder.get_object("Blogo").set_image(self.image_logo)
		except:
			print "No logo"
			self.Builder.get_object("Blogo").hide()
			self.Builder.get_object("label2").hide()
		
#Lectura de temas.
		temas = commands.getoutput("ls /usr/share/themes/")
		temas = temas.split("\n")
		self.temas = temas
		Lista_temas = Gtk.ListStore(str)
		for i in temas:
			Lista_temas.append([i])
		self.Builder.get_object("combobox1").set_model(Lista_temas)
#Lectura de iconos.
		iconos = commands.getoutput("ls /usr/share/icons")
		iconos = iconos.split("\n")
		iconos_nuevos = []
		
		for j in iconos:
			if(j.find(".jpg")==-1):
				if(j.find(".png")==-1):
					iconos_nuevos.append(j)
	
		#print iconos_nuevos
		iconos = iconos_nuevos
		Lista_iconos = Gtk.ListStore(str)
		for jj in iconos:
			Lista_iconos.append([jj])
		
		self.iconos = iconos
		self.Builder.get_object("combobox2").set_model(Lista_iconos)
				
#Lectura de usuarios.
		usuarios = commands.getoutput("groups")
		self.usuarios = usuarios.split(" ")

#Finalizando
		self.Builder.get_object("Bfont").set_font_name(self.lightdm.get_font())
		try:
			self.Builder.get_object("combobox1").set_active(temas.index(self.lightdm.get_theme()))
		except:
			self.Builder.get_object("combobox1").set_active(0)
		
		try:
			self.Builder.get_object("combobox2").set_active(iconos.index(self.lightdm.get_icon_theme()))
		except:
			self.Builder.get_object("combobox2").hide()
			print self.Builder.get_object("label4").hide()
		
		try:
			if(self.lightdm.get_active_autologin()!=0)&(self.lightdm.get_active_autologin()==self.usuarios[0]):
				self.Builder.get_object("autologin").set_active(True)
				self.Builder.get_object("autologin").set_label(self.Builder.get_object("autologin").get_label()+" "+self.usuarios[0])
			else:
				self.Builder.get_object("autologin").set_label(self.Builder.get_object("autologin").get_label()+" "+self.usuarios[0])
		except:
			self.Builder.get_object("autologin").set_label(self.Builder.get_object("autologin").get_label()+" "+self.usuarios[0])
			
		try:
			if(self.lightdm.get_active_guest()==0):
				self.Builder.get_object("autologin1").set_label("Cuenta de Invitado Desactivada")
			else:
				self.Builder.get_object("autologin1").set_label("Cuenta de Invitado Activada")
				self.Builder.get_object("autologin1").set_active(True)
		except:
			self.Builder.get_object("autologin1").set_label("Cuenta de Invitado Desactivada")
			print "Cuenta Invitado desactivada"
#-----------------------------------------------------------------------
		#EVENTOS
		self.Window.connect("destroy",self.window_quit)
		self.Builder.get_object("Bcerrar").connect("clicked",self.window_quit)
		self.Builder.get_object("Baplicar").connect("clicked", self.apply_changes)
		self.Builder.get_object("Bacerca").connect("clicked",self.view_about)
		self.Builder.get_object("autologin1").connect("clicked",self.is_active, self.Builder.get_object("autologin1"))
		
		self.Builder.get_object("Bimagen").connect("clicked", self.search_wallpaper)		
		self.Builder.get_object("Blogo").connect("clicked", self.search_logo)
#-----------------------------------------------------------------------		
		#MOSTRANDO TODO
		self.Window.show()
		
	def window_quit(self, signal):
		Gtk.main_quit()
		
	def view_about(self, signal):
		about = self.Builder.get_object("about_window")
		about.set_title("Acerca de Lightdm Configurator")
		try:
			self.Builder.get_object("image1").set_from_file("/usr/share/lightdm-configurator/data/about_image.png")
		except:
			self.Builder.get_object("image1").set_from_file("data/about_image.png")

		self.Builder.get_object("Bcerrar1").connect('clicked',self.cerrar,about)
		self.Builder.get_object("enlace").connect('clicked',self.openurl,self.Builder.get_object("enlace"))
		about.show()
	
	def message_window(self, texto):
		window = self.Builder.get_object("sucess_window")
		if(texto == False):
			window.set_title('Error')
			self.Builder.get_object("label7").set_text('No se aplican los cambios.')
		else:
			window.set_title('Behold')
			self.Builder.get_object("label7").set_text('Cambios Aplicados.')
			
		self.Builder.get_object("bcerrar").connect('clicked',self.cerrar, window)
		window.show()	
			
	def cerrar(self, signal, widget):
		widget.hide()
		
	def openurl(self,signal,Widget):
		if (commands.getoutput("whoami")=="root"):
			print "Navegando como root, esto puede ser peligroso."
			print "Arreglare esto en la proxima actualizacion."
			os.system("xdg-open http://" + Widget.get_uri())
		else:
			os.system("xdg-open http://" + Widget.get_uri())
#------------------------------------------------------------------------------------------------------
	def is_active(self, signal, widget):
		if(widget.get_active()==False):
			self.lightdm.set_active_guest(False)
			widget.set_label("Cuenta de Invitado Desactivada")
		else:
			self.lightdm.set_active_guest(True)
			widget.set_label("Cuenta de Invitado Activada")
#------------------------------------------------------------------------------------------------------
	def search_logo(self,signal):
		image = Gtk.Image()
		filtro = Gtk.FileFilter()
		filtro.set_name("Imagenes")
		filtro.add_mime_type("image/*")
		
		chooser = Gtk.FileChooserDialog("Selecciona Logo", None, Gtk.FileChooserAction.OPEN,
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                "Seleccionar", Gtk.ResponseType.OK))
		
		chooser.add_filter(filtro)
		chooser.set_preview_widget(image)
		chooser.connect("selection-changed", self.preview, image, chooser)
		
		chooser.show_all()
		result = chooser.run()
		
		if(result == Gtk.ResponseType.OK):
			self.sellogo(chooser)
			
		chooser.destroy()
#------------------------------------------------------------------------------------------------------
	def sellogo(self,selector):
		self.logo = selector.get_filename()
		self.lightdm.set_logo(self.logo)
		
		logo = GdkPixbuf.Pixbuf.new_from_file_at_size(self.logo,100,50)
		self.image_logo.set_from_pixbuf(logo)
		
		self.Builder.get_object("Blogo").set_image(self.image_logo)
		
#------------------------------------------------------------------------------------------------------
	def search_wallpaper(self,signal):
		image = Gtk.Image()
		filtro = Gtk.FileFilter()
		filtro.set_name("Imagenes")
		filtro.add_mime_type("image/*")
		
		chooser = Gtk.FileChooserDialog("Selecciona Wallpaper", None, Gtk.FileChooserAction.OPEN,
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                "Seleccionar", Gtk.ResponseType.OK))
		
		chooser.add_filter(filtro)
		chooser.set_preview_widget(image)
		chooser.connect("selection-changed", self.preview, image, chooser)
		
		chooser.show_all()
		result = chooser.run()
		
		if(result == Gtk.ResponseType.OK):
			self.selwallpaper(chooser)
			
		chooser.destroy()
		
#------------------------------------------------------------------------------------------------------
	def selwallpaper(self,selector):
		self.wall = selector.get_filename()
		self.lightdm.set_background(self.wall)
		wall = GdkPixbuf.Pixbuf.new_from_file_at_size(self.wall,100,50)
		self.image_background.set_from_pixbuf(wall)
		
		self.Builder.get_object("Bimagen").set_image(self.image_background)
		
#------------------------------------------------------------------------------------------------------
	def preview(self,signal,IMAGE,Widget):	
		try:
			active = Widget.get_preview_filename()
			background = GdkPixbuf.Pixbuf.new_from_file_at_size(active,200,100)
			IMAGE.set_from_pixbuf(background)
			have_preview = True
		except:
			have_preview = False
		Widget.set_preview_widget_active(have_preview)

#------------------------------------------------------------------------------------------------------
	def apply_changes(self, signal):
		
		self.lightdm.set_background(self.wall)
		
		self.lightdm.set_logo(self.logo)
				
		if(self.Builder.get_object("autologin").get_active()==True):
			self.lightdm.set_active_autologin(self.usuarios[0],self.Builder.get_object("spinbutton1").get_value_as_int())

		if(self.Builder.get_object("autologin1").get_active()==True):
			self.lightdm.set_active_guest(True)

		self.lightdm.set_theme(self.temas[self.Builder.get_object("combobox1").get_active()])
		
		if (self.Builder.get_object("combobox2").get_active()!=-1):
			self.lightdm.set_icon_theme(self.iconos[self.Builder.get_object("combobox2").get_active()])
			
		self.lightdm.set_font(self.Builder.get_object("Bfont").get_font_name())

		self.lightdm.set_antialias(True)
		
		self.lightdm.set_dpi(96)

		ORIG_LDM = "cp /etc/lightdm/lightdm.conf /etc/lightdm/lightdm.conf.orig"
		ORIG_GRT = "cp /etc/lightdm/"+self.lightdm.get_greeter()+" /etc/lightdm/"+self.lightdm.get_greeter()+".conf.orig"
		LDM = "/tmp/ldm/lightdm.conf"
		GRT = "/tmp/ldm/"+self.lightdm.get_greeter()+".conf"
		BACK = "/tmp/ldm/mkbackup.sh"
		
		
		os.system("mkdir -p /tmp/ldm/")
		self.lightdm.write_config_in_other_file(LDM,GRT)
			
		f = open(BACK,'w')
		f.write(ORIG_LDM + "\n")
		f.write(ORIG_GRT + "\n")
		f.write("cp /tmp/ldm/*.conf /etc/lightdm/")
		f.close()
		
		os.system("echo 1 > /tmp/ldm/copy") # Si copia no modifica esto
		os.system("chmod +x " + BACK)
		os.system("gksu " + BACK + " || echo 0 > /tmp/ldm/copy")
		
		lol = commands.getoutput("cat /tmp/ldm/copy")
		
		if(lol == '0' ):	
			print "No se cambia nada."
			self.message_window(False)
		else:
			print "Cambios Aplicados."
			self.message_window(True)

		
if __name__ == "__main__":
	MainWindow()
	Gtk.main()
