import json
import math
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class Scraper:
    _driver_path = None

    @classmethod
    def get_driver_path(cls):
        """
        Get the path to the GeckoDriver executable, installing it only if necessary.
        Caches the path for future use.

        Returns:
            str: Path to the GeckoDriver executable
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "geckodriver")

    @classmethod
    def get_all_rules_metadata_path(cls) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "scraped", "rules-metadata.json")

    @classmethod
    def get_all_rules_data_path(cls) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "scraped", "rules-data.json")

    def __init__(self, base_url="https://qavanin.ir", wait_time=10):
        self.base_url = base_url
        self.wait_time = wait_time
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
        )
        options.add_argument("--accept-language=en-US")
        self.driver = webdriver.Firefox(
            service=FirefoxService(self.get_driver_path()),
            options=options,
        )

    def normalize_text(self, text: str) -> str:
        """
        Normalize text by removing redundant characters and standardizing whitespace.

        Args:
            text (str): The text to normalize

        Returns:
            str: Normalized text
        """
        text = text.lower()
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.replace("\u200f", "")
        text = text.replace("\u200e", "")
        text = text.replace("\u200c", " ")
        text = text.strip()
        return text

    def get_page_with_selenium(self, url):
        """
        Uses Selenium to load a page with JavaScript protection and returns the page source
        after the JavaScript executes and the page reloads.

        Args:
            url (str): The URL to scrape
            wait_time (int): How many seconds to wait for the page to fully load

        Returns:
            BeautifulSoup object
        """

        try:
            # Navigate to the URL & wait for the page to load
            self.driver.get(url)
            time.sleep(self.wait_time)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            return soup
        except Exception as e:
            print(f"Error: {e}")
            return None

    def extract_elements(self, soup: BeautifulSoup) -> dict:
        """
        Extract useful elements from the BeautifulSoup object

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the page

        Returns:
            dict: A dictionary of extracted elements
        """
        elements = {}
        if soup is None:
            return elements
        elements["title"] = (
            self.normalize_text(soup.title.text) if soup.title else "No title found"
        )
        elements["headings"] = [
            self.normalize_text(h.text)
            for h in soup.find_all(["h1", "h2", "h3"])
            if h.text.strip()
        ]
        elements["paragraphs"] = [
            self.normalize_text(p.text) for p in soup.find_all("p") if p.text.strip()
        ]
        return elements

    def get_rule_text_from_link(self, link: str) -> str:
        soup = self.get_page_with_selenium(link)
        elements = self.extract_elements(soup)
        paragraphs = elements.get("paragraphs", [])
        return " ".join(paragraphs[1:])

    def extract_rules_data_from_table(self, soup: BeautifulSoup) -> list[dict]:
        table = soup.find("table", class_="table-striped")
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
        rules = []
        for row in rows:
            cells = row.find_all("td")
            title = self.normalize_text(cells[1].text)
            approval_date = self.normalize_text(cells[2].text)
            approval_authority = self.normalize_text(cells[3].text)
            link = self.base_url + cells[1].find("a")["href"].strip()
            rules.append(
                {
                    "title": title,
                    "approval_date": approval_date,
                    "approval_authority": approval_authority,
                    "link": link,
                }
            )
        return rules

    def extract_all_rules_metadata(
        self, batch_size: int = 500, total_count: int = 162302
    ):
        all_rules_metadata = []
        total_pages = total_count // batch_size + 1

        print(f"Starting to extract data from {total_pages} pages")
        start_time = time.time()

        for page in range(1, total_pages + 1):
            page_start_time = time.time()
            print(f"Processing page {page}/{total_pages} ...")

            all_rules_url = f"https://qavanin.ir/?CAPTION=&Zone=&IsTitleSearch=true&IsTitleSearch=false&IsTextSearch=false&_isLaw=false&_isRegulation=false&_IsVote=false&_isOpenion=false&SeachTextType=3&fromApproveDate=&APPROVEDATE=&IsTitleSubject=False&IsMain=&COMMANDNO=&fromCommandDate=&COMMANDDATE=&NEWSPAPERNO=&fromNewspaperDate=&NEWSPAPERDATE=&SortColumn=APPROVEDATE&SortDesc=True&Report_ID=&PageNumber={page}&page={page}&size={batch_size}&txtZone=&txtSubjects=&txtExecutors=&txtApprovers=&txtLawStatus=&txtLawTypes="
            soup = self.get_page_with_selenium(all_rules_url)
            if soup:
                rules_data = self.extract_rules_data_from_table(soup)
                all_rules_metadata.extend(rules_data)

                page_time = time.time() - page_start_time
                print(f"  Page {page} completed in {page_time:.2f} seconds")
                print(f"  Total rules collected so far: {len(all_rules_metadata)}")
            else:
                print(f"  Failed to extract data from page {page}")

            elapsed_time = time.time() - start_time
            estimated_total_time = (elapsed_time / page) * total_pages
            remaining_time = estimated_total_time - elapsed_time

            print(f"  Elapsed time: {elapsed_time:.2f} seconds")
            print(
                f"  Estimated time remaining: {remaining_time:.2f} seconds ({remaining_time/60:.2f} minutes)"
            )
            print("-" * 80)

        total_time = time.time() - start_time
        print(
            f"Extraction completed in {total_time:.2f} seconds ({total_time/60:.2f} minutes)"
        )
        print(f"Total rules collected: {len(all_rules_metadata)}")

        return all_rules_metadata


def get_id_from_link(link: str) -> str:
    return link.split("=")[-1]


def get_rules_data(rules_to_scrape_df: pd.DataFrame) -> list[dict]:
    scraper = Scraper(wait_time=8)
    scraped_rules = []
    total_in_batch = len(rules_to_scrape_df)
    quarter_of_batch = total_in_batch // 4

    print(f"Started processing batch with {total_in_batch} rules")
    start_time = time.time()

    for i in range(len(rules_to_scrape_df)):
        link = rules_to_scrape_df.iloc[i]["link"]
        rule_text = scraper.get_rule_text_from_link(link)
        scraped_rules.append(
            {
                "id": get_id_from_link(link),
                "title": rules_to_scrape_df.iloc[i]["title"],
                "date": rules_to_scrape_df.iloc[i]["approval_date"],
                "authority": rules_to_scrape_df.iloc[i]["approval_authority"],
                "link": link,
                "text": rule_text,
            }
        )

        if (i + 1) % quarter_of_batch == 0:
            elapsed_time = time.time() - start_time
            avg_time_per_rule = elapsed_time / (i + 1)
            remaining_time = avg_time_per_rule * (total_in_batch - i - 1)
            print(
                f"  Batch progress: {i+1}/{total_in_batch} rules ({((i+1)/total_in_batch*100):.1f}%) - ETA: {remaining_time:.1f}s"
            )

    scraper.driver.quit()
    print(
        f"Completed batch of {total_in_batch} rules in {time.time() - start_time:.1f}s"
    )
    return scraped_rules


def save_rules_data(
    rules_df: pd.DataFrame, batch_size: int = 100, max_workers: int = 10
):
    """
    Process and save rules data to a JSON file using ThreadPoolExecutor for parallel processing.

    Args:
        rules_df (pd.DataFrame): DataFrame containing rules metadata to scrape
        batch_size (int, optional): Size of each batch of rules to process. Defaults to 100.
        max_workers (int, optional): Maximum number of worker threads to use. Defaults to 10.
    """
    total_rules = len(rules_df)
    total_batches = math.ceil(total_rules / batch_size)
    all_rules_data = []
    with open(Scraper.get_all_rules_data_path(), "r", encoding="utf-8") as f:
        all_rules_data = json.load(f)

    # Create batches of rules
    batches = []
    for batch_idx in range(total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, total_rules)
        batches.append(rules_df.iloc[start_idx:end_idx])

    print(
        f"Starting to process {total_rules} rules in {total_batches} batches with {max_workers} parallel workers"
    )
    overall_start = time.time()

    # Process batches in chunks to control memory usage
    for chunk_idx in range(0, len(batches), max_workers):
        chunk_start_time = time.time()
        batch_chunk = batches[chunk_idx : chunk_idx + max_workers]
        current_chunk_num = chunk_idx // max_workers + 1
        total_chunks = math.ceil(len(batches) / max_workers)

        print(
            f"Processing batch chunk {current_chunk_num}/{total_chunks}, with {len(batch_chunk)} batches..."
        )

        # Use ThreadPoolExecutor to process batches in parallel
        with ThreadPoolExecutor(max_workers=len(batch_chunk)) as executor:
            # Submit all batches to the executor
            future_to_batch = {
                executor.submit(get_rules_data, batch): batch for batch in batch_chunk
            }

            # Collect results as they complete
            chunk_results = []
            for future in future_to_batch:
                try:
                    result = future.result()
                    chunk_results.extend(result)
                except Exception as exc:
                    print(f"Batch generated an exception: {exc}")

        # Add results from this chunk to overall results
        all_rules_data.extend(chunk_results)

        # Save intermediate results
        with open(Scraper.get_all_rules_data_path(), "w", encoding="utf-8") as f:
            json.dump(all_rules_data, f, indent=4, ensure_ascii=False)

        # Calculate and display progress info
        chunk_time = time.time() - chunk_start_time
        avg_time_per_chunk = (time.time() - overall_start) / current_chunk_num
        eta = avg_time_per_chunk * (total_chunks - current_chunk_num)

        processed_batches = min(chunk_idx + len(batch_chunk), total_batches)
        print(
            f"Processed {processed_batches}/{total_batches} batches, total rules so far: {len(all_rules_data)}/{total_rules}"
        )
        print(
            f"Chunk {current_chunk_num} completed in {chunk_time:.1f}s ({chunk_time/60:.1f} minutes) - Overall ETA: {eta:.1f}s ({eta/60:.1f} minutes)"
        )
        print("-" * 80)

    # Final timing information
    total_time = time.time() - overall_start
    print(
        f"Completed processing {len(all_rules_data)} rules in {total_time:.1f}s ({total_time/60:.1f} minutes)"
    )

    return all_rules_data


def save_all_rules_metadata():
    scraper = Scraper(wait_time=10)
    all_rules_metadata = scraper.extract_all_rules_metadata()
    print(f"scraped {len(all_rules_metadata)} rules")
    with open(Scraper.get_all_rules_metadata_path(), "w", encoding="utf-8") as f:
        json.dump(all_rules_metadata, f, indent=4, ensure_ascii=False)


def get_all_rules_metadata_df() -> pd.DataFrame:
    with open(Scraper.get_all_rules_metadata_path(), "r", encoding="utf-8") as f:
        all_rules_metadata = json.load(f)
    return pd.DataFrame(all_rules_metadata)


if __name__ == "__main__":
    df = get_all_rules_metadata_df()
    rdf = df[df["is_related"] == "True"]
    # save_rules_data(rdf, batch_size=10, max_workers=16)
