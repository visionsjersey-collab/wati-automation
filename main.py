import asyncio
import os
from aiohttp import web
from playwright.async_api import async_playwright
import random
import time

WATI_URL = "https://live.wati.io/1037246/teamInbox/68ffc1470d6e9f9ca7a0eca2?filter={%22filterType%22:13,%22channelType%22:0}"

async def run_wati_bot():
    print("🌐 Launching WATI automation...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="storageState.json")
        page = await context.new_page()
        await page.goto(WATI_URL)
        print("✅ WATI Inbox loaded")

        while True:
            try:
                # Check for unread badges
                unread = await page.query_selector_all("div.conversation-item__unread-count, div[class*='unread']")
                count = len(unread)
                print(f"📬 Unread count: {count}")

                if count > 0:
                    for badge in unread:
                        try:
                            parent = await badge.evaluate_handle("el => el.closest('a')")
                            if parent:
                                await parent.click()
                                print("💬 Clicked unread chat")
                                await asyncio.sleep(3)
                                await page.click("text=Ads (CTWA)")
                                print("🤖 Triggered Ads (CTWA) flow")
                                await asyncio.sleep(random.uniform(2, 5))
                        except Exception as e:
                            print("⚠️ Error in clicking unread chat:", e)
                else:
                    print("😴 No new chats. Sleeping 3-5 mins...")
                    await asyncio.sleep(random.uniform(180, 300))

            except Exception as e:
                print("❌ Error in main loop:", e)
                await asyncio.sleep(10)

async def start_web_server():
    async def handle(request):
        return web.Response(text="✅ WATI Bot is running!")
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌍 Web server running on port {port}")

async def main():
    await asyncio.gather(run_wati_bot(), start_web_server())

if __name__ == "__main__":
    asyncio.run(main())
