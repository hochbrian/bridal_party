#!/usr/bin/python

#
#  Copyright © 2014 Brian E Hoch
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#########################################################################
#                                 TO DO			                 		#
#########################################################################
#   ++ Write int to bool converter function								#
#      ++ Use function in read and write calls							#
#   - Write UI and functions for adding groomsman						#
#   - Switch TableView datasource to groomsmen array					#
#   - UIWebView for viewing Markdown speech								#
#   - Speech editor UI													#
#########################################################################

# coding: utf-8

import ui
import webbrowser
import random
from console import hud_alert
import sqlite3
import markdown2

global g

class groomsman():
	def __init__(self, **kwargs):
		#name, last_name, pronunciation, phone, paid, party_paid, tux, order, bridesmaid
		self.properties = kwargs

	def get_phone(self):
		return self.properties.get('phone', None)

	def set_phone(self, phone):
		self.properties['phone'] = phone

	def get_property(self, property):
		return self.properties.get(property, None)

	def set_property(self, property, value):
		self.properties[property] = value

	def list_data(self):
		for k in self.properties:
			print(k,self.properties[k])

def table_did_select_row(sender):
	global g
	g = groomsmen[str(sender.selected_row)]
	show_groomsman()

def table_did_select_accessory(sender):
	global g
	g = groomsmen[str(sender.selected_row)]
	show_groomsman()

def show_groomsman():
	subview = ui.load_view('bridal_party_detail')
	subview.name = g.get_property('name')
	nav_view.push_view(subview)
	#subview['name_label'].text = g.get_property('name')
	subview['paid'].value = g.get_property('paid')
	subview['tux'].value = g.get_property('tux')
	subview['party_paid'].value = g.get_property('party_paid')
	subview['position_label'].text = 'Position: {}'.format(g.get_property('order')+1)
	subview['bridesmaid_label'].text = 'Walking with {}'.format(g.get_property('bridesmaid'))
	print(g.get_property('pronunciation'))

def contact_button_press(sender):
	if sender.name == 'sms_button':
		protocol = 'sms'
		contact = g.get_phone()
	elif sender.name == 'dial_button':
		protocol = 'tel'
		contact = g.get_phone()
	elif sender.name == 'email_button':
		protocol = 'mailto'
		contact = '{}?subject=Graham%20and%20Kali%27s%20Wedding'.format(g.get_property('email'))
	else: print('throw error')
	webbrowser.open('{}:{}'.format(protocol, contact))

def toggle_switch_press(sender):
	# Provide random positive and negative feedback for toggle switches
	response = random.randrange(4)
	if response == 0:
		yes, no = 'Sweet!', 'Uh oh!'
	elif response == 1:
		yes, no = 'Tiger blood!', 'Oh Noes!'
	elif response == 2:
		yes, no = 'For Great Justice!', 'Well, dang'
	elif response == 3:
		yes, no = '#Winning', '::sigh::'

	# Convert boolean values to int
	if sender.value == True:
		b = 1
	else: b = 0

	try:
		write_data(sender.name,b,g.get_property('name'),True)
		hud_alert(yes,'success',.5)
	except:
		hud_alert(no,'error',.5)
		print('Did not attempt write')

def load_data():
	open_db()
	c.execute('SELECT * FROM groomsmen')
	#print(c.fetchall())
	party = {}
	# Loop through records within each row and split into groomsman object properties
	n=0
	for gm in c.fetchall():
		i = 0
		name=str(n)
		for p in gm:
			if i == 0:
				#name=p
				g = groomsman(name=p)
			elif i == 1:
				g.set_property('last_name',p)
			elif i == 2:
				g.set_property('pronunciation',p)
			elif i == 3:
				g.set_property('phone',p)
			elif i == 4:
				g.set_property('email',p)
			elif i == 5:
				# Convert int to Bool
				if p == 0:
					b = False
				else: b = True
				g.set_property('paid',b)
			elif i == 6:
				# Convert int to Bool
				if p == 0:
					b = False
				else: b = True
				g.set_property('party_paid',b)
			elif i == 7:
				# Convert int to Bool
				if p == 0:
					b = False
				else: b = True
				g.set_property('tux',b)
			elif i == 8:
				g.set_property('order',p)
			else:
				g.set_property('bridesmaid',p)
			i += 1
		# Add row to groomsman array
		party[name] = g
		n+=1
	close_db()
	return party

def write_data(field, value, name, is_switch):
	open_db()
	query = 'UPDATE groomsmen SET {}={} WHERE name=\'{}\''.format(field, value, name)
	try:
		c.execute(query)
	except DBWriteError:
		print('Could not write data to db')
	close_db()

	# Convert int to bool if sender was switch
	if is_switch == True:
		if value == 0:
			p = False
		else: p = True
	else: p = value

	g.set_property(field,p)

def main():
	global groomsmen
	# Load groomsmen from database
	groomsmen = load_data()
	for d in groomsmen:
		g = groomsmen[d]

	#present_groomsmen_view(1)
	present_top_nav(1)

def open_db():
	global conn
	conn = sqlite3.connect('groomsmen.sqlite')
	global c
	c = conn.cursor()

def close_db():
	conn.commit()
	conn.close()

def get_groomsman_by_row():
	r=[]
	for i in groomsmen:
		r.append(groomsmen[i].get_property('name'))
	return r

class g_table_datasource ():

	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(groomsmen.keys())

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell('subtitle')
		#cell.accessory_type = 'detail_button'
		#cell.accessory_type = 'detail_disclosure_button'
		cell.accessory_type = 'disclosure_indicator'
		cell.text_label.text = groomsmen[str(row)].get_property('name')
		cell.detail_text_label.text = groomsmen[str(row)].get_property('bridesmaid')
		cell.detail_text_label.text_color = '#777'
		#cell.image_view
		return cell

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		return False

	def tableview_can_delete(self, tableview, section, row):
		return False

	def tableview_can_move(self, tableview, section, row):
		return False

def add_groomsman():
	pass

def add_groomsman_button_tap(sender):
	subview = ui.load_view('groomsman_genesis')
	subview['phone_txtfld'].keyboard_type = ui.KEYBOARD_DECIMAL_PAD
	subview['email_txtfld'].keyboard_type = ui.KEYBOARD_EMAIL
	subview['order_txtfld'].keyboard_type = ui.KEYBOARD_NUMBER_PAD
	nav_view.push_view(subview)

def create_new_groomsman(sender):
	sql = "INSERT INTO groomsmen VALUES (?, ?, ?,?,?,0,0,0,?,?);"
	#'first', 'last', 'pronunc', 'phone', 'email', 0,0,0,order, 'bridesmaid');
	form = sender.superview
	name = form['name_txtfld'].text.split(None, 1)
	first_name = name[0]
	last_name = name[1].strip()
	if form['pronunciation_txtfld'].text != '':
		pronunc = form['pronunciation_txtfld'].text.strip()
	else: pronunc = ''
	phone = form['phone_txtfld'].text.strip()
	email = form['email_txtfld'].text.strip()
	order = form['order_txtfld'].text.strip()
	bridesmaid = form['bridesmaid_txtfld'].text.strip()
	#print(sql.format(first_name,last_name,pronunc,phone,email,order,bridesmaid))
	query = (first_name,last_name,pronunc,phone,email,order,bridesmaid)
	open_db()
	c.execute(sql, query)
	close_db()

	sender.superview.close()
	#sender.superview.navigation_view['groomsmen_tbl'].reload()

def close_groomsman_add(sender):
	#sender.superview.navigation_view
	pass

def present_groomsmen_view(sender):
	# Load bridal_party.pyui as NavigationView
	v = ui.load_view('bridal_party')
	v.name = 'Groomsmen'
	groomsmen_table = g_table_datasource()
	v['groomsmen_tbl'].data_source = groomsmen_table
	#global nav_view
	#nav_view = ui.NavigationView(v)
	#nav_view.bar_tint_color = '#cccccc'
	#nav_view.tint_color = '#90a681'
	#nav_view.title_color = '#90a681'
	#nav_view.present('fullscreen')#, hide_title_bar=True)

def present_speech_view(sender):
	global speech_nav_view
	sv = ui.load_view('speech_write')
	sv.name = 'Speech'
	speech_nav_view = ui.NavigationView(sv)
	speech_nav_view.bar_tint_color = '#90a681'
	speech_nav_view.tint_color = '#ffffff'
	speech_nav_view.title_color = '#ffffff'
	speech_nav_view.present('sv')

class nav_table_datasource():
	global nav_items
	nav_items = ['Groomsmen','Manage Groomsmen','Manage Bridesmaids','Write Speech','Schedule']

	def tableview_number_of_sections(self, tableview):
		return 1
	def tableview_number_of_rows(self, tableview, section):
		return len(nav_items)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.accessory_type = 'disclosure_indicator'
		cell.text_label.text = nav_items[row]
		return cell

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		return False

	def tableview_can_delete(self, tableview, section, row):
		return False

	def tableview_can_move(self, tableview, section, row):
		return False

def present_top_nav(sender):
	superview = ui.load_view('super_view')
	superview.name = 'Home'
	nav_table = nav_table_datasource()
	superview['nav_tbl'].data_source = nav_table
	global nav_view
	nav_view = ui.NavigationView(superview)
	nav_view.bar_tint_color = '#888888'
	#nav_view.tint_color = '#90a681'
	#nav_view.title_color = '#90a681'
	nav_view.tint_color = '#ffffff'
	nav_view.title_color = '#ffffff'
	nav_view.present('fullscreen')#, hide_title_bar=True)

def nav_did_select_row(sender):
	choice = sender.selected_row
	if choice == 0:
		subv = ui.load_view('bridal_party')
		subv.name = 'Groomsmen'
		groomsmen_table = g_table_datasource()
		subv['groomsmen_tbl'].data_source = groomsmen_table
	elif choice == 1:
		subv = ui.load_view('groomsman_genesis')
		subv.name = 'New Groomsman'
	elif choice == 2:
		print('3')
	elif choice == 3:
		subv = ui.load_view('speech_write')
		subv.name = 'Write'
		subv['speech'].font = ('SourceCodePro-Regular', 18)
		subv['speech'].text = load_speech()
	else: print('5')
	nav_view.push_view(subv)

def save_speech(sender):
	sql = 'INSERT INTO speech VALUES (NULL, ?);'
	query = (sender.superview['speech'].text,)
	open_db()
	c.execute(sql, query)
	close_db()

def load_speech():
	open_db()
	c.execute('SELECT speech FROM speech WHERE version = (SELECT MAX(version) FROM speech);')# 1;')
	text = ''
	try:
		for line in c.fetchone():
			text += line
	except:
		text = ''
	close_db()
	return text

def view_speech(sender):
	#save_speech(sender)
	speech = '''
<!DOCTYPE html>
<head>
  <style>
    body {
          font-family: Avenir, sans-serif;
          }
    h1:after {
              content: '';
              width: 100%;
              float: left;
              border-bottom: 1px solid #777;
              }
  </style>
</head>
<body>\n'''
	#speech += load_speech()
	speech += sender.superview['speech'].text
	speech += '''
</body>'''
	spview = ui.load_view('speech_viewer')
	spview.name = 'Speech'
	spview['md_viewer'].load_html(markdown2.markdown(speech))
	nav_view.push_view(spview)

if __name__ == "__main__":
	main()
