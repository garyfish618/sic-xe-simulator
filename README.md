# SIC/XE SIMULATOR PROJECT
This program simulates how a SIC/XE based system would run written in Python3. This included building memory, register, a parser, a console, and an interpreter. 
## Getting Started
Type `./simulator` to start the simulator.<br />
You can type `help` to view list of commands.<br />
To actually get the simulator run, type in 'parse (the asm file you want to read it)'.<br />
Type in `start` to assing addresses to each instruction.<br />
Type in `next` to progress through the instructions.<br />
Type in `viewreg A` anytime to get view the value in Register A.<br />
Type in `viewreg X` anytime to get view the value in Register X.<br />
Type in `viewreg L` anytime to get view the value in Register L.<br />
Type in `viewreg PC` anytime to get view the value in Register PC.<br />
Type in `viewmem (address)` to view the data stored at a specific memory location.<br />
Type in `changemem (address) (byte value)` to change the byte value at a specific memory address.<br />
Type in `changereg (register) (six digit hex value)` to change the value in a specific register.<br />
Type in `stop` to halt the program.<br />
Type in `credits` to view the credits of the program.<br />
Type in `exit` to exit the simulation.<br />
## Built With
[Visual Studio Code](https://code.visualstudio.com/) - The IDE used to build.
## Credits
**Salim Aweys** - Memory and Register management<br />
**Kristian Bunda** - Memory/Register Design and Assembler Directives management<br />
**Lauren DeLeon** - Parser Design and Documentation<br />
**Gary Fishell** - Console and Interpreter Architecture Design<br />
**SIC and SICXE Instruction implementation** - Collective effort<br />
