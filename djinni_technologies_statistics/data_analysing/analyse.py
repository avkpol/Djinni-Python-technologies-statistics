import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def preprocess_salary(salary):
    if pd.notnull(salary):
        if '-' in salary:
            salary_range = salary.strip().split('-')
            salary_values = [
                int(value.replace('$', '').
                    replace(',', '').strip()[-4:]) for value in salary_range
            ]
            return max(salary_values)
        elif salary.startswith('до'):
            return int(
                salary.strip().replace('до $', '').replace(',', '').strip()[-4:]
            )
        elif salary.startswith('від'):
            return int(
                salary.strip().replace('від $', '').replace(',', '').strip()[-4:]
            )
        else:
            return int(salary.strip().replace('$', '').replace(',', '').strip()[-4:])
    return 0

def perform_correlation_analysis(vacancies_file, skills_file):
    df_vacancies = pd.read_csv(vacancies_file)
    df_skills = pd.read_csv(skills_file)
    df_vacancies['salary'] = df_vacancies['salary'].apply(preprocess_salary)
    columns = ['experience', 'salary', 'views', 'applications']
    for skill in df_skills['Skill']:
        skill_vacancies = (
            df_vacancies[df_vacancies['description'].
            str.contains(skill, case=False, na=False)]
        )
        correlation_matrix = skill_vacancies[columns].corr()
        print(f"Correlation Matrix for Skill: {skill}")
        print(correlation_matrix)
        print("\n")



if __name__ == "__main__":
    analyze_skills()
    analyze_applicants()
    perform_correlation_analysis('../data/python_vacancies.csv', '../data/skills.csv')
