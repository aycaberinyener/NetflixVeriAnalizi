import pandas as pd
import matplotlib.pyplot as plt
import collections
import seaborn as sns

data = pd.read_csv('NetflixOriginals.csv', encoding="ISO-8859-1")
#Verileri çekiyorum.
print(data)

print(data.info())
#Verilerin bilgisi

data.isnull().sum()

print(data["Runtime"].mean())
#Filmlerin ortalama uzunluğu

FilmSuresi = []

for i in data.Runtime:
    if i <= 90:
        FilmSuresi.append('Çok Kısa')
    elif 90 < i <= 130:
        FilmSuresi.append('Normal')
    else:
        FilmSuresi.append('Çok Uzun')
#Film sürelerini 90 dakika ve daha az olanları çok kısa,90 ve 130 arasındakileri normal,
# 130 dakikadan uzun filmleri ise çok uzun olarak sınıflandırdım.

data['FilmSuresi'] = FilmSuresi
print(data.head())

uzun_soluklu = data[data.FilmSuresi == 'Çok Uzun']
print(uzun_soluklu)
#Uzun soluklu film verileri
labels = uzun_soluklu["Language"]
print(labels.unique())
#Uzun soluklu filmlerin dilleri
status_d = collections.Counter(labels)
print(status_d)
#uzun soluklu filmler hangi dillerde ve sayıları
key_list = list(status_d.keys())
val_list = list(status_d.values())

fig, ax = plt.subplots()
ax.pie(val_list, labels=key_list, autopct='%.0f%%')
ax.set_title('Dillere göre film dağılımı')
plt.show()
#Uzun soluklu filmlerin daire grafiğinde gösterimi

data["Date"] = pd.to_datetime(data.Premiere)
data["Yıl"] = data["Date"].dt.year
data["Month"] = data["Date"].dt.month
film = data[data["Genre"] == "Documentary"].sort_values(["Yıl", "Month"])
film_1 = film[film["Yıl"] == 2019]
film_2 = film[(film["Yıl"] == 2020) & (film["Month"] <= 6)]

film_imdb = pd.concat([film_1, film_2], axis=0)
print(film_imdb)

plt.figure(figsize=(8, 10))
sns.barplot(film_imdb["IMDB Score"], film_imdb["Title"])
plt.title("2019 Ocak ile 2020 Haziran tarihleri arasında 'Documentary' türünde çekilmiş filmlerin IMDB değerleri")
plt.show()
#2019 Ocak ile 2020 Haziran tarihleri arasında 'Documentary' türünde çekilmiş filmlerin IMDB değerleri
ingilizce_film = data[data["Language"] == "English"].groupby("Genre")
ingilizce_film_listesi = ingilizce_film.max().sort_values(by="IMDB Score", ascending=False)

print(ingilizce_film_listesi)
#İngilizce dilindeki filmlerin litesi

data_genre = data.value_counts("Genre")
print(data_genre)
plt.figure(figsize=(10, 20))
sns.barplot(data_genre, data_genre.index)
plt.title('Film Türleri')
data["Language"].value_counts().head()

data.sort_values("IMDB Score", ascending=False).head(10)
#IMDB puanı en yüksek olan ilk 10 film

data_korelasyon = data[["IMDB Score", "Runtime"]]
corr = data_korelasyon.corr()
ax = sns.heatmap(data_korelasyon, annot=True)
#IMDB puanı ile 'Runtime' arasındaki korelasyon
data.head()
yıl_sayısı = data["Yıl"].value_counts()
print(yıl_sayısı)
#HYıllara göre film sayısı

imdb_runtime = data.loc[:, ["Title", "Runtime"]]
sorted_runtime = imdb_runtime.sort_values("Runtime")
first_ten_score_runtime = sorted_runtime.tail(10)
print(first_ten_score_runtime)
#En uzun ilk 10 film

plt.figure(figsize=(7, 5))
sns.histplot(x='Yıl', data=data, bins=15, color='purple')
plt.title("Yıllara Göre Film Sayıları")
#yıllara göre film sayıları

ortalamasure = data.groupby("Language")["IMDB Score"].mean()
ortalamasure.sort_values()
#Dillere göre IMBD puanları

toplam_runtime= data.groupby("Yıl")["Runtime"].sum().sort_values(ascending=False)
print(toplam_runtime)
#yıllara göre film süreleri

max_genre = data.groupby("Language")["Genre"].max()
print(max_genre)
#her dilin kullanıldığı maksimum film türü

def show_outliers(data):
    sns.set_theme(style="whitegrid")
    for col in data.columns:
        if data[col].dtypes in ["float", "int", "int64", "float64"]:
            ax = sns.boxplot(x=data[col])
            plt.show()


show_outliers(data)
#süre, IMDB puanı ve yıl değerlerinde aykırı veriye rastlanmıştır.
#özellikle film süresinde çok fazla ayrıkırı veriye rastlanmıştır.
#ancak aya göre verilen grafikte de göründüğü üzere aykırı veriye rastlanmamıştır.
