The App "Moment" has a great feature that gets the total screen time for each App in your iPhone, using only a screenshot from "Battery Time" given by Apple. But it only (at least until the day I'm writing this) works with iPhones in English, and mine is in German. So this is the German version from Moment I tried to make with Tesseract (using pytesseract). 

You only need the "main.py" and "corretor.py" files. And you need to pip install pytesseract and cv2. 

To get the total screentime you'll need to take a daily photo from the Bildschirmzeit App (which is the Screentime App from Apple) like this: 

![alt text](https://imgur.com/18Xkp7A)

The script uses the words "Kategorien Einblenden" to locate itself, so you always need that in the printscreen. It does a montly analysis, so you get all of your screenshots and put in the same folder, together with the scripts. I name the folder "/photos", but you can change that name in the variable "folder_with_photos". You also need to set the month/year of the analysis, because Tesseract wasn't getting good results with the month name, so I decided to set it statically. 

And that's it, you'll get a .csv named "Times.csv" with all the data. I also made a very simple Jupyter Notebook to look through an example data with pandas, in case you want to see it's structure. 

The script doesn't get all the times correctly, so sometimes it makes estimates based on other apps usetime. But most of the time it gets everything right.