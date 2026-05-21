import os

import pandas as pd
from openai import OpenAI
import requests

class Get_Deepseek:
    def __init__(self,model:str ="deepseek-chat"):
        self.model =model
        self.client = OpenAI(
            api_key="sk-fb929c78ded9437b997592f44c4e0ebc",
            base_url="https://api.deepseek.com"
        )
        self.system_prompt="""
        你是一个专业的导游,包括中国以及国外,你需要根据用户输出的信息来为用户制定一个完整的旅游路线图,具体要求如下:
        1.需要根据用户给出的城市,季节,预算,以及行程天数给出对应的旅游路线:
        2.提供的旅游路线应该是固定的格式包括：景点名称,具体游玩时间,景点特点,经纬度,预计花费,表格格式如下:
        |景点名称|游玩时间|景色特点|经度|纬度|预计花费|
        3.只需要返回表格内容即可,不需要额外的文字说明
        4.切记返回的内容要合理,也要有逻辑可循
        5.经纬度只需要返回数字即可,不用单位,确保经纬度准确:
        6.游玩格式时间是:第X天-时间段(例如:第一天-上午,第二天-下午):
        7.预计花费请输出具体金额或"免费":
        8表格使用Markdown格式,用|分割
        9.确保返回的数据能正确解析为DataFrame
        10.景点数量应与行程天数匹配
        11.保证经纬度的准确性,并且经度和纬度要具体
        """
    def _get_travel_plan(self,city,season,budget,day):
        try:
            raw_result = self.get_ai_response(city,season,budget,day)
        except Exception as e:
            return{
                "code":500,
                "message":str(e),
                "raw": raw_result if 'raw_result' in locals() else ""
            }
    def parse_table_to_dataframe(self, table_text: str) -> pd.DataFrame:
        """
        将AI生成的Markdown表格文本解析为DataFrame
        
        Args:
            table_text: AI生成的Markdown表格文本
            
        Returns:
            pd.DataFrame: 解析后的DataFrame
        """
        # 分割表格文本为行
        lines = table_text.strip().split('\n')
        
        # 找到表头行和数据行
        header_line = None
        data_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 找到表头行
            if '|景点名称|' in line:
                header_line = line
                # 跳过分隔线
                if i + 1 < len(lines) and '|---|' in lines[i + 1]:
                    i += 1
                # 收集数据行
                for j in range(i + 1, len(lines)):
                    data_line = lines[j].strip()
                    if data_line and data_line.startswith('|') and data_line.endswith('|'):
                        data_lines.append(data_line)
                    else:
                        break
                break
        
        if not header_line or not data_lines:
            raise ValueError("无法解析表格文本")
        
        # 解析表头
        headers = [h.strip() for h in header_line.split('|') if h.strip()]
        
        # 解析数据行
        data = []
        for line in data_lines:
            row = [cell.strip() for cell in line.split('|') if cell.strip()]
            if len(row) == len(headers):
                data.append(row)
        
        # 创建DataFrame
        df = pd.DataFrame(data, columns=headers)
        
        # 处理数据类型
        try:
            # 转换经纬度为浮点数
            if '经度' in df.columns:
                df['经度'] = pd.to_numeric(df['经度'], errors='coerce')
            if '纬度' in df.columns:
                df['纬度'] = pd.to_numeric(df['纬度'], errors='coerce')
            
            # 处理预计花费
            if '预计花费' in df.columns:
                df['预计花费'] = df['预计花费'].apply(lambda x: '0' if '免费' in x else x)
                df['预计花费'] = df['预计花费'].str.replace('约', '').str.replace('元', '').str.strip()
                df['预计花费'] = pd.to_numeric(df['预计花费'], errors='coerce')
        except Exception as e:
            print(f"数据类型转换错误: {e}")
        
        return df

    def get_ai_response(self,city:str,season:str,budget:str,day:str)->str:
        content=f'''
    我想去的城市是{city},想去的季节是{season},有{day}天的时间,一共的预算是{budget}元
'''
        messages=[
            {"role":"system","content":self.system_prompt},
            {"role":"user","content":content}
        ]
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False,
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
deepseek=Get_Deepseek()
# 测试get_ai_response函数
response = deepseek.get_ai_response('南京','夏天','100','3')
print("AI生成的表格文本:")
print(response)

# 测试parse_table_to_dataframe函数
try:
    df = deepseek.parse_table_to_dataframe(response)
    print("\n解析后的DataFrame:")
    print(df)
    print("\nDataFrame信息:")
    print(df.info())
except Exception as e:
    print(f"解析表格时出错: {e}")
