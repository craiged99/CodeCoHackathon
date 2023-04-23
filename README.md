# CodeCoHackathon

NOTE: There is a second repository for the backend and frontend work for the web-tool - find it here:
https://github.com/nikiis/kicksmarter-hackathon?fbclid=IwAR2CvBAG07fps940BpMAyey5bVarnHy8PTpOcMzA-b9Vk3LhXRrdyK55iL8

The main 'live' data is in the all_func_live.py script - all other scripts are just functions used in this main script. For the sake of the demo, this code is intended to create text/plots for each minute of a game, so would not work in it's current state in an actual live game scenario, however, could easily be adapted. 

The output is a dictionary with the following info: 
- Game time (minute)
- Text to output
- Names of figures produced

Currently, there are 28 anomalies that the script looks for, with easy potential to add more.
