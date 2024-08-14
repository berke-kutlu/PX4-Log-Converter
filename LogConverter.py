"""
Log Converter for https://review.px4.io

This code is used for turning your flight reports into links and get an output as a txt file
To use it simply give a path and e-mail input
"""
import os
import requests
from bs4 import BeautifulSoup

# Function to return the links as a list
def get_review_links(path, file_names, e_mail):
    review_links = []
    url = "https://review.px4.io"
    form_data = {
        'description': '',
        'feedback': '',
        'type': 'flightreport',
        'public': 'false',
        'redirect': 'false',
        'email': e_mail
    }

    for file in file_names:
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        form = soup.find('form', {'id': 'upload-form'})
        action = form.get('action')
        form_url = requests.compat.urljoin(url, action)

        
        file_path = path + "\\" + file

        files = {
            'filearg': open(file_path, 'rb')
        }

        response = session.post(form_url, data=form_data, files=files)

        if response.ok:
            print("Review Succesfully Post")
            review_links.append(url + response.text.split("\"")[3])
        else:
            print("Review Post Process Failed")
    return review_links

# Function to print out the links in a txt file named as the same folder
def print_out_links(review_links, output_path):
    with open(output_path, "a") as file:
        for link in review_links:
            file.write(f"{link}\n\n")

def main(path, e_mail):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError
        output_path = path.split("\\")[-1] + ".txt"
        file_names = os.listdir(path)
        review_links = get_review_links(path, file_names, e_mail)
        print_out_links(review_links, output_path)
    except FileNotFoundError:
        print(f"ERROR: {path} doesn't exist")


if __name__ == "__main__" :
    # Give input as path\to\your\file\2024-07-29
    path = input("Enter Log Path: ")
    e_mail = input("Enter E-Mail: ")
    main(path, e_mail)