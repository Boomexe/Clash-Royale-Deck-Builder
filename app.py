import tkinter
from typing import Optional, Tuple, Union
from customtkinter.windows.widgets.font import CTkFont
import utils.util as util
import tkinter as tk
# import tkinter.messagebox
import customtkinter as ctk
from PIL import Image
import os

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class NumberInputEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        # super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, text_color, placeholder_text_color, textvariable, placeholder_text, font, state, **kwargs)
        self.var = tk.StringVar()
        ctk.CTkEntry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

        self.min = 0
        self.max = 10
    
    def check(self, *args):
        if self.get().isdigit():
            if int(self.get()) < self.min or int(self.get()) > self.max:
                self.set(self.old_value)

            else:
                self.old_value = self.get()
        
        elif self.get() == '':
            self.old_value = self.get()
        
        else:
            self.set(self.old_value)

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        # Settings
        self.max_decks = 5

        self.current_path = os.path.dirname(os.path.realpath(__file__))

        # Configure Window
        self.title("Clash Royale Deck Generator")
        self.geometry(f"{1100}x{580}")

        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text="CLASH ROYALE DECK GENERATOR", font=ctk.CTkFont(size=25, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="nsew")
        self.tabview = ctk.CTkTabview(self)
        # self.tabview.pack()
        self.tabview.grid(row=1, column=0, sticky="nsew")
        self.tabview.add("Generate Deck")
        self.tabview.add("Settings")

        # Settings Tab
        self.set_max_decks_label = ctk.CTkLabel(self.tabview.tab("Settings"), text="Decks to Find")
        self.set_max_decks_label.pack()
        self.set_max_decks_entry = NumberInputEntry(self.tabview.tab("Settings"), justify=tk.CENTER, placeholder_text="Enter number of decks to find (1-10)...")
        self.set_max_decks_entry.pack()
        self.api_key_label = ctk.CTkLabel(self.tabview.tab("Settings"), text="Update API Key")
        self.api_key_label.pack()
        self.api_key_entry = ctk.CTkEntry(self.tabview.tab("Settings"), width=250, placeholder_text="Enter API Key...")
        self.api_key_entry.pack()
        self.api_key_button = ctk.CTkButton(self.tabview.tab("Settings"), text="Update", command=lambda:util.update_api_key(self.api_key_entry.get()))
        self.api_key_button.pack(pady=10)
        self.api_key_button = ctk.CTkButton(self.tabview.tab("Settings"), text="Refresh Leaderboard", command=util.refresh_leaderboard)
        self.api_key_button.pack(pady=10)
        self.api_key_button = ctk.CTkButton(self.tabview.tab("Settings"), text="Redownload Assets", command=util.refresh_everything)
        self.api_key_button.pack(pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.tabview.tab("Settings"), text="Apperance:")
        self.appearance_mode_label.pack()
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.tabview.tab("Settings"), values=["System", "Dark", "Light"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack()

        # Generate Deck Tab
        self.card_input_label = ctk.CTkLabel(self.tabview.tab("Generate Deck"), text="Enter Card:")
        self.card_input_label.pack()
        self.card_input_box = ctk.CTkComboBox(self.tabview.tab("Generate Deck"), values=util.get_card_names())
        self.card_input_box.pack()
        self.enter_input_button = ctk.CTkButton(self.tabview.tab("Generate Deck"), text="Find Decks", command=self.find_decks)
        self.enter_input_button.pack(pady=10)

        self.progressbar = ctk.CTkProgressBar(self.tabview.tab("Generate Deck"))
        # self.progressbar.pack()

        # DECKS FRAME STUFF
        self.decks_frame = ctk.CTkScrollableFrame(self.tabview.tab("Generate Deck"), height=1000, label_text="Decks:")
        self.decks_frame.pack(padx=100, pady=25, fill="both")
        self.decks_frame.columnconfigure(0, weight=1)
    
        self.current_displayed_decks = []

        # Default Values
        self.progressbar.configure(mode="indeterminnate")
        self.set_max_decks_entry.insert(0, "5")
        self.api_key_entry.insert(0, util.api_key)

        if util.is_first_launch:
            self.first_launch()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def find_decks(self):
        if len(self.current_displayed_decks) > 1:
            for deck in self.current_displayed_decks:
                deck.grid_forget()
            
            self.current_displayed_decks = []

        card_id = util.get_id_from_name(self.card_input_box.get())

        decks = util.get_decks(card_id, int(self.set_max_decks_entry.get()))

        for deck_index, deck in enumerate(decks):
            deck_frame = ctk.CTkFrame(self.decks_frame)
            deck_frame.rowconfigure((0, 1), weight=1)
            deck_frame.columnconfigure((0, 1, 2, 3), weight=1)
            deck_frame.grid(row=deck_index, column=0, sticky="ew", padx=10, pady=10)

            self.current_displayed_decks.append(deck_frame)

            for card_index, card in enumerate(deck):
                image_directory = self.current_path + "\\storage\\card_images\\" + str(card['id']) + ".png"

                try:
                    card_image = ctk.CTkImage(Image.open(image_directory), size=(100, 119))
                except(FileNotFoundError):
                    card_image = ctk.CTkImage(Image.open(self.current_path + "\\utils\\placeholder.png"), size=(100, 119))
                    
                card_image_label = ctk.CTkLabel(deck_frame, image=card_image, text="")
                card_image_label.grid(row=0 if card_index<=3 else 1, column=card_index%4)

        # # self.bg_image = ctk.CTkImage(Image.open(self.current_path + "\\utils\\background.png"), size=(self.decks_frame.winfo_width()-20, 400))
        # # self.bg_image_label = ctk.CTkLabel(self.deck_frame, image=self.bg_image, text="")
        # # self.bg_image_label.grid(row=0, column=0)
    
    def first_launch(self):
        dialog = ctk.CTkInputDialog(text="Enter your API Key here", title="First Launch Requirements")
        util.run_on_first_launch(dialog.get_input())

        self.card_input_box.configure(values=util.get_card_names())
        self.card_input_box.set("Knight")

if __name__ in "__main__":
    app = App()
    app.mainloop()