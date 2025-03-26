# Project Description
## Project Directory Structure
- All file you need to run the project are in folder **[src](src)**
- There are two sub folders in **[src](src)**: **[python](src/python)** and **[resources](src/resources)**.  
  * Inside **[python](src/python)** are source of the project.
  * Inside **[resources](src/resources)** are resources file that required by the project, including models dataset and log file of training process

## Envorinment Setting
Please note that all command below should be run in folder **[advai-group-project](.)**
```shell
# Install virtual environment from file
conda env create -f environment.yml

# Activate environment
conda activate aitut

# Install a tool library developed by myself
pip install devtoolkit-0.1.0.2025032502-py3-none-any.whl

# Move model file to resources diectory
mv 

```
By command above, runtime environment successfully setup.
## Run the Project
- Firstly, you should run the **Quanser Interactive Labs**, select **Qbot Platform** > **Warehouse**
- Then, run command below. You may find logs print in console.
```shell
python ./src/python/main.py
```
- Congratulations! You have successfully run the project.
## How to Use the Project
- There are three ways to control qbot in virtual environment: Manual, Automatic(semi) and Pre-Programmed. After environment initialized, you will see line below in console:
```
Select a control method: (m/a/p)
```
You need to enter one of the three letters **m**(manual), **a**(automatic), and **p**(pro-programmed) in console and press **enter** to choose a control method.
* **Control Types**
  * Manual Control  
  In this control mode, you can simply use **wasd** to manually move qbot to anywhere you want. Due to the limited performance of your computer, please do not keep pressing a certain key. You should input every command seperately. It is also should be noted that there is no need to input command in console, for programme will listen to realtime input of keyboard.

  * Automatic Control  
  In this control mode, qbot will automatically follow the line if there is only a single way. Everytime when you encounter a fork in the line, there is a need to press **awd** to decide which way to go. Similar to manual control, there is also no need for you to input your command into the console, simply press the key will be fine. 

  * Pre-Programmed Control  
  After you select this control mode, you will find line below in console:
```
[Info][2025-03-26 10:03:56][main(combination)]: Programmed control selected.
Command sequences:
```
In this case, you need to input a sequence of **awd** in console and press **enter** to decide a specific routine that can reach target point.
- **Change Control Types**  
  You can press **q** to quit current control type and select a new way to control the qbot. When you press **q**, qbot will stop and line below will appear on console again:
```
Select a control method: (m/a/p)
```
- **Enable Image Mode**  
  When qbot in the main control loop, you can press **g** to enable/disable **image mode**. In image mode, qbot will automatically save image collected by its down camera to a certain folder. The initial status of image mode and image save folder can be simply altered by change several variables in **[main.py](src/python/main.py)**
- **Quit Program**  
  You cam quit the whole program by press **ese** on keyboard.