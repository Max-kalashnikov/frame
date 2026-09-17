from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUTPUT = "Отчет_ПР2_Калашников_МВ.docx"


def font(run, size=11, bold=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:cs"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)


def paragraph(doc, text, indent=True):
    item = doc.add_paragraph()
    item.paragraph_format.space_after = Pt(4)
    item.paragraph_format.line_spacing = 1.1
    if indent:
        item.paragraph_format.first_line_indent = Cm(1.0)
    font(item.add_run(text))


def heading(doc, text):
    item = doc.add_paragraph(style="Heading 1")
    item.paragraph_format.space_before = Pt(8)
    item.paragraph_format.space_after = Pt(4)
    font(item.add_run(text), 12, True)


def shade(cell, color):
    props = cell._tc.get_or_add_tcPr()
    fill = OxmlElement("w:shd")
    fill.set(qn("w:fill"), color)
    props.append(fill)


def table(doc):
    rows = (
        ("Раздел 01 Основы Python", "Коллекции; итерации и циклы; проект Приложение Холодильник."),
        ("Раздел 03 Python новый уровень", "Модули и пакеты; интроспекция; документация; исключения; файлы; контекстные менеджеры; практика."),
        ("Раздел 03 Расширенные возможности", "Пространство имен; итераторы и генераторы; lambda функции."),
    )
    result = doc.add_table(rows=1, cols=2)
    result.autofit = False
    widths = (Cm(4.2), Cm(12.5))
    for index, value in enumerate(("Раздел", "Темы ПР2")):
        cell = result.rows[0].cells[index]
        cell.width = widths[index]
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        shade(cell, "1F4E78")
        item = cell.paragraphs[0]
        item.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = item.add_run(value)
        font(run, 9, True)
        run.font.color.rgb = RGBColor(255, 255, 255)
    for row_index, values in enumerate(rows):
        cells = result.add_row().cells
        for index, value in enumerate(values):
            cell = cells[index]
            cell.width = widths[index]
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if row_index % 2:
                shade(cell, "F3F6F8")
            item = cell.paragraphs[0]
            item.paragraph_format.space_after = Pt(0)
            font(item.add_run(value), 9)


doc = Document()
section = doc.sections[0]
section.top_margin = Cm(1.8)
section.bottom_margin = Cm(1.8)
section.left_margin = Cm(2.0)
section.right_margin = Cm(2.0)

style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
style.font.size = Pt(11)

title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(10)
font(title.add_run("Отчет по практической работе 2"), 15, True)

for value in (
    "Дисциплина: Технологии разработки приложений на базе фреймворков",
    "Тема: Основы Python коллекции функции циклы и расширенные возможности Python",
    "Индивидуальный проект: Система мониторинга пользовательских заявок",
    "Студент: Калашников М. В.    Группа: ЭФБО-10-24    Год: 2026",
):
    paragraph(doc, value, False)

paragraph(doc, "В работе стартовый сценарий ПР1 переработан в приложение, работающее с набором пользовательских заявок, их статусами и событиями обработки.")
heading(doc, "Материалы Яндекс Практикума")
table(doc)
heading(doc, "Индивидуальный проект")
paragraph(doc, "Для системы мониторинга заявок реализованы создание, поиск и сортировка заявок, смена статуса, отмена, проверка срочности, фиксация событий и расчёт статистики. Логика разделена между main.py, requests.py, monitoring.py, storage.py и utils.py.")
paragraph(doc, "Данные сохраняются в data/requests.json и data/events.json. Заявка представлена словарем с идентификатором, темой, пользователем, приоритетом, статусом, временем создания и сроком реакции. Чтение и запись JSON выполняются через with; отсутствие файла и неверный JSON обрабатываются без аварийного завершения программы.")
paragraph(doc, "Репозиторий проекта: https://github.com/Max-kalashnikov/frame")
heading(doc, "Результат работы")
paragraph(doc, "В проекте применены списки, словари, циклы, генераторные выражения, lambda функция при сортировке, модули, исключения, JSON и аннотации типов. Функция determine_action сохранена из ПР1 и используется для проверки каждой заявки.")
paragraph(doc, "Создан каталог tests с пятью тестами pytest: проверяются создание, поиск и сортировка заявок, контроль срочности и отмена. pytest завершился со статусом 5 passed; flake8 не выявил замечаний.")
heading(doc, "Вывод")
paragraph(doc, "В результате ПР2 получена функциональная версия приложения для мониторинга заявок. Проект подготовлен к переходу от словарей и функций к объектной модели и дальнейшей реализации на Django.")
doc.save(OUTPUT)
print(OUTPUT)