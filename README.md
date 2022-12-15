Clone the file and install python requirements
```md
pip install -r requirements.txt
```

**Dataset link:**
https://grouplens.org/datasets/movielens/latest/

**dataset README file:**
https://files.grouplens.org/datasets/movielens/ml-latest-README.html

**Identifying Emotions from Voice using Transfer Learning:**
https://towardsdatascience.com/detecting-emotions-from-voice-clips-f1f7cc5d4827


merged dataset has columns:

movieId, title, genres, imbdId, tmbdId, userId, rating, timestamp

['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary', 'War', 'Musical', 'Western', 'Film-Noir']

movies are divided based on this article:
https://stephenfollows.com/understanding-movie-genres-emotions/


Happy : 
1. Musical
2. Animation
3. Romance - Happy
4. Comedy
5. Fantasy
6. Adventure
7. Drama - Sad

Sad: 
1. Mystery
2. Thriller
3. War
4. Drama - Happy 
5. Crime
6. Horror
7. Romance - Happy
8. Sci-fi  - Neutral

Nuetral:
1. Children
2. Action
3. Sci-Fi  - Sad
4. IMAX
5. Documentary
6. Film-Noir
7. Western

