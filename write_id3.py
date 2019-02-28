def write_id3(pod_path, file_name, titles, episode_num, season_num, alb, albart, art):

    print(season_num)
    for file_name_entry in file_name:
        file_name_index = file_name_entry.index(file_name_entry)
        try:
            audio = ID3(pod_path + file_name_entry)
            audio.delete()
            audio = ID3()
        except ID3NoHeaderError:
            audio = ID3()
        audio.add(TIT2(encoding=3, text=titles[file_name_index]))
        if len(episode_num) != 0:
            audio.add(TRCK(encoding=3, text=episode_num[file_name_index]))
        else:
            print("No Ep Num")
        if len(season_num) != 0:
            audio.add(TPOS(encoding=3, text=season_num[file_name_index]))
        else:
            print("No Sn Num")
        audio.add(TPE1(encoding=3, text=art))
        audio.add(TPE2(encoding=3, text=albart))
        audio.add(TALB(encoding=3, text=alb))
        audio.save(pod_path + file_name_entry)


