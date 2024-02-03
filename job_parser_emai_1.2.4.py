from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from selenium.common.exceptions import NoSuchElementException
from exchangelib import Account, Credentials, Message, Mailbox, HTMLBody, FileAttachment
import getpass
import argparse
import configparser

# Your existing code for reading credentials from the configuration file
config = configparser.ConfigParser()
config.read('credentials.ini')
email = config.get('Outlook', 'email')
password = config.get('Outlook', 'password')
a = Account(email, credentials=Credentials(email, password), autodiscover=True)

# Add command line arguments support
parser = argparse.ArgumentParser(description='Job Parser and Email Sender')
parser.add_argument('-a', '--apply', action='store_true', help='Apply for jobs')
parser.add_argument('-d', '--email', help='Email address for sending test emails')
parser.add_argument('--test_mode', action='store_true', help='Enable test mode')
args = parser.parse_args()

# Initial URLs for crawling
initial_urls = [


]

# Iterate through each initial URL
for initial_url in initial_urls:
    driver = webdriver.Chrome()
    driver.get(initial_url)
    time.sleep(2)


    links = driver.find_elements(By.CSS_SELECTOR, 'a')

    # Get links only to job postings
    job_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and link.get_attribute('href').startswith('https://www.jobbank.gc.ca/jobsearch/jobposting/')]

    # Iterate through each job posting
    for job_link in job_links:
        driver.get(job_link)
        time.sleep(5)

        # Get company name and email
        try:
            company_names, email_addresses = [], []
            company_name_elements = driver.find_elements(By.XPATH, "//span[@property='hiringOrganization']//span[@property='name']//*[self::strong or self::a]")

            for element in company_name_elements:
                if element.tag_name.lower() in ['strong', 'a']:
                    company_names.append(element.text.strip())

            apply_button = driver.find_element(By.ID, 'applynowbutton')
            apply_button.click()
            time.sleep(2)

            email_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'mailto')]")
            for email_link in email_links:
                email_address_match = re.search(r'mailto:(.*?)(&|\?|$)', email_link.get_attribute('href'))
                if email_address_match:
                    email_address = email_address_match.group(1)
                    if email_address:
                        email_addresses.append(email_address)

            if company_names and email_addresses:
                print(f"Company Names: {', '.join(company_names)}")
                print(f"Found Email Addresses: {', '.join(email_addresses)}")

                # Email body for debugging
                if args.test_mode:
                    if args.email:
                        test_email_address = args.email
                        print(f'Test mode: Sending test email to {test_email_address}')
                        m = Message(
                            account=a,
                            subject="Test Email Subject",
                            body=HTMLBody("This is a test email body."),
                            to_recipients=[Mailbox(email_address=test_email_address)]
                        )
                        m.send_and_save()
                        print(f"Test email sent to {test_email_address}")
                    else:
                        print('Test mode enabled, but no email address provided for testing.')
                else:
                    # Email body for other users
                    body = f"""
                        Dear HR team,<br><br>
                        <br><br>
                        I hope this message finds you well. My name is Levko Kravchuk, and I am writing to express my sincere interest in joining {company_names[0]} as a Sys Admin/Network Admin.
                        <br><br>
                        With a solid background in systems administration and network management, I am enthusiastic about the prospect of contributing my skills and expertise to your esteemed company. My experience in ensuring seamless operations, optimizing network performance, and maintaining system security aligns with the responsibilities of a Sys Admin/Network Admin role.
                        <br><br>
                        Having recently relocated to Canada, I hold an open work permit valid until 13th June 2026 and am eager to contribute my knowledge and expertise within the Canadian job market.
                        <br><br>
                        I have attached my resume for your consideration. I am confident that my experience in system administration, network maintenance, and troubleshooting aligns well with the needs of {company_names[0]}.
                        <br><br>
                        I would greatly appreciate the opportunity to discuss how my background and skills can contribute to the efficiency and success of {company_names[0]}. Please let me know if there is any additional information I can provide.
                        <br><br>
                        Thank you for considering my application. I am excited about the possibility of contributing to your team and look forward to the opportunity to discuss this further.
                    """

                    # Signature
                    signature = """
                        Warm regards,  <br><br>
                        System & Network Administrator by DevOps methodology   <br><br>
                        Levko Kravchuk  <br><br>
                    """

                    # Send email
                    for email_address in email_addresses:
                        m = Message(
                            account=a,
                            folder=a.sent,
                            subject=f"Levko Kravchuk Network Administrator | System Administrator by DevOps Technology | Tier1 support engineer at {company_names[0]}",
                            body=HTMLBody(body + signature),
##FOR DEBAUG ADD to CC                            to_recipients=[Mailbox(email_address=email_address)],
##                           cc_recipients=[Mailbox(email_address='xxxx@i.ua')]

                            to_recipients=[Mailbox(email_address=email_address)]

                        )

                        # Attach resume file
                        with open('Levko_Kravchuk_Resume.pdf', 'rb') as file:
                            content = file.read()
                            file_attachment = FileAttachment(name='Levko_Kravchuk_Resume.pdf', content=content)
                            m.attach(file_attachment)
                         
                        # Attach QR code image
                        with open('RH_QR_Levko_web_site.png', 'rb') as img_file:
                            img_content = img_file.read()
                            img_attachment = FileAttachment(name='RH_QR_Levko_web_site.png', content=img_content)
                            m.attach(img_attachment)

                        # Send and save email
                        m.send_and_save()
                        print(f"Email sent to {email_address}")

            else:
                print("No company names or email addresses found.")

        except Exception as e:
            print(f"Error processing job link: {e}")

        print("-----------------")

    driver.quit()

