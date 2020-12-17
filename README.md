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
- [Usage](#usage)
- [Controls](#other-controls)




## Usage.

### **Input Window**:


![Image of InpWdw](https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/InputWdw.png)



### there are five inputs in this window:

1. **Speed of Sound in material**: Speed with which sound wave propagates in the string material. 
"c" coefficient in the wave equation stands for this parameter.

**Validation** - must be positive real number in range  *5 <= param <= 343*  (speed of sound in the air).

abstract units of measurenment, not meters per second in particular.

**Default Value** - 1


2. **Simulation Time**: Simulation time interval length. 

**Validation** - must be a positive real in range  *5 <= param <= 100* .

measured in seconds.

**Default Value** - 5


3. **Number of points in a chain**: Number of material points in the chain. For more details see - [Physical Simulation](#description)

**Validation** - must be an integer in range  **3 <= param <= 1000** .

no specified units. 

**Default Value** - 20


4. **Precision of modelling**: parameter on which calculation step (i.e. precision with which these calculations are made).

**Validation** - an integer in range  **10 <= pararm <= 1000** .

no specified units.

**Default Value** - 10


5. **Simulation method**: Determines how physical string will be modelled. List with two options:
  
    1. Springs.
    2. Constant Force.

Details - [Physical Simulation](#description).

**Default value** - "Springs"

### Buttons ###

1. "**File Menu**" - after clicking you should choose a non-empty file with initial parameters of points of a string. Initial parameters include:
vertical components of velocities and y coordinates for each point in a string.
*file format* - **.txt**

2. "**Start**" - after you have filled all input fields correctly and choose file with initial parameters you may press start button. 
Pressing it will execute main modules of the program. In particular, you will see [Progress Bar](#progress-bar).


### **Progress Bar**:


If you have executed program with no exceptions you will see *progress bar*, 

![Image of PgrBr](https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/Безымянный.png)

The bar allows you to track relative completion time of simulation processing. 
When processing of simulation will be finished, window will display 100%. And you will see an [animation window](#animation-window).

![Gif PlSp](https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/gif2.gif)

### **Animation Window**:
When the processing was done, program will launch animation:

<img width=50% height=50% class="animated-gif" src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/Window1.png">


Besides animation itself - red points which represented the string, there is a playback bar:

<p><img width=50% height=50% src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/Window3.png"></p>

With two parameters:

1.[Simulation Time](#usage)

2.[Playback Speed](#usage)

Which supports player functionality,

For example: pressing **left** or **right button** 
<img width=5% height=5% src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/keyboard_key_right.png"> 
you may move forward or backward in animation playback:

<img width=40% height=40% class="animated-gif" src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/ezgif.com-video-to-gif.gif">

### Other Keyboard Controls ###

+ To control playback speed press **down** or **up button** - <img width=5% height=5% src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/keyboard_key_up.png"> 




![Gif PlSp2](https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/gif3.gif)


+ To **pause or resume** animation playback press <img width=5% height=5% src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/загруженное.png"> 

+ To **reset** playback press <img width=5% height=5% src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/4.jpg">

+ To **set** playback speed to *1* press <img width=5% height=5% src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/загруженное.jpg">

+ To **Exit** playback animation press <img width=5% height=5% src="https://github.com/AlexGameTester/StringSimulation/blob/master/images%20for%20readme/kissclipart-esc-keyboard-button-clipart-computer-keyboard-esc-836a93420436eb0a.png">
