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
#                                 TO DO                 		#
#########################################################################
#   - Write int to bool converter function				#
#      - Use function in read and write calls				#
#   - Write UI and functions for adding groomsman			#
#   - Switch TableView datasource to groomsmen array			#
#   - UIWebView for viewing Markdown speech				#
#   - Speech editor UI							#
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
	if sender.selected_row == 0:
		g = groomsmen['Brian']
	elif sender.selected_row == 1:
		g = groomsmen['Craig']
	elif sender.selected_row == 2:
		g = groomsmen['Eric']
	elif sender.selected_row == 3:
		g = groomsmen['Levi']
	elif sender.selected_row == 4:
		g = groomsmen['Elijah']
	else: g = None 
	show_groomsman()

def show_groomsman():
	subview = ui.load_view('bridal_party_detail')
	nav_view.push_view(subview)
	subview['name_label'].text = g.get_property('name')
	subview['paid'].value = g.get_property('paid')
	subview['tux'].value = g.get_property('tux')
	subview['party_paid'].value = g.get_property('party_paid')

def phone_button_press(sender):
	if sender.name == 'sms_button':
		protocol = 'sms'
	elif sender.name == 'dial_button':
		protocol = 'tel'
	else: print('throw error')
	webbrowser.open('{}:{}'.format(protocol, g.get_phone()))

def show_info(sender):
	# Display overlay of additional info
	info = ui.load_view('info')
	info['name_label'].text = '{} {}'.format(g.get_property('name'), g.get_property('last_name'))
	info['order_label'].text = 'Order : {}'.format(str(g.get_property('order')+1))
	info['bridesmaid_label'].text = 'Bridesmaid : {}'.format(g.get_property('bridesmaid'))
	nav_view.push_view(info)

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
	c.execute('SELECT * FROM groomsmen;')
	party = {}
	# Loop through records within each row and split into groomsman object properties
	for gm in c.fetchall():
		i = 0
		name = ''
		for p in gm:
			if i == 0:
				name = p
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
	
	# Load bridal_party.pyui as NavigationView
	v = ui.load_view('bridal_party')
	v.name = 'Groomsmen'
	global nav_view
	nav_view = ui.NavigationView(v)
	nav_view.tint_color = '#ed9500'
	nav_view.present('fullscreen')
	
def open_db():
	global conn 
	conn = sqlite3.connect('groomsmen.sqlite')
	global c
	c = conn.cursor()

def close_db():
	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	main()
