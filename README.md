# JSON Viewer

A simple JSON viewer application built with Python and ttkbootstrap.

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setting up a virtual environment

It's recommended to use a virtual environment for this project. Here's how to set it up:

1. Open a terminal/command prompt and navigate to the project directory.

2. Create a virtual environment:
   `python -m venv venv`

3. Activate the virtual environment:

- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

### Installing dependencies

With the virtual environment activated, install the required packages:
`pip install -r requirements.txt`

## Running the application

To run the application, ensure your virtual environment is activated, then run:
`python pyJsonViewer.py`

## Building an executable

To create a standalone executable, we'll use PyInstaller. First, ensure PyInstaller is installed, then, to create the executable:

`pyinstaller --onefile --windowed pyJsonViewer.py`

This will create a `dist` directory containing the executable file.

Note: The `--windowed` flag is used to prevent a console window from appearing when the application is run. If you're on macOS, you might want to add `--add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk'` to the command to ensure Tkinter is properly bundled.

## Usage

1. Click "Load JSON" to select and load a JSON file.
2. Use the "Expand All" and "Collapse All" buttons to manipulate the tree view.
3. Double-click on nodes to expand or collapse them individually.
4. For array nodes, a "Filter" dialgo will appear on right click. Use it to filter the array based on a property and value.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
