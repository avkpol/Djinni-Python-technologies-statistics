import csv
import matplotlib.pyplot as plt
import numpy as np


def analyze_skills():
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
    plt.show()


def analyze_applicants():
    applicants_data = {}
    with open('../data/python_vacancies.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            title = row[0]
            applicants = int(row[3])
            applicants_data[title] = applicants

    sorted_applicants = sorted(applicants_data.items(), key=lambda x: x[1], reverse=True)
    top_titles = [x[0] for x in sorted_applicants[:50]]
    top_counts = [x[1] for x in sorted_applicants[:50]]

    plt.figure(figsize=(10, 12))

    y_pos = np.arange(len(top_titles))
    plt.barh(y_pos, top_counts, align='center', alpha=0.5)
    plt.yticks(y_pos, top_titles)
    plt.xlabel('Applicants')
    plt.ylabel('Job Offers')
    plt.title('Applicants for Top 50 Job Offers')
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    analyze_skills()
    analyze_applicants()
