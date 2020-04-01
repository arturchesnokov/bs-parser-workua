import sqlite3


def save_to_db(summary, href, salary, company, address, requirements, description):
    connection = sqlite3.connect('work-ua.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                        Position text, 
                        Link_id text, 
                        Salary text, 
                        Company text, 
                        Address text, 
                        Requirements text, 
                        Description text)
                    ''')

    cursor.execute('INSERT INTO vacancies VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (summary,
                    href,
                    salary,
                    company,
                    address,
                    requirements,
                    description))

    connection.commit()
    connection.close()
