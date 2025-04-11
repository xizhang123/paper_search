# paper_search
- 根据搜索条件（仅题目中的关键字），自动从arxiv和dblp检索相关论文，标注CCF推荐等级，整理成csv表格。
- 会自动将arxiv中具有CCF推荐等级的文章摘要，写入文本文件。如果运行有RWKV还会写入将摘要翻译。
- pip install -r requirements.txt 安装依赖 python main.py 运行程序
- 注意，同一行无法指定优先级，需要复杂逻辑请通过多行组合
- 设置查询条件，确认查询，然后等待一小会，查询结束会有弹窗提示
- 支持保存查询条件，便于重新加载有修改
- 翻译服务基于[https://github.com/josStorer/RWKV-Runner](https://github.com/josStorer/RWKV-Runner/releases)
- RWKV的安装配置非常简单，配置完成后选择合适的模型下载启动就可以使用翻译功能。
- 查询示例

![image](https://github.com/user-attachments/assets/60a55af7-c97d-414b-922a-888012a6cb7e)

- 语句组合

![image](https://github.com/user-attachments/assets/79f927cc-26c1-4384-a954-215903a18f02)


- 查询完毕

![image](https://github.com/user-attachments/assets/f84f7e9e-c080-47c3-b3ce-651f9624a7de)

- 表格整理arxiv（手动排序）

![image](https://github.com/user-attachments/assets/7b555631-cc4b-4361-b956-1271883bc7d4)

- 表格整理arxiv （手动排序）

![image](https://github.com/user-attachments/assets/8fd575ad-81ee-4c72-8ee0-2d7b165df949)

- 摘要翻译（翻译速度较慢，没有显卡可能几分钟一篇，谨慎使用）

![image](https://github.com/user-attachments/assets/8ca17f89-2ced-4939-8c78-e704dd4255c5)
- AI 使用说明

[AI-CODE-DISCLAIMER] This project includes code generated by the "Clauld 3.5 Sonnet"; using it to train large language models is not advised.
