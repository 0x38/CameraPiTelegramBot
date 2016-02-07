#!/usr/bin/python
import telepot
import time
import picamera
import sqlite3
import sys
import os
import logging
from subprocess import check_call, CalledProcessError

""" Class based implementation of the telepot bot """
class PiCameraBot(telepot.Bot):

    def __init__(self, access_token):
        telepot.Bot.__init__(self, access_token)
        self.camera = picamera.PiCamera()
        self.listening_since = time.time()
        self.request_count = 0
        self.invalid_users_count = 0
        # Set some camera options if needed
        # self.camera.vflip = True
        # self.camera.hflip = True
        
    """ Handles incoming messages """
    def handle(self, msg):
        chat_id = msg['from']['id']
        user_name = "%s %s" % (msg['from']['first_name'], msg['from']['last_name'])
        command = msg['text']
        self.request_count += 1
        
        conn = sqlite3.connect('camerapibot_auth.db')
        c = conn.cursor()
        
        c.execute('SELECT id FROM allowed_user_ids')
        query = c.fetchall()
        
        valid_ids = []
        for x in query:
            s = str(x[0])
            valid_ids.append(s)
        if not str(chat_id) in valid_ids:
            logging.warning("[Access] Failed authentication attempt! user_id: %s" % chat_id)
            self.invalid_users_count += 1
        else:
            if command == '/get_status':
                logging.info("Received /get_status from %s (username: %s )" % (chat_id, user_name))                
                self.sendMessage(chat_id, 'The Bot is listening since: %s' % self.listening_since)
                self.sendMessage(chat_id, 'Total request count: %s' % self.request_count)
                self.sendMessage(chat_id, 'Total unauthorized access attempts: %s' % self.invalid_users_count)
                logging.info("Sent the current status to %s (username: %s )" % (chat_id, user_name))
            elif command == '/get_image':
                logging.info("Received /get_image from %s (username: %s )" % (chat_id, user_name))
                self.camera.resolution = (1920, 1080)
                self.camera.capture('image.jpg')
                f = open('image.jpg', 'rb')
                self.sendPhoto(chat_id, f)                
                logging.info("Sent a picture to %s (username: %s )" % (chat_id, user_name))
            elif command == '/get_video':
                logging.info("Received /get_video from %s (username: %s )" % (chat_id, user_name))
                try:
                    os.remove('video.h264')
                except OSError:
                    pass
                try:
                    os.remove('video.mp4')
                except OSError:
                    pass
                self.camera.resolution = (1280, 720)
                self.camera.start_recording('video.h264')
                self.camera.wait_recording(10)
                self.camera.stop_recording()
                cmd = ['MP4Box', '-add', 'video.h264', 'video.mp4']
                try:
                    check_call(cmd)
                    f = open('video.mp4', 'rb')                
                    self.sendVideo(chat_id, f)
                    logging.info("Sent a video to %s (username: %s )" % (chat_id, user_name))
                except CalledProcessError:
                    logging.info("A problem occured while encoding the video!")
                    self.sendMessage(chat_id, 'A problem occured!')                
        conn.close()
# Getting the token from command line input is a safer way than to put it into the script as it is meant to be kept secret
TOKEN = sys.argv[1]

# Set up the logging format
logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='camerapi_bot.log', level=logging.INFO)
logging.info("Initializing CameraPiBot")
# Initialize the bot
bot = PiCameraBot(TOKEN)
bot.notifyOnMessage()
logging.info("Listening...")

# Main loop catching Keyboard Interrupts: If one is detected it shuts down the bot and cleans up the produces files except for the log file
while 1:
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        try:
            os.remove("image.jpg")
        except OSError:
            pass
        try:
            os.remove("video.h264")
        except OSError:
            pass
        try:
            os.remove("video.mp4")
        except OSError:
            pass
        logging.info("KeyboardInterrupt detected, shutting down the bot!")
        sys.exit("\nShutting down the Telegram Bot!")
    