import json
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView

class NotebookApp(MDApp):
    notes = []

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"

        layout = MDBoxLayout(orientation="vertical")

        self.note_name_input = MDTextField(hint_text="Введите название заметки")
        layout.add_widget(self.note_name_input)

        self.note_input = MDTextField(hint_text="Введите заметку")
        layout.add_widget(self.note_input)

        save_button = MDIconButton(icon="content-save")
        save_button.bind(on_release=self.save_note)
        layout.add_widget(save_button)

        add_button = MDIconButton(icon="plus")
        add_button.bind(on_release=self.add_note)
        layout.add_widget(add_button)

        self.scroll_view = ScrollView()
        layout.add_widget(self.scroll_view)

        dark_mode_button = MDIconButton(icon="moon-waning-crescent")
        dark_mode_button.bind(on_release=self.toggle_dark_mode)
        layout.add_widget(dark_mode_button)

        # При запуске приложения загружаем сохраненные заметки
        self.load_notes()
        self.refresh_notes()

        return layout

    def save_note(self, instance):
        note_name = self.note_name_input.text.strip()
        note_text = self.note_input.text.strip()

        if note_name and note_text:
            self.notes.append({"name": note_name, "text": note_text})
            self.save_notes()  # Сохраняем заметки после добавления новой
            print(f"Сохранена заметка '{note_name}': {note_text}")
            self.refresh_notes()

    def add_note(self, instance):
        note_name = self.note_name_input.text.strip()
        note_text = self.note_input.text.strip()

        if note_name and note_text:
            self.notes.append({"name": note_name, "text": note_text})
            self.save_notes()  # Сохраняем заметки после добавления новой
            print(f"Добавлена заметка '{note_name}': {note_text}")
            self.note_name_input.text = ""
            self.note_input.text = ""
            self.refresh_notes()

    def refresh_notes(self):
        layout = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=10)

        for idx, note in enumerate(self.notes):
            panel_content = MDBoxLayout(orientation="vertical")
            panel_content.add_widget(MDLabel(text=note["text"], halign='center', valign='center'))

            delete_button = MDIconButton(icon="delete")
            delete_button.bind(on_release=lambda instance, i=idx: self.delete_note(i))
            panel_content.add_widget(delete_button)

            panel = MDExpansionPanel(
                icon="folder",
                content=panel_content,
                panel_cls=MDExpansionPanelOneLine(
                    text=note["name"],
                    on_press=self.show_full_text
                )
            )
            layout.add_widget(panel)

        self.scroll_view.clear_widgets()
        self.scroll_view.add_widget(layout)
    

    def delete_note(self, idx):
        del self.notes[idx]
        self.save_notes()  # Сохраняем заметки после удаления
        self.refresh_notes()

    def show_full_text(self, instance):
        panel = instance.parent
        panel.content.height = 200  # устанавливаем высоту контента панели

    def toggle_dark_mode(self, instance):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def save_notes(self):
        with open("notes.json", "w") as file:
            json.dump(self.notes, file)

    def load_notes(self):
        try:
            with open("notes.json", "r") as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            self.notes = []  # Если файл не найден, начинаем с пустого списка заметок

if __name__ == '__main__':
    NotebookApp().run()