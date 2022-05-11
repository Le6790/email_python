import gmail_email
import config


def main():

    gmail = gmail_email.GmailEmail()
    labels = gmail.get_labels()

    gmail.send_text_email(to_email=config.MY_EMAIL,from_email=config.MY_EMAIL,subject="Subjectline",message="The message")

if __name__ == '__main__':
    main()
    