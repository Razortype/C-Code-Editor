# C Code Editor
![Project Image](https://user-images.githubusercontent.com/55176611/161594144-96af0d5f-5505-4014-8962-e82fb67c211b.png)


> C Code Editor is a system that allow user to run, compile and edit the C based code with GUI supported program.

---

### Table of Contents
Location of project referance destinations.

- [Description](#description)
- [How to use](#how-to-use)
- [Referances](#referances)
- [License](#license)
- [Author Info](#author-info)

---

## Description

Design of the project is aimed to accessibility of files and good interaction with users. Although, so many code editor publicized back then, this code editor helps us to get files' enviroment and thier attributes. For a software engineer student, it help me to manage C lesson files.

#### Toolkits
- Tkinter
- Threading

---

## How to use
Firstly we have to execute "run.pyw" file. If it is first time, system ask for folder directory that should contain C files. After a folder directory selected, editor window shoul be appeared on screen.

![Editor Main Screen](https://user-images.githubusercontent.com/55176611/161594204-6a05ed79-6996-4704-a6f8-19e21c56a3f3.png)


### Buttons ~
- **Editor Related**
    - Select : changing different location for searching C files.
    - Fetch : fetching all C files in given directory and in its child folders.
    - Search : fetched items can be searched by typing in the box and pressed.
    > Search as its given items. Second search may not show up anything.

- **File Realted**
    - Process Type
        - Run : run only previously compiled C file.
            > Gives error when difference founded.
        - Compile : just compile C file.
        - Both : compile the file and run afterwards.
        - Edit : opens edit page for editing C file similar to notepad.
    
    - START : start the process as given process type.
        > Default = Run
    - All : compile all fetched files in given directory.
    - Settings : opens settings page.

<br />
When the start button is pressed system will be searching for C files in the given path and its childs. When all the information is gathered, files will be listed as table items. By double clicking it, items' data will appear right of the main page. File attributes demonstration can be changed in setting page.
<br />
<br />
The most import thing is structuring of C files. Fetched files also called by its folder name. Recommend design is that for every C file, another directory can be created. If that applied to your initial path, tracking files can be easier in editor.
<br />
<br />
After double clicking to selected item, file can be manipulated as wished.

---

## Referances
[Description](#description) <br />
[Buttons](#buttons~) <br />
[Back To The Top](#c-code-editor) 🔺

---

## License

MIT License

Copyright (c) 2022 Orkun Kurul

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Author Info

 - LinkedIn - [(orkun-kurul)]("https://www.linkedin.com/in/orkun-kurul/")
 - Github - [(Razortype)]("https://github.com/Razortype")

 [Back To The Top](#c-code-editor) 🔺
