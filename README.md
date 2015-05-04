![Vest logo](http://pr4.me/css/images/vest_transparent.png)

##Overview

A Facebook friend network building tool, an RCOS project at RPI

Vest allows for easy data scraping from friend pages with analysis built in. This project was inspired by studies that found that while violent crime may be prevelent in some areas, most of the violence is contained within a smaller group of individuals. The overall goal of Vest is to take an input of violent crime victims and output the ids of the users most closely connected to them.

The project employs the selenium webdriver running a firefox browser. Data is saved into a sqlite3 database and analyzed using simple set interactions.

Check out the articles that inspired out project:

[Chicago Gun Violence: Big Numbers, But a Surprisingly Small Network](http://www.chicagomag.com/city-life/April-2014/Chicago-Gun-Violence-Big-Numbers-But-a-Surprisingly-Small-Network/)

[Study finds social networks are key to city violence](http://news.yale.edu/2013/11/14/study-finds-social-networks-are-key-city-violence)



##Dependencies
- Python3
- Sqlite3
- Selenium
- Firefox

##Usage

    $ git clone https://github.com/emmetthitz/Vest.git
    $ cd Vest/bin/
    $ python3 main.py 

