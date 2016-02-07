# CameraPiTelegramBot

## Basic Installation
In order for the script to work, you need a working Python 2.7.x installation. You can check which version is installed by running `python --version` inside your shell. It is recommendable to use `python-pip` for module management, because pip resolves dependencies automatically.

### Prequesites
* The telepot module for Python
 * You can install it by running `pip install telepot`
* The picamera module for Python
 * You can install it by running `pip install picamera`
* Set up the bot by contacting @BotFather on Telegram using the following commands:
 * `/newbot` (@BotFather will ask you for a name and a username and after this you get your **Auth Token**)
 * `/setcommands` (select your bot with the provided custon keyboard)
 * The camerapibot is programmed to give a response on the following commands (this is the configuration I gave to @BotFather, you can use it as it is):
  ```
  get_status - Returns the bot status
  get_image - Returns an image
  get_video - Returns a 10 second video
  ```
  * As the bot does not support inline queries right now, you might want to disable this feature by sending the command `/setnoinline` to @BotFather if it is enabled by default.

### Setting up the SQLite database
This step is pretty straight forward. The only thing you really need to do is to insert the Telegram chat_id's of the clients you want to have access to your camera into the table `allowed_user_ids`.
* If you are on Windows you might try out [SQLite Database Browser](http://sqlitebrowser.org/) to edit the file. This should be easy enough.
* On Unix systems you can use the sqlite3 package, which is available for almost every distribution. On a Debian/Ubuntu system you would run `sudo apt-get install sqlite3` for example.
  * Then you can open the database by typing `sqlite3 camerapibot_auth.db` while in the directory where the file is located.
  * Now you can insert the desired chat_id's by issueing the SQL statement `INSERT INTO allowed_user_ids VALUES (the_chat_id_you_want);` inside the sqlite3 interactive shell. Type `.quit` to end the sqlite3 session.

### _OPTIONAL_: Editing the launch.sh script
This step is only required when you want the bot to be started on system startup automatically. You need to change the following lines to fit your setup:
```bash
cd your/path/to/the/camerapibot/folder
python camerapibot.py YOUR_AUTH_TOKEN_HERE
```

## Running the bot
This is achieved by either running `python camerapibot.py YOUR_AUTH_TOKEN_HERE` where you put the files or setting up a cronjob to run it at system startup. Setting up the cronjob is easy as well, just follow these steps:
* Run `sudo crontab -e` (I am suggesting nano as editor, because it is very easy to use)
* Add the following line, adjusting the paths for your system: `@reboot sh /path/to/launch.sh >/path/to/desired/log/folder/cronlog 2>&1`. The `>/path/to/desired/log/folder/cronlog 2>&1` part is not necessary, but it helps to fix errors when they occur.

Now simply text your bot one of the defined commands in order to test your setup.
