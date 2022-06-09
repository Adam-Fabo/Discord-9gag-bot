
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import discord
import io
import aiohttp




class Downloader:



    def __init__(self):

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        s=Service("chromedriver.exe")
        self.driver = webdriver.Chrome(service=s,options=chrome_options)
        print("Turnedd on chromedriver")
        self.driver.get("https://9gag.com/")
        print("I am at 9gag")

        self.picture_stack = []
        self.counter = 0

        #accept cookies button stuff
        while 1:
            try:
                print("trying")
                self.driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
                break
            except Exception:
                time.sleep(0.1)

        time.sleep(1)
        print("all OK")


    def __del__(self):
        self.driver.quit()

    async def _upload_pic(self,channel,url):

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await channel.send(file=discord.File(data, 'cool_image.png'))


    async def upload_pictures(self,channel,desired,info_msg):
        print(desired)
        print(self.counter)
        cont = "Loaded " + str(min(len(self.picture_stack),desired)) +" / " + str(desired)
        await info_msg.edit(content=cont)
        while(len(self.picture_stack) < desired):
            while(1):
                try:
                    element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(((By.ID, "stream-" + str(self.counter)))))
                    print(self.counter)
                    item = self.driver.find_element(By.ID, "stream-" + str(self.counter))
                    break
                except (TimeoutException,NoSuchElementException):
                    print("exc")
                    self.driver.execute_script("window.scrollTo(0, window.scrollY + 2000);")
            print(item.get_attribute("class"))


            sada = item.find_elements(By.CLASS_NAME,"image-post")
            for posts in sada:

                images = posts.find_elements(By.TAG_NAME,"img")

                for img in images:
                    #print(img.get_attribute("src"))
                    self.picture_stack.append(img.get_attribute("src"))
                    cont = "Loaded " + str(min(len(self.picture_stack),desired)) +" / " + str(desired)
                    await info_msg.edit(content=cont)

            self.counter+=1

        #print("stack pred  ", self.picture_stack)

        for i in range(desired):
            print("Posting: " + self.picture_stack[i])
            await self._upload_pic(channel,self.picture_stack[i])

        #print("dlzka pred popom: " + str(len(self.picture_stack)))
        for i in range(desired):
            print("popujem: " + self.picture_stack[0])
            self.picture_stack.pop(0)
        #print("dlzka po popom: " + str(len(self.picture_stack)))

        #print("stack po  ", self.picture_stack)






