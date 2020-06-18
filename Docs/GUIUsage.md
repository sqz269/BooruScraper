# User Interface (Component)
## Concept
Reading an hundred line ini file to configuration a scraper while watching out for data types is sometimes annoying, 
a user interface which can limit the data type of input and allow clearer picture of the configuration
is helpful to config the scraper

## NOTE
The User interface is built upon the Qt Framework (PyQt5 to be specific), it uses GPL license 
which restricts multiple aspects of the original MIT license this project published as.
So the GUI component of this project is built to be detached w/o modifying any files in our scraper components.
To completely remove any Qt/Graphical related files, simply delete *main_graphical.py* and *UserInterface* directory.

## Adding a new configuration window
### Setting up
#### Windows
QtDesigner is required, to install: use `pip install PyQt5Designer` 
and navigate to `<python root>/Lib/site-packages/QtDesigner/designer.exe`,
or if python is in your PATH, run directly using `designer.exe`

#### Creating a window
1. Create an new window or use the window with basic configuration fields exists in
`UserInterface/Source/simple_config_window.ui`.

2. Compile the ui file you've created using `pyuic <Your .UI file's path> -o <Output .py file path>`

3. Link your ui with the module selection window if you are using it, detailed instruction can be found in
    module_selection_handler.py

#### Adding functions
Just mimic pixiv_handler.py
