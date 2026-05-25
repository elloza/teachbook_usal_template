import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🎭 Launching browser...")
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        url = "http://127.0.0.1:8000/en/intro.html"
        print(f"🌍 Navigating to {url}...")
        try:
            await page.goto(url, timeout=10000)
        except Exception as e:
            print(f"❌ Could not connect to {url}. Is the preview server running?")
            print(e)
            await browser.close()
            return

        # Check initial state
        checkbox = await page.wait_for_selector("#pst-primary-sidebar-checkbox", state="attached")
        initial_checked = await checkbox.is_checked()
        print(f"🔒 Initial Sidebar Checkbox State: {initial_checked}")

        # Find the toggle button
        # Note: Our fix removes the 'for' attribute, so we look for the class
        print("👆 Looking for sidebar toggle...")
        toggle = await page.wait_for_selector(".primary-toggle")
        
        # Click it
        print("🖱️ Clicking toggle...")
        await toggle.click()
        
        # Wait a bit for JS to handle it
        await page.wait_for_timeout(500)
        
        # Check new state
        new_checked = await checkbox.is_checked()
        print(f"🔓 Post-Click Sidebar Checkbox State: {new_checked}")
        
        if initial_checked != new_checked:
            print("✅ SUCCESS: Sidebar toggled successfully!")
        else:
            print("❌ FAILURE: Sidebar state did not change.")

        await page.screenshot(path="sidebar_verification.png")
        print("📸 Screenshot saved to sidebar_verification.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
