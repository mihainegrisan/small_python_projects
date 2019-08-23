#! python3
# randomQuizGenerator.py - Creates quizzes with questions and answers in random order, along with the answer key.

import random
import os

capitals = {'Romania': 'Bucharest', 'Germany': 'Berlin', 'Bulgaria': 'Sofia', 'Ukraina': 'Kiev'}

os.chdir('D:\\Python_code\\Automate_stuff\\quizzes')

   # Generate x quiz files.
for quiz_num in range(3):
    # Create the quiz and answer key files.
    quiz_file = open(f'capitalsquiz{quiz_num + 1}.txt', 'w')
    answer_key_file = open(f'capitalsquiz_answers{quiz_num + 1}.txt', 'w')

    # Write out the header for the quiz.
    quiz_file.write('Name:\n\nDate:\n\nPeriod:\n\n')
    quiz_file.write((' ' * 20) + f'State Capitals Quiz (Form {quiz_num + 1})\n\n')

    # Shuffle the order of the countries.
    countries = list(capitals.keys())
    random.shuffle(countries)

    # Loop through all 50 states, making a question for each.
    for question_num in range(len(capitals.keys())):

        # Get right and wrong answers.
        correct_answer = capitals[countries[question_num]]
          # duplicating all the values in the capitals dictionary
        wrong_answers = list(capitals.values())
          # deleting the correct answer from the copy I just made
        del wrong_answers[wrong_answers.index(correct_answer)]
          # selecting three random values from this list
        wrong_answers = random.sample(wrong_answers, 3)
          # wrong_answers is a list so it's 'list + list'
        answer_options = wrong_answers + [correct_answer]
        random.shuffle(answer_options)


        # TODO: Write the question and answer options to the quiz file.
        quiz_file.write(f'{question_num + 1}. What is the capital of {countries[question_num]}?\n')

        for i in range(4):
            quiz_file.write(' %s. %s\n' % ('ABCD'[i], answer_options[i]) )
        quiz_file.write('\n')

        # TODO: Write the answer key to a file.
        answer_key_file.write(' %s. %s\n' % (question_num + 1, 'ABCD'[answer_options.index(correct_answer)]) )

    quiz_file.close()
    answer_key_file.close()
