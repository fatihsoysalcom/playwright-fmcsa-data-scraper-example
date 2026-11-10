import asyncio
from playwright.async_api import async_playwright

async def scrape_fmcsa_data(company_name):
    """Scrapes FMCSA data for a given company name using Playwright."""
    async with async_playwright() as p:
        # Launch a browser instance (headless=True means it runs in the background)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to the FMCSA search page
            await page.goto("https://safer.fmcsa.dot.gov/CompanySearch/CompanySearch.aspx")

            # Fill in the company name in the search box
            # The selector might need to be updated if FMCSA changes their website structure
            await page.fill("input#query", company_name)

            # Click the search button
            await page.click("input#searchBtn")

            # Wait for the search results to load. 
            # We'll wait for a specific element that usually appears on the results page.
            # This selector is an example and might need adjustment.
            await page.wait_for_selector("table.table-bordered", timeout=30000) # Increased timeout

            # Extract relevant data from the results table
            # This part is highly dependent on the exact HTML structure of the results page.
            # We'll try to get the first result's company name and USDOT number as an example.
            company_info = {
                "company_name": None,
                "usdott_number": None
            }

            # Example selectors for the first row of the results table
            first_row_selector = "table.table-bordered tbody tr:nth-child(1)"
            
            # Check if the first row exists before trying to extract data
            if await page.query_selector(first_row_selector):
                company_info["company_name"] = await page.text_content(f"{first_row_selector} td:nth-child(1)")
                company_info["usdott_number"] = await page.text_content(f"{first_row_selector} td:nth-child(2)")

            return company_info

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            await browser.close()

async def main():
    # Example usage: Replace with a real company name you want to search
    company_to_search = "UPS"
    print(f"Searching FMCSA for: {company_to_search}")
    data = await scrape_fmcsa_data(company_to_search)

    if data:
        print("\n--- Search Results ---")
        print(f"Company Name: {data.get('company_name', 'N/A')}")
        print(f"USDOT Number: {data.get('usdott_number', 'N/A')}")
    else:
        print("Could not retrieve data.")

if __name__ == "__main__":
    # Ensure you have Playwright installed: pip install playwright
    # And have installed the browser binaries: playwright install
    asyncio.run(main())
