# Prosjekt i TDAT3025 Anvendt maskinlæring med prosjekt høsten 2019
Dette er git-repoet vi har brukt i forbindelse med den avsluttende prosjektoppgaven i faget TDAT3025 - Anvendt maskinlæring med prosjekt høsten 2019 ved NTNU i Trondheim.
Her finnes all python kode vi har brukt for å prosessere datasettet og for modellene vi har trent. 

Mer informasjon om dette prosjektet finner du i tilhørende [prosjektrapport](https://drive.google.com/open?id=1sHK-rPTRa16II3QMYkG_vRW4RvNbq1tDX4yEnjYj0dU). 

## Installasjon

Clone og cd inn i git-repoet: 

```
git clone https://gitlab.stud.idi.ntnu.no/teamkoko/tdat3025-mlp.git
cd tdat3025-mlp
```

Installer avhengigheter 

```
pip3 install keras tensorflow mxnet matplotlib numpy pandas sklearn nltk gluon gluonnlp
```

Hvis man har problemer med sertifikater så kjør følgende kommando i en bash terminal (MacOS):

```
/Applications/Python\ 3.6/Install\ Certificates.command
```


For å trene og kjøre CNN:

```
cd NeuralNetwork
python3 CNN2.py                #Denne filen trener en CNN model
python3 loadeAndRunModel.py    #Denne filen kører en CLI hvor man kan teste modellen
```

Tren og kjør naive bayes og SVM
```
cd NaiveBays_SVM
python3 naiveBayes_SVM.py
```






### Datasettet
[Datasettet](https://drive.google.com/open?id=10yC-95yhLjNj6HoOzBP00euuiG0sEywF) - Her finnes alle rådataene vi har samlet for å sette sammen datasettet vårt.

Alle modellene vi har undersøkt i denne oppgaven, var trent på *./dataset.csv*, som ligger i rotmappa her i gitlab repoet. Dette datasettet består av data fra to forskjellige kilder. Størsteparten av dataene kommer fra 23 forskjellige StackExchange (SE) forum, samt også [twitter hate speech datasettet (Davidson *et al.*, 2017)](https://data.world/thomasrdavidson/hate-speech-and-offensive-language). 

Publikasjonene fra hvert av forumene er inndelt i mappestrukturen som følger (i linken over) 

```
./Dataset/SE Dataset/SE #forumnavn# Data/
```

Samt er også data fra hvert av forumene inndelt i *bad.csv* og *good.csv*, basert på totalt antall stemmer på hvert spørsmål, som avgjør om publikasjonen skal godkjennes eller ikke i forbindelse med automoderasjon av vårt system. 


Vi pre-prosseserte dataene fra SE forumene, ved å fjerne html og oprettet en "label" kollonne med de to klassene 'g' og 'b', hvor 'g' representerer godkjente publikasjoner og 'b' representerer ikke godkjente publikasjoner.
Pre-prosessing av dataene ble utført slik:
```
cd Data\ preprocessing/

python3 combine_all_in_root.py --root_dir ../SE\ Dataset --output_dir ../

python3 remove_html.py --i ../combined_good.csv --o ../HTML\ Cleaned/html_cleaned_good.csv

python3 remove_html.py --i ../combined_bad.csv --o ../HTML\ Cleaned/html_cleaned_bad.csv

python3 create_label_column.py --i ../HTML\ Cleaned/html_cleaned_good.csv --o ../output_good.csv --l g

python3 create_label_column.py --i ../HTML\ Cleaned/html_cleaned_bad.csv --o ../output_bad.csv --l b

python3 combine_files.py --i1 ../output_good.csv --i2 ../outpyt_bad.csv --o ../combined_cleaned_labeled.csv
```

Dette slo vi deretter sammen med dataene fra hate-speech datasettet, som vi renset for all twitter metadata ved å kjøre følgende python skript:
```
python3 twitter-preprocessing.py
```

