import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QScrollArea, QLabel, QSpinBox,
                             QFileDialog)
from PyQt6.QtCore import Qt
from translator import translate_zh_en

class SearchUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.active_text_edit = None
        self.setWindowTitle('文献检索系统')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(main_widget)
        
        # 添加使用说明标签
        instruction_label = QLabel()
        instruction_label.setText('使用说明：\n'
        '1. 行内支持简单布尔运算：\n'
        '空格" "代表AND运算、竖线"|"代表OR运算、下划线"_"用于转义空格\n'
        '2. 行间关系：\n'
        '各行的逻辑运算独立进行，相当于使用括号指定优先级\n'
        '点击新增按钮添加行，各行之间通过OR运算连接，转义按钮用于将当前行中的空格变成下划线')
        instruction_label.setStyleSheet('QLabel { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }')
        main_layout.addWidget(instruction_label)
        
        # 创建水平布局用于放置滚动区域和按钮
        content_layout = QHBoxLayout()
        
        # 创建左侧滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.text_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        
        # 设置滚动区域的大小策略
        scroll_area.setMinimumWidth(int(self.width() * 0.7))
        
        # 添加初始文本框
        self.add_text_edit()
        
        # 创建右侧按钮布局
        button_layout = QVBoxLayout()
        
        # 创建按钮
        add_button = QPushButton('新增')
        copy_button = QPushButton('复制')
        escape_button = QPushButton('转义')
        delete_button = QPushButton('删除')
        translate_button = QPushButton('辅助翻译')
        save_button = QPushButton('保存查询')
        load_button = QPushButton('加载历史')
        confirm_button = QPushButton('确认查询')
        
        # 连接按钮信号
        add_button.clicked.connect(self.add_text_edit)
        copy_button.clicked.connect(self.copy_text_edit)
        escape_button.clicked.connect(self.escape_text)
        delete_button.clicked.connect(self.delete_text_edit)
        translate_button.clicked.connect(self.translate_text)
        confirm_button.clicked.connect(self.confirm_text)
        save_button.clicked.connect(self.save_query)
        load_button.clicked.connect(self.load_history)
        
        # 创建数字输入框用于设置最大返回数量
        self.max_results_spinbox = QSpinBox()
        self.max_results_spinbox.setRange(1, 999)
        self.max_results_spinbox.setValue(5)
        self.max_results_spinbox.setPrefix('数量: ')
        self.max_results_spinbox.setMinimumWidth(150)  # 设置最小宽度为150像素
        
        # 将按钮和数字输入框添加到布局中
        button_layout.addWidget(add_button)
        button_layout.addWidget(copy_button)
        button_layout.addWidget(escape_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(translate_button)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)
        button_layout.addWidget(self.max_results_spinbox)
        button_layout.addStretch()
        
        # 将滚动区域和按钮布局添加到水平布局
        content_layout.addWidget(scroll_area)
        content_layout.addLayout(button_layout)
        
        # 将水平布局添加到主布局
        main_layout.addLayout(content_layout)
    
    def add_text_edit(self):
        """添加新的文本输入框"""
        text_edit = QTextEdit()
        text_edit.setMinimumHeight(20)
        text_edit.setStyleSheet("QTextEdit { font-size: 18px; }")
        text_edit.setAcceptRichText(False)
        text_edit.setMouseTracking(True)
        text_edit.setTextInteractionFlags(text_edit.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByMouse)
        # 使用mouseReleaseEvent来处理文本框激活，这样不会影响文本选择
        text_edit.mouseReleaseEvent = lambda e, te=text_edit: self.set_active_text_edit(te)
        
        # 如果存在激活的文本框，在其后插入新文本框
        if self.active_text_edit:
            text_edits = [self.text_layout.itemAt(i).widget() for i in range(self.text_layout.count())]
            index = text_edits.index(self.active_text_edit)
            self.text_layout.insertWidget(index + 1, text_edit)
        else:
            self.text_layout.addWidget(text_edit)
        self.active_text_edit = text_edit
        # 更新激活文本框的边框颜色
        self.set_active_text_edit(text_edit)

    def set_active_text_edit(self, text_edit):
        """设置当前活动的文本框"""
        # 恢复所有文本框的默认样式
        text_edits = [self.text_layout.itemAt(i).widget() for i in range(self.text_layout.count())]
        for te in text_edits:
            te.setStyleSheet("QTextEdit { font-size: 18px; }")
        
        # 设置当前激活的文本框样式
        text_edit.setStyleSheet("QTextEdit { font-size: 18px; border: 2px solid #87CEEB; }")
        self.active_text_edit = text_edit

    def delete_text_edit(self):
        """删除文本输入框"""
        text_edits = [self.text_layout.itemAt(i).widget() for i in range(self.text_layout.count())]
        if not text_edits:
            return
            
        if len(text_edits) == 1:
            # 当只有一个文本框时，清空内容
            text_edits[0].clear()
            return
            
        if self.active_text_edit:
            # 删除激活的文本框
            index = text_edits.index(self.active_text_edit)
            self.text_layout.removeWidget(self.active_text_edit)
            self.active_text_edit.deleteLater()
            # 将激活状态转移到前一个文本框
            if index > 0:
                self.active_text_edit = text_edits[index - 1]
            else:
                self.active_text_edit = text_edits[1] if len(text_edits) > 1 else None
            # 更新激活文本框的边框颜色
            if self.active_text_edit:
                self.set_active_text_edit(self.active_text_edit)
        else:
            # 如果没有激活的文本框，删除最后一个
            last_text_edit = text_edits[-1]
            self.text_layout.removeWidget(last_text_edit)
            last_text_edit.deleteLater()

    def escape_text(self):
        """将当前激活文本框中的空格转换为下划线"""
        if self.active_text_edit and isinstance(self.active_text_edit, QTextEdit):
            current_text = self.active_text_edit.toPlainText()
            escaped_text = current_text.replace(' ', '_')
            self.active_text_edit.setPlainText(escaped_text)
    
    def copy_text_edit(self):
        """复制最后一个文本框的内容到新文本框"""
        text_edits = [self.text_layout.itemAt(i).widget() for i in range(self.text_layout.count())]
        if text_edits:
            last_text = text_edits[-1].toPlainText()
            self.add_text_edit()
            self.active_text_edit.setPlainText(last_text)

    def translate_text(self):
        """翻译当前激活文本框中的文本"""
        if self.active_text_edit and isinstance(self.active_text_edit, QTextEdit):
            current_text = self.active_text_edit.toPlainText()
            translated_text = translate_zh_en(current_text)
            if translated_text:
                self.active_text_edit.setPlainText(translated_text)

    def save_query(self):
        """保存当前所有文本框的内容到文件"""
        text_edits = [self.text_layout.itemAt(i).widget() for i in range(self.text_layout.count())]
        contents = [text_edit.toPlainText() for text_edit in text_edits if text_edit.toPlainText().strip()]
        
        if not contents:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, '保存查询', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contents))
    
    def load_history(self):
        """从文件加载历史查询"""
        file_path, _ = QFileDialog.getOpenFileName(self, '加载历史', '', 'Text Files (*.txt);;All Files (*)')
        if not file_path:
            return
            
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        # 清除现有的文本框，并重置激活状态
        self.active_text_edit = None
        while self.text_layout.count() > 0:
            widget = self.text_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        # 为每一行创建新的文本框
        for line in lines:
            text_edit = QTextEdit()
            text_edit.setMinimumHeight(20)
            text_edit.setStyleSheet("QTextEdit { font-size: 18px; }")
            text_edit.setAcceptRichText(False)
            text_edit.setMouseTracking(True)
            text_edit.setTextInteractionFlags(text_edit.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByMouse)
            text_edit.mouseReleaseEvent = lambda e, te=text_edit: self.set_active_text_edit(te)
            text_edit.setPlainText(line)
            self.text_layout.addWidget(text_edit)
            
        # 如果没有内容，至少添加一个空文本框
        if not lines:
            self.add_text_edit()
        else:
            # 设置最后一个文本框为激活状态
            text_edits = [self.text_layout.itemAt(i).widget() for i in range(self.text_layout.count())]
            if text_edits:
                self.set_active_text_edit(text_edits[-1])
    
    def confirm_text(self):
        """确认文本并生成查询语句"""
        text_edits = [self.text_layout.itemAt(i).widget() for i in range(self.text_layout.count())]
        
        # 获取每个文本框的内容并处理
        query_parts = []  # 用于arxiv查询
        dblp_query_list = []  # 用于dblp查询
        
        for text_edit in text_edits:
            text = text_edit.toPlainText().strip()
            if text:
                # 对于dblp查询，先将竖线替换为带空格的格式，然后为每个关键词添加$后缀
                text = text.replace('|', ' | ')
                words = [word.strip() + '$' if word.strip() != '|' else word.strip() 
                         for word in text.split()]
                formatted_text = ' '.join(words).replace('_', ' ')
                dblp_query_list.append(formatted_text)
                
                # 对于arxiv查询，先将竖线替换为OR
                text = text.replace('|', ' OR ')
                words = text.split()
                
                keywords = []
                for word in words:
                    if word == 'OR':
                        keywords.append('OR')
                    else:
                        keywords.append(f'ti:"{word.strip()}"')
                
                if keywords:
                    query = ' AND '.join(keywords)
                    query = query.replace('AND OR AND', 'OR')
                    query_parts.append(f'({query})')
        
        # 生成最终的查询语句
        if query_parts:
            arxiv_query = f'{" OR ".join(query_parts)}'
            arxiv_query = arxiv_query.replace('_', ' ')
            return arxiv_query, dblp_query_list
        return None, None

def main():
    app = QApplication(sys.argv)
    window = SearchUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()