import email
import imaplib

#email send
import smtplib
import ssl
from email.message import EmailMessage
import sys

while True:
    
    EMAIL = 'rohithsuri3@gmail.com'
    PASSWORD = sys.argv[1]
    SERVER = 'imap.gmail.com'

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    # we choose the inbox but you can select others
    mail.select('inbox')

    # we'll search using the ALL criteria to retrieve
    # every message inside the inbox
    # it will return with its status and a list of ids
    status, data = mail.search(None,'(FROM "Rohith S" SUBJECT "Deployment" UNSEEN)')
    # the list returned is a list of bytes separated
    # by white spaces on this format: [b'1 2 3', b'4 5 6']
    # so, to separate it first we create an empty list
    mail_ids = []
    # then we go through the list splitting its blocks
    # of bytes and appending to the mail_ids list
    for block in data:
        # the split function called without parameter
        # transforms the text or bytes into a list using
        # as separator the white spaces:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()

    # now for every id we'll fetch the email
    # to extract its content
    for i in mail_ids:
        # the fetch function fetch the email given its id
        # and format that you want the message to be
        status, data = mail.fetch(i, '(RFC822)')

    
        # the content data at the '(RFC822)' format comes on
        # a list with a tuple with header, content, and the closing
        # byte b')'
        for response_part in data:
            # so if its a tuple...
            if isinstance(response_part, tuple):
                # we go for the content at its second element
                # skipping the header at the first and the closing
                # at the third
                message = email.message_from_bytes(response_part[1])

                # with the content we can extract the info about
                # who sent the message and its subject
                mail_from = message['from']
                mail_subject = message['subject']
                message_id = message['Message-ID']
                print ("messageId"+message_id)
            


                # then for the text we have a little more work to do
                # because it can be in plain text or multipart
                # if its not plain text we need to separate the message
                # from its annexes to get the text
                if message.is_multipart():
                    mail_content = ''

                    # on multipart we have the text message and
                    # another things like annex, and html version
                    # of the message, in that case we loop through
                    # the email payload
                    for part in message.get_payload():
                        # if the content type is text/plain
                        # we extract it
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    # if the message isn't multipart, just extract it
                    mail_content = message.get_payload()

                # and then let's show its result
                if(("Deployment" in mail_subject) and ("rohithsuri77@gmail.com" in mail_from ) ):
                    print(f'From: {mail_from}')
                    print(f'Subject: {mail_subject}')
                    print(f'Content: {mail_content}')

                    # trigger a mail to deploy
            
                    email_sender = 'rohithsuri3@gmail.com'
                    email_password = sys.argv[1]
                    email_receiver = 'rohithsuri77@gmail.com'
                    body = """please deploy"""

                    em = EmailMessage()
                    em["Subject"] = "RE: "+message["Subject"].replace("Re: ", "").replace("RE: ", "")
                    em['In-Reply-To'] = message["Message-ID"]
                    em['References'] = message["Message-ID"]
                    em['Thread-Topic'] = message["Thread-Topic"]
                    em['Thread-Index'] = message["Thread-Index"]

                
                
                    em.set_content(body)

                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())

                        # move to archive
##                      imaplib.IMAP4.store(message_id, '+FLAGS', '\\Flagged')



            
            

            

            
