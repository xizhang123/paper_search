import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui import SearchUI
from arxiv_search import search_papers as arxiv_search
from dblp_search import search_papers as dblp_search

class MainApp(SearchUI):
    def __init__(self):
        super().__init__()
    
    def confirm_text(self):
        """重写确认按钮的功能，添加搜索和结果处理"""
        arxiv_query, dblp_queries = super().confirm_text()
        max_results = self.max_results_spinbox.value()
        
        if arxiv_query and dblp_queries:
            try:
                # 执行arxiv搜索
                arxiv_papers, arxiv_abstracts = arxiv_search(arxiv_query, max_results=max_results)
                # 执行dblp搜索
                dblp_papers = dblp_search(dblp_queries, max_results=max_results)
                
                # 显示结果统计
                message = f"搜索完成！\n\n"
                message += f"arXiv搜索结果：\n"
                message += f"- 找到{arxiv_papers}篇论文\n"
                message += f"- 其中{arxiv_abstracts}篇CCF收录论文的摘要已翻译\n\n"
                message += f"DBLP搜索结果：\n"
                message += f"- 找到{dblp_papers}篇论文"
                
                QMessageBox.information(self, '搜索结果', message)
                
            except Exception as e:
                QMessageBox.warning(self, '错误', f'搜索过程中出现错误：{str(e)}')
        else:
            QMessageBox.warning(self, '提示', '请输入搜索关键词！')

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()