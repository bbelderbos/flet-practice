import flet as ft
import requests
import bs4
from bs4 import BeautifulSoup


def get_meaning(word, site, datasrc):
    """Get the meaning for a given word from an online dictionary."""
    response = requests.get(site + word)
    if not response.ok:
        if response.status_code == 404:
            print("Word not found")
        else:
            print(f"An error occurred: {response.reason}")
        
        return f"An error occurred: {response.reason}"

    soup = BeautifulSoup(response.text, "html.parser")

    data = soup.find("section", attrs=datasrc).findAll("div")

    meaning = ""
    for line in data:
        meaning = f"{meaning}\n{line.get_text()}"

    return meaning


# Main
def main(page):
    page.title = "Meaning"
    page.window_width=500
    page.window_height=500
    page.scroll = "adaptive"

    # establish defaults in English
    page.session.set("intro", "Your word's definition:\n")
    page.session.set("datasrc", {"data-src": "hc_dict"})
    page.session.set("site", "https://www.thefreedictionary.com/")
    
    def set_language(e):
        ''' Toggle language between English and Deutsch '''
        if lang_icon.data == "EN":
            set_deutsch()
        elif lang_icon.data == "DE":
            set_english()
            
            
    def set_english():
        ''' Set the language options to English in the page.session values '''
        page.session.set("intro", f"Your word was ")
        page.session.set("datasrc", {"data-src": "hc_dict"})
        page.session.set("site", "https://www.thefreedictionary.com/")
        page.session.set("button_txt", "Define")
        txt_word.clean()
        txt_word.value = ""
        print("Switched to ENGLISH")
        lang_icon.data = "EN"
        lang_text.value = "EN"
        txt_word.label = "What's a word you'd like to learn?"
        page.title = "Get a Word's Meaning - English"
        btn.text = "Define"
        page.update()
    
    def set_deutsch():
        ''' Set the language options to Deutsch in the page.session values '''
        page.session.set("intro", f"Dein Wort war ")
        page.session.set("datasrc", {"data-src": "pons"})
        page.session.set("site", "https://de.thefreedictionary.com/")
        page.session.set("button_txt", "Definieren")
        txt_word.clean()
        txt_word.value = ""
        print("Switched to DEUTSCH")
        lang_icon.data = "DE"
        lang_text.value = "DE"
        txt_word.label = "Welches Wort möchtest du lernen?"
        page.title = "Verstehe die Bedeutung eines Wortes - Deutsch"
        btn.text = "definieren"
        page.update()
    
    
    # When the button is clicked, we display the results of the lookup.
    def btn_click(e):
        # update the "word"
        word = txt_word.value
        
        if not word:
            txt_word.error_text = "Please enter a word to lookup"
            page.update()
        else:
            # show the progress bar
            page.splash = ft.ProgressBar()
            
            page.update()
            # get the current language settings
            intro = page.session.get("intro") + f": {word}\n"
            datasrc = page.session.get("datasrc")
            site = page.session.get("site")
            # get the definition in response
            response = get_meaning(word, site, datasrc)
            # clear and repopulate the response output view
            response_list.clean()
            response_list.value = f"{intro}{response}"
            # end the progress bar
            page.splash = None
            
            page.update()

    # The language switching icon in the lower right corner
    lang_text = ft.Text("LANG")
    lang_icon = ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.LANGUAGE_OUTLINED), ft.Text("")], alignment="center", spacing=5
        ),
        tooltip="EN/DE",
        text="EN/DE",
        bgcolor=ft.colors.BLACK54,
        shape=ft.RoundedRectangleBorder(radius=15),
        width=60,
        mini=True,
        data="EN",
        on_click=set_language
    )
    page.add(lang_icon)
    page.update()
    
    # Input controls - text box and button
    txt_word = ft.TextField(label="What's a word you'd like to learn?",on_submit=btn_click, width=350)
    btn = ft.ElevatedButton("Define", on_click=btn_click)
    input_controls = ft.Column(controls=[
        ft.Row(controls=[txt_word, btn] ,
               alignment=ft.MainAxisAlignment.SPACE_EVENLY),
    ])
    page.add(input_controls)
    
    # Output View - display window for the results
    response_list = ft.Text("")  # ft.Text("")
    page.add(response_list)
    
    page.update()

ft.app(target=main)

