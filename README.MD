# SUMO-SCENIC GUI

This project is part of a collaboration between Embry-Riddle Aeronautical University and Istanbul Technical University. 

This project implements previously impossible Atomic Blocks, which are modular and measurable Autonomous Vehicle Validation scenarios using the SUMO interface of the Scenic scenario description language.

Contributions of this project include:
* Bug fixes to the SUMO-SCENIC interface.
* A Graphical User Interface (GUI) which streamlines choosing, running, and evaluating scenario tests.
* Seven (7) new Atomic Blocks featuring intersections and pedestrians.

## Authors
<u>**Faculty Advisors**</u><br>
<sup>1</sup>Dr. Mustafa İlhan Akbaş - `akbasm@erau.edu`<br>
<sup>2</sup>Dr. Tahir Çetin<br>

<u>**Graduate Student Researchers**</u><br>
<sup>1</sup>Quentin Goss - `gossq@my.erau.edu`<br>
<sup>2</sup>İlke Kutlu<br>


<sup>1</sup>**Embry Riddle Aeronautical University**<br>
*Daytona Beach, Florida, USA*

<sup>2</sup>**Istanbul Technical University**<br>
*Istanbul, Turkey*

## Installation
This software requires [Python 3.8](https://www.python.org/downloads/release/python-3810/) and [SUMO Traffic Simlator](https://eclipse.dev/sumo/). 

Once SUMO is installed, install the sumo-scenic package, then requirements.txt.

**Windows**
```
python -m pip install --force-reinstall scenic-2.0.0-py3-none-any.whl
python -m pip install -r requirements.txt
```

**Linux**
```
python3.8 -m pip install --force-reinstall scenic-2.0.0-py3-none-any.whl
python3.8 -m pip install -r requirements.txt
```