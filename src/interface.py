import flet as ft
from algorithm import is_correct_regex, match


def main(page: ft.Page):
    def check_regex(e):
        regex = regex_entry.value
        word = word_entry.value
        if not is_correct_regex(regex):
            result_label.value = "Invalid regular expression"
            page.update()
            return
        if word == "":
            result_label.value = "Enter the word"
        else:
            if match(regex, word):
                result_label.value = "The word belongs to a regular expression"
            else:
                result_label.value = "The word doesn't belong to a regular expression"
        page.update()
        

    regex_entry = ft.TextField(label="Enter a regular expression", width=350, height=50)
    word_entry = ft.TextField(label="Enter the word", width=350, height=50)
    check_button = ft.ElevatedButton(text="Check", on_click=check_regex)

    result_label = ft.Text(value="", color="#B8BCC3")

    page.dark_theme
    page.title = "Regular Expression Checker"
    page.window_width = 420
    page.window_height = 310
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_center()

    page.add(
        ft.Column(
            [
                regex_entry,
                word_entry,
                check_button,
                result_label
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
