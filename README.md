<h1 align="center">News Dashboard - Analyzing the world in real-time</h1>

[![Streamlit_App]][streamlit_App_url]

BBC News Dashboard - Analyzing the world in real-time, is a web-based application that provides users with up-to-date news and analysis from around the world. The dashboard gathers information from the BBC News website , and performs sentiment analysis, entity recognition, and topic modeling on the text. The results are displayed on an interactive dashboard that allows users to explore the news in different ways, such as by sentiment, topic, or entity.


<p align="center"><img src ="https://github.com/Ansem-chaieb/Streamlit-for-news-analysis/blob/main/images/bbc.gif" alt = "Bassmalah" class="center"></p>
  

## Instructions
**1 . Clone the repository:**
```bash
https://github.com/Ansem-chaieb/Streamlit-for-news-analysis.git
cd Streamlit-for-news-analysis/
pip3 install -r requirements.txt
```
If you want to try out the jupyter notebook for knowledge graphs, you should clone this fascinating project:
```
git clone https://github.com/thunlp/OpenNRE.git
```

**2 . Run project**
 ```bash
  python3 main.py --scrape --preprocess --web_app
  ```

  The command comes with 3 flags:
  
--scrape:  Scrape https://www.bbc.co.uk/news/science-environment-56837908 for all the news 
links. Include link, author, date, subject, text, and images. 
  
--preprocess:  Process collected data.

--web_app:  Display streamlit web page.
  
  
  <!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Streamlit_App]: https://img.shields.io/badge/streamlit-%23FF4B4B.svg?&style=for-the-badge&logo=streamlit&logoColor=white
[streamlit_App_url]: https://share.streamlit.io/ansem-chaieb/streamlit-for-news-analysis/main/app.py
