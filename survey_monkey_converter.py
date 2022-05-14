#!/usr/bin/env python3
""" Convert survey monkey csv to csv with collapsed answers

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
"""

from pathlib import Path
import csv
from type_docopt import docopt

def fix_table(input, output):
    """ Fix headers of multiple choice matrix questions. Convert to multiple questions with multiply choice answers.

    Args:
        input (str): Input csv file
        output (str): Output csv file

    Example:
        Input:
            Question 1              ,                         ,                         ,
            Subquestion 1 - Answer 1, Subquestion 1 - Answer 2, Subquestion 2 - Answer 1, Subquestion 2 - Answer 2

        Output:
            Question 1 (Subquestion 1),         , Question 1 (Subquestion 2),
            Answer 1,                 , Answer 2, Answer 1                  , Answer 2
    """

    with open(input, 'r', encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file)

        # read first header
        header = list(map(str.strip, next(csv_reader)))

        # read second header
        second_header = list(map(str.strip, next(csv_reader)))

        current_question = ""
        current_subquestion = ""
        for i in range(len(header)):
            if header[i].strip() != '':
                current_question = header[i]
            
            # is second header subquestion (noted by a '-' in the second header and not an open-ended question)
            is_subquestion = '-' in second_header[i] and not second_header[i].strip() == "Open-Ended Response"

            if not is_subquestion: continue

            # get subquestion and answer option
            subquestion = second_header[i].split('-')[0].strip()
            answer_option = second_header[i].split('-')[1].strip()

            # don't add subquestion empty parenthesis if subquestion is empty
            if subquestion != '':
                new_subquestion = f"{current_question} ({subquestion})"

            # create modified header "Q1 (Sq 1)" only for new subquestion and not each answer option of the same subquestion
            if current_subquestion != new_subquestion:
                header[i] = new_subquestion
                current_subquestion = new_subquestion

            # always update answer option with shorted version
            second_header[i] = answer_option

        with open(output, 'w', encoding="UTF-8", newline='') as output_file:
            csv_writer = csv.writer(output_file)
            # write header
            csv_writer.writerow(header)
            csv_writer.writerow(second_header)

            # write rest of rows
            for row in csv_reader:
                csv_writer.writerow(row)

def collapse_csv(input, output):
    """ Collapse answers to single column. Expanded csv file has multiple columns for each answer option.

    Args:
        input (str): Input csv file
        output (str): Output csv file

    Example:
        Input:
            Question 1,         , 
            Answer 1  , Answer 2, Answer 3
                      ,         , 
            Answer 1  ,         , 
                      , Answer 2, Answer 3
            Answer 1  , Answer 2, Answer 3

        Output:
            Question 1
            ""
            Answer 1
            "Answer 2,Answer 3"
            "Answer 1,Answer 2,Answer 3"
    """

    with open(input, 'r', encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file)

        # read first header
        header = next(csv_reader)

        # extract question and number of answers per question
        question = []
        question_index = []
        answer_options = []
        for i, q in enumerate(header):
            
            # if header is present add new question (with one answer)
            if q.strip() != '':
                question.append(q)
                question_index.append(i)
                answer_options.append(1)
            # else add answer option to previous question
            else:
                answer_options[-1] += 1

        # use second header as answer strings (not for open-ended questions)
        predefined_answers = next(csv_reader)

        with open(output, 'w', encoding="UTF-8", newline='') as output_file:
            csv_writer = csv.writer(output_file)
            # write header (skip second header; not needed anymore)
            csv_writer.writerow(question)

            # for each row collapse answers
            for row in csv_reader:
                output_row = []
                for i in range(len(question)):

                    # collect all answers for this question
                    answers = []
                    for j in range(question_index[i], question_index[i] + answer_options[i]):
                        predefined_answer = predefined_answers[j].strip()
                        answer = row[j].strip()

                        # open ended questions have no predefined answer and original answer is kept
                        if predefined_answer == "Open-Ended Response" or predefined_answer == '':
                            answers.append(answer)
                        else:
                            # skip empty answers
                            if answer == '': continue
                            
                            # use predefined answer from second header
                            answers.append(predefined_answer)
                    
                    # filter empty answers
                    answers = [a for a in answers if a != '']

                    # create collapsed answer string
                    output_row.append(','.join(answers))

                # write output file
                csv_writer.writerow(output_row)

if __name__ == "__main__":

    arguments = docopt(__doc__, version='Survey Monkey Converter 1.0')

    input_file = Path(arguments['<input_file>'])
    output_file = Path(arguments['<output_file>'])
    temp_file = Path(f"{output_file.stem}_temp.csv")

    fix_table(input_file, temp_file)
    collapse_csv(temp_file, output_file)

    temp_file.unlink()