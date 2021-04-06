import pandas as pd
from crawler import MyDict


class MeinWoerterbuch(MyDict):
    def __init__(self, url):
        super(MeinWoerterbuch, self).__init__(url)
        self.url_2 = 'http://www.godic.net/dicts/cg/{}?forcecg=true'
    
    def print_kraus(self, kraus_table):
        print("+--------------------+--------------------+--------------------+--------------------+")
        print("|%-20s|%-20s|%-20s|%-20s|" % (kraus_table[0][0], kraus_table[0][1], kraus_table[0][2], kraus_table[0][3]))
        print("+--------------------+--------------------+--------------------+--------------------+")
        print("|%-20s|%-20s|%-20s|%-20s|" % (kraus_table[1][0], kraus_table[1][1], kraus_table[1][2], kraus_table[1][3]))
        print("+--------------------+--------------------+--------------------+--------------------+")
        print("|%-20s|%-20s|%-20s|%-20s|" % (kraus_table[2][0], kraus_table[2][1], kraus_table[2][2], kraus_table[2][3]))
        print("+--------------------+--------------------+--------------------+--------------------+")
        print("|%-20s|%-20s|%-20s|%-20s|" % (kraus_table[3][0], kraus_table[3][1], kraus_table[3][2], kraus_table[3][3]))
        print("+--------------------+--------------------+--------------------+--------------------+")
        print("|%-20s|%-20s|%-20s|%-20s|" % (kraus_table[4][0], kraus_table[4][1], kraus_table[4][2], kraus_table[4][3]))
        print("+--------------------+--------------------+--------------------+--------------------+")
        print("|%-20s|%-20s|%-20s|%-20s|" % (kraus_table[5][0], kraus_table[5][1], kraus_table[5][2], kraus_table[5][3]))
        print("+--------------------+--------------------+--------------------+--------------------+")

    def lookup(self, word):
        output = {}
        raw_text = self.get_web_result(self.url, word)
        
        meanings = raw_text.find_all(name='div', class_='lemma featured')
        if len(meanings) < 1:
            return None
        definition_list = []
        for m in meanings:
            tag = m.find(name='span', class_='tag_lemma')

            sub_definitions = m.find_all(name='div', class_='translation sortablemg featured')
            sub_definitio_list = []
            for sub_m in sub_definitions:
                sub_definitio_list.append(sub_m.find(name='span', class_='tag_trans').get_text())
            definition_list.append(tag.get_text()+':\n' + '; '.join(sub_definitio_list))
        output['definitions'] = '\n\n'.join(definition_list)
        print(output['definitions'])

        raw_text = self.get_web_result(self.url_2, word)
        table = raw_text.find(name='table', class_='table-col-3')
        kraus_table = []
        if table is not None:
            kraus = table.find_all('tr')
            for row in kraus[1:]:
                sub_kraus = []
                for col in row.children:
                    sub_kraus.append(col.string)
                kraus_table.append(sub_kraus)
            self.print_kraus(kraus_table)
            output['kraus'] = kraus_table
        
        return output


if __name__ == '__main__':
    df = pd.DataFrame(columns=["Word", "Meaning", "Example", "Source"])
    df_2 = pd.DataFrame(columns=["Word", "kraus-1-1", "kraus-1-2", "kraus-1-3", "kraus-2-1", "kraus-2-2", "kraus-2-3",
                               "kraus-3-1", "kraus-3-2", "kraus-3-3", "kraus-4-1", "kraus-4-2", "kraus-4-3",
                               "kraus-5-1", "kraus-5-2", "kraus-5-3", "kraus-6-1", "kraus-6-2", "kraus-6-3"])
    
    Woerterbuch = MeinWoerterbuch("https://www.linguee.de/deutsch-englisch/search?source=auto&query=")
    while True:
        print("//--------------------------------------")
        unknown_word = input("请输入查询的单词/输入‘886’离开：")
        if unknown_word == '886':
            empty = input("将要替代上次记录的结果，按回车继续...")
            df.to_csv('./save_recode_German_definition.csv', index=False, header=False, encoding='utf-8_sig')
            df_2.to_csv('./save_recode_German_kraus.csv', index=False, header=False, encoding='utf-8_sig')
            break
        result = Woerterbuch.lookup(unknown_word)
        if result is None:
            print("找不到单词TAT")
            continue
        sentence = input("输入例句保存单词/输入回车不保存单词：")
        if sentence != '':
            source = input("输入例句来源（可选）：")
            df = df.append([{'Word': unknown_word, "Meaning": result['definitions'], "Example": sentence, "Source": source}], ignore_index=True)
            
        if 'kraus' in result:
            sentence = input("输入'Y'保存变格/输入回车不保存变格：")
            if sentence != '':
                tmp = {'Word': unknown_word}
                for i in range(6):
                    for j in range(1, 4, 1):
                        tmp['kraus-'+str(i+1)+'-'+str(j)] = result['kraus'][i][j]
                df_2 = df_2.append([tmp], ignore_index=True)
