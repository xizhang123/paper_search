# paper_search
- 根据搜索条件（仅题目中的关键字），自动从arxiv和dblp检索相关论文，标注CCF推荐等级，整理成csv表格。
- 会自动将arxiv中具有CCF推荐等级的文章摘要，写入文本文件。如果运行有RWKV还会写入将摘要翻译。
- pip install requirements.txt 安装依赖 python main.py 运行程序
- 注意，同一行无法指定优先级，需要复杂逻辑请通过多行组合
- 设置查询条件，确认查询，然后等待一小会，查询结束会有弹窗提示
- 支持保存查询条件，便于重新加载有修改
- 翻译服务基于[https://github.com/josStorer/RWKV-Runner](https://github.com/josStorer/RWKV-Runner/releases)
- RWKV的安装配置非常简单，配置完成后选择合适的模型下载启动就可以使用翻译功能。
