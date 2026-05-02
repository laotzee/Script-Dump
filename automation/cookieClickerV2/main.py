import asyncio
from camoufox.async_api import AsyncCamoufox
from camoufox import DefaultAddons


async def run():
    async with AsyncCamoufox(
        headless=False,
        humanize=False,
        exclude_addons=[DefaultAddons.UBO],
    ) as browser:
        page = await browser.new_page()

        print("Opening Cookie Clicker...")
        await page.goto("https://orteil.dashnet.org/cookieclicker/")

        try:
            await page.wait_for_selector("#langSelect-EN", timeout=60000)
            await asyncio.sleep(2)
            await page.click("#langSelect-EN")

            print("Successfully entered the game.")

            while True:
                try:
                    await page.evaluate("""
                        const cookie = document.querySelector("#bigCookie");
                        if (cookie) cookie.click();

                        const shimmer = document.querySelector("#shimmers .shimmer");
                        if (shimmer) shimmer.click();

                        const excludedIds = ['74', '85'];

                        const upgrades = Array.from(document.querySelectorAll('.storeSection.upgradeBox .crate')).filter(el => !excludedIds.includes(el.getAttribute('data-id')));
                        if (upgrades.length > 0) {
                            upgrades[upgrades.length - 1].click();
                        }

                        const products = document.querySelectorAll('.product.unlocked');
                        const lastElements = Array.from(products).slice(-2);
                        const enabledLastElements = lastElements.filter(el => el.classList.contains('enabled'));

                        if (enabledLastElements.length > 0) enabledLastElements[enabledLastElements.length - 1].click();
                    """)

                except Exception as e:
                    print(f"Navigation or crash detected, retrying... {e}")
                    await asyncio.sleep(0.5)
                    continue

        except Exception as error:
            print("Error outsite the loop")
            print(f"Workflow error: {error}")


if __name__ == "__main__":
    asyncio.run(run())
