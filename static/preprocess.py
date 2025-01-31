import pandas as pd
import os

df = pd.read_csv('static/dataset_olympics.csv')
df['index'] = df.index



def show_files_of_folder():
    files = os.listdir()
    print(files)


def show_list_of_sports():
    sports_types = df['Sport'].tolist()
    sports_set = set(sports_types)

    output = ""
    for i in sports_set:
        output = output + i + ", "

    print(output)

def split_csv_to_groups():
    dict_for_sports = {
        '1': ['Football', 'Handball', 'Hockey', 'Ice Hockey', 'Rugby Sevens', 'Water Polo', 'Lacrosse', 'Basketball', 'Volleyball', 'Rugby', 
                               'Softball', 'Baseball', 'Cricket', 'Polo', 'Beach Volleyball', 'Polo'],
        '2': ['Tennis', 'Badminton', 'Table Tennis', 'Croquet', 'Jeu De Paume', 'Racquets'],
        '3': ['Judo', 'Taekwondo', 'Boxing', 'Wrestling', 'Fencing'],
        '4': ['Sailing', 'Swimming', 'Diving', 'Synchronized Swimming', 'Canoeing', 'Rowing'],
        '5': ['Biathlon', 'Ski Jumping', 'Snowboarding', 'Alpine Skiing', 'Freestyle Skiing', 'Cross Country Skiing', 'Bobsleigh', 'Skeleton', 
                               'Luge', 'Nordic Combined', 'Curling', 'Military Ski Patrol'],
        '6': ['Athletics', 'Weightlifting', 'Triathlon', 'Cycling', 'Speed Skating', 'Short Track Speed Skating', 'Modern Pentathlon'],
        '7': ['Gymnastics', 'Rhythmic Gymnastics', 'Trampolining', 'Figure Skating'],
        '8': ['Art Competitions', 'Alpinism', 'Tug-Of-War', 'Motorboating', 'Basque Pelota', 'Roque', 'Golf', 'Archery', 
                               'Shooting', 'Equestrianism']
    }
    df1 = df[df['Sport'].isin(dict_for_sports['1'])]
    df2 = df[df['Sport'].isin(dict_for_sports['2'])]
    df3 = df[df['Sport'].isin(dict_for_sports['3'])]
    df4 = df[df['Sport'].isin(dict_for_sports['4'])]
    df5 = df[df['Sport'].isin(dict_for_sports['5'])]
    df6 = df[df['Sport'].isin(dict_for_sports['6'])]
    df7 = df[df['Sport'].isin(dict_for_sports['7'])]
    df8 = df[df['Sport'].isin(dict_for_sports['8'])]

    all_df = [df1,df2,df3,df4,df5,df6,df7,df8]

    for ind, item in enumerate(all_df, start=1):
        item["Group"] = ind

    # for ind1, item1 in enumerate(all_df, start=1):
    #     for ind2, item2 in enumerate(all_df, start=1):
    #         if ind2 <= ind1:
    #             continue
    #         combined = pd.merge(item1, item2, how='inner', on=['index'])
    #         size = len(combined.index)
    #         if size > 0:
    #             print("index 1: ", ind1, ", index 2: ", ind2, ", size: ", size)
    #             print(combined.head(min(size,10)))
    
    df_combined = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8], ignore_index=True, sort=False)
    df_combined = df_combined.sort_values(by="index")
    df_combined = df_combined.reset_index(drop=True)
    print(len(df_combined.index))
    print(df_combined.head(20))

    df_combined.to_csv('static/edited_olym.csv', header=True, index=False, sep=",")

    #df_res = df[~df['index'].isin(df_combined['index'])]
    #print(len(df_res.index))
    #print(df_res.head(10))

    #print(set(df_res["Sport"].tolist()))

split_csv_to_groups()