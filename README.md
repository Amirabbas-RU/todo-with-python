
![Python Todo (2)](https://github.com/AmirabbasRouintan/todo-with-python/assets/110909074/2568b98f-f2ca-4232-99ca-47ffa89c7f3b)




# **installation library** 


```python
import tkinter as tk
import pygame
from tkinter import messagebox, ttk
from datetime import datetime, time as dt_time
import pickle
from tkcalendar import Calendar
from time import strftime
``` 



## In linux 


- **pygame :** `pip install pygame` **or** `sudo pacman -S python-pygame`

- **tkcalendar :** `pip install tkcalendar`


 ### For install _tkinter_ in linux

- For Debian-based Linux (such as Ubuntu, Debian, Pop!_OS), run the following command:
`sudo apt-get install python3-tk`

- For Arch-based Linux systems, run the following command:
`sudo pacman -S tk`



## In windows 
- **pygame :** `pip install pygame` 

- **tkcalendar :** `pip install tkcalendar`

 ### For install _tkinter_ in windows


# Install Python
Download and install the latest version of Python from the official website: https://www.python.org/downloads/


### Check Tkinter installation
Open a command prompt and type the following command:
`python -m tkinter
`
### Install ActivePython (optional)
Download and install ActivePython from the official website: https://www.activestate.com/products/python/downloads/

###  Install Tkinter using pip
Open a command prompt and type the following command:
`pip install tkinter`




---
# You can change the alert 

>  In line **196**

```python
sound = pygame.mixer.Sound('alert.mp3')
``` 



![undraw_cat_epte](https://github.com/AmirabbasRouintan/todo-with-python/assets/110909074/62c6d96e-587e-4dd4-8829-0f04b3514441)

---

# Usage

Run the app from the repository root:

```bash
python todo.py
```

## Command-line options

| Option | Description |
| --- | --- |
| `-h`, `--help` | Show the usage message and exit. |
| `-d`, `--data-file PATH` | Path to the pickle file used to store tasks. Defaults to `tasks.pkl`. |

Point the app at a different file to keep separate task lists, or to keep
your tasks outside the working directory:

```bash
python todo.py --data-file ~/tasks/work.pkl
```

Press `Ctrl+C` in the terminal to close the app; pending tasks are saved
before the window exits.
