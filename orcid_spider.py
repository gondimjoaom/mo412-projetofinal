import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy import signals
import sys, json
from collections import defaultdict
from tqdm import tqdm

class QuoteAPISpider(scrapy.Spider):
    name = "quotes_api"

    def __init__(self, urls=None, indexes=None, col=None, afilliation=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls or []
        self.indexes = indexes
        self.results = []  # store scraped data here
        self.col = col
        self.afilliation = afilliation
    
    def start_requests(self):
        # Pass the DataFrame index as meta
        for idx, url in zip(self.indexes, self.start_urls):
            # print(idx, url)
            if "orcid" not in url:
                yield scrapy.Request(url, callback=self.parse, meta={"row_idx": idx}, dont_filter=True)
            elif self.afilliation:
                url = url + "/affiliationGroups.json"
            else:
                url = url + "/public-record.json"
            yield scrapy.Request(url, callback=self.parse, meta={"row_idx": idx}, dont_filter=True)


    def parse(self, response):
        if not self.afilliation:
            if response.url == "https://quotes.toscrape.com/api/quotes?page=1": # sem orcid
                d = {f"{self.col}_nome": "sem orcid", f"{self.col}_país": "sem orcid", "row_idx": response.meta["row_idx"]}
            elif response.url == "https://quotes.toscrape.com/api/quotes?page=2": # não tem url
                d = {f"{self.col}_nome": pd.NA, f"{self.col}_país": pd.NA, "row_idx": response.meta["row_idx"]}
            else:
                data = json.loads(response.text)
                # print(data["countries"], response.url)
                d = {}
                d[f"{self.col}_nome"] = data["displayName"]
                if data["countries"]["addresses"] != []:
                    d[f"{self.col}_país"] = data["countries"]["addresses"][0]["countryName"]
                else:
                    d[f"{self.col}_país"] = "no info"
                if data["keyword"]["keywords"] != []:
                    j = 1
                    for keyword_value in data["keyword"]["keywords"]:
                        for k_string in keyword_value["content"].split(","):
                            d[f"{self.col}_keyword_{j}"] = k_string
                            j -=- 1
            # for quote in data.get("quotes", []):
            #     item = {
            #         "source_url": response.url,
            #         "text": quote["text"],
            #         "author": quote["author"]["name"],
            #         "tags": quote["tags"],
            #     }
            #     self.results.append(item)
            #     yield data
            d["row_idx"] = response.meta["row_idx"]
            # d["key"] = response.url.split("/public-record.json")[0]
            # d["url"] = response.url
            yield d
        else:
            if response.url == "https://quotes.toscrape.com/api/quotes?page=1": # sem orcid
                d = {f"{self.col}_filiação": "sem orcid", "row_idx": response.meta["row_idx"]}
            elif response.url == "https://quotes.toscrape.com/api/quotes?page=2": # não tem url
                d = {f"{self.col}_filiação": pd.NA, "row_idx": response.meta["row_idx"]}
            else:
                data = json.loads(response.text)
                d = {}
                # print(response.url)
                # print(data["affiliationGroups"]["EMPLOYMENT"][0]["affiliations"][0]["affiliationName"]["value"])
                if data["affiliationGroups"]["EMPLOYMENT"] != []:
                    d[f"{self.col}_filiação"] = data["affiliationGroups"]["EMPLOYMENT"][0]["affiliations"][0]["affiliationName"]["value"]
                else:
                    d[f"{self.col}_filiação"] = "no info"
            d["row_idx"] = response.meta["row_idx"]
            # d["key"] = response.url.split("/affiliationGroups.json")[0]
            yield d
def crawler_results(spider, item, response, **kwargs):
    results.append(item)

if __name__ == "__main__":
    # ✅ Pass your JSON API URLs as a list
    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    csv = sys.argv[1]
    # afilliation = sys.argv[2]
    data = pd.read_csv(csv)
    DEBUG = False
    DEBUG_Q = 10
    url_w_columns = [col for col in data.columns if ("orientador" in col or "avaliador" in col)]
    urls_columns = defaultdict(list)
    # https://orcid.org/0000-0002-6540-8686/public-record.json
    # print(data["orientador"].tolist())
    for col in url_w_columns:
        urls_columns[col] = data[col].values
        urls_columns[col] = ["https://quotes.toscrape.com/api/quotes?page=1" if url == "sem orcid" else url for url in urls_columns[col]]
        urls_columns[col] = ["https://quotes.toscrape.com/api/quotes?page=2" if url!=url else url for url in urls_columns[col]]
        urls_columns[col] = ["https://" + u if not u.startswith("http") else u for u in urls_columns[col]]
        # if not afilliation:
        #     urls_columns[col] = [url + "/public-record.json"  if "orcid.org" in url else url for url in urls_columns[col]]
        # else:
        #     urls_columns[col] = [url + "/affiliationGroups.json"  if "orcid.org" in url else url for url in urls_columns[col]]
        if DEBUG:
            urls_columns[col] = urls_columns[col][:DEBUG_Q]
    if DEBUG:
        indexes = data[col].index[:DEBUG_Q]
    else:
        indexes = data[col].index
    col = "orientador"
    # print(len(urls_columns["orientador"]))
    results = []

    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",  # keep logs clean
    })

    # spider = QuoteAPISpider(urls=urls_columns["orientador"])
    col = "orientador"
    # print(len(urls_columns[col]))
    for afilliation in [True, False]:
        for col in tqdm(url_w_columns):
            process.crawl(QuoteAPISpider, urls=urls_columns[col], indexes=indexes, col=col, afilliation=afilliation)
    process.start()  # blocks until crawl finishes

    # After crawling, access results
    # print(results)
# 
    results_filiacao = []
    results_record = []
    for result in results:
        for k, v in result.items():
            if k == "row_idx": pass
            if k not in data.columns:
                data[k] = ""
            data.at[result["row_idx"], k] = v
    # print(results_record[0], len(results_filiacao))
    # df_filiacao = pd.DataFrame(results_filiacao)
    # print(len(results_filiacao), len(results_record))
    # df_record = pd.DataFrame(results_record)
    # print(df_record["row_idx"].unique())
    # df = pd.DataFrame(results)
    # data.to_csv("test.csv")
    # df_filiacao.set_index("row_idx", inplace=True)
    # df_filiacao.sort_index(inplace=True)
    # df_record.set_index("row_idx", inplace=True)
    # df_record.sort_index(inplace=True)
    # print(df)
    # data = pd.merge(data, df_filiacao, left_index=True, right_index=True)
    # data = pd.merge(data, df_record, left_index=True, right_index=True)
    data.to_csv(f"final_{csv}")