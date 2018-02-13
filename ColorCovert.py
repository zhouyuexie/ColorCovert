#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sublime
import sublime_plugin
import re
from .utils import util
from .utils import colorName

matchRGBNumber = re.compile( r'\d{1,3}')

"""settings"""
covertMode = 'rgb'
capitalization = True

class ColorCovertCommand(sublime_plugin.TextCommand):
	# all value outputs
	outputs = []
	# view and edit
	view = None
	edit = None
	# if innerCovertMode != "", must covert to innerCovertMode
	innerCovertMode = covertMode

	def __init__(self, view):
		# Load settings
		self.view = view

		settings = sublime.load_settings("ColorCovert.sublime-settings")
		capitalization = settings.get("capitalization")
		settings.add_on_change("covertMode", loadSettings) # addEventListener for covertMode
		settings.add_on_change("capitalization", loadSettings) # addEventListener for capitalization

		loadSettings()

	# main
	def run(self, edit, value, isSelect):
		self.outputs = []
		self.edit = edit

		if (value != ""):
			self.innerCovertMode = value
		else:
			self.innerCovertMode = covertMode

		# select section entry
		if isSelect:
			self.selectModeReplace(self.view.sel())
		# all page(todo)
		else:
			self.allReplace()

	def handle(self, selectPart):
		# selectPart: '#1722DF' or 'rgba(0,0,0,1)' or 'hsla(100, 80.0%, 29.2%, 0.2)'...
		output = util.covertColor(selectPart, self.innerCovertMode) # core handle function

		if output != None:
			if capitalization:
				output = output.upper()
			self.outputs.append(output)

	"""replace view select color"""
	def selectModeReplace(self, regions):
		"""covert select section"""
		for region in regions:
			if not region.empty():
				self.handle(self.view.substr(region))

		for i, output in enumerate(self.outputs):
			for j, region in enumerate(regions):
				if i == j and not region.empty():
					self.view.replace(self.edit, region, output)

	"""replace view all color"""
	def allReplace(self):
		for name in ['rgb', 'rgba', 'hsl', 'hsla', 'hex', 'cmyk', 'hsv']:
			firstMatchRegion = self.view.find(util.matchRE.get(name), 0, sublime.IGNORECASE)
			allMatchRegin = self.view.find_all(util.matchRE.get(name), sublime.IGNORECASE)

			if name == self.innerCovertMode:
				continue

			for i in range(len(allMatchRegin)):
				if firstMatchRegion.empty():
					outputs.append(1)
					continue

				output = util.covertColor(self.view.substr(firstMatchRegion), self.innerCovertMode) # core handle function
				if output != None:
					if capitalization:
						output = output.upper()
					# outputs.append(output)
					self.view.replace(self.edit, firstMatchRegion, output)
				firstMatchRegion = self.view.find(util.matchRE.get(name), firstMatchRegion.end(), sublime.IGNORECASE)

class ColorCovertNameCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view

		# main
	def run(self, edit):
		self.edit = edit

		self.covertColorName()

	"""covert color name"""
	def covertColorName(self):
		regions = self.view.sel()
		outputs = []

		for region in regions:
			if not region.empty():
				name = colorName.mapColorName.get(self.view.substr(region).lower(), self.view.substr(region))
				output = colorName.colorName.get(name, name)

				if output != name:
					outputs.append(output)

		for i, output in enumerate(outputs):
			for j, region in enumerate(regions):
				if i == j and not region.empty():
					self.view.replace(self.edit, region, output)

def loadSettings():
	"""Loads settings from the ColorCovert.sublime-settings file"""

	global covertMode
	global capitalization

	settings = sublime.load_settings("ColorCovert.sublime-settings")

	covertMode = settings.get("covert_mode")
	capitalization = settings.get("capitalization")