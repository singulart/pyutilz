from bs4 import BeautifulSoup
import csv

with open("source.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table containing program manager information
table = soup.find('table', {'id':'programmanagerslist'})  # Adjust the selector as needed

# Open a CSV file to write the data
with open('program_managers.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Email'])  # Write the header row

    # Iterate through the table rows and extract Name and Email
    for row in table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if len(columns) >= 2:
            name = columns[3].get_text(strip=True)
            email = columns[4].get_text(strip=True)
            writer.writerow([name, email])

print('Data has been written to program_managers.csv')

