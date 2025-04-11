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
  
![image](https://github.com/user-attachments/assets/57b35b90-1b0a-4360-9747-02a3d4756163)
- 查询完毕

![image](https://github.com/user-attachments/assets/a0245f0c-132d-4734-bac9-8037b1709bc2)
- 表格整理

![image](https://github.com/user-attachments/assets/8777a9b7-bc24-48a2-82e5-ac0bc3c90089)
![image](https://github.com/user-attachments/assets/503cef87-084e-4467-91b8-c8c17d76bfde)
- 摘要翻译（百度翻译版本，RWKV免费，效果可能不如展示的好）

![image](https://github.com/user-attachments/assets/5be3c53e-8968-4748-a3a3-1353950ab5b1)

- 自认为90%工作是 Trae + Clauld 3.5 Sonnet 完成的。。。
