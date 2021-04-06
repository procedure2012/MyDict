import pandas as pd
from crawler import MyDict

class MyEnglishDict(MyDict):
    def __init__(self, url):
        super(MyEnglishDict, self).__init__(url)
    
    def lookup(self, word):
        output = {}
        raw_text = self.get_web_result(self.url, word)
        phonetic_symbols = raw_text.find(name='ul', class_='Mean_symbols__5dQX7')
        if phonetic_symbols is None:
            return None
        phonetic_symbols = phonetic_symbols.find_all('li')
        if len(phonetic_symbols) < 2:
            return None
        phonetic_symbols_text = [x for x in phonetic_symbols[1].strings]
        output['phonetic_symbol'] = phonetic_symbols_text[1]
        print(output['phonetic_symbol'])
        
        meanings = raw_text.find(name='ul', class_='Mean_part__1RA2V').find_all('li')
        if meanings is None:
            return None
        definitions = []
        for m in meanings:
            lexical_category = m.find('i').string
            raw_definitions = m.find_all('span')
            sub_definitions = [lexical_category]
            for d in raw_definitions:
                sub_definitions.append(d.text)
            definitions.append(' '.join(sub_definitions))
        output['definitions'] = '\n'.join(definitions)
        print(output['definitions'])
        
        return output
        
        
if __name__ == '__main__':
    df = pd.DataFrame(columns=["Word", "Audio", "Meaning", "Example", "Source"])
    dictionary = MyEnglishDict("http://www.iciba.com/word?w=")
    while True:
        print("//--------------------------------------")
        unknown_word = input("请输入查询的单词/输入‘886’离开：")
        if unknown_word == '886':
            empty = input("将要替代上次记录的结果，按回车继续...")
            df.to_csv('./save_recode_english.csv', index=False, header=False, encoding='utf-8_sig')
            break
        result = dictionary.lookup(unknown_word)
        if result is None:
            print("找不到单词TAT")
            continue
        sentence = input("输入例句/输入'N'不保存：")
        if sentence != 'N':
            source = input("输入例句来源（可选）：")
            df = df.append([{'Word': unknown_word, "Audio": result['phonetic_symbol'], "Meaning": result['definitions'], "Example": sentence, "Source": source}], ignore_index=True)
