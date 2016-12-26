# Sublime-Uncrustify

This is a source code beautifier/formatter plugin that allows the user to use **Uncrustify**(1) to format the C-like languages in **Sublime Text**.

**Sublime-Uncrustify** can setup to read different configures (as different code styles) according to the languages and filenames or projects.

NOTE: (1) [**Uncrustify**](http://uncrustify.sourceforge.net/) is a source code beautifier for C, C++, C#, ObjectiveC, D, Java, Pawn and VALA.

## Screenshot

![screenshot](https://raw.github.com/obxyann/Sublime-Uncrustify/master/Screenshot.gif)

## Install

1. An **Uncrustify** MUST be installed before **Sublime-Uncrustify** can work.

    1. An Win32 binary is available in [**Sourceforge**](http://sourceforge.net/projects/uncrustify/files/).

    2. OSX can install via **'brew install uncrustify'** by [**Homebrew**](http://brew.sh/) or **'port install uncrustify'** by [**MacPorts**](https://www.macports.org/).

    3. Other Linux-like OS please see http://uncrustify.sourceforge.net/ or build the program yourself.

    Remember the path of your **Uncrustify** executable (for step 4.2).

2. Configuring the **Uncrustify**:

    Examine the example config files in *Uncrustify/etc* (from uncrustify source) or *Uncrustify/cfg* (from Win32 pre-built).

    or you can find in:

    http://sourceforge.net/p/uncrustify/code/ci/master/tree/etc/

    Copy the existing config file that closely matches your style and modify(2) as your version.

    Remember the path of your config file for uncrustify (for step 4.3).

    NOTE: (2) See 'Other Uncrustify Utilities' below...

3. Install the **Sublime-Uncrustify**:

    The preferred method is to use the Sublime package manager [**Package Control**](https://packagecontrol.io/):

    [*sublime text menu*]->[***Preferences***]->[***Package Control***]->[***Install Package***]->Search "*Uncrustify*" and install.

    Alternatively, the files can be obtained on **GitHub**:

    https://github.com/obxyann/Sublime-Uncrustify

    Just create a new folder named *Uncrustify* under your **Sublime Text** *Packages* folder and copy the files into.

4. Configure the **Sublime-Uncrustify**:

    [*sublime text menu*]->[***Preferences***]->[***Package Settings***]->[***Uncrustify***]

    1. Copy the default settings as user settings.

    2. Specify the path to uncrustify executable...(where step 1 installed)

    3. Specify the config file for uncrustify...(where step 2 copied and modified)

    4. Add your rules to use different config files (code styles) according to the languages and filenames.

## Usage

> **NOTE: Although it can UNDO after a format action, please backup/SAVE your important/unsaved file before using!**

1. Format whole document:

    Current document

    [*sublime text menu*]->[***Tools***]->[***Uncrustify***]->[***Format Document***]

2. Format a selection:

    Make a selection then

    [*sublime text menu*]->[***Tools***]->[***Uncrustify***]->[***Format Selection***]

3. Undo formatted:

    Just ***Undo*** before exit.

4. You can edit the **Uncrustify** config file specified in settings:

    [*sublime text menu*]->[***Preferences***]->[***Package Settings***]->[***Uncrustify***]

    ->[***Open Uncrustify Config - Default***]

      for all languages/file types supported and no custom filter or language matched

    ->[***Open Uncrustify Config - Matches Current Document***]

      according to current document matches one of filters or languages...

## Notices

1. Some languages/file types don't supported by **Uncrustify** will pop a warning.

    **Currently only supports C, C++, D, C#, Java, Pawn, Objective C, Objective C++, Vala, SQL and ECMA.**

2. This is my first Python program. Before I have no knowledge about Python. So I must warn again...

    **It is not guaranteed to work perfectly, please backup/SAVE your important/unsaved file before using!**

3. Only tested in **Windows 7** + **Sublime Text 2/3**. Please help to improve this plugin if it don't work in your OS!

## License

1. **Uncrustify** is **GPL** V2 belongs to its authors. (**Uncrustify** binary not include in **Sublime-Uncrustify**)

2. **Sublime-Uncrustify** is released under the **MIT** license.

## Other Uncrustify Utilities

You can change your **Uncrusify** config file easily by:

1. (WIN32) **UniversalIndentGUI**: http://universalindent.sourceforge.net/

2. (OSX) **UncrustifyX**: https://github.com/ryanmaxwell/UncrustifyX/

But I think the default config file *default.cfg* from **Uncrusify** is well documented to modify directly!
