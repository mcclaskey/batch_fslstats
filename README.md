# batch_fslstats
Small set of functions to run fslstats on a WSL machine and compile output to a csv file

# How to use the code
Use these directions to run the batch_fslstats scripts to get mean values of .nii files. You must first have done the setup (see below).

If it's been a while since you set up the scripts, it might be a good idea to pull any new changes from the repo using git.

# 1. Set up a list of files to run fslstats on
First you need to put together a list of .nii files that you need to run FSL stats on. This must be a csv where the first row says "input_file" and each subsequent row contains the full file path to a .nii file. Each .nii file will have its average value calculated.

> [!IMPORTANT]
> The first row of the .csv must have the header "input_file" and all subsequent rows must be strings indicating the full file path to each .nii file

> [!Tip]
> I usually create this .csv file in MATLAB using the `dir()` command and then save the result using `write_table()`. You can also do this in python or bash.

# 2. Run scripts 
Open a terminal window (or open the WSL2). Type the following 2 lines:
```
workon batch_fslstats_env
python compile_fsl_data.py
```

A dialogue box will now open and you will now need to select the .csv file you created in step 1. Select the file and press ok.

Wait while the files are created. When it is done you will have a .csv file in the same directory as the input file. The output file's name will be prepended with the date/time and appended with '*_compiled'


# SETUP:
Use these directions to set up the batch fslstats scripts on a new computer. This will step you through installing everything needed, so if you get to a part that isn’t necessary just skip it. 

## A. Setup requirements
* A Unix or Linux operating system, or a PC with WSL2
* The admin password to the computer
* git 
* Familiarity with terminal commands, basic understanding of bashrc in linux, and very basic competency with a shell text editor
  * On unix/linux the `~` symbol means “home directory”. So if you see `~/.bashrc`, then the full path to that file is `/Users/USERNAME/.bashrc` on a mac or `/home/USERNAME/` on a linux

> [!TIP]
> Follow [these instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to install git if you need it. In this example I am using an ubuntu in WSL so i just typed `sudo apt install git-all` in the WSL2 Ubuntu terminal and entered my password when prompted.

## B. Setup recommmendations
* WSL2 on windows running Ubuntu
  
## C. Setup instructions

### 1. Install WSL2 if you are on a PC

This can be done on a mac or linux, but I originally set this up for us to use on our PCs via WSL. 
See Microsoft’s website for how to do this. As of the time of this writing, the website can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install).

> [!IMPORTANT]
> If you are working on a WSL but the .nii files to process are on your Windows machine, ensure that you mount the correct drives to the WSL so that you can access your files.

### 2. Install FSL
Open a shell/command window/terminal and type the following command into it:
```
fsl
```

If you see the following GUI pop up, you have FSL on the machine and can skip subsequent FSL install steps: 

![image](https://github.com/user-attachments/assets/633d0aa3-9f9c-436b-8757-749fa10de778)

Otherwise, go to the FSL installation page (currently [here](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation)) and follow the instructions for your operating system and try `fsl` again. For troubleshooting, see the FSL website.


### 3. Install Python

Python often comes natively on new machines but you may need to download it. Open a shell/command window/terminal, hereafter called terminal, and type:

```
python
```

If that doesn’t work, your computer may not have the python alias. Instead try:

```
python3
```

> [!NOTE]
> If you are missing the python alias, you may need to use `python3` anytime the current directions say `python`

If nothing is found, download the latest stable python release from the main python downloads page [here](https://www.python.org/downloads/) and try again. 

If a version of python is found, it will start in the terminal. Scan the lines to check the version. Ensure you have a version that is at least 3.11. If it’s a few years old, it’s probably a good idea to download a newer version just in case. 

To quit python, type `quit()`.


### 4. Clone this repo to your computer
Open a terminal and change directories to where you will store the repo (or use `mkdir` to create a new folder). In this example I am using `~/repos/`. 
Once you are in the folder where the repo will be stored, clone the repo by typing:
```
git clone git@github.com:mcclaskey/batch_fslstats.git
```

This has created a folder called `/batch_fslstats/` inside the current folder. 

> [!TIP] 
> You will need to know the path to this repository directory for subsequents steps, so make a note of it here.
> As an example, because mine is stored in `~/repos/`, the path to my repository is  `~/repos/batch_fslstats/`.

### 5. Install the virtualenvwrapper python package for path management

These steps are also found in [the install page for virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) but I will detail them here. If these steps fail, see that webpage for troubleshooting.

Open a new terminal window and type:
```
pip3 install virtualenvwrapper
```

If that doesn’t work, your computer may have pip and not pip3. Try:
```
pip install virtualenvwrapper
```
Next, print the path to the `virtualenvwrapper.sh` file by typing:
```
which virtualenvwrapper.sh
```
The location to the shell file will print into the terminal window. Make a note of it because you will need it for the next step.

Next you need modify the `.bashrc` file to do 3 things: 
1. define where to store the virtual environments
2. define the default project location, and
3. run the `virtualenvwrapper.sh` file.

Detailed instructions for this step are currently explained [on this page](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#shell-startup-file) but I will list the minimum necessary steps here. You will now need to open your `.bashrc` file in a text editor. 

> [!TIP]
> If you are on a WSL you can usually open the file in your Windows File Explorer by finding the “Linux” tab in the sidebar. 

Otherwise, open it directly in Linux by typing this in the command line if you use a bash shell:
```
sudo nano ~/.bashrc
```
or, for `.zshrc` if you use a zsh shell instead of bash:
```
sudo nano ~/.zshrc
```
Because this command uses sudo, the terminal will next prompt you for the admin password. Enter it and the text file will open in the terminal window. 

Once you’ve opened the text file by any means, add the following lines to the bottom: 
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```
But replace `/usr/local/bin/virtualenvwrapper.sh` with the location to the `virtualenvwrapper.sh` location you looked up above. 

Then type ctrl+X to close the nano text editor (if not using Windows). When it ask if you want to save your changes, press Y on the keyboard to say yes. When it asks you to confirm the filename, press enter to save the file under its current name.

Close the terminal window.

CMcC’s notes for the lab:
* If you add it to the .bashrc file then those commands will only run if you open a normal bash shell. If you add it to the .zshrc file then they will run every time you open a zsh shell.
* Your goal is to set it up so that those lines run every time you open the shell you’re going to use, otherwise the computer won’t be able to find the environment
* The lines you added must always be at the bottom of the file, so that any modifications to the path will be known to virtualenvwrapper. If it ever breaks in the future, it may be that relevant path changes were inserted below those virtualenvwrapper lines (for example FSL)
* If you find that you can’t edit the `~/.zshrc` or `~/.basrc` file to add those three lines, then you will need to manually run them each time a new shell is opened. The 1st and 3rd are the most important ones to run and the 2nd line can be skipped

### 6. Create the virtual environment (batch_fslstats_env)

Open a new terminal window and type:
```
mkvirtualenv batch_fslstats_env
```
This will create the environment and also activate it. It will print something like this:

![image](https://github.com/user-attachments/assets/c289d83f-6b36-49cf-9c95-2c457d83cf30)


When the environment is activated you will see at the start of each line as in the above screenshot.

Now `cd` to the main repository directory. If following my example, your `cd` command will look like this:
```
cd ~/repos/batch_fslstats
```
> [!IMPORTANT]
> If you have cloned the repository to a different location on your computer, replace `~/repos/batch_fslstats` with the path to your custom repository.

Now we need to link the virtual environment that you just created to the current batch_fslstats folder. This step requires you to know where the environment is located. If you followed all directions using my example directories and used the line `export WORKON_HOME=$HOME/.virtualenvs` then it’s located at `~/.virtualenvs/batch_fslstats_env/`. 

> [!TIP] 
> The location of the virtual environment will be printed in the terminal window 

Run the following in the terminal, but replace `<path/to/batch_fslstats_env/>` with the path to the `batch_fslstats_env` that you found above:
```
setvirtualenvproject <path/to/batch_fslstats_env> $(pwd)
```
As an example, my command looked like this when I did it:
```
setvirtualenvproject ~/.virtualenvs/dkifa_fslcalcs_env $(pwd)
```
If it works you’ll see this:

![image](https://github.com/user-attachments/assets/e1de220b-3063-427a-82e1-a24ce9702070)


We will now run two checks to verify that this worked. Open a new terminal window and run the following command:
```
workon batch_fslstats_env
```
You should see `(batch_fslstats_env)` at the start of the line as before, like this:

![image](https://github.com/user-attachments/assets/55630c8b-e58f-49e9-9843-d89aee172c72)



Now print the current working directory using this command:
```
pwd
```
It should print the full path to the batch_fslstats directory. If these steps don’t work, then the virtualenv didn’t work correctly. See their webpage for troubleshooting.

Close the terminal window.

### 7. Install python packages into the batch_fslstats_env:
Open a fresh terminal window and run the following to activate the batch_fslstats_env:
```
workon batch_fslstats_env
```
> [!NOTE]
> Any time you need to run the scripts, open a terminal and run `workon batch_fslstats_env` to activate the environment. Code will only work in the active environment.

With the environment activated as shown above, run the follow command in the command line to load the required packages into the environment:
```
pip install -r requirements.txt
```
You are now ready to run the main scripts.




