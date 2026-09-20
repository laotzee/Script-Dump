import asyncio
from camoufox import DefaultAddons
from datetime import datetime
from urllib.parse import urlparse
from camoufox.async_api import AsyncCamoufox
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

TLD_TO_COUNTRY = {
    ".at": "Austria",
    ".be": "Belgium",
    ".ch": "Switzerland",
    ".com": "Global/US",
    ".de": "Germany",
    ".dk": "Denmark",
    ".es": "Spain",
    ".fi": "Finland",
    ".fr": "France",
    ".it": "Italy",
    ".lu": "Luxembourg",
    ".nl": "Netherlands",
    ".no": "Norway",
    ".pl": "Poland",
    ".pt": "Portugal",
    ".se": "Sweden",
    ".uk": "United Kingdom",
}


def get_country_from_url(url: str) -> str:
    domain = urlparse(url).netloc
    tld = "." + domain.split(".")[-1]
    return TLD_TO_COUNTRY.get(tld, f"Unknown ({tld})")


# --- CHUNKING HELPER ---
def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i : i + size]


async def process_batch(links: list, results_by_country: dict, today_str: str):
    """Processes a small batch of links in a fresh browser context."""
    async with AsyncCamoufox(
        headless=True, exclude_addons=[DefaultAddons.UBO]
    ) as browser:
        for link in links:
            country = get_country_from_url(link)
            if country not in results_by_country:
                results_by_country[country] = []

            print(f"\nProcessing {link} ({country})...")

            page = await browser.new_page()
            page.on("pageerror", lambda err: print(f"  [Browser JS Error]: {err}"))

            try:
                await page.goto(link, wait_until="domcontentloaded", timeout=60000)
                page_num = 1

                while True:
                    print(f"  -> Scanning Page {page_num}...")
                    try:
                        await page.wait_for_selector("div#results", timeout=30000)
                    except PlaywrightTimeoutError:
                        break

                    job_divs = await page.locator("div#results div.job").all()

                    for job in job_divs:
                        try:
                            if not await job.is_visible():
                                continue
                            job_text = await job.inner_text()
                            if today_str in job_text:
                                h3_element = job.locator("h3")
                                job_title = (await h3_element.inner_text()).strip()

                                new_page = None
                                try:
                                    async with page.context.expect_page(
                                        timeout=5000
                                    ) as new_page_info:
                                        await h3_element.click(force=True)
                                    new_page = await new_page_info.value
                                except PlaywrightTimeoutError:
                                    swal_btn = page.locator(
                                        "button.swal-button--confirm.btn-ok"
                                    )
                                    if await swal_btn.is_visible():
                                        await swal_btn.click()
                                        await page.wait_for_timeout(1000)
                                        async with page.context.expect_page(
                                            timeout=15000
                                        ) as new_page_info:
                                            await h3_element.click(force=True)
                                        new_page = await new_page_info.value

                                if new_page:
                                    try:
                                        await new_page.wait_for_load_state(
                                            "domcontentloaded", timeout=30000
                                        )
                                        results_by_country[country].append(
                                            {"title": job_title, "url": new_page.url}
                                        )
                                        print(f"    -> Match found! {job_title}")
                                    finally:
                                        await new_page.close()
                        except Exception:
                            continue

                    next_button = page.locator("span.pagination a").first
                    if await next_button.count() > 0 and await next_button.is_visible():
                        await next_button.click()
                        await page.wait_for_load_state(
                            "domcontentloaded", timeout=30000
                        )
                        await page.wait_for_timeout(2000)
                        page_num += 1
                    else:
                        break
            except Exception as e:
                print(f"  -> Error processing {link}: {str(e)}")
            finally:
                try:
                    await page.close()
                except:
                    pass


async def process_all_links(target_links: list):
    today_str = datetime.now().strftime("%B %d").replace(" 0", " ")
    results_by_country = {}

    # Process 3 countries at a time
    for batch in chunk_list(target_links, 3):
        print(
            f"\n--- Starting new browser batch for: {[get_country_from_url(l) for l in batch]} ---"
        )
        await process_batch(batch, results_by_country, today_str)

    return results_by_country


def save_to_markdown(results: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        for country, jobs in results.items():
            f.write(f"# {country}\n\n")
            if not jobs:
                f.write("- No matches found for this region today.\n\n")
            else:
                for job in jobs:
                    f.write(f"- [{job['title']}]({job['url']})\n")
            f.write("\n")
    print(f"\nResults successfully saved to {filename}")


async def main():
    target_links = [
        "https://englishjobsearch.at/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.fr/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.be/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.de/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.es/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.lu/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.no/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.pt/jobs/junior?include=portuguese.spanish",
        "https://englishjobsearch.ch/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.dk/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.fi/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.it/jobs/junior?include=portuguese.spanish",
        "https://englishjobsearch.nl/jobs/junior?include=portuguese.spanish",
        "https://englishjobs.pl/jobs/junior?include=portuguese.spanish",
        "https://englishjobsearch.se/jobs/junior?include=portuguese.spanish",
    ]

    results = await process_all_links(target_links)
    date_formatted = datetime.now().strftime("%Y-%m-%d")
    save_to_markdown(results, f"jobs_{date_formatted}.md")


if __name__ == "__main__":
    asyncio.run(main())
