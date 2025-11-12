"""
JARVIS Web Controller - Chrome Browser Automation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import webbrowser
import urllib.parse

class WebController:
    def __init__(self):
        self.driver = None
        self.is_browser_open = False
        self.use_simple_mode = False  # Fallback to simple browser opening
        
    def open_chrome(self):
        """Open Chrome browser"""
        if self.is_browser_open:
            return True, "Chrome is already open, Sir."
        
        try:
            # Chrome options with stealth settings
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-browser-side-navigation")
            chrome_options.add_argument("--disable-gpu")
            
            # Setup ChromeDriver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set user agent to look more human
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            
            # Go to Google
            self.driver.get("https://www.google.com")
            self.is_browser_open = True
            
            return True, "Chrome opened and ready for search, Sir."
            
        except Exception as e:
            # Fallback to simple browser opening
            self.use_simple_mode = True
            return False, f"Selenium failed, switching to simple mode: {str(e)}"
    
    def search_google(self, query):
        """Search on Google"""
        # Try simple mode first if selenium failed
        if self.use_simple_mode:
            return self._simple_search(query)
        
        if not self.is_browser_open:
            success, message = self.open_chrome()
            if not success:
                return self._simple_search(query)
        
        try:
            # Find search box and enter query
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            return True, f"Searched for '{query}', Sir. Results are displayed."
            
        except Exception as e:
            # Fallback to simple search
            return self._simple_search(query)
    
    def _simple_search(self, query):
        """Simple search using default browser"""
        try:
            # Encode query for URL
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            # Open in default browser
            webbrowser.open(search_url)
            
            return True, f"Opened Google search for '{query}' in your default browser, Sir."
            
        except Exception as e:
            return False, f"Failed to open search: {str(e)}"
    
    def search_youtube(self, query):
        """Search YouTube for videos"""
        if self.use_simple_mode:
            return self._simple_youtube_search(query)
        
        if not self.is_browser_open:
            success, message = self.open_chrome()
            if not success:
                return self._simple_youtube_search(query)
        
        try:
            # Go to YouTube
            self.driver.get("https://www.youtube.com")
            
            # Find search box and enter query
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "contents"))
            )
            
            return True, f"YouTube search results for '{query}' are ready, Sir."
            
        except Exception as e:
            return self._simple_youtube_search(query)
    
    def _simple_youtube_search(self, query):
        """Simple YouTube search using default browser"""
        try:
            encoded_query = urllib.parse.quote_plus(query)
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(youtube_url)
            return True, f"Opened YouTube search for '{query}', Sir."
        except Exception as e:
            return False, f"Failed to open YouTube"
    
    def play_youtube_video(self, position=1):
        """Play YouTube video by position (1, 2, 3, etc.)"""
        if not self.is_browser_open or self.use_simple_mode:
            return False, "YouTube automation not available in simple mode, Sir."
        
        try:
            # Check if driver is still alive
            if not self.driver:
                self.is_browser_open = False
                return False, "Browser session lost. Please search again, Sir."
            
            # Find video thumbnails
            videos = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a#video-title"))
            )
            
            if len(videos) < position:
                return False, f"Only {len(videos)} videos found, Sir."
            
            # Click the specified video (position-1 for 0-based index)
            video_to_play = videos[position - 1]
            video_title = video_to_play.get_attribute("title")
            video_to_play.click()
            
            time.sleep(3)  # Wait for video to load
            
            return True, f"Playing video {position}: '{video_title}', Sir."
            
        except Exception as e:
            # Reset browser state on connection error
            if "connection" in str(e).lower() or "session" in str(e).lower():
                self.driver = None
                self.is_browser_open = False
                return False, "Browser session lost. Please search YouTube again, Sir."
            return False, f"Failed to play video: {str(e)}"
    
    def pause_video(self):
        """Pause/Play YouTube video"""
        if not self.is_browser_open or self.use_simple_mode:
            return False, "Video control not available in simple mode, Sir."
        
        try:
            # Try to find and click the video player to pause/play
            video_player = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "video"))
            )
            video_player.click()
            return True, "Video paused/resumed, Sir."
            
        except Exception as e:
            # Alternative: use spacebar key
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                ActionChains(self.driver).send_keys(' ').perform()
                return True, "Video paused/resumed, Sir."
            except:
                return False, "Could not control video playback, Sir."
    
    def stop_video(self):
        """Stop video and go back to search results"""
        if not self.is_browser_open or self.use_simple_mode:
            return False, "Video control not available in simple mode, Sir."
        
        try:
            # Go back to previous page (search results)
            self.driver.back()
            return True, "Stopped video and returned to search results, Sir."
        except Exception as e:
            return False, f"Failed to stop video: {str(e)}"
    
    def get_youtube_results(self, count=3):
        """Get YouTube search results"""
        if not self.is_browser_open or self.use_simple_mode:
            return False, "YouTube results not available in simple mode, Sir."
        
        try:
            # Find video titles
            videos = self.driver.find_elements(By.CSS_SELECTOR, "a#video-title")
            
            if not videos:
                return False, "No YouTube videos found, Sir."
            
            video_titles = []
            for i, video in enumerate(videos[:count]):
                title = video.get_attribute("title")
                if title:
                    video_titles.append(f"{i+1}. {title}")
            
            if video_titles:
                results_text = "Top YouTube videos: " + "; ".join(video_titles)
                return True, results_text
            else:
                return False, "Could not extract video titles, Sir."
                
        except Exception as e:
            return False, f"Failed to get YouTube results: {str(e)}"
    
    def get_search_results(self, count=3):
        """Get top search results"""
        if not self.is_browser_open:
            return False, "Chrome is not open, Sir."
        
        try:
            # Find search result elements
            results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
            
            if not results:
                return False, "No search results found, Sir."
            
            result_titles = []
            for i, result in enumerate(results[:count]):
                title = result.text.strip()
                if title:
                    result_titles.append(f"{i+1}. {title}")
            
            if result_titles:
                results_text = "Top search results: " + "; ".join(result_titles)
                return True, results_text
            else:
                return False, "Could not extract search results, Sir."
                
        except Exception as e:
            return False, f"Failed to get results: {str(e)}"
    
    def click_first_result(self):
        """Click the first search result"""
        if not self.is_browser_open:
            return False, "Chrome is not open, Sir."
        
        try:
            # Find and click first result
            first_result = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
            )
            
            first_result.click()
            time.sleep(2)  # Wait for page to load
            
            return True, "Opened the first search result, Sir."
            
        except Exception as e:
            return False, f"Failed to click result: {str(e)}"
    
    def go_back(self):
        """Go back to previous page"""
        if not self.is_browser_open:
            return False, "Chrome is not open, Sir."
        
        try:
            self.driver.back()
            return True, "Went back to previous page, Sir."
        except Exception as e:
            return False, f"Failed to go back: {str(e)}"
    
    def close_chrome(self):
        """Close Chrome browser"""
        if not self.is_browser_open:
            return False, "Chrome is not open, Sir."
        
        try:
            self.driver.quit()
            self.driver = None
            self.is_browser_open = False
            return True, "Chrome closed, Sir."
        except Exception as e:
            return False, f"Failed to close Chrome: {str(e)}"
            self.driver = None
            self.is_browser_open = False
            return True, "Chrome closed, Sir."
        except Exception as e:
            return False, f"Failed to close Chrome: {str(e)}"
    
    def get_page_title(self):
        """Get current page title"""
        if not self.is_browser_open:
            return False, "Chrome is not open, Sir."
        
        try:
            title = self.driver.title
            return True, f"Current page: {title}"
        except Exception as e:
            return False, f"Failed to get page title: {str(e)}"
    
    def open_youtube(self):
        """Open YouTube directly"""
        if self.use_simple_mode:
            try:
                webbrowser.open("https://www.youtube.com")
                return True, "Opened YouTube in your default browser, Sir."
            except Exception as e:
                return False, f"Failed to open YouTube: {str(e)}"
        
        if not self.is_browser_open:
            success, message = self.open_chrome()
            if not success:
                try:
                    webbrowser.open("https://www.youtube.com")
                    return True, "Opened YouTube in your default browser, Sir."
                except Exception as e:
                    return False, f"Failed to open YouTube: {str(e)}"
        
        try:
            self.driver.get("https://www.youtube.com")
            return True, "YouTube is ready, Sir."
        except Exception as e:
            return False, f"Failed to open YouTube: {str(e)}"

# Singleton instance
web_controller = WebController()