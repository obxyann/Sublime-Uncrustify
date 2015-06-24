# Sublime-Uncrustify

This is a source code beautifier/formatter plugin that allows the user to use [**Uncrustify**](http://uncrustify.sourceforge.net/)[*] to format the C-like languages in Sublime Text.

[*]: [**Uncrustify**](http://uncrustify.sourceforge.net/) is a source code beautifier for C, C++, C#, ObjectiveC, D, Java, Pawn and VALA.

## Install

1. A **Uncrustify** MUST be installed before **Sublime-Uncrustify** can work.

   >- An Win32 binary is availabled in [Sourceforge](http://sourceforge.net/projects/uncrustify/files/).
   >
   >- OS X can install via **'brew install uncrustify'** by [Homebrew](http://brew.sh/) or **'port install uncrustify'** by [MacPorts](https://www.macports.org/).
   >
   >- Other Linux-like OS please see http://uncrustify.sourceforge.net/ or build the program yourself.

   Rememebr the path of your **Uncrustify** executable (for step 3.2).

2. Configuring the **Uncrustify**:

    Examine the example config files in *Uncrustify/etc* (from uncrustify source) or *Uncrustify/cfg* (from Win32 pre-built).

    or you can find in:
    http://sourceforge.net/p/uncrustify/code/ci/master/tree/etc/

    Copy the existing config file that closely matches your style and modify[**] as your version.

    Rememebr the path of your config file for uncrustify (for step 3.3).

    [**]: See 'Other Uncrustify Utilities' below...

2. Install **Sublime-Uncrustify**:

    The preferred method is to use the Sublime package manager [Package Control](https://packagecontrol.io/).
    
    Alternatively, the files can be obtained on GitHub:
    https://github.com/obxyann/Sublime-Uncrustify

    Just create a new folde named *Uncrustify* under your **Sublime Text** *Packages* folder and copy the files into.

3. Configure the **Sublime-Uncrustify**:

    [*sublime text menu*]->[***Preferences***]->[***Package Settings***]->[***Uncrustify***]

    1. Copy the default settings as user settings.

    2. Specify the path to uncrustify executable...(where step 1 installed)

    3. Specify the config file for uncrustify...(where step 2 copied and modified)

## Usage

> **NOTE:** Although it can UNDO after a formatted action, please backup/SAVE your important/unsaved file before using!

1. Format whole document:

    current document

    [*sublime text menu*]->[***Tools***]->[***Uncrustify***]->[***Format Document***]

2. Format a selection:

    make a selection then

    [*sublime text menu*]->[***Tools***]->[***Uncrustify***]->[***Format Selection***]

3. You can edit the **Uncrustify** config file specified in settings:

    [*sublime text menu*]->[***Preferences***]->[***Package Settings***]->[***Uncrustify***]

    ->[***Open Uncrustify Config - Default***]

      for all languages/file types supported and no custom filter or language matched

    ->[***Open Uncrustify Config - Matches Current Document***]

      according to current document matches one of filters or languages...

## Notices

1. Some languages/file types don't supported by **Uncrustify** will pop a warning.

2. This is my first Python program. Before I have no knowledge about Python. So I must warn again...

  **It is not guaranteed to work perfectly, please backup/SAVE your important/unsaved file before using!**

3. Only tested in Windows 7 + Sublime Text 2/3. Please help to improve this plugin if it don't work in your OS!

## License

1. **Uncrustify** is GPL V2 belongs to its authors. (**Uncrustify** binary not include in **Sublime-Uncrustify**)

2. **Sublime-Uncrustify** is released under the MIT license.

## Other Uncrustify Utilities

You can change your **Uncrusify** config file easily by:

1. (WIN32) universalindent: http://universalindent.sourceforge.net/

2. (OS X) UncrustifyX: https://github.com/ryanmaxwell/UncrustifyX/

But I think the default config file *default.cfg* from **Uncrusify** is well documented to modify directly!

