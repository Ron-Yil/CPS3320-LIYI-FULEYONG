Speech Emotion Recognition

Environment:
Python 3.6

File Structure:
├── Common_Model.py 
├── DNN_Model.py        
├── ML_Model.py          
├── Utilities.py          
├── SER.py            
├── File.py   
├── DataSet
│   ├── Angry
│   ├── Happy
│   ...
│   ...
└── Models

Package Requirments:
Keras
TensorFlow
scikit-learn
speechpy
librosa
SciPy
Matplotlib
numpy

Datesets:
About 500 audio recordings of four people (male) expressing seven different emotions (the first letter indicates the emotion category) : 
A = anger, D = disgust, F = fear, h = happiness, n = neutral, sa = sadness, su = surprise
Download URL:http://kahlan.eps.surrey.ac.uk/savee/Download.html

The DataSet is placed in the /DataSet directory, and the audio of the same emotion is placed in the same folder (see Structure). 
Consider using file.py to collate data.
Enter the data set path DATA_PATH and the label name CLASS_LABELS in SER.py





