
![Python Todo (2)](https://github.com/AmirabbasRouintan/todo-with-python/assets/110909074/2568b98f-f2ca-4232-99ca-47ffa89c7f3b)

# To-Do List App

A feature-rich to-do list application built with Python and Tkinter.

## Features

- Add, edit, delete tasks with date and time
- Set task priorities (Low, Medium, High)
- Mark tasks as complete/incomplete
- Search and filter tasks by keyword
- Set reminders with sound alerts
- Persistent task storage (pickle)
- Keyboard shortcuts for quick actions

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Add task |
| Delete / D | Delete selected task |
| E | Edit selected task |

## Installation

### Required Libraries

```python
import tkinter as tk
import pygame
from tkinter import messagebox, ttk
from datetime import datetime, time as dt_time
import pickle
from tkcalendar import Calendar
from time import strftime
``` 

### Linux

- **pygame :** `pip install pygame` **or** `sudo pacman -S python-pygame`
- **tkcalendar :** `pip install tkcalendar`

#### Install tkinter in Linux

- For Debian-based Linux (such as Ubuntu, Debian, Pop!_OS):
  `sudo apt-get install python3-tk`

- For Arch-based Linux systems:
  `sudo pacman -S tk`

### Windows

- **pygame :** `pip install pygame` 
- **tkcalendar :** `pip install tkcalendar`

#### Install tkinter in Windows

1. Download and install Python from: https://www.python.org/downloads/
2. Check Tkinter installation: `python -m tkinter`
3. Install via pip: `pip install tkinter`

## Usage

Run the application:

```bash
python todo.py
```

## Change Alert Sound

You can change the alert sound by replacing the `alert.mp3` file in the project directory.

The sound file is referenced in the source code:

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
