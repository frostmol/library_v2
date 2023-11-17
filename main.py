import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, \
    QStackedWidget, QMessageBox, QComboBox, QHBoxLayout
from datetime import datetime


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.books = []
        self.load_books_from_file()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Электронная библиотека")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.central_widget_layout = QVBoxLayout()
        self.central_widget_layout.addWidget(self.stacked_widget)
        self.central_widget.setLayout(self.central_widget_layout)

        self.home_widget = QWidget(self)
        self.home_layout = QVBoxLayout()
        self.home_widget.setLayout(self.home_layout)

        self.add_book_btn = QPushButton("Добавить книгу", self)
        self.add_book_btn.clicked.connect(self.show_add_book_form)

        self.search_id_btn = QPushButton("Поиск по ID", self)
        self.search_id_btn.clicked.connect(self.show_search_id_form)

        self.search_title_author_btn = QPushButton("Поиск по названию/автору", self)
        self.search_title_author_btn.clicked.connect(self.show_search_title_author_form)

        self.statistics_btn = QPushButton("Статистика по периоду", self)
        self.statistics_btn.clicked.connect(self.show_statistics_form)

        self.home_layout.addWidget(self.add_book_btn)
        self.home_layout.addWidget(self.search_id_btn)
        self.home_layout.addWidget(self.search_title_author_btn)
        self.home_layout.addWidget(self.statistics_btn)

        self.stacked_widget.addWidget(self.home_widget)

        self.add_book_form = QWidget(self)
        self.add_book_form_layout = QVBoxLayout()
        self.add_book_form.setLayout(self.add_book_form_layout)

        self.book_title_label = QLabel("Название книги:", self)
        self.book_title_input = QLineEdit(self)
        self.book_author_label = QLabel("Автор книги:", self)
        self.book_author_input = QLineEdit(self)
        self.add_book_submit_btn = QPushButton("Добавить", self)
        self.add_book_submit_btn.clicked.connect(self.add_book)
        self.add_book_cancel_btn = QPushButton("Вернуться", self)
        self.add_book_cancel_btn.clicked.connect(self.show_home_page)

        self.add_book_form_layout.addWidget(self.book_title_label)
        self.add_book_form_layout.addWidget(self.book_title_input)
        self.add_book_form_layout.addWidget(self.book_author_label)
        self.add_book_form_layout.addWidget(self.book_author_input)
        self.add_book_form_layout.addWidget(self.add_book_submit_btn)
        self.add_book_form_layout.addWidget(self.add_book_cancel_btn)

        self.stacked_widget.addWidget(self.add_book_form)

        self.search_id_form = QWidget(self)
        self.search_id_layout = QVBoxLayout()
        self.search_id_form.setLayout(self.search_id_layout)

        self.search_id_label = QLabel("Введите ID книги:", self)
        self.search_id_input = QLineEdit(self)
        self.search_id_submit_btn = QPushButton("Найти", self)
        self.search_id_submit_btn.clicked.connect(self.search_by_id)
        self.search_id_back_btn = QPushButton("Вернуться", self)
        self.search_id_back_btn.clicked.connect(self.show_home_page)

        self.search_id_layout.addWidget(self.search_id_label)
        self.search_id_layout.addWidget(self.search_id_input)
        self.search_id_layout.addWidget(self.search_id_submit_btn)
        self.search_id_layout.addWidget(self.search_id_back_btn)

        self.stacked_widget.addWidget(self.search_id_form)

        self.search_title_author_form = QWidget(self)
        self.search_title_author_layout = QVBoxLayout()
        self.search_title_author_form.setLayout(self.search_title_author_layout)

        self.search_title_author_label = QLabel("Введите название или автора книги:", self)
        self.search_title_author_input = QLineEdit(self)
        self.search_title_author_submit_btn = QPushButton("Найти", self)
        self.search_title_author_submit_btn.clicked.connect(self.search_by_title_author)
        self.search_title_author_back_btn = QPushButton("Вернуться", self)
        self.search_title_author_back_btn.clicked.connect(self.show_home_page)

        self.search_title_author_layout.addWidget(self.search_title_author_label)
        self.search_title_author_layout.addWidget(self.search_title_author_input)
        self.search_title_author_layout.addWidget(self.search_title_author_submit_btn)
        self.search_title_author_layout.addWidget(self.search_title_author_back_btn)

        self.stacked_widget.addWidget(self.search_title_author_form)

        self.statistics_form = QWidget(self)
        self.statistics_layout = QVBoxLayout()
        self.statistics_form.setLayout(self.statistics_layout)

        self.statistics_options_combo = QComboBox()
        self.statistics_options_combo.addItems(["Книга", "Автор", "Все книги"])
        self.statistics_options_combo.currentIndexChanged.connect(self.update_statistics_input)

        self.statistics_input_layout = QHBoxLayout()

        self.statistics_input_label = QLabel("Введите название книги/имя автора:", self)
        self.statistics_input = QLineEdit(self)
        self.statistics_input.setVisible(False)

        self.statistics_input_layout.addWidget(self.statistics_input_label)
        self.statistics_input_layout.addWidget(self.statistics_input)

        self.start_date_label = QLabel("Начальная дата (гггг-мм-дд):", self)
        self.start_date_input = QLineEdit(self)
        self.end_date_label = QLabel("Конечная дата (гггг-мм-дд):", self)
        self.end_date_input = QLineEdit(self)
        self.statistics_submit_btn = QPushButton("Показать статистику", self)
        self.statistics_submit_btn.clicked.connect(self.show_statistics)
        self.statistics_back_btn = QPushButton("Вернуться", self)
        self.statistics_back_btn.clicked.connect(self.show_home_page)

        self.statistics_layout.addWidget(self.statistics_options_combo)
        self.statistics_layout.addLayout(self.statistics_input_layout)
        self.statistics_layout.addWidget(self.start_date_label)
        self.statistics_layout.addWidget(self.start_date_input)
        self.statistics_layout.addWidget(self.end_date_label)
        self.statistics_layout.addWidget(self.end_date_input)
        self.statistics_layout.addWidget(self.statistics_submit_btn)
        self.statistics_layout.addWidget(self.statistics_back_btn)

        self.stacked_widget.addWidget(self.statistics_form)



    def load_books_from_file(self):
        try:
            with open("library.json", "r") as file:
                self.books = json.load(file)
        except FileNotFoundError:
            pass

    def save_books_to_file(self):
        with open("library.json", "w") as file:
            json.dump(self.books, file, indent=2)

    def show_home_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_add_book_form(self):
        self.book_title_input.clear()
        self.book_author_input.clear()
        self.stacked_widget.setCurrentIndex(1)

    def show_search_id_form(self):
        self.search_id_input.clear()
        self.stacked_widget.setCurrentIndex(2)

    def show_search_title_author_form(self):
        self.search_title_author_input.clear()
        self.stacked_widget.setCurrentIndex(3)

    def update_statistics_input(self, index):
        if index == 0:  # "Книга"
            self.statistics_input_label.setText("Введите название книги:")
            self.statistics_input.setVisible(True)
            self.statistics_input.setEnabled(True)
        elif index == 1:  # "Автор"
            self.statistics_input_label.setText("Введите имя автора:")
            self.statistics_input.setVisible(True)
            self.statistics_input.setEnabled(True)
        else:
            self.statistics_input.setVisible(False)

    def show_statistics_form(self):
        self.start_date_input.clear()
        self.end_date_input.clear()
        self.statistics_options_combo.setCurrentIndex(0)  # Сбросить выбранную опцию на "Книга"
        self.statistics_input_label.setText("Введите название книги:")
        self.statistics_input.setVisible(True)
        self.stacked_widget.setCurrentIndex(4)

    def add_book(self):
        book_title = self.book_title_input.text()
        book_author = self.book_author_input.text()

        if book_title and book_author:
            last_id = max([0] + [int(book["id"]) for book in self.books])
            new_id = str(last_id + 1)
            book = {
                "id": new_id,
                "title": book_title,
                "author": book_author,
                "history": []
            }
            self.books.append(book)
            self.save_books_to_file()
            QMessageBox.information(self, "Успех", "Книга успешно добавлена.")
            self.show_home_page()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите название и автора книги.")

    def search_by_id(self):
        book_id = self.search_id_input.text()
        found_book = next((book for book in self.books if book["id"] == book_id), None)
        if found_book:
            history = found_book["history"]
            history_text = "\n".join([f"{entry['reader']} - {entry['action']} ({entry['date']})" for entry in history])
            result = f"ID: {found_book['id']}\nНазвание: {found_book['title']}\nАвтор: {found_book['author']}\nИстория выдачи:\n{history_text}"
            QMessageBox.information(self, "Результат поиска", result)
        else:
            QMessageBox.warning(self, "Результат поиска", "Книга не найдена.")

    def search_by_title_author(self):
        query = self.search_title_author_input.text()
        found_books = [book for book in self.books if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]
        if found_books:
            result = ""
            for book in found_books:
                history = book["history"]
                history_text = "\n".join([f"{entry['reader']} - {entry['action']} ({entry['date']})" for entry in history])
                result += f"ID: {book['id']}\nНазвание: {book['title']}\nАвтор: {book['author']}\nИстория выдачи:\n{history_text}\n\n"
            QMessageBox.information(self, "Результат поиска", result)
        else:
            QMessageBox.warning(self, "Результат поиска", "Книги не найдены.")

    def show_book_statistics(self):
        print("Inside show_book_statistics")
        book_title = self.statistics_input.text().strip()
        found_books = [book for book in self.books if book_title.lower() == book["title"].lower()]

        if found_books:
            book_statistics = self.generate_statistics(found_books, self.start_date_input.text(),
                                                       self.end_date_input.text())
            self.show_statistics_dialog(book_statistics)
        else:
            QMessageBox.warning(self, "Результат поиска", "Книга не найдена.")

    def show_author_statistics(self):
        print("Inside show_author_statistics")
        author_name = self.statistics_input.text().strip()
        found_books = [book for book in self.books if author_name.lower() == book["author"].lower()]

        if found_books:
            author_statistics = self.generate_statistics(found_books, self.start_date_input.text(),
                                                         self.end_date_input.text())
            self.show_statistics_dialog(author_statistics)
        else:
            QMessageBox.warning(self, "Результат поиска", "Автор не найден.")

    def show_all_statistics(self):
        print("Inside show_all_statistics")
        all_statistics = self.generate_statistics(self.books)
        self.show_statistics_dialog(all_statistics)

    def generate_statistics(self, books, start_date=None, end_date=None):
        print("Inside generate_statistics")
        statistics = {}
        print("Start Date:", start_date)
        print("End Date:", end_date)

        for book in books:
            count = 0
            history = book["history"]
            for entry in history:
                entry_date = entry["date"]
                print("Start Date Type:", type(start_date))  # Убедимся, что это строковый тип данных
                print("Start Date Value:", start_date)  # Выведем значение начальной даты
                print("End Date Type:", type(end_date))  # Убедимся, что это строковый тип данных
                print("End Date Value:", end_date)  # Выведем значение конечной даты
                print("Entry Date Type:", type(entry_date))  # Убедимся, что это строковый тип данных
                print("Entry Date Value:", entry_date)  # Выведем саму дату
                if start_date <= entry_date <= end_date:
                    count += 1
            if count > 0:
                author = book["author"]
                if author not in statistics:
                    statistics[author] = {}
                statistics[author][book["title"]] = count
        return statistics

    def show_statistics_dialog(self, statistics):
        if statistics:
            QMessageBox.information(self, "Статистика", statistics)
        else:
            QMessageBox.warning(self, "Статистика", "Нет данных для статистики.")

    def show_statistics(self):
        print("Inside show_statistics")
        option = self.statistics_options_combo.currentText()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        query = self.statistics_input.text()
        print("Option:", option)
        print("Query:", query)
        print("Start Date:", start_date)
        print("End Date:", end_date)

        if option == "Все книги":
            statistics = self.generate_statistics(self.books, start_date, end_date)
            statistics_str = ""
            for author, books in statistics.items():
                statistics_str += f"{author}:\n"
                for book, count in books.items():
                    statistics_str += f"{book} - {count}\n"
                statistics_str += "\n"
            self.show_statistics_dialog(statistics_str)
            return  # Завершаем функцию для опции "Все книги"

        if start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неверный формат даты. Используйте гггг-мм-дд.")
                return

            if option == "Книга":
                if not query:
                    QMessageBox.warning(self, "Ошибка", "Введите название книги для статистики.")
                    return
                filtered_books = [book for book in self.books if query.lower() == book["title"].lower()]
                print("Filtered Books (Книга):", filtered_books)  # Отладочный вывод
            elif option == "Автор":
                if not query:
                    QMessageBox.warning(self, "Ошибка", "Введите имя автора для статистики.")
                    return
                filtered_books = [book for book in self.books if query.lower() == book["author"].lower()]
                print("Filtered Books (Автор):", filtered_books)  # Отладочный вывод
            else:
                filtered_books = self.books


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("style.css",encoding="utf-8").read())  # Применить CSS-стили
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
