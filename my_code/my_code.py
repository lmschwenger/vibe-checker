import requests
import stanza
from bs4 import BeautifulSoup


class Analyzer:
    def __init__(self):
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment', tokenize_no_ssplit=True)

    def analyze_website(self, url):
        soup = self.fetch_website_content(url)
        sentences = []
        for para in soup.find_all("p"):
            txt = para.get_text()
            sentences += self.analyze_sentiment(txt)

        highlighted_soup = self.highlight_sentiments(soup, sentences)
        return str(highlighted_soup)

    def fetch_website_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def analyze_sentiment(self, text):
        doc = self.nlp(text)
        id_to_color = {0: 'negative', 1: 'neutral', 2: 'positive'}
        sentences = [(sentence.text, id_to_color[sentence.sentiment]) for sentence in doc.sentences]

        # Debug: Print the identified sentiments
        print("Sentiments Identified:")
        for sentence, color in sentences:
            print(f"Sentence: {sentence}\nSentiment: {color}")

        return sentences

    def highlight_sentiments(self, soup, sentences):
        for para in soup.find_all('p'):
            original_text = para.get_text()
            new_html = original_text
            for sentence, color in sentences:
                if sentence in original_text:
                    highlighted_sentence = f'<span class="{color}">{sentence}</span>'
                    new_html = new_html.replace(sentence, highlighted_sentence, 1)
            para.clear()
            para.append(BeautifulSoup(new_html, 'html.parser'))

        # Debug: Print the highlighted soup content
        print("Highlighted Soup Content:")
        print(soup.prettify())

        return soup
