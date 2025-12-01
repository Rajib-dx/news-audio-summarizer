import requests
from bs4 import BeautifulSoup
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
import pyttsx3

def extract_article_text(url):
    html = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0"
    }).text

    soup = BeautifulSoup(html, "lxml")

    article = soup.find("article")
    if not article:
        # fallback: biggest div
        divs = soup.find_all("div")
        article = max(divs, key=lambda d: len(d.get_text(strip=True)))

    # collect paragraphs
    paragraphs = [p.get_text(strip=True) for p in article.find_all("p")]
    return "\n\n".join(paragraphs)

# Text summariser

def summary(extract,count):
    parser = PlaintextParser.from_string(extract, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summarise = summarizer(parser.document, count)
    print("\n--- SUMMARY ---\n")
    summary_text = " ".join(str(s) for s in summarise)
    return summary_text

def voice_summary(text):
     engine = pyttsx3.init()
     engine.setProperty("rate", 165)
     engine.say(text)
     engine.runAndWait()





if __name__ == "__main__":

  url = "https://www.thedailyjagran.com/india/delhi-aqi-update-air-quality-slips-to-298-nears-very-poor-category-after-single-day-respite-check-area-wise-data-10283157"
  extract = extract_article_text(url)
  sum = int(input("In how many lines do you want the summary in? :"))
  final_text = summary(extract,sum)
  print(final_text)
  print("\n")
  print("\n")
  
  q = str(input("Do you want a audio summary of the news?(Type Y for yes and N for no): \n"))

  if q.lower() == "y":
      print("Playing Audio.......\n")
      voice_summary(final_text)


print("Thank you for using news summariser")





