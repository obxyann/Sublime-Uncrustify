# ref:
# https://www.sublimetext.com/forum/viewtopic.php?f=3&t=11292
# http://superuser.com/questions/556609/filtering-sublime-text-2-buffer-contents-through-an-external-program

import sublime, sublime_plugin, subprocess, traceback, os.path
import re

DefaulBinary = "uncrustify"

def getProgram():
	# load settings
	settings = sublime.load_settings("Uncrustify.sublime-settings")
	user_settings = sublime.load_settings("Preferences.sublime-settings")

	# get binary setting
	program = user_settings.get("uncrustify_binary") or \
			    settings.get("uncrustify_binary")
	if program:
		# only if exists
		if not os.path.exists(program):
			err = "Cannot find '%s'" % program
			sublime.error_message(err)
			return ""
	else:
		# will find uncrustify in PATH
		program = DefaulBinary

	return program

def getConfig():
	# load settings
	settings = sublime.load_settings("Uncrustify.sublime-settings")
	user_settings = sublime.load_settings("Preferences.sublime-settings")

	# get default config setting
	config = user_settings.get("uncrustify_config") or \
			 settings.get("uncrustify_config")
	if config:
		# only if exists
		if not os.path.exists(config):
			err = "Cannot find '%s'" % config
			sublime.error_message(err)
			return ""
	else:
		# try from environment variable
		config = os.getenv("UNCRUSTIFY_CONFIG", "")
		if not config:
			err = "Need to specify the config file in settings or set UNCRUSTIFY_CONFIG in OS"
			sublime.error_message(err)
			return ""
		# only if exists
		if not os.path.exists(config):
			err = "Cannot find '%s' (from UNCRUSTIFY_CONFIG)" % config
			sublime.error_message(err)
			return ""

	return config

def getConfigByLang(lang):
	# load settings
	settings = sublime.load_settings("Uncrustify.sublime-settings")
	user_settings = sublime.load_settings("Preferences.sublime-settings")

	# get config setting
	configs = user_settings.get("uncrustify_config_by_lang", []) or \
			  settings.get("uncrustify_config_by_lang", [])

	# find one matched the lang
	for each in configs:
		for key, config in each.items():
			# print(key, config)
			if key and config and lang == key:
				# only if exists
				if not os.path.exists(config):
					err = "Cannot find '%s' (for %s)" % (config, lang)
					sublime.error_message(err)
					return ""
				return config

	# just no one matched
	return "none"

def getConfigByFilter(path_name):
	# load settings
	settings = sublime.load_settings("Uncrustify.sublime-settings")
	user_settings = sublime.load_settings("Preferences.sublime-settings")

	# get config setting
	configs = user_settings.get("uncrustify_config_by_filter", []) or \
			  settings.get("uncrustify_config_by_filter", [])

	# find one appeared in path_name
	for each in configs:
		for key, config in each.items():
			# print(key, config)
			if key and config and path_name.find(key):
				# only if exists
				if not os.path.exists(config):
					err = "Cannot find '%s' (for %s)" % (config, lang)
					sublime.error_message(err)
					return ""
				return config

	# just no one matched
	return "none"

def guessLanguage(ext_name):
	if ext_name == ".c":
		return "C"
	elif ext_name == ".cpp" or \
		 ext_name == ".h" or \
		 ext_name == ".cxx" or \
		 ext_name == ".hpp" or \
		 ext_name == ".cc" or \
		 ext_name == ".cp" or \
		 ext_name == ".C" or \
		 ext_name == ".CPP" or \
		 ext_name == ".c++":
		return "CPP"
	elif ext_name == ".d" or \
		 ext_name == ".di":
		return "D"
	elif ext_name == ".cs":
		return "CS"
	elif ext_name == '.java':
		return "JAVA"
	elif ext_name == ".pawn" or \
		 ext_name == ".p" or \
		 ext_name == ".sma" or \
		 ext_name == ".inl":
		return "PAWN"
	elif ext_name == ".m":
		return "OC"
	elif ext_name == ".mm":
		return "OC+"
	elif ext_name == ".vala":
		return "VALA"
	elif ext_name == ".sql":
		return "SQL"
	elif ext_name == ".es":
		return "ECMA"

	err = "Unknown extention '%s'" % ext_name
	sublime.error_message(err)
	return ""

def getLanguage(view):
	scope = view.scope_name(view.sel()[0].end())

	result = re.search("\\bsource\\.([a-z+\-]+)", scope)

	source = result.group(1) if result else "Plain Text"
	# print(source)
	if source == "Plain Text":
		# check if macth our extention names
		file_name, ext_name = os.path.splitext(view.file_name())
		return guessLanguage(ext_name)

	if source == "c":
		return "C"
	elif source == "c++":
		return "CPP"
	elif source == "d":
		return "D"
	elif source == "c#":
		return "CS"
	elif source == 'java':
		return "JAVA"
	elif source == "pawn":		# not listed in sublime default
		return "PAWN"
	elif source == "objc":
		return "OC"
	elif source == "objc++":
		return "OC+"
	elif source == "vala":		# not listed in sublime default
		return "VALA"
	elif source == "sql":
		return "C"
	elif source == "es":		# not listed in sublime default
		return "ECMA"

	msg = "Unsupported language '%s'" % source
	sublime.message_dialog(msg)
	return ""

def reformat(view, edit, region):
	content = view.substr(region)
	command = []

	# assign the external program
	program = getProgram()
	if not program:
		return

	command.append(program)

	# specify the lauguage override (because input is from stdin)
	lang = getLanguage(view)
	if not lang:
		return

	command.append("-l")
	command.append(lang)

	# specify the config file:
	# try 1
	config = getConfigByFilter(view.file_name())
	if not config:
		return
	# try 2
	if config == "none":
		config = getConfigByLang(lang)
		if not config:
			return
	# try 3
	if config == "none":
		config = getConfig()
		if not config:
			return

	command.append("-c")
	command.append(config)

	print(command)
	# MEMO:
	# command[] should like
	# ['C:/path/uncrustify.exe', '-l', 'CPP', '-c', 'C:/path/ob.cfg']

	try:
		# run
		proc = subprocess.Popen(command, \
			   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

		output = proc.communicate(input=content.encode("utf-8"))[0]

		# wait return
		return_code = proc.poll()
		if (return_code != 0):
			stderr = proc.communicate()[1]
			print(" Error:\n" + stderr.decode("utf-8"))
			raise Exception(("Non-zero return code (%d): " + stderr) % return_code)

		# print(output)

		# replace by result
		view.replace(edit, region, output.decode("utf-8"))

	except (OSError, ValueError, subprocess.CalledProcessError, Exception) as e:
		err = "%s was unable to executed (%s)" % (command[0], traceback.print_exc())
		sublime.error_message(err)

def open_file(window, file_name):
	window.open_file(file_name)

# Uncrustify the document
class UncrustifyDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# make full view as region
		region = sublime.Region(0, self.view.size())
		if region.empty():
			sublime.message_dialog("Empty document")
			return

		# go
		reformat(self.view, edit, region)

# Uncrustify only the selection region
class UncrustifySelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get selections
		sel = self.view.sel()

		# pick 1st selection as regoin
		# TODO: try to support multi-selection...
		# for region in self.view.sel():
		# 	...
		region = sel[0]
		if region.empty():
			sublime.message_dialog("No selection")
			return

		# go
		reformat(self.view, edit, region)

# open the config file to edit
class UncrustifyOpenCfgCommand(sublime_plugin.WindowCommand):
	def run(self):
		config = getConfig()
		if not config:
			return

		# go
		open_file(self.window, config)


# open the config file which matches current document to edit
class UncrustifyOpenCfgCurrentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get the lauguage
		lang = getLanguage(self.view)
		if not lang:
			return

		# specify the config file:
		# try 1
		config = getConfigByFilter(self.view.file_name())
		if not config:
			return
		# try 2
		if config == "none":
			config = getConfigByLang(lang)
			if not config:
				return
		# try 3
		if config == "none":
			config = getConfig()
			if not config:
				return

		# go
		open_file(sublime.active_window(), config)
