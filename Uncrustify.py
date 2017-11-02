import sublime
import sublime_plugin
import os.path
import subprocess
import re			# need regular expression operations
import fnmatch		# need Unix filename pattern matching
# import traceback

DEFAULT_EXECUTABLE = "uncrustify"
DEFAULT_RULE = 0

keep_quiet = False	# force all messages goto the status bar (do not pop dialog to the user)

def getSetting(name):
	# User, or project, specific settings. These take priority
	# over other settings.
	user_settings = sublime.active_window().active_view().settings()

	# Package specific settings -- fallback.
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

# This allows a project specific override (and will normally also pick
# up the normal settings from the user preferences.) We expand
# ${project_dir} into the directory where the project file is located,
# giving projects the ability to specify a relative file name for the
# uncrustify.cfg (e.g. they might store this within their project)
def expandConfig(path):
	# get project name
	project_name = sublime.active_window().project_file_name()
	if project_name:
		variables = {
		   'project_dir': os.path.dirname(project_name)
		}
		# permit '${project_dir}' to allow a configuration file
		# relative to the project to be specified.
		path = sublime.expand_variables(path, variables)
	return os.path.expandvars(path)

def getConfig():
	# get default config setting
	config = getSetting("uncrustify_config")
	if config:
		config = expandConfig(config)
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
		config = expandConfig(config)
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
				config = expandConfig(config)
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
				config = expandConfig(config)
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
	lang = lang_dict.get(ext_name)
	if not lang:
		msg = "Unknown file extension: %s" % ext_name
		# get popup rule
		rule = getSetting("uncrustify_popup_unsupport") and not keep_quiet
		if rule == True:
			sublime.message_dialog(msg)
		else:
			sublime.status_message(msg)
		return ""

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
			# get popup rule
			rule = getSetting("uncrustify_popup_unsupport") and not keep_quiet
			if rule == True:
				sublime.message_dialog(msg)
			else:
				sublime.status_message(msg)
			return ""

		file_name, ext_name = os.path.splitext(path)
		return guessLanguage(ext_name)

	lang_dict = {
		"c": "C",
		"c++": "CPP",
		"d": "D",
		"cs": "CS",
		"java": "JAVA",
		"pawn": "PAWN",		# not listed in sublime default, just for the future
		"objc": "OC",
		"objc++": "OC+",
		"vala": "VALA",		# not listed in sublime default, just for the future
		"es": "ECMA"		# not listed in sublime default, just for the future
	}
	lang = lang_dict.get(lang_name)
	if not lang:
		msg = "Unsupported language: %s" % lang_name
		# get popup rule
		rule = getSetting("uncrustify_popup_unsupport") and not keep_quiet
		if rule == True:
			sublime.message_dialog(msg)
		else:
			sublime.status_message(msg)
		return ""

	return lang

# ***WIP*** below codes need to review 
# Uncrustify the selection
def format(view, edit, text,region, indent_count, indent_size):
	# assign the external program
	program = getExecutable()
	if not program:
		return

	# specify the language override (because input is from stdin)
	lang = getLanguage(view)
	if not lang:
		return

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

	command = [program, "-l", lang, "-c", config]
	# command[] should like
	# ['C:/path/uncrustify.exe', '-l', 'CPP', '-c', 'C:/path/my.cfg']

	# show command[]
	running = ' '.join(command)
	print("> " + running + " ...")
	sublime.status_message(running + " ...")

	# prepare the input
	content = text.encode("utf-8")

	platform = sublime.platform()

	try:
		# run
		# TODO: si = None
		# TODO: if os.name == 'nt':
		if platform == "windows":
			# to hide the console window brings from command
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			# si.wShowWindow = subprocess.SW_HIDE 	# this is default provided

			proc = subprocess.Popen(command, \
				   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, startupinfo = si)
		else: # "osx" or "linux"
			proc = subprocess.Popen(command, \
				   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

		# send input and wait for the process terminated
		outs, errs = proc.communicate(input=content)

		# check the return code from Uncrustify
		ret_code = proc.poll()
		if ret_code != 0:
			if errs:
				msg = errs.decode("utf-8")
				# slice the last useless part if found (from Uncrustify)
				pos = msg.find("Try running with -h for usage information")
				err = "Uncrustify return error %d:\n\n%s" % (ret_code, msg[:pos])
			else:
				err = "Uncrustify return error %d:" % ret_code
			sublime.error_message(err)
			return

	except (OSError, ValueError, subprocess.CalledProcessError, Exception) as e:
		# only for debug
		# traceback.print_exc()

		if command[0] == DEFAULT_EXECUTABLE:
			err = "Cannot execute '%s' (from PATH):\n\n%s\n\nNeed to specify the executable file in Uncrustify settings!" % (command[0], e)
		else:
			err = "Cannot execute '%s':\n\n%s" % (command[0], e)
		sublime.error_message(err)
		return

	formatted_code=outs.decode("utf-8")
		
	# remove unnecessary things
		
	for x in range(0,indent_count):
		index = formatted_code.find('{\n') + 2
		formatted_code = formatted_code[:index].replace('{\n', '')+formatted_code[index+1:]
	for x in range(0,indent_count):
		index = formatted_code.rfind('\n}')
		formatted_code = formatted_code[:index]

	# converting spaces to tabs(if necessary sublime will convert it to spaces)
	# but sublime doesn't auto convert spaces to tabs in my settings

	tor=' '*indent_size
	formatted_code = formatted_code[:(indent_size*indent_count)].replace(tor,'\t')+formatted_code[(indent_size*indent_count):]
	if indent_count>0:
		formatted_code='\t'+formatted_code
	
	# sublime.error_message("%d"%indent_count)

	# replace by result
	view.replace(edit, region, formatted_code)

	sublime.status_message(running + " ...done")

def reformat(view, edit, region):
	# assign the external program
	program = getExecutable()
	if not program:
		return

	# specify the language override (because input is from stdin)
	lang = getLanguage(view)
	if not lang:
		return

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

	command = [program, "-l", lang, "-c", config]
	# command[] should like
	# ['C:/path/uncrustify.exe', '-l', 'CPP', '-c', 'C:/path/my.cfg']

	# show command[]
	running = ' '.join(command)
	print("> " + running + " ...")
	sublime.status_message(running + " ...")

	# prepare the input
	content = view.substr(region).encode("utf-8")

	platform = sublime.platform()

	try:
		# run
		# TODO: si = None
		# TODO: if os.name == 'nt':
		if platform == "windows":
			# to hide the console window brings from command
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			# si.wShowWindow = subprocess.SW_HIDE 	# this is default provided

			proc = subprocess.Popen(command, \
				   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, startupinfo = si)
		else: # "osx" or "linux"
			proc = subprocess.Popen(command, \
				   stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

		# send input and wait for the process terminated
		outs, errs = proc.communicate(input=content)

		# check the return code from Uncrustify
		ret_code = proc.poll()
		if ret_code != 0:
			if errs:
				msg = errs.decode("utf-8")
				# slice the last useless part if found (from Uncrustify)
				pos = msg.find("Try running with -h for usage information")
				err = "Uncrustify return error %d:\n\n%s" % (ret_code, msg[:pos])
			else:
				err = "Uncrustify return error %d:" % ret_code
			sublime.error_message(err)
			return

	except (OSError, ValueError, subprocess.CalledProcessError, Exception) as e:
		# only for debug
		# traceback.print_exc()

		if command[0] == DEFAULT_EXECUTABLE:
			err = "Cannot execute '%s' (from PATH):\n\n%s\n\nNeed to specify the executable file in Uncrustify settings!" % (command[0], e)
		else:
			err = "Cannot execute '%s':\n\n%s" % (command[0], e)
		sublime.error_message(err)
		return

	# replace by result
	view.replace(edit, region, outs.decode("utf-8"))

	sublime.status_message(running + " ...done")

def open_file(window, file_name):
	window.open_file(file_name)

# Uncrustify the document
class UncrustifyDocumentCommand(sublime_plugin.TextCommand):
	def run(self, edit, **kwargs):
		# get argument
		global keep_quiet
		if 'keep_quiet' in kwargs:
			keep_quiet = kwargs['keep_quiet']
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
	def run(self, edit, **kwargs):
		# get argument
		global keep_quiet
		if 'keep_quiet' in kwargs:
			keep_quiet = kwargs['keep_quiet']
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
		# reformat(self.view, edit, region)

		# return
		# ***WIP*** below codes need to review 

		def get_line_indentation_pos(view, point):
			line_region = view.line(point)
			pos = line_region.a
			end = line_region.b
			while pos < end:
				ch = view.substr(pos)
				if ch != ' ' and ch != '\t':
					break
				pos += 1
			return pos

		def get_indentation_count(view, start):
			indent_count = 0
			i = start - 1
			while i > 0:
				ch = view.substr(i)
				scope = view.scope_name(i)
				# Skip preprocessors, strings, characaters and comments
				if ('string.quoted' in scope or
						'comment' in scope or 'preprocessor' in scope):
					extent = view.extract_scope(i)
					i = extent.a - 1
					continue
				else:
					i -= 1

				if ch == '}':
					indent_count -= 1
				elif ch == '{':
					indent_count += 1
			if view.substr(start-1)=='\n':
				indent_count=0
			# sublime.error_message("%d"%indent_count)
			return indent_count

		view = self.view
		for sel in view.sel():
			start = get_line_indentation_pos(view, min(sel.a, sel.b))
			region = sublime.Region(
				view.line(start).a,  # line start of first line
				view.line(max(sel.a, sel.b)).b)  # line end of last line
			indent_count = get_indentation_count(view, start)
			# Add braces for indentation hack
			text = '{\n' * (indent_count)
			text += view.substr(region)
			text += '\n}' * (indent_count)

			#convert spaces to tabs because otherwise it doesn't work properly
			#in my settings
			indent_size=view.settings().get('tab_size')
			tor = ' ' * (indent_size)
			text=text.replace(tor,'\t')

			format(self.view, edit, text, region, indent_count, indent_size)

# open the config file to edit
class UncrustifyOpenCfgCommand(sublime_plugin.WindowCommand):
	def run(self):
		# get filepath
		config = getConfig()
		if not config:
			return
		# go
		open_file(self.window, config)

# open the config file which matches current document to edit
class UncrustifyOpenCfgCurrentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get current language
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

# listen sublime event
class UncrustifyEventListener(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		# get on save rule
		rule = getSetting("uncrustify_format_on_save")
		if rule == True:
			view.run_command("uncrustify_document", {"keep_quiet":True})
