# main.py
import asyncio
from playwright.async_api import async_playwright
import random, time

WATI_INBOX = "https://live.wati.io/1037246/teamInbox/68ffc1470d6e9f9ca7a0eca2?filter={\"filterType\":13,\"channelType\":0}"
FLOW_ID = "flow-nav-68ff67df4f393f0757f108d8"  # Ads (CTWA)

async def run_wati_bot():
    print("🌐 Launching WATI Automation (24/7 Mode)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="storageState.json")
        page = await context.new_page()

        await page.goto(WATI_INBOX)
        await page.wait_for_timeout(8000)
        print("✅ Logged in to WATI Inbox")

        while True:
            try:
                # Get unread chats count
                unread_count = await page.evaluate("""
                    () => {
                        let e = document.querySelector('[data-testid="teamInbox-leftSide-filterBar-filter-dropdown-unreadCount"]');
                        if (!e) return 0;
                        let s = e.innerText || '';
                        let n = s.replace(/\\D/g, '');
                        return n ? parseInt(n, 10) : 0;
                    }
                """)
                print(f"📬 Unread Count: {unread_count}")

                if unread_count > 0:
                    # Click first unread chat
                    chat_clicked = await page.evaluate("""
                        () => {
                            let badge = document.querySelector('.conversation-item__unread-count, .conversation-item__unread');
                            if (!badge) return false;
                            let link = badge.closest('a[data-testid="teamInbox-leftSide-conversationItem"]') ||
                                       badge.parentElement.querySelector('a[data-testid="teamInbox-leftSide-conversationItem"]');
                            if (link) { link.click(); return true; }
                            return false;
                        }
                    """)

                    if chat_clicked:
                        print("💬 Opened unread chat...")
                        await page.wait_for_timeout(2000)

                        # Click bot icon
                        await page.click("css=span.sc-ekrnMf.ldDJbr.chat-input__icon-option > svg")
                        await page.wait_for_timeout(1500)

                        # Click Ads (CTWA) flow
                        await page.click(f"//*[@id='{FLOW_ID}']")
                        print("🤖 Triggered Ads (CTWA) flow successfully!")

                        # Random delay between 2–5 seconds
                        delay = random.randint(2, 5)
                        print(f"⏳ Waiting {delay}s before next loop...")
                        await page.wait_for_timeout(delay * 1000)
                    else:
                        print("⚠️ No clickable unread chat found.")
                else:
                    wait_min = round(random.uniform(3, 5), 2)
                    print(f"😴 No new chats. Sleeping {wait_min} minutes...")
                    await asyncio.sleep(wait_min * 60)

            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(10)

        await browser.close()

asyncio.run(run_wati_bot())
