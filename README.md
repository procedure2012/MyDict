# MyDict

I present MyDict, which is a dictionary integreted the function of online word search and word record. The backbone search engine is chinese-english dictionary iciba and the programm used for word recod is Anki. 

## Prerequisites

1. Download and install Anki according to the Instruction.
2. Import the python environment. 
```
conda env create -f environment.yaml
```

## Usage

1. Clone the project.

```
git clone https://github.com/procedure2012/MyDict.git
```

2. Enter the folder `MyDict` and start the program.

```
cd MyDict
python english.py
```

3. Type the word you want to look up. The program will automatically save the words in the current folder when you exit the program.

```
请输入查询的单词/输入‘886’离开：hunter
[ˈhʌntər]
n. 猎人;  猎犬;  猎狐马，猎食其他动物的野兽;  亨特
输入例句/输入'N'不保存：Farewell, good hunter.
输入例句来源（可选）：Bloodborne
```

4. If this is the first time you use my MyDict, you should first import my card templates. Click `Import File` at the bottom and load `test.apkg`.


5. Open Anki. Click `File->Import...` and load the csv file that recods your desired words. 

## Appendix

I also made a german-english dictionary. Besides the word recod, the german-english dictionary can also recode the conjugation of verb (which I always forget......) It uses Liguee for the definitions and Godict for the conjugation. 
```
cd MyDict
python deutsch.py
``` 