# C3X Dark Cloud Rising: Challenges

## Purpose
Challenges must be organized in a standard format to automate deployment to CTFd, and to make it easier to modify challenge state over time and on game day. In this repository there are three folders corresponding to each competition scenario or "level"; they are Level1, Level2, and Level3. Under each level folder, a directory must be created for each question or "challenge" we wish to present to the players. At a minimum, you must create two files under each challenge directory:
```
- manifest.yml <--- contains challenge metadata (point value, flag, etc.)
- documentation/instructions.txt <--- contains the challenge question
```

That being said, you may need to add more files depending on your requirements. A complete guide to the standard directory structure is provided below.

## Example Challenge Directory Structure
```
.
├── Level1
│   └── ExampleChallenge
│       ├── documentation
│       │   ├── hint.txt
│       │   ├── instructions.txt
│       │   └── solution.txt
│       ├── manifest.yml
│       └── player_files
│           ├── forensic-artifact-1
│           └── log-dump.json
├── Level2
├── Level3
└── prepare-for-deployment.py
```

### `Level1, Level2, Level3` Directories:
- required 
- challenge category name on CTFd.
- correspond to scenario levels (but do not necessarily need to).

### `ExampleChallenge` Directory:
- required 
- challenge directory, child of a category directory (Ex: "Level1")
- Best named after the challenge. For example, if the challenge is named "Ben's Bistro", the directory name could be "BensBistro".
- Do not use spaces or weird special characters in the directory's name: dashes and underscores only.
- Must be unique across the category.

### `manifest.yml` file:
- required
- contains challenge metadata including challenge name, author, category, point value, flags, dependencies, tags, etc.
- more detailed instructions inside.

### `documentation` directory:
- required
- contains the challenge's documentation files including instructions.txt, hint.txt, and solution.txt. 

### `instructions.txt` file:
- required 
- contains the challege's instructions or in other words, what students see on CTFd when they click a particular challenge.
- later added to a CTFd deployment file programmatically via prepare-for-deployment.py

### `hint.txt` file:
- optional
- contains a hint that can aid the player in solving the challenge. 
- later added to a CTFd deployment file programmatically via prepare-for-deployment.py
- The hint can be free or may have a cost associated with it. The cost is deducted from the team's total points.
- The hint_cost is not specified in hint.txt, only the hint itself. The hint_cost is specified using the "hint_cost" key in manifest.yml.  

### `solution.txt` file:
- optional
- contains a detailed walkthrough of the challenge solution for mentors and/or students.
- DOES NOT contain the solution students must submit on CTFd. The "flag" submitted on CTFd is specified using the "flags" key in manifest.yml.

### `player_files` directory:
- optional
- contains any files the challenge developer wishes to share with the players. These could be additional instructions, forensics artificats, etc.
- later zipped into a single archive via prepare-for-deployment.py

### `prepare-for-deployment.py` script:
- This script converts previous inputs into CTFd standard format (which is difficult and cumbersome to generate by hand)
- It zips the player_files directory into a single zip file, adds necessary html tags to the instructions and hints, and generates CTFd's challenge.yml file. 


