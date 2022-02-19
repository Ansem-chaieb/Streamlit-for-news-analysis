# DeepSearch-Labs-Test
[![Streamlit_App]][streamlit_App_url]

**1.** Scrape https://www.bbc.co.uk/news/science-environment-56837908 for all the news 
links. Include link, author, date, subject, text, and images. Make sure to introduce human delay. Put the data in a nice format.



## Instructions
**1 . Clone the repository:**
```bash
git clone https://github.com/Ansem-chaieb/DeepSearch-Labs-.git
cd DeepSearch-Labs-/
pip3 install -r requirements.txt
git clone https://github.com/thunlp/OpenNRE.git
```

#### Run project
 ```bash
  python3 main.py --scrape --preprocess --web_app
  ```

  The command comes with 3 flags:
  
  **--scrape:**  Scrape climate bbc data. 
  
  **--preprocess:**  Process collected data.
  
  **--web_app:**  Display streamlit web page.
  
  
  <!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Streamlit_App]: https://img.shields.io/badge/streamlit-%23FF4B4B.svg?&style=for-the-badge&logo=streamlit&logoColor=white
[streamlit_App_url]: https://share.streamlit.io/ansem-chaieb/streamlit-for-news-analysis/main/app.py
