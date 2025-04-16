# batch_fslstats
batch_fslstats is a small set of functions that use FSL to get mean values for a set of .nii files and compile output to a csv file. Can be run on a Mac, Linux, or PC. 

Mean values are calculated using the FSL call `fslstats -M`. This means that the output values are the mean intensity value of the .nii file, excluding empty voxels. [Read more about FSL here](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/). 

These functions work very quickly and require minimal coding knowledge, but some limited familiarity with unix to do the initial setup. Setup can be time-consuming if you need to do the entire thing (FSL can take a long time to install), but once installed, the scripts can process ~200 .nii files in 90 seconds. Your mileage may vary depending on your machine's resources.

> [!WARNING]
> These scripts only work with 2D .nii files.

# Instructions
> [!IMPORTANT]
> FSL only works in a linux/unix environment. If you have a PC then it will run inside a WSL. For the purposes of this readme, any mention of a "terminal window" or "command line" is referring to a unix or linux terminal and not a PC terminal. In other words if you are on a PC running WSL2 or Docker, open the linux terminal and run commmands there.


> [!NOTE]
> This readme is written with the assumption you will be using virtualenvwrapper to manage your environments. If you are using a different way of managing your environments, disregard all `workon batch_fslstats_env` lines and instead just activate your environment and `cd` to repo dir.



If this is your first time working with the scripts, first run through the setup instructions [here](https://github.com/mcclaskey/batch_fslstats/blob/iss3-update-documentation/README.md#setup). 
If it's been a while since you set up the scripts and you have not made any alterations to the code, you can run the following lines in your terminal to update the code to the latest version:
```
workon batch_fslstats_env
git pull
```

## 1. Create a list of .nii files
First you need to put together a list of your .nii files. Save this list as a single-column .csv file where the first row says "input_file" and each subsequent row contains the full file path to a .nii file. Each .nii file will have its average value calculated.

> [!IMPORTANT]
> The first row of the .csv must say "input_file" and all subsequent rows must be strings indicating the full file path to each .nii file

> [!Tip]
> I usually create this .csv file in MATLAB with something like `T = struct2table(dir('wildcardsearchstring')))` where 'wildcardsearchstring' is a path that points to all my files. Then I edit the table in matlab's Variable Editor and save the result using `writetable(T,'datalist.csv')`. You can also do this in python or bash.

## 2. Run scripts 

Open a terminal and run the following 2 lines:
```
workon batch_fslstats_env
python compile_fsl_data.py
```

A file selection dialogue box will now open. Select the .csv file you created in step 1 and press ok. Wait while the program runs.

When it is done you will have a .csv file in the same directory as the input .csv file. The output file's name will be be the same as the input filename but will have a timestamp and the suffix '*_compiled'.


# Troubleshooting
The following section lists some issues that I have come across that may be causing problems. WIP.

- If you are working on a WSL but the .nii files to process are on your Windows machine, ensure that you mount the correct drives to the WSL so that you can access your files. A good check for this is to use the `ls` command to print contents of directories
- The default shell file for MacOS recently changed from `bash` to `zsh`. If you previously installed FSL and/or virtualenvwrapper on an older macOS that ran `bash` but then updated to a newer MacOS that uses `zsh`, you need to migrate the shell configuration lines from your .`bashrc` file to your `.zshrc` file. [This page from FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/install/configuration) provides more details on how to do this for FSL, but you can do the same thing for the virtualenvwrapper configuration commands as well

# Setup (Advanced Users)
If you are an FSL user with git, python and FSL on your path and an established system for managing environments (such as conda), no special setup is needed: 
1. create/activate an environment that has access to FSL
2. cd to where you store repos and clone this repo with `git clone git@github.com:mcclaskey/batch_fslstats.git`
3. cd to repo directory
4. run `pip install -r requirements.txt` if you don't have pandas in your env

Alternately, if you are working on a machine that has FSL, python, and git installed but you're not sure about environment, you can start at [setup step 5](https://github.com/mcclaskey/batch_fslstats/tree/iss3-add-to-readme?tab=readme-ov-file#5-install-the-virtualenvwrapper-python-package-for-path-management).

# Setup (Full Instructions)

## A. Setup requirements
* Linux or Mac, or a PC running either Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11
* Ability to restart your machine if you are on a PC installing WSL for the first time
* The admin password to the linux/unix machine
  * If you are working on a previously created WSL then you need the admin password to the WSL and not the PC (they may be different)
* Basic familiarity with unix terminal commands such as `cd` and `mkdir`, basic understanding of bashrc in linux, and only very basic competency with a shell text editor if not on a PC
  * These instructions attempt to cover everything possible but some limited experience with unix can help you if you run into problems

> [!NOTE]
> By convention, unix and linux specify file paths using `/` and Windows OS uses `\`. For the purposes of this readme, I use `/` for paths that are typed into the linux/unix terminal and `\` to indicate the address to a file accessed via the PC's Windows File Explorer.

> [!NOTE]
> On unix/linux the `~` symbol means “home directory”. So if you see `~/.bashrc`, then the full path to that file is `/Users/USERNAME/.bashrc` on a mac or `/home/USERNAME/.bashrc` on a linux

## B. Setup recommmendations
* WSL2 on windows running the default Ubuntu distribution
  
## C. Setup instructions

### 1. Install WSL2 if you are on a PC

Follow Microsoft's instructions to set up a WSL. As of the time of this writing, the best instructions are found [here](https://learn.microsoft.com/en-us/windows/wsl/setup/environment). You can also see [the official WSL page here](https://learn.microsoft.com/en-us/windows/wsl/install) for more context. Use the default installation options.

> [!CAUTION]
> When creating a linux username and password, best practices are to use a short username with all lowercase letters and with *no spaces*. A space may cause problems later. See [this link](https://learn.microsoft.com/en-us/windows/wsl/setup/environment#set-up-your-linux-username-and-password) for further information.

> [!TIP]
> Don't forget to restart your computer after installing the linux distro.

Next mount your PC's data drives to your WSL so you can access your neuroimaging files. Run the following command in the WSL terminal:

```
sudo mount -t drvfs C: /mnt/c/
```
> [!TIP]
> Right click in the WSL terminal to paste text. The `ctrl-v` shortcut won't work.

When prompted, enter the password to your WSL distro and press enter. Repeat for other Z: or D: drives as needed to access your data. 

> [!IMPORTANT]
> If you have data on a network drive, you can first mount the network drive to the PC and assign it a letter, then mount the drive to the WSL by the letter.

If you want to set up your WSL so that these drives automatically attach upon starting the WSL, you need to add these `mount` commands to your `.bashrc` file. To do this, open File Explorer in your PC and find the wsl machine. I usually find it through the File Explorer's sidebar. Then navigate to your WSL home directory and locate the .bashrc file. As an example, the address to my WSL .bashrc is `\\wsl.localhost\Ubuntu\home\mcclaskey\.bashrc`. Open the `.bashrc` file in notepad, scroll to the bottom, add the mount commands, then save and close the file.  

>[!TIP]
> If you don't see the .bashrc file, it may be hidden. Check that your file explorer is set to show hidden files. Alternately, you can edit this .bashrc file inside your WSL using a shell text editor such as nano or gedit or vim. [Choose wisely](https://en.wikipedia.org/wiki/Editor_war).

Close and reopen your WSL terminal. If this worked you should be prompted for your admin password. 

### 2. Install FSL

> [!NOTE]
> I know from my colleagues here at MUSC that FSL also works inside [PyDesigner via NeuroDock](https://pydesigner.readthedocs.io/en/latest/index.html), which uses Docker Desktop. However, one of the first steps in installing Docker Desktop and PyDesigner is installing WSL2, so I just skipped the extra Docker steps. But if you have FSL already installed on some unix/linux machine, then feel free to use that instead.

Open a shell/command window/terminal and type the following command into it:
```
fsl
```

If you see the following GUI pop up, you have FSL on the machine and can skip subsequent FSL install steps: 

![image](https://github.com/user-attachments/assets/633d0aa3-9f9c-436b-8757-749fa10de778)

Otherwise, go to the FSL installation page (currently [here](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation)) and follow the instructions for your operating system and try `fsl` again. For troubleshooting, see the FSL website.

### 3. Install Python

Python often comes natively on new machines but you may need to download it. To check if it's installed, run the following command in the terminal:

```
python --version
```

If that doesn’t work, your computer may not have the python alias and you may need to use `python3` instead of `python` going forward:

```
python3 --version
```


If nothing is found, download the latest stable python release from the main python downloads page [here](https://www.python.org/downloads/) and try again. 

> [!NOTE]
> These scripts were developed with python 3.11+. If your version is older than that, it might be a good idea to download a newer version just in case. 

### 4. Install git
Git also often comes natively installed on most WSL linux distros. In your terminal window, run the following command to check for git:
```
git version
```
If nothing comes up then you need to install git. See the top of [this page](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to find the command that installs it.

### 5. Install virtualenvwrapper python package for path management if necessary

These steps are also found in [the install page for virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html). Open a new terminal window and type:
```
pip install virtualenvwrapper
```

If that doesn’t work, your computer may not have the pip alias and you may need to use `pip3` instead of `pip` going forward:

```
pip3 install virtualenvwrapper
```

Next, print the path to the `virtualenvwrapper.sh` file by typing:
```
which virtualenvwrapper.sh
```
The location to the shell file will print into the terminal window. Make a note of it because you will need it for the next step.

Next you need to modify the `.bashrc` file to do 3 things: 
1. define where to store the virtual environments
2. define the default project location, and
3. run the `virtualenvwrapper.sh` file.

Detailed instructions for this step are currently explained [on this page](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#shell-startup-file) but I will list the minimum necessary steps here. You will now need to open your `.bashrc` file in a text editor. 

If you are on a WSL you can open the file in your Windows File Explorer. The official address of your wsl is likely `\\wsl.localhost\`, but you may also be able to navigate there using a link in the sidebar.

Otherwise, open it directly in Linux by typing this in the command line if you use a bash shell (which is the default for WSL):
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

Save and close the file. If using nano text editor, these are the steps to do so: type `ctrl+X` to close the nano text editor, then enter `Y` when asked if you want to save your changes, then when asked to confirm the filename, press enter to save the file under its current name.

Close the terminal window.

_CMcC’s notes for the lab:_
* _If you add it to the .bashrc file then those commands will only run if you open a normal bash shell. If you add it to the .zshrc file then they will run every time you open a zsh shell._
* _Your goal is to set it up so that those lines run every time you open the shell you’re going to use, otherwise the computer won’t be able to find the environment_
* _The lines you added must always be at the bottom of the file, so that any modifications to the path will be known to virtualenvwrapper. If it ever breaks in the future, it may be that relevant path changes were inserted below those virtualenvwrapper lines (for example FSL)._
* _NOTE: sometimes FSL adds its configuration lines to ~/.zprofile or ~/.bash_profile. These configuration files run everytime you log in to your username, rather than every time you open a shell. This may be why you don't see FSL's path configuration when you open your configuration file._
* _If you find that you can’t edit the `~/.zshrc` or `~/.basrc` file to add those three lines, then you will need to manually run them each time a new shell is opened. The 1st and 3rd are the most important ones to run and the 2nd line can be skipped_

### 6. Clone this repository (repo) to your computer
Open a terminal and change directories to where you will store the repo (or use `mkdir` to create a new folder). In this example I am using `~/repos/`. 
Once you are in the folder where the repo will be stored, clone the repo with this command:
```
git clone https://github.com/mcclaskey/batch_fslstats.git
```
This has created a folder called `/batch_fslstats/` inside the current folder. 

> [!TIP] 
> You will need to know the path to this repository for subsequents steps, so make a note of it here.
> As an example, because mine is stored in `~/repos/`, the path to my repository is  `~/repos/batch_fslstats/`.

### 7. Create the virtual environment (batch_fslstats_env) and link it with the repo

Open a new terminal window and type:
```
mkvirtualenv batch_fslstats_env
```
> [!NOTE]
> If this step doesn't work then see setup step 5 above

This will create the environment and also activate it. It will print something like this:

![image](https://github.com/user-attachments/assets/c289d83f-6b36-49cf-9c95-2c457d83cf30)

When the environment is activated you will see at the start of each line as in the above screenshot.

> [!NOTE]
> If you are on a Mac, you will see (Betach_fslstats_env) without the (base), as in the following screenshot: <img width="362" alt="image" src="https://github.com/user-attachments/assets/fb0ce957-4ff9-4793-8ae8-852d852df14f" />

Now `cd` to the main repository. If following my example, your `cd` command will look like this:
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
setvirtualenvproject ~/.virtualenvs/batch_fslstats_env $(pwd)
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

### 7. Install python packages into the batch_fslstats_env:
Open a fresh terminal window and run the following to activate the batch_fslstats_env and install the required packages:
```
workon batch_fslstats_env
pip3 install -r requirements.txt
```
You are now ready to run the main scripts using [these instructions](https://github.com/mcclaskey/batch_fslstats/blob/iss3-update-readme-for-clarify/README.md#instructions)

> [!NOTE]
> Any time you need to work with this project, open a terminal and run `workon batch_fslstats_env` to activate the environment. Code will only work in the active environment.




