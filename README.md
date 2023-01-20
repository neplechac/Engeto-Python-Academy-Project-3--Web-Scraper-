# **ENGETO Python Academy**
## **Project 3 – Web Scraper**
Write a script that **downloads election results** of every municipality in chosen district **into csv file.**

[At this page](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ), you first have to choose the district by the X key in the column *Výběr obce* (on the right). So for when you choose i.e. [district Příbram](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2111) you then have to choose the municipality. This time you choose by the number of the municipality (column *číslo* on the left). So, i.e. [Dobříš](https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=540111&xvyber=2111) will have the number 540111.

The header of the csv file should have the following: municipality code, name of location, voters in the list, distributed voting envelopes, valid votes, candidate parties. Each row of the csv file will then represent individual municipalities. So an example of Hradec Králové would look like this:

![Output table](https://i.ibb.co/LPdzwMN/epa-p3-img.png)

### Requirements
Required Python packages are listed in `requirements.txt` file.

