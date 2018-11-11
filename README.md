# ROMalas

AFK/Helper script for popular MMORPG mobile game.

## Installation

* Python 3.6.
* NOXEmu (1280x720) with [ADB](https://www.bignox.com/blog/how-to-connect-android-studio-with-nox-app-player-for-android-development-and-debug/) support.

```bash
pip install -r requirements.txt
```

## Usage
* Modify "macro.txt" with **"key, delay(sec), health(percentage), mana(percentage)"**.

```csv
##health potion trigger if reach 80% health
item3,None,80,None
##skill3 trigger every 5sec
skill3,5,None,None
```
* Run **"python autopot.py"**
* **"--auto true"** to trigger auto-attack when script started.
* **"--verbose true"** to  enable terminal output (will slow your script).
## TODO
* Random move around the town and world map.
* Select monster through auto-attack menu
## Macro List
* skill6
* skill5
* skill4
* skill3
* skill2
* skill1
* item5
* item4
* item3
* item2
* item1

## USE THIS SCRIPT AT YOUR OWN RISK!
These scripts come without warranty of any kind. Use them at your own risk. I assume no liability for the accuracy, correctness, completeness, or usefulness of any information provided by this site nor for any sort of damages/ban using these scripts may cause.