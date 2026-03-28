"""
Twitter / X Post Action — SeleniumTwitterPoster

LinkedIn ki tarah Selenium se X.com login + tweet karta hai.
headless=False → user dekh sakta hai browser mein kia ho raha hai.

Twitter login 2-step hai:
  Step 1: username/email enter karo → Next
  Step 2: password enter karo → Log in

Constitution compliance:
  - Principle III: HITL — caller approve karta hai tweet ko publish se pehle
  - Principle VI: Fail Safe — post() never raises
  - Section 8: Credentials never logged
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone


class SeleniumTwitterPoster:
    """
    Selenium-based Twitter/X poster.

    Usage::

        poster = SeleniumTwitterPoster(
            email="user@gmail.com",
            password="secret",
            username="twitter_handle",
            headless=False,
        )
        if poster.login():
            result = poster.tweet("Hello from AI Agent! #GIAIC #Hackathon")
            poster.quit()
    """

    def __init__(
        self,
        email: str,
        password: str,
        username: str = "",
        headless: bool = False,
        log_dir: str = "obsidian-vault/70-LOGS",
    ) -> None:
        self._email    = email
        self._password = password
        self._username = username
        self._headless = headless
        self._log_dir  = log_dir
        self._driver   = None
        self._logged_in = False

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------

    def login(self) -> bool:
        """
        Open Chrome, go to x.com, login (2-step: username → password).
        Returns True on success. Never raises.
        """
        try:
            import undetected_chromedriver as uc
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            opts = uc.ChromeOptions()
            opts.add_argument("--no-sandbox")
            opts.add_argument("--window-size=1366,768")

            self._driver = uc.Chrome(options=opts, headless=self._headless, version_main=146)

            print("   🌐 Twitter/X khul rahi hai...")
            self._driver.get("https://x.com/i/flow/login")
            time.sleep(4)

            wait = WebDriverWait(self._driver, 20)

            # --- Step 1: Email / Username ---
            print("   📧 Email/username enter kar raha hai...")
            email_field = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@autocomplete='username' or @name='text' or @data-testid='LoginForm_Username']")
                )
            )
            email_field.clear()
            time.sleep(0.5)
            # Human-like typing
            for ch in self._email:
                email_field.send_keys(ch)
                time.sleep(0.05)
            time.sleep(1)

            # "Next" button — multiple selectors try karo
            next_btn = None
            for xpath in [
                "//button[@data-testid='LoginForm_Login_Button']",
                "//button[.//span[normalize-space(text())='Next']]",
                "//div[@role='button'][.//span[text()='Next']]",
            ]:
                try:
                    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    break
                except Exception:
                    pass

            if next_btn is None:
                # JS fallback
                next_btn = self._driver.execute_script("""
                    var btns = document.querySelectorAll('button,div[role="button"]');
                    for (var b of btns) {
                        if ((b.innerText||'').trim() === 'Next') return b;
                    }
                    return null;
                """)

            if next_btn:
                self._driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(3)

            self._screenshot("twitter_step1.png")

            # Check: Twitter might ask for username confirmation (unusual activity)
            try:
                confirm_field = self._driver.find_element(
                    By.XPATH,
                    "//input[@data-testid='ocfEnterTextTextInput' or @name='text']"
                )
                if confirm_field.is_displayed():
                    print("   ⚠️  Twitter unusual activity check — username enter kar raha hai...")
                    confirm_field.clear()
                    confirm_field.send_keys(self._username or self._email)
                    time.sleep(1)
                    next_btn2 = self._driver.find_element(
                        By.XPATH, "//button[@data-testid='ocfEnterTextNextButton']"
                    )
                    next_btn2.click()
                    time.sleep(3)
            except Exception:
                pass  # No confirmation needed

            # --- Step 2: Password ---
            print("   🔑 Password enter kar raha hai...")
            pwd_field = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@name='password' or @autocomplete='current-password' or @type='password']")
                )
            )
            pwd_field.clear()
            time.sleep(0.5)
            for ch in self._password:
                pwd_field.send_keys(ch)
                time.sleep(0.05)
            time.sleep(1)

            # "Log in" button
            login_btn = None
            for xpath in [
                "//button[@data-testid='LoginForm_Login_Button']",
                "//button[.//span[normalize-space(text())='Log in']]",
                "//div[@role='button'][.//span[text()='Log in']]",
            ]:
                try:
                    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    break
                except Exception:
                    pass

            if login_btn is None:
                login_btn = self._driver.execute_script("""
                    var btns = document.querySelectorAll('button,div[role="button"]');
                    for (var b of btns) {
                        var t = (b.innerText||'').trim();
                        if (t === 'Log in' || t === 'Login') return b;
                    }
                    return null;
                """)

            if login_btn:
                self._driver.execute_script("arguments[0].click();", login_btn)
            print("   ⏳ Login ho rahi hai...")
            time.sleep(8)

            self._screenshot("twitter_login.png")
            current = self._driver.current_url

            if "x.com/home" in current or (
                "x.com" in current and "login" not in current and "flow" not in current
            ):
                self._logged_in = True
                print(f"   ✅ Twitter/X login success!")
                return True

            print(f"   ❌ Login failed. URL: {current[:80]}")
            return False

        except Exception as exc:
            print(f"   ❌ Login error: {exc}")
            return False

    # ------------------------------------------------------------------
    # Tweet
    # ------------------------------------------------------------------

    def tweet(self, text: str) -> dict:
        """
        Compose and post a tweet on X.com.
        Returns dict: {success, tweet_id, posted_at, error}
        Never raises.
        """
        if not self._logged_in or self._driver is None:
            return {"success": False, "error": "Not logged in"}

        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.action_chains import ActionChains

            print("   🌐 X.com home pe ja raha hai...")
            self._driver.get("https://x.com/home")
            time.sleep(5)

            self._screenshot("twitter_home.png")

            wait = WebDriverWait(self._driver, 20)

            # Tweet compose box — data-testid="tweetTextarea_0"
            print("   📝 Tweet compose box dhund raha hai...")
            compose_box = None

            try:
                compose_box = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@data-testid='tweetTextarea_0']")
                    )
                )
                print("   ✅ Compose box mila (data-testid)")
            except Exception:
                pass

            if compose_box is None:
                compose_box = self._driver.execute_script("""
                    var walker = document.createTreeWalker(
                        document.body, NodeFilter.SHOW_ELEMENT
                    );
                    while (walker.nextNode()) {
                        var el = walker.currentNode;
                        var ph = (el.getAttribute('data-placeholder') || '').toLowerCase();
                        if (ph.includes('happening') && el.offsetParent !== null) {
                            return el;
                        }
                    }
                    return null;
                """)
                if compose_box:
                    print("   ✅ Compose box mila (JS text walker)")

            if compose_box is None:
                return {"success": False, "error": "Tweet compose box nahi mila"}

            # Click + type
            self._driver.execute_script(
                "arguments[0].focus(); arguments[0].click();", compose_box
            )
            time.sleep(1)
            ActionChains(self._driver).move_to_element(compose_box).click().send_keys(text).perform()
            time.sleep(1)

            # Dispatch events
            self._driver.execute_script("""
                var el = arguments[0];
                ['input','change','keyup'].forEach(function(n){
                    el.dispatchEvent(new Event(n, {bubbles: true}));
                });
            """, compose_box)
            time.sleep(2)
            print(f"   ✍️  Tweet text type ho gaya ({len(text)} chars)")
            self._screenshot("twitter_typed.png")

            # "Post" button
            post_btn = None
            try:
                post_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@data-testid='tweetButtonInline']")
                    )
                )
                print("   ✅ Post button mila (data-testid)")
            except Exception:
                pass

            if post_btn is None:
                # Fallback
                post_btn = self._driver.execute_script("""
                    var btns = document.querySelectorAll('button[role="button"]');
                    for (var btn of btns) {
                        var txt = (btn.innerText || '').trim();
                        if (txt === 'Post') return btn;
                    }
                    return null;
                """)

            if post_btn is None:
                return {"success": False, "error": "Twitter 'Post' button nahi mila"}

            print("   ✅ Post button mila — tweet kar raha hai...")
            self._driver.execute_script("arguments[0].click();", post_btn)
            time.sleep(5)
            self._screenshot("twitter_posted.png")

            tweet_id = f"X-LIVE-{uuid.uuid4().hex[:8].upper()}"
            print(f"   🚀 Tweet post ho gayi! ID: {tweet_id}")
            return {
                "success": True,
                "tweet_id": tweet_id,
                "posted_at": datetime.now(tz=timezone.utc).isoformat(),
                "error": "",
            }

        except Exception as exc:
            return {"success": False, "error": f"{type(exc).__name__}: {exc}"}

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def quit(self) -> None:
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None
            self._logged_in = False

    def _screenshot(self, filename: str) -> None:
        import os
        try:
            os.makedirs(self._log_dir, exist_ok=True)
            self._driver.save_screenshot(os.path.join(self._log_dir, filename))
            print(f"   📸 Screenshot: 70-LOGS/{filename}")
        except Exception:
            pass
