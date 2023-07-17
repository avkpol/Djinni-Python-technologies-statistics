import csv
import matplotlib.pyplot as plt
import numpy as np

skills_data = {}
with open('../data/skills.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        skill = row[0]
        count = int(row[1])
        skills_data[skill] = count

skills = list(skills_data.keys())
counts = list(skills_data.values())

x_pos = np.arange(len(skills))
plt.bar(x_pos, counts, align='center', alpha=0.5)
plt.xticks(x_pos, skills, rotation='vertical')
plt.xlabel('Skills')
plt.ylabel('Total')
plt.title('Skills Analysis')
plt.tight_layout()

# Display the bar plot
plt.show()
