import sublime
import sublime_plugin
import os.path
import subprocess
import re			# need regular expression operations
import fnmatch		# need Unix filename pattern matching
# import traceback

DEFAULT_EXECUTABLE = "uncrustify"
DEFAULT_RULE = 0

def getSetting(name):
	# load settings
	user_settings = sublime.load_settings("Preferences.sublime-settings")
	settings = sublime.load_settings("Uncrustify.sublime-settings")

	# get setting
	value = user_settings.get(name) or settings.get(name)

	return value;

def getExecutable():
	# get executable setting
	executable = getSetting("uncrustify_executable")

	if executable:
		# check if a file exists
		if not os.path.exists(executable):
			err = "Cannot find '%s'\n\nCheck your Uncrustify settings!" % executable
			sublime.error_message(err)
			return ""
	else:
		# will find uncrustify in PATH
		executable = DEFAULT_EXECUTABLE

	return executable

def getConfig():
	# get default config setting
	config = getSetting("uncrustify_config")

	if config:
		# check if a file exists
		if not os.path.exists(config):
			err = "Cannot find '%s'\n\nCheck your Uncrustify settings!" % config
			sublime.error_message(err)
			return ""
	else:
		# try from environment variable
		config = os.getenv("UNCRUSTIFY_CONFIG", "")

		if not config:
			err = "Need to specify the config file in Uncrustify settings\nor set UNCRUSTIFY_CONFIG in OS!"
			sublime.error_message(err)
			return ""

		# check if a file exists
		if not os.path.exists(config):
			err = "Cannot find '%s'\nfrom environment variable UNCRUSTIFY_CONFIG\n\nCheck your Uncrustify settings!" % config
			sublime.error_message(err)
			return ""

	return config

def getConfigByLang(lang):
	# get config setting
	configs = getSetting("uncrustify_config_by_lang")

	if not configs:
		return "none"

	# find one matched the language
	for each in configs:
		for key, config in each.items():
			if not key or not config:
				continue

			# only for debug
			# print(key, config)

			if lang == key:
				# check if a file exists
				if not os.path.exists(config):
					err = "Cannot find '%s'\nfor language: %s\n\nCheck your Uncrustify settings!" % (config, lang)
					sublime.error_message(err)
					return ""
				return config

	# just no one matched
	return "none"

def getConfigByFilter(path_name):
	if not path_name:
		return "none"

	# get config setting
	configs = getSetting("uncrustify_config_by_filter")

	if not configs:
		return "none"

	# get filtering rule
	rule = getSetting("uncrustify_filtering_rule")

	if not rule:
		rule = DEFAULT_RULE

	if not isinstance(rule, int):
		err = "Invalid filtering rule, not an integer\n\nCheck your Uncrustify settings!"
		sublime.error_message(err)
		return ""

	if rule < 0 or rule > 2:
		err = "Invalid filtering rule: %d, out of range\n\nCheck your Uncrustify settings!" % rule
		sublime.error_message(err)
		return ""

	# force to unix style
	path_name = path_name.replace('\\', '/')

	# only for debug
	# print("path_name: " + path_name)

	# find one appeared in path_name
	for each in configs:
		for pattern, config in each.items():
			if not pattern or not config:
				continue

			# only for debug
			# print(rule, pattern, config)

			if (rule == 0 and path_name.find(pattern) >= 0) or \
			   (rule == 1 and fnmatch.fnmatch(path_name, pattern)) or \
			   (rule == 2 and re.match(pattern, path_name)):
				# check if a file exists
				if not os.path.exists(config):
					err = "Cannot find '%s'\nfor pattern: %s\n\nCheck your Uncrustify settings!" % (config, pattern)
					sublime.error_message(err)
					return ""
				return config

	# just no one matched
	return "none"

def guessLanguage(ext_name):
	lang_dict = {
		".c": "C",
		".cpp": "CPP",
		".h": "CPP",
		".cxx": "CPP",
		".hxx": "CPP",
		".cc": "CPP",
		".cp": "CPP",
		".C": "CPP",
		".CPP": "CPP",
		".c++": "CPP",
		".d": "D",
		".di": "D",
		".cs": "CS",
		".java": "JAVA",
		".pawn": "PAWN",
		".p": "PAWN",
		".sma": "PAWN",
		".m": "OC",
		".mm": "OC+",
		".vala": "VALA",
		".sqc": "SQL",		# embedded SQL
		".es": "ECMA"
	}
	lang = lang_dict.get(ext_name, "")

	if not lang:
		msg = "Unknown file extension: %s" % ext_name
		# sublime.message_dialog(msg)
		sublime.status_message(msg)

	return lang

def getLanguage(view):
	# get topmost scope
	scope = view.scope_name(view.sel()[0].end())

 	# should be source.<lang_name>
	result = re.search("\\bsource\\.([a-z0-9+\-]+)", scope)

	lang_name = result.group(1) if result else "Plain Text"

	# only for debug
	# print("lang_name: " + lang_name)

	if lang_name == "Plain Text":
		# check if match our extension names
		path = view.file_name()
		if not path:
			msg = "Unknown language: %s" % lang_name
			# sublime.message_dialog(msg)
			sublime.status_message(msg)
			return ""

		file_name, ext_name = os.path.splitext(path)
		return guessLanguage(ext_name)

	lang_dict = {
		'c': 'C',
		'c++': 'CPP',
		'd': 'D',
		'cs': 'CS',
		'java': 'JAVA',
		'pawn': 'PAWN',		# not listed in sublime default, just for the future
		'objc': 'OC',
		'objc++': 'OC+',
		'vala': 'VALA',		# not listed in sublime default, just for the future
		'es': 'ECMA',		# not listed in sublime default, just for the future
		# 'js': "ECMA"
	}
	lang = lang_dict.get(lang_name, "")

	if not lang:
		msg = "Unsupported language: %s" % lang_name
		# sublime.message_dialog(msg)
		sublime.status_message(msg)

	return lang

def reformat(view, edit, region):
	content = view.substr(region)
	command = []

	# only for debug
	# print("content: " + content)

	# assign the external program
	program = getExecutable()
	if not program:
		return

	command.append(program)

	# specify the language override (because input is from stdin)
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

	# only for debug
	#	command[] should like
	#	['C:/path/uncrustify.exe', '-l', 'CPP', '-c', 'C:/path/my.cfg']
	# print("command[]: " + command)

	# dump command[]
	msg = ""
	for str in command:
		msg += str
		msg += " "
	print("> " + msg + "...")
	sublime.status_message(msg + "...")

	try:
		# run
		proc = subprocess.Popen(command, \
			   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

		output = proc.communicate(input=content.encode("utf-8"))[0]

		# wait return
		return_code = proc.poll()
		if return_code != 0:
			stderr = proc.communicate()[1]
			if stderr:
				err = "Found error in executing '%s':\n\n%s" % (command[0], stderr.decode("utf-8"))
			else:
				err = "Found error in executing '%s':\n\nCode: %d" % (command[0], return_code)
			sublime.error_message(err)
			return

		# only for debug
		# print("output: " + output)

		# replace by result
		view.replace(edit, region, output.decode("utf-8"))

	except (OSError, ValueError, subprocess.CalledProcessError, Exception) as e:
		# only for debug
		# traceback.print_exc()

		if command[0] == DEFAULT_EXECUTABLE:
			err = "Cannot execute '%s' (from PATH)\n\n%s\n\nNeed to specify the executable file in Uncrustify settings!" % (command[0], e)
		else:
			err = "Cannot execute '%s'\n\n%s" % (command[0], e)
		sublime.error_message(err)

def open_file(window, file_name):
	window.open_file(file_name)

# Uncrustify the document
class UncrustifyDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# make full view as region
		region = sublime.Region(0, self.view.size())
		if region.empty():
			# sublime.message_dialog("Empty document!")
			sublime.status_message("Empty document!")
			return

		# go
		reformat(self.view, edit, region)

# Uncrustify only the selection region
class UncrustifySelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get selections
		sels = self.view.sel()

		# pick 1st selection as region
		# TODO: try to support multi-selection...
		# for region in sels
		# 	...
		region = sels[0]
		if region.empty():
			# sublime.message_dialog("No selection!")
			sublime.status_message("No selection!")
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
		# get the language
		lang = getLanguage(self.view)
		if not lang:
			return

		# specify the config file:
		# try 1, if matches one of filters
		config = getConfigByFilter(self.view.file_name())
		if not config:
			return
		# try 2, if matches one of languages
		if config == "none":
			config = getConfigByLang(lang)
			if not config:
				return
		# try 3, use default
		if config == "none":
			config = getConfig()
			if not config:
				return

		# go
		open_file(sublime.active_window(), config)
