# DeepSearch-Labs-Test
[![Streamlit_App]][streamlit_App_url]

**1.** Scrape https://www.bbc.co.uk/news/science-environment-56837908 for all the news 
links. Include link, author, date, subject, text, and images. Make sure to introduce human delay. Put the data in a nice format.

**2.** Create a web-based application including a dynamic graph (knowledge graph if you can) that is adjustable on the date of the data you collected. 
The graph should show sentiment analysis of articles over time and named-entities associated.there should be drop down menus to select different categories or NERs or whatever you decide.
Recommend a few papers that are doing something interesting related to what you have achieved and how you would go about implementing them.

**Bonus point 1:** When you click on a named entity, category, or your choice of insight, 
you should get descriptions associated to that NER, etc.

**Bonus point 2:** Implementing one of the methodologies of the papers you have recommended.

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
[streamlit_App_url]: https://share.streamlit.io/ansem-chaieb/deepsearch-labs-/main/app.py
