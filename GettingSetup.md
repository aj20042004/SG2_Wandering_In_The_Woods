
<!-- quick explanation of what this is and why its important -->



# Setting Up a Python Virtual Environment


Using a virtual enviorment accomplishes two main things

- _it prevent polluting our global python installation and_
- _ensure the correct versions of dependencies are being used_
<br>

**1. create a virtual environment**
	creates a virtual enviornment in a new folder named .venv
```sh
python3 -m venv .venv
```


</details>

**2. Activate our virtual environment.**

This should give a (.venv) prefix to our shell prompt
    
```sh
source ".venv/bin/activate"
```

<details>
<summary>Click here for Windows version </summary>

**Please note these are untested**
  
```sh
python -m venv .venv
venv\Scripts\activate
```
</details>
<br>

## Installing Packages

> [!CAUTION]
> Ensure that your venv is activated first otherwise the packages will be installed globaly 

<!-- matplotlib installs numpy but we manually do it anyways-->
```sh
pip3 install matplotlib
pip3 install numpy
pip3 install mypy
```
<br>

## Deactivating 
if you want to deactivate a virtual enviorment 

```sh
deactivate
```
<br>
<br>

# Using Mypy
after activating our venv mypy can be run using the `mypy` command followed by the name of the python file you want to check
```sh
mypy SG2_Program.py
```


<br>
<br>

# VS Code

You're welcome to use any IDE you like. I personaly use vscode so i've included the setup for anyone else who uses it. 

## Changing Interpreter to our venv
If you are using VS-Code you may wish to change the interpreter it's using from your default to your virtual enviorments interpreter.
This allows intellisense to know what packages you have and installed, as well as direct mypy integration

1. press `ctr+shift+p` (open command pallet) <br>
2. type `>Python: Select Interpreter` until it autofills, and select it. <br>
3. select `Enter Interpreter Path` <br>
4. type the path to our venv interpreter`./.venv/bin/python`

<br>

## Extensions
If you are using vscode I would highly recommend you use these extensions. \
To quickly install an extension in vscode press `ctr+p` and paste the commands bellow.

**Python (Required)** | Microsoft \
_Base python extension for vscode_
```
ext install ms-python.python
```


**Pylance** | Microsoft \
_IntelliSense support for Python_
```
ext install ms-python.vscode-pylance
```


**Python Type Hint** | njqdev \
_enables autocomplete for type hints_
```
ext install njqdev.vscode-python-typehint
```


**Mypy** | Matan Gover \
_enables mypy integration into IntelliSense_
```
ext install matangover.mypy
```
<br>

## Settings 

### Pylance 
Support Restructured Text **☑** \
_use reST style formatting for docstrings_

Support Docstring Template **☑** \
_enable pylance to autogenerate docstrings by typing `"""` and hitting `ctr+.`_

### Mypy
Run Using Active Interpreter **☑** \
_use our venv version of mypy instead of using path to search for a system installation_

<br>

If you dont feel like searching for the settings you can hit `ctr+shift+p` and search for \
`>Preferences: Open User Settings (JSON)`. Then paste these lines above the last `}`
```
"python.analysis.supportDocstringTemplate": true,
"python.analysis.supportRestructuredText": true,
"mypy.runUsingActiveInterpreter": true
```
<br>
<br>


