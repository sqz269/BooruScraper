# Framework
## Concept
I've made few scrapers for specific image websites but most of them are only few functions different. So I decided to extract those commonly changed functions and write a simple framework that can wrap around those changed functions and perform the rest of the scraping operation w/o copy & pasting the entire code base.

## Usage
### **Python Programming Knowledge is required!!!**

---

### DATA STRUCTURE FOR IMAGE DATA
`image data` should be a dictionary that contains useful data that determines if an image is fit for the requirements. returned by process_page with a list of `image data`
Some field it **must** contain:
```
{
    image_id:           <string>,       # An Unique identifier for the image
    image_links:        List[string],   # A list of direct link for all the image in the album
    image_parent_link:  <string>,       # The actual link to the post/page that contains the images, used in referrers
}
```

---

### _base_component.py and BaseComponent class
#### Accessing Configurations
configurations can be accessed via `self.config` all the config are lowercase from the original key in the file; for example configuration with name `TAGS` in ini file can be access via `self.config['tags']`

#### More on configurations
to convert certain configuration into lists. simply call `self.config.cvt_str_list()` with the parameter of list of keys you want to convert

#### Accessing Loggers
Loggers can be access via `self.logger`

---

### _component.py
#### Your own class should be using import & inherit: `ComponentBasic`, which can be imported via: `from Scraper.framework._components_basic import ComponentBasic`

#### 3 Functions must be changed `generate_urls`, `process_page`,  `are_requirements_satisfied`

#### Function: `generate_urls`

#### Function: `process_page`
Arguments: url {string} -- the url to the page that need it's image data to be extracted
This function should provide the caller a list of dictionaries that contains the `image data` for all images that is present on the page.


#### Function: `are_requirements_satisfied`
Arguments: img_data {dict} -- the dictionary contains `image data`
This function should check if the image's meta data fit for the requirements the user set in the configuration
Returns {bool} - True if the image matches the requirements, else it should return false

---

### Making your module appear when running `main.py`
1. Open \_\_init__.py for editing
2. Import your module in that file using `from ... import ...`
3. Add the name of the module and the class to `AVAILABLE_MODULES`

---

### Information for configuration

Configuration can either be loaded from an absolute path or an configuration directory base on it's file name
### Loading Configuration From Absolute Path (Not Recommended)
Open the script that inherited ComponentBasic and use argument: `load_config_from_abs_path=True` in `super.__init__()` to use absolute path to load configuration;
Example: `super.__init__(<Your Abs Path To Config>, load_config_from_abs_path=true)`

### Loading Configuration From Configuration Directory (Recommended)
Create a configuration directory that is on or below the directory level of main.py
and then with in the configuration directory create a file name: `.config_directory` to mark the directory so the program knows.
Then simply call `super.__init__(<ConfigFileName>)` to load the configuration

#### List of Required fields
##### The keys in the ini file must be exact match in-order to work
##### An .ini file with pre-existing fields available at Scraper/framework/basic_config.ini
- SAVE_PATH {string(path-like)} --
- FILENAME_STRING {string(formatted)} --
- CSV_ENTRY_STRING {string(formatted)} --
- MASTER_DIRECTORY_NAME_STRING {string(formatted)} --

- MAX_CONCURRENT_THREAD {int} --
- DELAY_START {float} --
- USER_AGENT {string} --
- COLLECT_DATA_ONLY {bool} --
- FLUSH_CSV_IMMINENTLY {bool} --
- USE_SUBMISSION_SPECIFIC_DIRECTORY {bool} --

- LOGGER_STDOUT {string(pre-defined)} --
- LOGGER_FIELD {string(pre-defined)} --
- LOGGER_NAME {string}

- MERGE_FILES {bool} --
- MERGE_FILES_KEEP_SEPARATE {bool} --

---
