SSH_TEST.PY:
	from pexpect import pxssh <- for using ssh connection in python
	$ sudo apt install python-pip or $ sudo apt get install python3-pip
	$ sudo pip install pexpect or $ sudo pip3 install pexpect

	If you want to run on integrated linux (on windows) you have to install Xming, because linux terminal does not have visual interface and it can not open GUIs. If have Xming on your windows you can run your program.
link: https://sourceforge.net/projects/xming/

	You have to run the program on linux, because windows does not supports pxssh.
