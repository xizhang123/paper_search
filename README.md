# paper_search
- 自动从arxiv于dblp检索论文，整理成csv，标注CCF 推荐等级，并将高质量文献的摘要写入文本文件。如果运行有RWKV还会自动识别服务，添加文献摘要的翻译。
- pip install requirements.txt 安装依赖
- python main.py 运行程序
- 设置查询条件，然后等待一小会，查询结束会有弹窗提示
- 支持保存查询条件，便于重新加载有修改
- 注意，同一行无法指定优先级，需要复杂逻辑请通过多行组合
- 翻译服务使用[https://github.com/josStorer/RWKV-Runner](https://github.com/josStorer/RWKV-Runner/releases)，运行后选择合适的模型下载启动就好。
