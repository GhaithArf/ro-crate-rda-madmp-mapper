ECHO Test madmp to rocrate
python mapper.py -r "examples\madmp\madmp-dataset-many" -o "examples\madmp\results\ex1"
python mapper.py -r "examples\madmp\madmp-closed" -o "examples\madmp\results\ex2"
python mapper.py -r "examples\madmp\madmp-funded-project" -o "examples\madmp\results\ex3"
python mapper.py -r "examples\madmp\madmp-life-expectancy-prediction" -o "examples\madmp\results\ex4"
python mapper.py -r "examples\madmp\madmp-long" -o "examples\madmp\results\ex5"
python mapper.py -r "examples\madmp\madmp-calculation-of-nice-sunny-days" -o "examples\madmp\results\ex6"
python mapper.py -r "examples\madmp\madmp-minimal-content" -o "examples\madmp\results\ex7"
python mapper.py -r "examples\madmp\madmp-multilayer-perceptron-on-hypothyroid" -o "examples\madmp\results\ex8"
python mapper.py -r "examples\madmp\madmp-swedish-motor-insurance" -o "examples\madmp\results\ex9"
python mapper.py -r "examples\madmp\madmp-World-development-indicators" -o "examples\madmp\results\ex10"

ECHO Test rocrate to madmp
python mapper.py -r "examples\rocrate\Glop_Pot" -o "examples\rocrate\results\ex1"
python mapper.py -r "examples\rocrate\GTM" -o "examples\rocrate\results\ex2"
python mapper.py -r "examples\rocrate\NursingResidentStuff" -o "examples\rocrate\results\ex3"

ECHO Test rocrates to madmp
python mapper.py -r "examples\rocrate" -o "examples\rocrate\results\ex4"

PAUSE
