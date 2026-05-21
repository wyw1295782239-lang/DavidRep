from openai import OpenAI
import traceback
import pandas as pd
import os

class Get_Chat:
    def __init__(self):
        try:
            self.client = OpenAI(
                api_key="sk-fb929c78ded9437b997592f44c4e0ebc",
                base_url="https://api.deepseek.com"
            )
            self.api_available = True
        except Exception as e:
            print(f"API初始化失败: {e}")
            self.api_available = False
        
        # 从data.csv读取景点数据
        self.sightseeing_data = self._load_sightseeing_data()
        
        # 构建系统提示词，包含data.csv中的景点数据
        self.system_prompt = self._build_system_prompt()
    
    def _load_sightseeing_data(self):
        """从data.csv加载景点数据"""
        try:
            # 获取data.csv的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, '..', 'data', 'data_control.csv')
            df = pd.read_csv(data_path, encoding='utf-8')
            
            # 提取关键字段
            df = df[['景点名称', '城市名称', '省份', '所在区域', '评分', '评论数量', '热度评分', '实际票价', '标签']]
            return df.to_dict('records')
        except Exception as e:
            print(f"加载景点数据失败: {e}")
            return []
    
    def _build_system_prompt(self):
        """构建包含景点数据的系统提示词"""
        # 基础提示词
        prompt = """
        你是一个专业的旅游智能客服，需要根据用户的问题提供准确、友好的旅游信息。
        请基于以下景点数据库回答用户问题：
        
        景点数据库（数据来自data.csv）：
        """
        
        # 添加景点数据（最多显示50个景点）
        if self.sightseeing_data:
            for i, spot in enumerate(self.sightseeing_data[:50], 1):
                prompt += f"{i}. 景点名称：{spot.get('景点名称', '')}，城市：{spot.get('城市名称', '')}，省份：{spot.get('省份', '')}，区域：{spot.get('所在区域', '')}，评分：{spot.get('评分', '')}，评论数：{spot.get('评论数量', '')}，热度：{spot.get('热度评分', '')}，票价：{spot.get('实际票价', '')}，标签：{spot.get('标签', '')}\n"
        
        # 回答要求
        prompt += """
        
        回答要求：
        1. 回答必须基于上述景点数据库
        2. 如果数据库中没有相关信息，请明确说明"数据库中未找到相关信息"
        3. 回答要准确、专业、友好
        4. 回答要与旅游相关，不要回答与旅游无关的问题
        5. 回答要简洁明了，避免冗长
        6. 如果用户询问的景点不在数据库中，不要编造信息
        """
        
        return prompt
        
        # 本地回退回答

    
    def get_chat_response(self, user_question):
        """
        获取智能客服的回答
        
        Args:
            user_question: 用户的问题
            
        Returns:
            str: 智能客服的回答
        """
        # 如果API可用，尝试调用API
        if self.api_available:
            try:
                messages=[
                    {"role":"system","content":self.system_prompt},
                    {"role":"user","content":user_question}
                ]
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    stream=False,
                    temperature=0.3,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"API调用失败: {e}")
                traceback.print_exc()
                return "抱歉，AI服务暂时不可用，请稍后再试。"
        else:
            return "抱歉，AI服务暂时不可用，请稍后再试。"
question=Get_Chat()
print(question.get_chat_response('北京有什么好玩的地方吗'))



