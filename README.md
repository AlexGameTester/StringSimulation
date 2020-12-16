# StringSimulation

## Description
* Simulates string oscillations using two main methods:

### Method #1: Physical simulation.
1. Springs.
Simulates a string as a set of point masses connected with springs governed by [Hooke's Law](https://en.wikipedia.org/wiki/Hooke%27s_law).
2. Constant force.
Simulates a spring as a set of point masses that apply force T on neighbours. The force has constant magnitude and it's pointing on the neighbouring point.

### Method #2: Solving wave equation.
Wave equation, more about wave equation:

+ [Wave Equation](https://en.wikipedia.org/wiki/Wave_equation)

1. Fourier method.
Solves wave PDE via fourier method, 

more on Fourier method:

+ [Fourier Method](https://www.roe.ac.uk/japwww/teaching/fourier/fourier_lectures_part5.pdf)

+ [Fourier Transform](https://en.wikipedia.org/wiki/Fourier_transform)

+ [Fourier Method for Wave Equation(RUS)](http://window.edu.ru/resource/137/47137/files/sssu081.pdf)



## Contents
- [Description](#description)
- [Functions](#description)
- [Usage](#usage)
- [Module Description](#module-description)


## Usage.

### **Input Window**:


![Image of InpWdw](https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/InputWdw.png)



### there are five inputs in this window:

1. **Speed of Sound in material**: Speed with which sound wave propagates in the string material. 
"c" coefficient in the wave equation stands for this parameter.

**Validation** - must be positive real number in range  *5 <= param <= 343*  (speed of sound in the air).
abstract units of measurenment, not meters per second in particular.

**Default Value** - 5


2. **Simulation Time**: Simulation time interval length. 

**Validation** - must be a positive real in range  *5 <= param <= 100* .
measured in seconds.

**Default Value** - 5


3. **Number of points in a chain**: Number of material points in the chain. For more details see - [Physical Simulation](#description)

**Validation** - must be an integer in range  *3 <= param <= 1000* .
no specified units. 

**Default Value** - 20


4. **Precision of modelling**: parameter on which calculation step (i.e. precision with which these calculations are made).

**Validation** - an integer in range  *10 <= pararm <= 1000* .
no specified units.

**Default Value** - 10


5. **Simulation method**: Determines how physical string will be modelled. List with two options:
  
    1. Springs.
    2. Constant Force.

Details - [Physical Simulation](#description).

**Default value** - "Springs"

#### Buttons ####

1. "**File Menu**" - after clicking you should choose a non-empty file with initial parameters of points of a string. Initial parameters include:
vertical components of velocities and y coordinates for each point in a string.
*file format* - **.txt**

2. "**Start**" - after you have filled all input fields correctly and choose file with initial parameters you may press start button. 
Pressing it will execute main modules of the program. In particular, you will see [Progress Bar](#progress-bar).


### **Progress Bar**:


If you have executed program with no exceptions you will see *progress bar*, 

![Image of PgrBr](https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/Безымянный.png)

The bar allows you to track relative completion time of simulation processing. 
When processing of simulation will be finished, window will display 100%.

### **Animation Window**:




## Module Description.



* **animation_window**:
* **calculations_manager**:
* **config**: 
* **image_reading**: 

* **inputwindow**: user interface in which initial conditions(elastic characteristics of a string e.g.) can be inputted. For usage see - [Usage](#usage) inputwindow.

* **main**: main module.

* **manager**: regulates work of Output_manager, Calculation_manager, Input_window. and their interaction via passing necessary data(starting parameters, solutions...).

*some functions*:starts calculation processes, starts string animations, shows input window.

* **math_simulator**:
* **output_manager**:
* **physical_simulator**:
* **simulation**:
* **simulator**:
