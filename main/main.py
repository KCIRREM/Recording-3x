import re
import time

import requests
from bs4 import BeautifulSoup
import ast
from tkinter import filedialog
import os
import pyaudio
import aiohttp
import asyncio
import win32gui, win32process
from subprocess import run
import subprocess
from array import array
import threading
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import shutil
import urllib.request
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


data_1 = {'hello': 'url'}


class extract:
    def __init__(self, data_dict):
        # self.url = data['test']['url']
        # create lists for each individual items
        urls = []
        creators = []
        titles = []
        dates = []
        spans = []
        group = []
        stuff = {}

        # create async function to extract url data
        async def get_urls(url_list):
            async with aiohttp.ClientSession() as session:
                tasks = ((asyncio.create_task(session.get(url, ssl=False))) for url in url_list)
                responses = await asyncio.gather(*tasks)
                print(responses)
                for index, response in enumerate(responses):
                    url = str(response.url)
                    soup = await response.text()
                    result = BeautifulSoup((soup), 'lxml').prettify()
                    info = ((re.search('<title>\n(.*)', result).group(1)).split(' - ', 1))
                    if index == 0:
                        creator = info[0][3:]

                    title = info[1].rsplit(' -', 1)[0]
                    date = re.search('\d\d? [a-zA-Z]{3} \d\d\d\d\d?', soup).group(0)
                    span = re.search('aria-label="duration: (\d*) mins"', soup).group(1)
                    print('url loaded : ', url, ' creator : ', creator, ' title : ', title, ' date : ', date,
                          ' span : ', span)
                    urls.append(url)
                    creators.append(creator)
                    titles.append(title)
                    dates.append(date)
                    spans.append(span)
                    group.append(key)
                    #stuff[key]
                    stuff[url] = {'creator': creator, 'title': title, 'date': date, 'span': span}
                    print(key)

        keys = [key for key in data_dict]

        for item in keys:
            key = item
            url = data_dict[key]['url']

            if data_dict[key]["record method"] == "episode":
                asyncio.run(get_urls([url]))


            elif data_dict[key]["record method"] == "all":
                html_page = (requests.get(url)).content
                soup = BeautifulSoup(html_page, 'lxml')
                soup_for_stuff = soup.prettify()
                max_page = re.search('Page 1 of (\d*)', soup_for_stuff)
                all_available_eps = re.search('<span class="hidden grid-visible@bpb2 grid-visible@bpw">\n *\((\d+)\)\n',
                                              soup_for_stuff).group(1)
                bbc_sounds_urls = (
                    re.findall(r'href="(https://www\.bbc\.co\.uk/sounds/play/[a-zA-Z0-9]*)', soup_for_stuff))
                asyncio.run(get_urls(bbc_sounds_urls))
                num_page = 1
                while len(bbc_sounds_urls) < int(all_available_eps):
                    num_page = num_page + 1
                    page_url = f'{url}?page={num_page}'
                    # print(page_url)
                    html_page = requests.get(page_url).content
                    soup_for_stuff = (BeautifulSoup(html_page, 'lxml')).prettify()
                    bbc_sounds_urls_temp = (
                        re.findall(r'href="(https://www\.bbc\.co\.uk/sounds/play/[a-zA-Z0-9]*)', soup_for_stuff))
                    bbc_sounds_urls = bbc_sounds_urls + bbc_sounds_urls_temp
                    asyncio.run(get_urls(bbc_sounds_urls))



            elif data_dict["record method"] == 'page':
                html_page = (requests.get(url)).content
                soup = BeautifulSoup(html_page, 'lxml')
                soup_for_stuff = soup.prettify()
                bbc_sounds_urls = (
                    re.findall(r'href="(https://www\.bbc\.co\.uk/sounds/play/[a-zA-Z0-9]*)', soup_for_stuff))
                asyncio.run(get_urls(bbc_sounds_urls))


        self.urls = tuple(urls)
        print(self.urls)
        self.creators = tuple(creators)
        self.titles = tuple(titles)
        self.dates = tuple(dates)
        self.spans = tuple(spans)
        self.group = tuple(group)

    def get_urls(self):
        return self.urls

    def get_creator(self):
        return self.creators

    def get_title(self):
        return self.titles

    def get_date(self):
        return self.dates

    def get_spans(self):
        return self.spans

    def get_group(self):
        return self.group


class individual_data(extract):
    def __init__(self, data_dict):
        super().__init__(data_dict)
        set_of_data = {}
        for pair in zip(((self.get_urls())), ((self.get_creator())), ((self.get_title())), ((self.get_date())),
                        ((self.get_spans())), ((self.get_group()))):
            key = (pair[5])
            add_pair = pair[:-1]
            if key in set_of_data:
                set_of_data[key].append(add_pair)
            else:
                set_of_data[key] = []
                set_of_data[key].append(add_pair)
        self.set_of_data = set_of_data

    def get_stuff(self):
        return self.set_of_data


class get_initial_data:
    def __init__(self):
        with open(f"{os.getcwd()}\\BBC sounds\\profiles-chromedriver.txt", 'r') as file:
            sounds_dict = ast.literal_eval(file.read())

        self.profile_1 = (sounds_dict["profile_1"]).rsplit('\\', 1)
        self.profile_2 = sounds_dict["profile_2"]
        self.profile_3 = (sounds_dict["profile_3"]).rsplit('\\', 1)
        self.name_3 = sounds_dict["name_3"]

        try:
            os.system("taskkill /F /im chrome.exe")
            os.system("taskkill /F /im firefox.exe")
            os.system("taskkill /F /im msedge.exe")
        except Exception as ProcessException:
            pass


class start_browsers(get_initial_data):
    path_to_SoundExe = os.path.join(os.getcwd(), "SoundVolumeView.exe")

    def __init__(self):
        super().__init__()

    def get_window_pid(self,title):
        hwnd = win32gui.FindWindow(None, title)
        threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
        return int(pid)

    def start_browser1(self):
        options = ChromeOptions()
        options.add_argument(f"user-data-dir={self.profile_1[0]}")
        options.add_argument(f"--profile-directory={self.profile_1[1]}")
        options.add_argument("--start-maximized")
        driver_profile_1 = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver_profile_1.get('https://duckduckgo.com/profile_1?ia=web')
        ProcessId_1 = self.get_window_pid(f'profile 1 at DuckDuckGo - Google Chrome')
        while (ProcessId_1) < 0:
            ProcessId_1 = self.get_window_pid(f'profile 1 at DuckDuckGo - Google Chrome')
        driver_profile_1.get('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        run(
            rf'"{self.path_to_SoundExe}" /SetAppDefault "VB-Audio Virtual Cable" all "chrome.exe"',
            shell=True)
        return driver_profile_1

    def start_browser2(self):
        options = webdriver.FirefoxOptions()
        options.set_preference('profile', self.profile_2)

        driver_profile_2 = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),
                                             options=options)
        driver_profile_2.maximize_window()
        driver_profile_2.get('https://duckduckgo.com/profile_2?ia=web')
        ProcessId_2 = self.get_window_pid(f'profile 2 at DuckDuckGo — Mozilla Firefox')
        while int(ProcessId_2) < 0:
            ProcessId_2 = self.get_window_pid(f'profile 2 at DuckDuckGo — Mozilla Firefox')
        run(
            rf'"{self.path_to_SoundExe}" /SetAppDefault "VB-Audio Cable A" all "firefox.exe"',
            shell=True)
        return driver_profile_2

    def start_browser3(self):
        options = webdriver.EdgeOptions()
        options.add_argument(f"user-data-dir={self.profile_3[0]}")
        options.add_argument(f"profile-directory={self.profile_3[1]}")
        options.add_argument("--start-maximized")
        driver_profile_3 = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),
                                          options=options)
        driver_profile_3.get('https://duckduckgo.com/profile_3?ia=web')
        ProcessId_3 = self.get_window_pid(f'profile 3 at DuckDuckGo - {self.name_3} - Microsoft​ Edge')
        while ProcessId_3 < 0:
            ProcessId_3 = self.get_window_pid(f'profile 3 at DuckDuckGo - {self.name_3} - Microsoft​ Edge')
        driver_profile_3.get('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        run(
            rf'"{self.path_to_SoundExe}" /SetAppDefault "VB-Audio Cable B" all "msedge.exe"',
            shell=True)
        return driver_profile_3




class recording(extract):
    def __init__(self, data_dict):
        super().__init__(data_dict)
        p = pyaudio.PyAudio()
        num_sound_devices = (p.get_host_api_info_by_index(0)).get('deviceCount')

        sound_devices_dict = {}
        for i in range(0, num_sound_devices):
            info = (p.get_device_info_by_index(i))
            print(info)
            if 'CABLE' in info.get('name') and info.get('maxInputChannels') > 0:
                sound_devices_dict[(info.get('name'))] = i

        self.VB_Audio_Virtual_Cable = sound_devices_dict["CABLE Output (VB-Audio Virtual "]
        self.VB_Audio_Virtual_Cable_A = sound_devices_dict["CABLE-A Output (VB-Audio Cable "]
        self.VB_Audio_Virtual_Cable_B = sound_devices_dict["CABLE-B Output (VB-Audio Cable "]

    def record(self, FILE_NAME, FILE_LENGTH, Dev_index):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44800
        CHUNK = 1024
        RECORD_SECONDS = 1

        silence_2_mins = 4520
        total_length = 2290 * int(FILE_LENGTH)
        lower_bound = total_length - 9160
        upper_bound = total_length - 9160
        s_or_f = 'success'

        audio = pyaudio.PyAudio()  # instantiate the pyaudio

        # recording prerequisites
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            input_device_index=Dev_index,
                            frames_per_buffer=CHUNK)

        # starting recording
        frames = []
        num_of_nothings = 0
        i = 0
        while i != int(RATE // CHUNK * RECORD_SECONDS):
            # print(i)
            # print((RATE/CHUNK*RECORD_SECONDS))
            data = stream.read(CHUNK)
            data_chunk = array('h', data)
            vol = max(data_chunk)
            if (vol >= 500):
                print("something said")
                frames.append(data)
                num_of_nothings = 0
                RECORD_SECONDS = RECORD_SECONDS + 1
            else:
                num_of_nothings = num_of_nothings + 1
                frames.append(data)
                print('nothing')
                if num_of_nothings != silence_2_mins:
                    RECORD_SECONDS = RECORD_SECONDS + 1
                elif num_of_nothings == silence_2_mins and lower_bound <= i and i <= upper_bound:
                    print('recording written succefully')
                    break
                else:
                    print('recording failed exiting')
                    s_or_f = 'failure'
                    break

            print(num_of_nothings)
            i = i + 1
        stream.stop_stream()
        stream.close()
        audio.terminate()

        if s_or_f == 'success':
            raw_pcm = b''.join(frames)
            l = subprocess.Popen(
                f'"{os.getcwd()}\\lame3.100.1-x64\\lame.exe" - -r -m m {FILE_NAME}',
                stdin=subprocess.PIPE)
            l.communicate(input=raw_pcm)

    def record_for_individual_driver(self, driver_url_list, driver_name, dev_index):
        for item in range(0, len(driver_url_list)):
            driver_name.get(driver_url_list[item])
            if driver_name == "driver_profile_2":
                pass
            else:
                WebDriverWait(driver_name, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='smphtml5iframesmp-wrapper']")))
            WebDriverWait(driver_name, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='p_audioui_playpause']")))
            time.sleep(3)
            driver_name.find_element(By.XPATH, "//button[@id='p_audioui_playpause']").click()
            print('done')

            self.record((f"{self.creators[item]}--{self.dates[item]}--{self.titles[item]}--{self.spans[item]}"),
                        self.spans[item],
                        dev_index)


class begin_recording(recording, start_browsers):
    def __init__(self, data_dict):
        recording.__init__(self, data_dict)
        start_browsers.__init__(self)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(self.start_browser1)
            future2 = executor.submit(self.start_browser2)
            future3 = executor.submit(self.start_browser3)
        self.driver_profile_1 = future1.result()
        self.driver_profile_2 = future2.result()
        self.driver_profile_3 = future3.result()
        work_load_individual = len(self.urls) // 3
        work_load_extra = len(self.urls) % 3
        urls_profile_1 = [self.urls[i] for i in range(0, work_load_individual)]
        urls_profile_2 = [self.urls[i] for i in
                          range(work_load_individual, work_load_individual + work_load_individual)]
        urls_profile_3 = [self.urls[i] for i in range(work_load_individual + work_load_individual,
                                                      work_load_individual + work_load_individual +
                                                      work_load_individual + work_load_extra)]
        print(self.urls)
        p1 = threading.Thread(target=recording.record_for_individual_driver,
        args=(self,urls_profile_1, self.driver_profile_1,self.VB_Audio_Virtual_Cable))

        p2 = threading.Thread(target=recording.record_for_individual_driver,
        args=(self,urls_profile_2, self.driver_profile_2,self.VB_Audio_Virtual_Cable_A))

        p3 = threading.Thread(target=recording.record_for_individual_driver,
                              args=(self, urls_profile_3, self.driver_profile_3, self.VB_Audio_Virtual_Cable_B))
        p3.start()
        p1.start()
        p2.start()


data_dict1 = {0: {'url': 'https://www.bbc.co.uk/programmes/p09pt8w7/episodes/guide',
                  'sound_drivers': ['VB-Audio Virtual Cable', 'VB-Audio Cable A', 'VB-Audio Cable B'],
                  'record method': 'all', 'record time': '2020', 'schedule': 'yes'},
              1: {'url': 'https://www.bbc.co.uk/programmes/b00jlwqd/episodes/guide',
                  'sound_drivers': ['VB-Audio Virtual Cable', 'VB-Audio Cable A', 'VB-Audio Cable B'],
                  'record method': 'all', 'record time': '2020', 'schedule': 'yes'}}


data = ['https://www.bbc.co.uk/sounds/play/m0017bln', 'https://www.bbc.co.uk/sounds/play/m00173rc',
        'https://www.bbc.co.uk/sounds/play/m0016yyb']
d = individual_data(data_dict1)
print(d.get_stuff())
