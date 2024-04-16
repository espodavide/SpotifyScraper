def SpotifyScraper(url_playlist):

    # %%
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup


    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    import time
    import os
    import re
    import logging

    # Configura il logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting app..")

    # %%
    URL = url_playlist
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("enable-automation")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    #options.add_argument("--disable-gpu")
    options.add_argument("enable-features=NetworkServiceInProcess")


    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),options=options)
    #driver.set_page_load_timeout(300*1000)
    logging.info("Driver getting base link ..")
    res = requests.get(URL)
    logging.info(res.status_code)
    driver.get(URL)
    logging.info("Driver is working ..")
    logging.info('Waititng for the page to open...')
    time.sleep(10)

    coocki_button_path = '//*[@id="onetrust-accept-btn-handler"]'
    coocki_button_path=driver.find_element(By.XPATH, coocki_button_path)
    coocki_button_path.click()

    # %%
    # Prendo il nome della playlist
    playlist_name_path='//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[1]/section/div[1]/div[5]/span[2]/h1'
    playlist_name_html = driver.find_element(By.XPATH, playlist_name_path)
    playlist_name = playlist_name_html.text.strip()
    print(playlist_name)
    # %%
    # Itero lunga la pagina per prendere html con le varie canzoni
    count = 0
    html_list = []
    while count<=3:
        print(count)
        class_song_name='RfidWIoz8FON2WhFoItU'
        song_list=driver.find_elements(By.CLASS_NAME,class_song_name)
        for song in song_list:
            try:
                for _ in range(4):
                    html = driver.page_source

                    song.send_keys(Keys.PAGE_DOWN)
                    #time.sleep(1)
            except:
                continue
            #prendo html della pagina con tutte le canzoni
            html_list.append(html)
        count+=1


    df_list = []
    for html_part in html_list:
        # Prendo tutte le canzoni in fila
        soup = BeautifulSoup(html_part, "html.parser")
        song_class = "t_yrXoUO3qGsJS4Y6iXX"
        song_element = soup.find_all("div", class_=song_class)
        song_name_list=[song_name.text for song_name in song_element]

        # Prendo tutti gli artisti in fila
        artists_class = "Text__TextElement-sc-if376j-0 gYdBJW encore-text-body-small"
        artist_element = soup.find_all("div", class_=artists_class)
        artist_name_list=[artist_name.text for artist_name in artist_element]

        # creo un df dove salvarmi tutte le canzoni e artisti
        df_single_part=pd.DataFrame({'SONG_NAME':song_name_list[:len(artist_name_list)], 'ARTIST_NAME':artist_name_list})
        df_list.append(df_single_part)

    # Concateno i df e droppo i duplicati che si sono creati
    df = pd.concat(df_list).drop_duplicates().reset_index(drop=True)

    # Aggiungo il nome della playlist
    df['PLAYLIST_NAME'] = playlist_name

    # salvo in csv prossimamento su db
    try:
        os.makedirs("Playlist/PlaylistCsv")
    except FileExistsError:
        pass
    df.to_csv(f'Playlist/PlaylistCsv/{playlist_name}.csv',index=False)
    return playlist_name

if __name__ =='__main__':
    SpotifyScraper(url_playlist="https://open.spotify.com/playlist/4wWiV3w2OsZrITueawQ5vK")



    