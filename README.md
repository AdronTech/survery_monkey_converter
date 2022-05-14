# Survey Monkey csv to normal csv converter
The survey monkey csv format (expanded) has two problems.
1. Each answer has its own column. 
   -> It is desired to collapse all answers of one question into a comma separated list.
2. Matrix multiple choice questions have for each sub question and answer pair a separate column.
   -> Each sub question gets it's own column "Question (Sub question)"

## Example
Input:
``` csv
q1 ,q2 ,q3 ,   ,q4       ,         ,         ,
   ,a1 ,a1 ,a2 ,sq1 - a1 ,sq1 - a2 ,sq2 - a1 ,sq2 - a2
1  ,a1 ,a1 ,   ,         ,         ,a1       ,
   ,   ,   ,a2 ,a1       ,         ,a1       ,a2
2  ,a1 ,a1 ,a2 ,         ,a2       ,         ,
o  ,   ,   ,   ,a1       ,a2       ,         ,a2
```

Output:
``` csv
q1 ,q2 ,q3      ,q4 (sq1) ,q4 (sq2)
1  ,a1 ,a1      ,         ,a1
   ,   ,a2      ,a1       ,"a1,a2"
2  ,a1 ,"a1,a2" ,a2       ,
o  ,   ,        ,"a1,a2"  ,a2
```

## Installation
* install Python 3
* install required modules with `python -m pip install -r requirements.txt`

## Execution

```
python3 survey_monkey_converter.py <input_file> <output_file>
```

```
Convert survey monkey csv to csv with collapsed answers

Usage:
    survey_monkey_converter.py <input_file> <output_file>
    survey_monkey_converter.py (-h | --help)
    survey_monkey_converter.py --version

Arguments:
    <input_file>  Input survey monkey expanded csv file
    <output_file> Output csv file

Options:
    -h --help     Show this screen.
    --version     Show version.
```