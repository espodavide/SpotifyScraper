def YoutubeToMp3(playlist_name):
    # %%
    import pandas as pd
    import requests
    import re
    from pytube import YouTube 
    import os 
    import zipfile

    import logging

    # Configura il logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting downloading app..")

    # %%
    #playlist_name='itunes'
    playlist_name = playlist_name.strip()

    # %%
    #Import del csv che contiene tutte le playlist
    df=pd.read_csv(f'Playlist/PlaylistCsv/{playlist_name}.csv')

    # %%
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0',inplace=True,axis=1)

    # %%
    search_name_list = []
    if len(list(df.columns))<2:
        df=pd.read_csv(f'Playlist/PlaylistCsv/{playlist_name}.csv',sep=';')

    for i,row in df.iterrows():
        song = row['SONG_NAME']
        artist = row['ARTIST_NAME']
        
        song = '+'.join(song.split(' ')).lower()
        artist = '+'.join(artist.split(' ')).lower()
        search_name_list.append(song +'+'+ artist)


    # %%
    url_list=[]
    for name in search_name_list:
        url = 'https://www.youtube.com/results?search_query='+name
        url_list.append(url)

    # %%
    regex='watch\?v=[^&"]+' #regex pre prendere tutto i video id della pagina
    for url in url_list:
        print(url)
        res = requests.get(url)
        first_video_id=re.findall(regex,res.text)[0]
        url_video =f'https://www.youtube.com/{first_video_id}'
        # url input from user 
        yt = YouTube(url_video)

        # extract only audio 
        video = yt.streams.filter(only_audio=True).first() 

        # check for destination to save file 
        try:
            os.makedirs("Playlist/PlaylistSong")
        except FileExistsError:
            pass
        destination = f'Playlist/PlaylistSong/{playlist_name}'

        # download the file 
        out_file = video.download(output_path=destination) 

        # save the file 
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 

        # result of success 
        print(yt.title + " has been successfully downloaded.")
        
    logging.info("Starting zipping files ..")


    zip_file_path = f'{playlist_name}.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for song_path in os.listdir(destination):
            zipf.write(os.path.join(destination,song_path), os.path.basename(song_path))

    return zip_file_path

if __name__ =='__main__':
    YoutubeToMp3(playlist_name='Get out of the crisis')


