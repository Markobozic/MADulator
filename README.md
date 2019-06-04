# MADulator

![Image of MADultor UI](https://github.com/Markobozic/MADulator/blob/master/img/MadulatorUI.jpg | width=1021)

Developed by Marko, Angelic and Daniel (MAD), this program allows one to explore functionally generated sounds, also known as "bytebeat". Each function is built from a tree of mathematical and bitwise expression nodes. Audio is generated at 8-bit 11,025 hz using a pyaudio stream.

* Index of 2^32 randomly generated functions to explore
* waveform and spectrogram visualization
* Real time function editor with 10 binary operators, constants and variables
* Save functions to and load from MAD file format
* Save audio to WAV file (scaled to 16-bit 44.1khz)

## Development environment

### Linux packages
* portaudio19-dev

### Python modules
* pyaudio ([How install pyaudio on Windows for python v3.7](https://stackoverflow.com/questions/54998028/how-do-i-install-pyaudio-on-python-3-7))
* pyqt5
* pyqtgraph
* numpy
* pickle (installed by default)
* wave (installed by default)

To install the required modules, use the following command: `pip3 install -r requirements.txt`

## Code Additions

To make changes to the repository please checkout the master branch:

```git checkout master```

Pull in any changes to master and resolve conflicts if necessary, use the sequence of commands below:

1. ```git fetch```
2. ```git pull```

To branch off master, use one of the following commands:

1. ```git checkout -b feature/{feature-to-add}```
2. ```git checkout -b bugfix/{bug-to-fix}```

## Code Review

Look to get at least one approval on pull requests before merging changes into master. 

It's also **highly** recommended that you use the following git feature to merge your code.

> squash and merge
