from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
import difflib
import emoji

genres = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy',
        'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror',
        'Mystery', 'Sci-Fi', 'IMAX', 'Documentary', 'War', 'Musical',
        'Western', 'Film-Noir']

def main():
    recognizer=sr.Recognizer()

    with sr.Microphone() as source: 
        #print('Clearing background noise...')
        recognizer.adjust_for_ambient_noise(source,duration=1)
        print('Waiting for your message...')
        recordedaudio=recognizer.listen(source, phrase_time_limit=5)
        print('Done recording..') 
     
    try:
        text=recognizer.recognize_google(recordedaudio,language='en-US')
        print('Your message:{}'.format(text))
    except Exception as ex:
        print(ex)
    
    text2 = text.split()
    for x in range(len(text2)):
        if text2[x].capitalize() in genres:
            return text2[x].capitalize()

    #Sentiment analysis 
    Sentence=[str(text)]
    analyser=SentimentIntensityAnalyzer()
    
    mood="neu"

    for i in Sentence:
        v=analyser.polarity_scores(i)
        #print(v)
        if(v["neg"]>v["pos"] and v["neg"]>v["neu"]):
            mood="neg"
        elif(v["pos"]>v["neg"] and v["pos"]>v["neu"]):
            mood="pos"
        else:
            mood="neu"      
    
    if mood == "neg":
        print(f'Mood: sad {emoji.emojize(":pensive_face:")}')
    elif mood == "pos":
        print(f'Mood: happy {emoji.emojize(":grinning_face_with_big_eyes:")}')
    else:
        print(f'Mood: neutral {emoji.emojize(":upside-down_face:")}')

    print("Choose any of the following:")
    if(mood=="neg"):
        print("\t1.Drama\n\
                2.Comedy\n\
                3.Documentary\n\
                4.Romance\n\
                5.Horror")

    elif(mood=="pos"):
        print("\t1.Action\n\
            2.Animation\n\
            3.Fantasy\n\
            4.Comedy\n\
            5.Drama\n\
            6.Musical\n\
            7.Romance\n\
            8.Thriller\n\
            9.Sci-Fi\n\
            10.Western")        
    else:
        print("\t1.Adventure\n\
            2.Children\n\
            3.Crime\n\
            4.Thriller\n\
            5.Mystery\n\
            6.War\n\
            7.Film-Noir\n\
            8.Sci-Fi")                                                        
    
    with sr.Microphone() as source2: 
        #print('Clearing background noise...')
        recognizer.adjust_for_ambient_noise(source2,duration=1)
        print('Waiting for your message...(Choose your genre)')
        recordedaudio=recognizer.listen(source2, phrase_time_limit=5)
        print('Done recording..') 
    
    try:
        genre=recognizer.recognize_google(recordedaudio,language='en-US')
        print('Your message:{}'.format(genre))
    except Exception as ex:
        print(ex)
    
    genre = genre.split()[0]
    find_close_match = difflib.get_close_matches(genre, genres)
    match = find_close_match[0]
    print("match: ", match)
    return match.capitalize()