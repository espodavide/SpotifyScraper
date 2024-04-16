# SpotifyScraper
## Table of Contents
1. [Motivation](#motivation)
2. [Overview](#overview)
3. [Installation](#installation)
4. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Motivation
In a rapidly evolving technological landscape, job seekers face the challenge of deciphering market demands. My LinkedinScraper project aims to simplify this process by extracting key job offer keywords. By providing insights into market trends, I empower individuals to tailor their profiles effectively and navigate the job market with confidence.

## Overview

Welcome to the SpotifyScraper repository! This project is a personal endeavor aimed at create a simple web application that automate the boring task to maunally download your favourite music offline. This webb app allows the user with just simple copy and paste to have his/her favourite music online in a metter of minutes.
* Python
* Docker
* Selenium
* Flask

Overall the flow of the data is the following:

![Architecture](AirQaulityLight.png)


First the user is prompt to copy and paste the URL playlist, then in background a scraper will search the playlist. With webScraping techniques the script will download all your favourite song from the internet and starts a download of a zip file once completed.
## Installation

To get started with this project you need to have python and docker installed  and  you need to follow these simple steps:

1. **Clone the Repository:**
   
        git clone https://github.com/espodavide/SpotifyScraper.git
   
2. **Install Python Dependencies:**

       pip install -r requirements.txt

3. ** Create docker image docker **

       docker build . -t spotifyscraper 
   
4. **Run docker container:**

        docker run -p 8080:8080 spotifyscraper

Please note if yu decide to change the port of the docker remember to check for the file app_running.py, docker file and change the docker run command in accordingly
  
  


## Usage

Here are some instructions on how to use the project:

1. **Run the Application:**
   
Just visit localhost:8080 you fill find the interface. 


## Contributing

Since this project is meant for personal use, I'm solely responsible for its development and maintenance. However, if you have any suggestions, feedback, or spot any issues, feel free to open an issue or reach out to me directly.

## License
This project is licensed under the MIT licence. For more details, please refer to the [MIT](https://choosealicense.com/licenses/mit/) file.


