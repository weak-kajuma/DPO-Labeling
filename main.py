import customtkinter as ctk
import json
from tkinter import messagebox
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', help='input jsonファイル', default='input.json')
parser.add_argument('-o', '--output', help='output jsonファイル', default='output.json')
args = parser.parse_args()

FONT = "meiryo UI"
FONTSIZE = 16
MDFONT = "Noto Sans CJK JP"
MDFONTSIZE = 16
MDCODEFONT = "Courier New"


class MdViewer(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.Object = []
        self.enum_num = []
        self.code_buffer = []
        self.line_is_code = False

    def make_md_view(self, markdown_text):
        for widget in self.winfo_children():
            widget.destroy()  # 既存のウィジェットをクリア
        self.Object = []
        text = markdown_text.split("\n")  # Markdownテキストを改行で分割
        for line in text:
            if self.line_is_code:
                self.code_analysis(line)
            else:
                self.Object.append(self.line_analysis(line))
        for obj in self.Object:
            obj.pack(anchor="nw", fill="x")  # 横幅にフィットさせる

    def line_analysis(self, line):
        line = line.replace("\t", "    ")
        if line.startswith("#"):
            count = line.count("#")
            line = line.replace("#", "").strip()
            label = ctk.CTkLabel(
                self, 
                text=line, 
                font=(MDFONT, MDFONTSIZE + (6 - count) * 3),
                wraplength=self.winfo_width()  # 折り返し幅を設定
            )
            return label
        elif line.startswith("```"):
            self.line_is_code = True
            return ctk.CTkLabel(self, text="", fg_color="transparent")  # ダミー
        else:
            label = ctk.CTkLabel(
                self, 
                text=line, 
                font=(MDFONT, MDFONTSIZE),
                wraplength=self.winfo_width()  # 折り返し幅を設定
            )
            return label

    def code_analysis(self, line):
        if line.startswith("```"):
            self.line_is_code = False
            code = "\n".join(self.code_buffer)
            self.code_buffer.clear()
            textbox = ctk.CTkTextbox(self, font=(MDCODEFONT, MDFONTSIZE - 4), wrap="none")
            textbox.insert("0.0", code)
            textbox.configure(state="disabled")
            self.Object.append(textbox)
        else:
            self.code_buffer.append(line)


class JsonViewer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.md_viewer_1 = MdViewer(self)
        self.md_viewer_1.grid(row=0, column=0, sticky="nsew")

        self.md_viewer_2 = MdViewer(self)
        self.md_viewer_2.grid(row=1, column=0, sticky="nsew")

        self.json_list = []
        self.current_index = 0

    def load_json(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.json_list = data
                self.current_index = 0
                self.update_view()
            else:
                messagebox.showinfo("Error", "Invalid JSON structure. Must be a list of objects.")
        except (OSError, json.JSONDecodeError) as e:
            messagebox.showinfo("Error", f"Failed to load JSON: {e}")

    def update_view(self):
        if self.json_list:
            data = self.json_list[self.current_index]
            markdown_text_1 = data.get("prompt", "")
            markdown_text_2 = data.get("answer", "")
            feedback = data.get("feedback", "None")

            self.md_viewer_1.make_md_view(markdown_text_1)
            self.md_viewer_2.make_md_view(markdown_text_2)

            self.master.feedback_label.configure(text=f"Feedback: {feedback}")

    def show_next(self):
        if self.json_list and self.current_index < len(self.json_list) - 1:
            self.current_index += 1
            self.update_view()

    def show_previous(self):
        if self.json_list and self.current_index > 0:
            self.current_index -= 1
            self.update_view()

    def save_json(self, json_path):
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.json_list, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Success", f"JSON saved successfully to {json_path}")
        except OSError as e:
            messagebox.showinfo("Error", f"Failed to save JSON: {e}")

    def add_feedback(self, feedback):
        if self.json_list:
            current_item = self.json_list[self.current_index]
            current_item["feedback"] = feedback
            self.update_view()  # 更新表示


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DPO Labeling")
        self.geometry("800x600")
        self.minsize(400, 300)

        self.json_viewer = JsonViewer(self)
        self.json_viewer.pack(fill="both", expand=True)

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(fill="x", pady=5)

        self.feedback_label = ctk.CTkLabel(self.bottom_frame, text="Feedback: None", font=(FONT, FONTSIZE))
        self.feedback_label.pack(side="left", padx=10)

        self.save_button = ctk.CTkButton(self.bottom_frame, text="Save JSON", command=self.save_json_file)
        self.save_button.pack(side="right", padx=10)

        self.load_button = ctk.CTkButton(self.bottom_frame, text="Load JSON", command=self.load_json_file)
        self.load_button.pack(side="right", padx=10)

        self.bind("<Left>", lambda event: self.json_viewer.show_previous())
        self.bind("<Right>", lambda event: self.json_viewer.show_next())
        self.bind("<Up>", lambda event: self.json_viewer.add_feedback("good"))
        self.bind("<Down>", lambda event: self.json_viewer.add_feedback("bad"))

    def load_json_file(self):
        json_path = args.input  # サンプルJSONファイルのパス
        self.json_viewer.load_json(json_path)

    def save_json_file(self):
        json_path = args.output  # 保存するJSONファイルのパス
        self.json_viewer.save_json(json_path)


if __name__ == "__main__":
    app = App()
    app.mainloop()
