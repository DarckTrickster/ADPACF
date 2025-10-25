import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class ADPACFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("АДПАЦФ - Анализ целей и функций")
        self.root.geometry("800x600")

        # Данные проекта
        self.project_name = "Новый проект"
        self.classifiers = []
        self.elements = {}
        self.structure = []
        self.current_stage = 0  # 0-ввод признаков, 1-ввод элементов, 2-анализ связей, 3-результаты

        # Создание интерфейса
        self.create_main_frame()
        self.create_menu()

        # Начать с ввода признаков
        self.show_classifiers_input()

    def create_main_frame(self):
        """Создание основного фрейма приложения"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новый проект", command=self.new_project)
        file_menu.add_command(label="Открыть", command=self.open_project)
        file_menu.add_command(label="Сохранить", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.about)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        self.root.config(menu=menubar)

    def clear_main_frame(self):
        """Очистка основного фрейма"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def new_project(self):
        """Создание нового проекта"""
        self.project_name = "Новый проект"
        self.classifiers = []
        self.elements = {}
        self.structure = []
        self.current_stage = 0
        self.clear_main_frame()
        self.show_classifiers_input()

    def open_project(self):
        """Открытие существующего проекта"""
        filepath = filedialog.askopenfilename(
            title="Открыть проект",
            filetypes=[("АДПАЦФ проекты", "*.adpacf"), ("Все файлы", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.project_name = data.get('project_name', "Новый проект")
                self.classifiers = data.get('classifiers', [])
                self.elements = data.get('elements', {})
                self.structure = data.get('structure', [])
                self.current_stage = data.get('current_stage', 0)
                self.clear_main_frame()
                if self.current_stage == 0:
                    self.show_classifiers_input()
                elif self.current_stage == 1:
                    self.show_elements_input()
                elif self.current_stage == 2:
                    self.show_analysis()
                else:
                    self.show_results()
                messagebox.showinfo("Успех", f"Проект '{self.project_name}' успешно загружен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить проект: {str(e)}")

    def save_project(self):
        """Сохранение проекта"""
        if not hasattr(self, 'project_name'):
            self.project_name = "Новый проект"
        filepath = filedialog.asksaveasfilename(
            title="Сохранить проект",
            defaultextension=".adpacf",
            filetypes=[("АДПАЦФ проекты", "*.adpacf"), ("Все файлы", "*.*")],
            initialfile=self.project_name
        )
        if filepath:
            try:
                data = {
                    'project_name': self.project_name,
                    'classifiers': self.classifiers,
                    'elements': self.elements,
                    'structure': self.structure,
                    'current_stage': self.current_stage
                }
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Успех", "Проект успешно сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить проект: {str(e)}")

    def about(self):
        """Окно 'О программе'"""
        about_text = (
            "АДПАЦФ - Автоматизированные диалоговые процедуры\n"
            "анализа целей и функций систем управления\n\n"
            "Версия 0.1\n"
            "Разработано для проекта"
        )
        messagebox.showinfo("О программе", about_text)

    def show_classifiers_input(self):
        """Показать интерфейс ввода признаков структуризации"""
        self.clear_main_frame()
        self.current_stage = 0
        ttk.Label(self.main_frame, text="Ввод признаков структуризации", font=('Arial', 14)).pack(pady=10)
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        self.new_classifier_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.new_classifier_var, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Добавить", command=self.add_classifier).pack(side=tk.LEFT)
        ttk.Button(input_frame, text="Вставить", command=lambda: self.paste_from_clipboard(self.new_classifier_var)).pack(side=tk.LEFT, padx=5)
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.classifiers_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.classifiers_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.classifiers_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.classifiers_listbox.config(yscrollcommand=scrollbar.set)
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.remove_classifier).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.edit_classifier).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Далее", command=self.go_to_elements_input).pack(side=tk.RIGHT)
        self.update_classifiers_list()

    def add_classifier(self):
        """Добавить новый признак структуризации"""
        new_classifier = self.new_classifier_var.get().strip()
        if new_classifier:
            if new_classifier not in self.classifiers:
                self.classifiers.append(new_classifier)
                self.new_classifier_var.set("")
                self.update_classifiers_list()
            else:
                messagebox.showwarning("Предупреждение", "Такой признак уже существует")
        else:
            messagebox.showwarning("Предупреждение", "Введите название признака")

    def remove_classifier(self):
        """Удалить выбранный признак структуризации"""
        selection = self.classifiers_listbox.curselection()
        if selection:
            index = selection[0]
            classifier = self.classifiers[index]
            if classifier in self.elements:
                del self.elements[classifier]
            self.classifiers.pop(index)
            self.update_classifiers_list()

    def edit_classifier(self):
        """Редактировать выбранный признак структуризации"""
        selection = self.classifiers_listbox.curselection()
        if selection:
            index = selection[0]
            old_classifier = self.classifiers[index]
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Редактирование признака")
            edit_window.geometry("300x100")
            ttk.Label(edit_window, text="Новое название признака:").pack(pady=5)
            edit_var = tk.StringVar(value=old_classifier)
            ttk.Entry(edit_window, textvariable=edit_var, width=30).pack(pady=5)
            def save_edit():
                new_name = edit_var.get().strip()
                if new_name and new_name != old_classifier:
                    if new_name not in self.classifiers:
                        self.classifiers[index] = new_name
                        if old_classifier in self.elements:
                            self.elements[new_name] = self.elements.pop(old_classifier)
                        self.update_classifiers_list()
                        edit_window.destroy()
                    else:
                        messagebox.showwarning("Предупреждение", "Такой признак уже существует")
                else:
                    messagebox.showwarning("Предупреждение", "Введите новое название признака")
            ttk.Button(edit_window, text="Сохранить", command=save_edit).pack(pady=5)

    def update_classifiers_list(self):
        """Обновить список признаков структуризации"""
        self.classifiers_listbox.delete(0, tk.END)
        for classifier in self.classifiers:
            self.classifiers_listbox.insert(tk.END, classifier)

    def go_to_elements_input(self):
        """Перейти к вводу элементов структуризации"""
        if len(self.classifiers) > 0:
            self.current_stage = 1
            self.show_elements_input()
        else:
            messagebox.showwarning("Предупреждение", "Добавьте хотя бы один признак структуризации")

    def show_elements_input(self):
        """Показать интерфейс ввода элементов структуризации"""
        self.clear_main_frame()
        self.current_stage = 1
        ttk.Label(self.main_frame, text="Ввод элементов структуризации", font=('Arial', 14)).pack(pady=10)
        classifier_frame = ttk.Frame(self.main_frame)
        classifier_frame.pack(fill=tk.X, pady=5)
        ttk.Label(classifier_frame, text="Текущий признак:").pack(side=tk.LEFT)
        self.current_classifier_var = tk.StringVar()
        if self.classifiers:
            self.current_classifier_var.set(self.classifiers[0])
        classifier_menu = ttk.OptionMenu(
            classifier_frame,
            self.current_classifier_var,
            self.classifiers[0] if self.classifiers else "",
            *self.classifiers
        )
        classifier_menu.pack(side=tk.LEFT, padx=5)
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        self.new_element_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.new_element_var, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Добавить", command=self.add_element).pack(side=tk.LEFT)
        ttk.Button(input_frame, text="Вставить", command=lambda: self.paste_from_clipboard(self.new_element_var)).pack(side=tk.LEFT, padx=5)
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.elements_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.elements_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.elements_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.elements_listbox.config(yscrollcommand=scrollbar.set)
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.remove_element).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.edit_element).pack(side=tk.LEFT, padx=5)
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        ttk.Button(nav_frame, text="Назад", command=self.show_classifiers_input).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="Далее", command=self.go_to_analysis).pack(side=tk.RIGHT)
        self.current_classifier_var.trace_add('write', lambda *_: self.update_elements_list())
        self.update_elements_list()

    def add_element(self):
        """Добавить новый элемент для текущего признака"""
        current_classifier = self.current_classifier_var.get()
        new_element = self.new_element_var.get().strip()
        if current_classifier and new_element:
            if current_classifier not in self.elements:
                self.elements[current_classifier] = []
            if new_element not in self.elements[current_classifier]:
                self.elements[current_classifier].append(new_element)
                self.new_element_var.set("")
                self.update_elements_list()
            else:
                messagebox.showwarning("Предупреждение", "Такой элемент уже существует")
        else:
            messagebox.showwarning("Предупреждение", "Введите название элемента")

    def remove_element(self):
        """Удалить выбранный элемент"""
        current_classifier = self.current_classifier_var.get()
        selection = self.elements_listbox.curselection()
        if current_classifier and selection:
            index = selection[0]
            self.elements[current_classifier].pop(index)
            self.update_elements_list()

    def edit_element(self):
        """Редактировать выбранный элемент"""
        current_classifier = self.current_classifier_var.get()
        selection = self.elements_listbox.curselection()
        if current_classifier and selection:
            index = selection[0]
            old_element = self.elements[current_classifier][index]
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Редактирование элемента")
            edit_window.geometry("300x100")
            ttk.Label(edit_window, text="Новое название элемента:").pack(pady=5)
            edit_var = tk.StringVar(value=old_element)
            ttk.Entry(edit_window, textvariable=edit_var, width=30).pack(pady=5)
            def save_edit():
                new_name = edit_var.get().strip()
                if new_name and new_name != old_element:
                    if new_name not in self.elements[current_classifier]:
                        self.elements[current_classifier][index] = new_name
                        self.update_elements_list()
                        edit_window.destroy()
                    else:
                        messagebox.showwarning("Предупреждение", "Такой элемент уже существует")
                else:
                    messagebox.showwarning("Предупреждение", "Введите новое название элемента")
            ttk.Button(edit_window, text="Сохранить", command=save_edit).pack(pady=5)

    def update_elements_list(self):
        """Обновить список элементов для текущего признака"""
        self.elements_listbox.delete(0, tk.END)
        current_classifier = self.current_classifier_var.get()
        if current_classifier and current_classifier in self.elements:
            for element in self.elements[current_classifier]:
                self.elements_listbox.insert(tk.END, element)

    def go_to_analysis(self):
        """Перейти к анализу связей"""
        valid = True
        missing = []
        for classifier in self.classifiers:
            if classifier not in self.elements or len(self.elements[classifier]) == 0:
                valid = False
                missing.append(classifier)
        if valid:
            self.current_stage = 2
            self.show_analysis()
        else:
            messagebox.showwarning(
                "Предупреждение",
                f"Для следующих признаков не указаны элементы:\n{', '.join(missing)}\nПожалуйста, добавьте элементы для всех признаков."
            )

    def show_analysis(self):
        """Показать интерфейс анализа связей"""
        self.clear_main_frame()
        self.current_stage = 2
        self.structure = []
        ttk.Label(self.main_frame, text="Анализ связей между элементами", font=('Arial', 14)).pack(pady=10)
        self.combination_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.combination_var, font=('Arial', 12), wraplength=700).pack(pady=20)
        ttk.Label(self.main_frame, text="Комментарий к связи:").pack(pady=5)
        self.comment_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.comment_var, width=50).pack(pady=10)
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady=20)
        ttk.Button(buttons_frame, text="Значимая связь", command=lambda: self.process_combination(True)).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Незначимая связь", command=lambda: self.process_combination(False)).pack(side=tk.LEFT, padx=10)
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        ttk.Button(nav_frame, text="Назад", command=self.show_elements_input).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="Завершить", command=self.go_to_results).pack(side=tk.RIGHT)
        self.combination_generator = self.generate_combinations()
        self.show_next_combination()

    def generate_combinations(self):
        """Генератор комбинаций элементов"""
        for i in range(len(self.classifiers) - 1):
            classifier1 = self.classifiers[i]
            classifier2 = self.classifiers[i + 1]
            if classifier1 in self.elements and classifier2 in self.elements:
                for element1 in self.elements[classifier1]:
                    for element2 in self.elements[classifier2]:
                        yield (classifier1, element1, classifier2, element2)

    def show_next_combination(self):
        """Показать следующую комбинацию"""
        try:
            self.current_combination = next(self.combination_generator)
            classifier1, element1, classifier2, element2 = self.current_combination
            text = f"Комбинация: '{element1}' ({classifier1}) → '{element2}' ({classifier2})"
            self.combination_var.set(text)
        except StopIteration:
            self.combination_var.set("Все комбинации проанализированы. Нажмите 'Завершить' для просмотра результатов.")

    def process_combination(self, is_valid):
        """Обработать текущую комбинацию"""
        if hasattr(self, 'current_combination'):
            classifier1, element1, classifier2, element2 = self.current_combination
            comment = self.comment_var.get().strip()
            if is_valid:
                self.structure.append({
                    'from_classifier': classifier1,
                    'from_element': element1,
                    'to_classifier': classifier2,
                    'to_element': element2,
                    'comment': comment
                })
                self.comment_var.set("")
            self.show_next_combination()

    def go_to_results(self):
        """Перейти к результатам"""
        self.current_stage = 3
        self.show_results()

    def show_results(self):
        """Показать результаты анализа"""
        self.clear_main_frame()
        self.current_stage = 3
        ttk.Label(self.main_frame, text="Результаты анализа", font=('Arial', 14)).pack(pady=10)
        result_frame = ttk.Frame(self.main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.tree = ttk.Treeview(result_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        self.tree["columns"] = ("type", "comment")
        self.tree.column("#0", width=300, minwidth=200)
        self.tree.column("type", width=150, minwidth=100)
        self.tree.column("comment", width=200, minwidth=150)
        self.tree.heading("#0", text="Элемент", anchor=tk.W)
        self.tree.heading("type", text="Тип", anchor=tk.W)
        self.tree.heading("comment", text="Комментарий", anchor=tk.W)
        self.build_structure_tree()

        # Добавление кнопок для редактирования
        edit_frame = ttk.Frame(self.main_frame)
        edit_frame.pack(fill=tk.X, pady=5)
        ttk.Button(edit_frame, text="Добавить элемент", command=self.add_tree_element).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="Удалить элемент", command=self.remove_tree_element).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="Переименовать элемент", command=self.rename_tree_element).pack(side=tk.LEFT, padx=5)

        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        ttk.Button(buttons_frame, text="Назад", command=self.show_analysis).pack(side=tk.LEFT)
        ttk.Button(buttons_frame, text="Экспорт в файл", command=self.export_results).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Печать", command=self.print_results).pack(side=tk.RIGHT, padx=5)

    def build_structure_tree(self):
        """Построить дерево структуры"""
        self.tree.delete(*self.tree.get_children())  # Очистить дерево перед построением
        first_classifier = self.classifiers[0] if self.classifiers else None
        if first_classifier and first_classifier in self.elements:
            for element in self.elements[first_classifier]:
                has_connections = any(
                    item['from_element'] == element and item['from_classifier'] == first_classifier
                    for item in self.structure
                )
                if has_connections:
                    node = self.tree.insert("", tk.END, text=element, values=(first_classifier, ""))
                    self.add_children(node, first_classifier, element)
                else:
                    self.tree.insert("", tk.END, text=element, values=(first_classifier, ""))

    def add_children(self, parent_node, parent_classifier, parent_element):
        """Добавить дочерние элементы к узлу"""
        connections = [
            item for item in self.structure
            if item['from_element'] == parent_element and item['from_classifier'] == parent_classifier
        ]
        for connection in connections:
            child_classifier = connection['to_classifier']
            child_element = connection['to_element']
            comment = connection['comment']
            has_children = any(
                item['from_element'] == child_element and item['from_classifier'] == child_classifier
                for item in self.structure
            )
            if has_children:
                node = self.tree.insert(parent_node, tk.END, text=child_element, values=(child_classifier, comment))
                self.add_children(node, child_classifier, child_element)
            else:
                self.tree.insert(parent_node, tk.END, text=child_element, values=(child_classifier, comment))

    def add_tree_element(self):
        """Добавить новый элемент в дерево"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите родительский элемент для добавления дочернего.")
            return

        parent_item = selected_item[0]
        parent_text = self.tree.item(parent_item, "text")
        parent_classifier = self.tree.item(parent_item, "values")[0]

        # Диалог для ввода нового элемента
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить элемент")
        add_window.geometry("500x300")
        ttk.Label(add_window, text="Название нового элемента:").pack(pady=5)
        new_element_var = tk.StringVar()
        ttk.Entry(add_window, textvariable=new_element_var, width=30).pack(pady=5)
        ttk.Label(add_window, text="Классификатор:").pack(pady=5)
        classifier_var = tk.StringVar()
        classifier_menu = ttk.OptionMenu(add_window, classifier_var, *self.classifiers)
        classifier_menu.pack(pady=5)
        ttk.Label(add_window, text="Комментарий:").pack(pady=5)
        comment_var = tk.StringVar()
        ttk.Entry(add_window, textvariable=comment_var, width=30).pack(pady=5)
        def save_new_element():
            new_element = new_element_var.get().strip()
            classifier = classifier_var.get()
            comment = comment_var.get().strip()
            if new_element and classifier:
                # Добавить новый элемент в структуру
                self.structure.append({
                    'from_classifier': parent_classifier,
                    'from_element': parent_text,
                    'to_classifier': classifier,
                    'to_element': new_element,
                    'comment': comment
                })
                # Обновить дерево
                self.build_structure_tree()
                add_window.destroy()
            else:
                messagebox.showwarning("Предупреждение", "Введите название элемента и выберите классификатор")
        ttk.Button(add_window, text="Добавить", command=save_new_element).pack(pady=10)

    def remove_tree_element(self):
        """Удалить выбранный элемент из дерева"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите элемент для удаления.")
            return

        item = selected_item[0]
        element_text = self.tree.item(item, "text")
        classifier = self.tree.item(item, "values")[0]

        # Удалить все связи, связанные с этим элементом
        self.structure = [conn for conn in self.structure if not (
            (conn['from_element'] == element_text and conn['from_classifier'] == classifier) or
            (conn['to_element'] == element_text and conn['to_classifier'] == classifier)
        )]

        # Обновить дерево
        self.build_structure_tree()

    def rename_tree_element(self):
        """Переименовать выбранный элемент в дереве"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите элемент для переименования.")
            return

        item = selected_item[0]
        if self.tree.parent(item) == "":
            messagebox.showwarning("Предупреждение", "Нельзя переименовывать главные элементы.")
            return

        old_element = self.tree.item(item, "text")
        classifier = self.tree.item(item, "values")[0]

        # Диалог для ввода нового имени
        rename_window = tk.Toplevel(self.root)
        rename_window.title("Переименовать элемент")
        rename_window.geometry("300x100")
        ttk.Label(rename_window, text="Новое название элемента:").pack(pady=5)
        new_name_var = tk.StringVar(value=old_element)
        ttk.Entry(rename_window, textvariable=new_name_var, width=30).pack(pady=5)
        def save_rename():
            new_name = new_name_var.get().strip()
            if new_name and new_name != old_element:
                # Обновить имя в структуре
                for conn in self.structure:
                    if conn['from_element'] == old_element and conn['from_classifier'] == classifier:
                        conn['from_element'] = new_name
                    if conn['to_element'] == old_element and conn['to_classifier'] == classifier:
                        conn['to_element'] = new_name
                # Обновить дерево
                self.build_structure_tree()
                rename_window.destroy()
            else:
                messagebox.showwarning("Предупреждение", "Введите новое название элемента")
        ttk.Button(rename_window, text="Сохранить", command=save_rename).pack(pady=5)

    def export_results(self):
        """Экспорт результатов в файл"""
        filepath = filedialog.asksaveasfilename(
            title="Экспорт результатов",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            initialfile=f"{self.project_name}_результаты.txt"
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Результаты анализа проекта: {self.project_name}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write("Структура целей и функций:\n")
                    if not self.structure:
                        f.write("Нет значимых связей между элементами\n")
                    else:
                        first_classifier = self.classifiers[0] if self.classifiers else None
                        if first_classifier and first_classifier in self.elements:
                            for element in self.elements[first_classifier]:
                                self.export_element_recursive(f, element, first_classifier, "", 0)
                messagebox.showinfo("Успех", "Результаты успешно экспортированы")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать результаты: {str(e)}")

    def export_element_recursive(self, file, element, classifier, comment, level):
        """Рекурсивный экспорт элемента и всех его потомков с комментариями"""
        indent = "    " * level
        if comment:
            file.write(f"{indent}{element} ({classifier}) [Комментарий: {comment}]\n")
        else:
            file.write(f"{indent}{element} ({classifier})\n")
        connections = [
            item for item in self.structure
            if item['from_element'] == element and item['from_classifier'] == classifier
        ]
        for connection in connections:
            child_element = connection['to_element']
            child_classifier = connection['to_classifier']
            child_comment = connection['comment']
            self.export_element_recursive(file, child_element, child_classifier, child_comment, level + 1)

    def print_results(self):
        """Печать результатов"""
        messagebox.showinfo("Печать", "Функция печати будет реализована в следующей версии")

    def paste_from_clipboard(self, var):
        """Вставить текст из буфера обмена в переменную"""
        try:
            clipboard_text = self.root.clipboard_get()
            var.set(clipboard_text)
        except tk.TclError:
            messagebox.showwarning("Предупреждение", "Буфер обмена пуст")

if __name__ == "__main__":
    root = tk.Tk()
    app = ADPACFApp(root)
    root.mainloop()