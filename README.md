# Sublime-Uncrustify

This is a code beautifier/formatting plugin that allows the user to use [**Uncrustify**](http://uncrustify.sourceforge.net/)[*] to format the C-like language codes in Sublime Text.

[*]: [**Uncrustify**](http://uncrustify.sourceforge.net/) is a source code beautifier for C, C++, C#, ObjectiveC, D, Java, Pawn and VALA.

## Install

1. A **Uncrustify** MUST be installed before **Sublime-Uncrustify** can work.

    - Win32 binary is availabled in [Sourceforge](http://sourceforge.net/projects/uncrustify/files/).

    - OS X can install via **'brew install uncrustify'** by [Homebrew](http://brew.sh/) or **'port install uncrustify'** by [MacPorts](https://www.macports.org/).

    - Other Linux-likes OS please see http://uncrustify.sourceforge.net/ or build the program yourself.

2. Configuring the **Uncrustify**:

    Examine the example config files in *Uncrustify/etc* (Source) or *Uncrustify/cfg* (Win32 pre-built).

	$ http://sourceforge.net/p/uncrustify/code/ci/master/tree/etc/

    Copy the existing config file that closely matches your style and modify[**] as your version.

    [**]: See 'Other Uncrustify Utilities' below...

2. Install **Sublime-Uncrustify**:

    The preferred method is to use the Sublime package manager [Package Control](https://packagecontrol.io/).
    
    Alternatively, the files can be obtained on GitHub:

	$ https://github.com/obxyann/Sublime-Uncrustify

    Just create a new folde named *Uncrustify* in your *Sublime_Text_Installed/Data/Packages/ and copy the files into.

3. Configure the **Sublime-Uncrustify**:

    [*sublime text*]->[*Preferences*]->[*Package Settings*]->[*Uncrustify*]

    1. Copy the default settings as user settings.

    2. Specify the path to uncrustify binary...(where step 1 installed)

    3. Specify the config file for uncrustify...(where step 2 copied and modified)

## Usage

> **NOTE:** Although it can UNDO after formatted, please backup/SAVE your important/unsaved file before using!

1. Format whole document:

    current document

    [*sublime text*]->[*Tools*]->[*Uncrustify*]->[*Format Document*]

2. Format a selection:

    make a selection then

    [*sublime text*]->[*Tools*]->[*Uncrustify*]->[*Format Selection*]

3. You can edit the Uncrustify config file specified in settings:

    [*sublime text*]->[*Preferences*]->[*Package Settings*]->[*Uncrustify*]

    ->[*Open Uncrustify Config - Default*]

    ->[*Open Uncrustify Config - Matches Current Document*]

      according current document matches one of filters or languages...

## Notices

1. Some languages/extensions don't supported by **Uncrustify** will pop a warning.

2. This is my first Python program. Before I have no knowledge about Python. I just read some sublime plugin codes of others, API docs and write after!

  **It is not guaranteed to work perfectly, please backup/SAVE your important/unsaved file before using!**

3. Only tested in Windows 7 + Sublime Text 3. Please help to improve this plugin if it don't work in your OS!

## License

1. **Uncrustify** is GPL V2 belongs to its authors. (**Uncrustify** binary not include in **Sublime-Uncrustify**)

2. All of **Sublime-Uncrustify** is licensed under the MIT license.

Copyright (c) 2015 Yann "OB" Chou

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Other Uncrustify Utilities

You can easily change your **Uncrusify** config file by:

1. (WIN32) universalindent: http://universalindent.sourceforge.net/

2. (OS X) UncrustifyX: https://github.com/ryanmaxwell/UncrustifyX/

But I think the default config file *default.cfg* from **Uncrusify** is well documented to modify directly!
