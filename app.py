import facebook as fb
import psycopg2
import base64
import time
from datetime import datetime
import pytz

# conn = psycopg2.connect('postgresql://18.134.145.20/AIADB?user=ubuntu&password=postgres')
conn = psycopg2.connect('postgresql://172.31.12.25/AIADB?user=ubuntu&password=postgres')

cursor = conn.cursor()

# Get Access token - Follow on how to get access token for your fb account
access_token ='EAAMG9lJMFZB8BAIVAtQpRhv6OYSd5MgBLzyv3DElVGwlqqs2uMLNdYZCkpHZAqNVOr10dhZATU49PZAAKzgpHe1x6iAUETDfUFQwcKXo06eFbR3mo8AZBEbSGXz3nKWg2JfIPDxMDbUj1UOgkXrEZA3aLXYPXFyfQXvojaeUOgShdeMNeEhT9XZBYZBcYmxp6prrjsg0c5C7IrwZDZD'
# The Graph API allows you to read and write data to and from the Facebook social graph
asafb = fb.GraphAPI(access_token)

# Post a message in the facebook page
def postMessage(msg):
    asafb.put_object("me","feed",message = msg)

def postMessageAndPicture(img, msg):
    print(asafb.put_photo(open(img,"rb"), message = msg))


def checkForPosts():
    cursor.execute("SELECT id, post, image, date_to_be_posted FROM socialmediaposts where status='Pending'")
    return cursor.fetchall()

def updatePostStatus(id):
    cursor.execute("UPDATE socialmediaposts SET status='Posted' where id=" + id)
    conn.commit()
    # return cursor.fetchall()

def compareTime(timestring):
    # format = '%Y-%m-%dT%H::%M::%S.%f' 
    # postTime = datetime.strptime(timestring, format)
    # nowTime = datetime.strptime(str(datetime.now()), format)
    if datetime.now().replace(tzinfo=pytz.utc) >= timestring:
        return True
    else:
        return False

while True:
    if len(checkForPosts()) > 0:
        for row in checkForPosts():
            if  compareTime(row[3]):
                imagName = 'Post1.png'
                image_result = open(imagName, 'wb') # create a writable image and write the decoding result
                image_result.write(base64.b64decode(row[2]))
                postMessageAndPicture(imagName, row[1])
                updatePostStatus(str(row[0]))
                print('Posted '+ str(row[0]))
    else:
        print('Nothing to Post')
    
    time.sleep(600)
