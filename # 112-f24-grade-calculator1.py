# 112-f24-grade-calculator1.py

# You can use this script to explore how your grade will change based
# on your estimated midterm2, term project, and final exam scores.

# 1. Fill these in from your gradebook on Autolab:
hwAvg = 99.8         # from Autolab (already includes two half-weighted)
quizAvg =  85.2        # from Autolab (already drops + half-weights_
midterm1Score = 88.7 # from Autolab

# 2. Fill these in based on your best guesses:
midterm2Score = 85.5
termProjectScore = 94
finalExamScore = None  # None means "not taking"

# 3. Find tpAvg and examAvg:
tpAvg = termProjectScore # these are the same :-)
loMidterm = min(midterm1Score, midterm2Score)
hiMidterm = max(midterm1Score, midterm2Score)
if finalExamScore == None:
    examAvg = (hiMidterm + loMidterm/2) / 1.5
else:
    # final exam taken, so counts as much as higher midterm:
    examAvg = (finalExamScore + hiMidterm + loMidterm/2) / 2.5

# 4. Compute semesterAvg and semesterGrade
semesterAvg = (hwAvg*.20 + tpAvg*.20 + quizAvg*.15 + examAvg*.45)
if semesterAvg >=   89.5: semesterGrade = 'A'
elif semesterAvg >= 79.5: semesterGrade = 'B'
elif semesterAvg >= 69.5: semesterGrade = 'C'
elif semesterAvg >= 59.5: semesterGrade = 'D'
else:                     semesterGrade = 'R'

# 5. Print report
components = (('Homework',    hwAvg,   0.20),
              ('TermProject', tpAvg,   0.20),
              ('Quizzes',     quizAvg, 0.15),
              ('Exams',       examAvg, 0.45))
print('Component   Score    Weight  Contribution')
for label, avg, weight in components:
    print(f'{label:11} {avg:5.1f} {100*weight:-8}% {avg*weight:7.1f}')
print(f'Projected semester numeric grade: {semesterAvg:0.1f}')
print(f'Projected semester letter grade:  {semesterGrade}')