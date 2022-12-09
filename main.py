import random
from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO

pokemon_types_color = {
    'Grass': '#78C850',
    'Poison': '#A040A0',
    'Fire': '#F08030',
    'Flying': '#A890F0',
    'Water': '#6890F0',
    'Bug': '#A8B820',
    'Normal': '#A8A878',
    'Dark': '#705848',
    'Electric': '#F8D030',
    'Psychic': '#F85888',
    'Ground': '#E0C068',
    'Ice': '#98D8D8',
    'Steel': '#B8B8D0',
    'Fairy': '#EE99AC',
    'Fighting': '#C03028',
    'Dragon': '#7038F8',
    'Ghost': '#705898',
    'Rock': '#B8A038',
}

root = Tk()
root.title("Pokémon")
icon = PhotoImage(file="ball.png")
root.iconphoto(False, icon)
root.config(bg="grey")

FONT_1 = ('Chalkboard', 20, 'bold')
FONT_2 = ('Arial', 16, 'italic bold')
FONT_3 = ('Corsiva', 14, 'normal')

def to_pascal_case(value):
    return " ".join(value.title().split())

def search_poke():
    for widgets in root.winfo_children():
        widgets.destroy()

    back_button = Button(root, text="<---", command=home)
    back_button.grid(row=0, column=0)

    pokemon_input = Entry(root, font=FONT_2)
    pokemon_input.focus_set()
    pokemon_input.grid(row=0, column=1, padx=10, pady=20)

    inv_name = None

    search_result = Frame(root, highlightbackground="black", highlightthickness=2)

    def search(inv_name):
        search_result.grid(row=1, column=0, columnspan=4, padx=40, pady=40)
        search_button.config(state="disabled")
        pokemon_name = pokemon_input.get().lower()
        if not pokemon_name:
            for widgets in search_result.winfo_children():
                widgets.destroy()
            inv_name = Label(search_result)
            inv_name.config(text="Please enter something", font=FONT_2)
            inv_name.pack()
        else:
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}").json()
            except requests.exceptions.JSONDecodeError:
                for widgets in search_result.winfo_children():
                    widgets.destroy()
                inv_name = Label(search_result)
                inv_name.config(text="Invalid name of pokémon", font=FONT_2)
                inv_name.pack()
            else:
                if inv_name:
                    inv_name.destroy()

                for widgets in search_result.winfo_children():
                    widgets.destroy()
                search_result_name = LabelFrame(search_result, text="Name", font=FONT_2, padx=10, pady=5)
                search_result_name.grid(row=0, column=2, padx=(0, 10), pady=10)

                search_result_image = Label(search_result)

                search_result_stats = LabelFrame(search_result, text="Stats", highlightbackground="black",
                                                 highlightthickness=2, font=FONT_2, padx=10, pady=10)
                search_result_stats.grid(row=2, column=2, padx=(0, 10), pady=10)
                hp_stat = Label(search_result_stats, font=FONT_3)
                att_stat = Label(search_result_stats, font=FONT_3)
                def_stat = Label(search_result_stats, font=FONT_3)

                search_result_types = LabelFrame(search_result, text="Type", highlightbackground="black",
                                                 highlightthickness=2, font=FONT_2, padx=10, pady=10)
                search_result_types.grid(row=1, column=2, padx=(0, 10), pady=10)

                search_result_evolution = LabelFrame(search_result, text="Evolution Chain", highlightbackground="black",
                                                     highlightthickness=2, font=FONT_2, padx=10, pady=10)
                search_result_evolution.grid(row=3, column=2, padx=(0, 20), pady=10)

                actual_name = Label(search_result_name, text=f"{to_pascal_case(response['name'])}", font=FONT_1)
                actual_name.pack()

                image_url = f'{response["sprites"]["other"]["official-artwork"]["front_default"]}'
                r = requests.get(image_url)
                pilImage = Image.open(BytesIO(r.content))
                pilImage.mode = 'RGBA'
                pilImage = pilImage.resize((400, 400))
                image = ImageTk.PhotoImage(pilImage)
                search_result_image.config(image=image)
                search_result_image.image = image
                search_result_image.grid(row=0, column=0, columnspan=2, rowspan=4)

                stats = response["stats"]
                hp_stat.config(text=f"{stats[0]['base_stat']} HP")
                hp_stat.pack(anchor="w")
                att_stat.config(text=f"{stats[1]['base_stat']} Attack")
                att_stat.pack(anchor="w")
                def_stat.config(text=f"{stats[2]['base_stat']} Defense")
                def_stat.pack(anchor="w")

                poke_types = response["types"]
                for widgets in search_result_types.winfo_children():
                    widgets.destroy()
                for item in poke_types:
                    f = to_pascal_case(item['type']['name'])
                    type_label = Label(search_result_types, text=f, bg=pokemon_types_color[f], font=FONT_3)
                    type_label.pack(side=LEFT)

                for widgets in search_result_evolution.winfo_children():
                    widgets.destroy()
                species_response = requests.get(response['species']['url']).json()
                evolution_response = requests.get(species_response['evolution_chain']['url']).json()
                base_poke = evolution_response['chain']['species']['name']
                if pokemon_name == "meowth" or pokemon_name == "persian" or pokemon_name == "perrserker" or pokemon_name == "slowbro" or pokemon_name == "slowpoke" or pokemon_name == "slowking" or pokemon_name == "nincada" or pokemon_name == "shedinja" or pokemon_name == "ninjask" or pokemon_name == "snorunt" or pokemon_name == "froslass" or pokemon_name == "glalie" or pokemon_name == "clamperl" or pokemon_name == "gorebyss" or pokemon_name == "huntail" or pokemon_name == "burmy" or pokemon_name == "mothim" or pokemon_name == "wormadam" or pokemon_name == "cofagrigus" or pokemon_name == "runerigus" or pokemon_name == "yamask" or pokemon_name == "applin" or pokemon_name == "appletun" or pokemon_name == "flapple":
                    level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                    level_1.pack(side=LEFT)
                    level_2 = Frame(search_result_evolution)
                    level_2.pack(side=LEFT)
                    level_2_l1 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][0]['species']['name']), font=FONT_3)
                    level_2_l1.pack()
                    level_2_l2 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][1]['species']['name']), font=FONT_3)
                    level_2_l2.pack()
                elif pokemon_name == "tyrogue" or pokemon_name == "hitmontop" or pokemon_name == "hitmonlee" or pokemon_name == "hitmonchan":
                    level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                    level_1.pack(side=LEFT)
                    level_2 = Frame(search_result_evolution)
                    level_2.pack(side=LEFT)
                    level_2_l1 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][0]['species']['name']), font=FONT_3)
                    level_2_l1.pack()
                    level_2_l2 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][1]['species']['name']), font=FONT_3)
                    level_2_l2.pack()
                    level_2_l3 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][2]['species']['name']), font=FONT_3)
                    level_2_l3.pack()
                elif pokemon_name == "eevee" or pokemon_name == "vaporeon" or pokemon_name == "jolteon" or pokemon_name == "flareon" or pokemon_name == "espeon" or pokemon_name == "umbreon" or pokemon_name == "sylveon" or pokemon_name == "leafeon" or pokemon_name == "glaceon":
                    level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                    level_1.pack(side=LEFT)
                    level_2 = Frame(search_result_evolution)
                    level_2.pack(side=LEFT)
                    level_2_l1 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][0]['species']['name']), font=FONT_3)
                    level_2_l1.pack()
                    level_2_l2 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][1]['species']['name']), font=FONT_3)
                    level_2_l2.pack()
                    level_2_l3 = Label(level_2, text=to_pascal_case(
                        evolution_response['chain']['evolves_to'][2]['species']['name']), font=FONT_3)
                    level_2_l3.pack()
                    level_2_l4 = Label(level_2,
                                       text=to_pascal_case(
                                           evolution_response['chain']['evolves_to'][3]['species']['name']),
                                       font=FONT_3)
                    level_2_l4.pack()
                    level_2_l5 = Label(level_2,
                                       text=to_pascal_case(
                                           evolution_response['chain']['evolves_to'][4]['species']['name']),
                                       font=FONT_3)
                    level_2_l5.pack()
                    level_2_l6 = Label(level_2,
                                       text=to_pascal_case(
                                           evolution_response['chain']['evolves_to'][5]['species']['name']),
                                       font=FONT_3)
                    level_2_l6.pack()
                    level_2_l7 = Label(level_2,
                                       text=to_pascal_case(
                                           evolution_response['chain']['evolves_to'][6]['species']['name']),
                                       font=FONT_3)
                    level_2_l7.pack()
                    level_2_l8 = Label(level_2,
                                       text=to_pascal_case(
                                           evolution_response['chain']['evolves_to'][7]['species']['name']),
                                       font=FONT_3)
                    level_2_l8.pack()
                elif pokemon_name == "wurmple" or pokemon_name == "silcoon" or pokemon_name == "cascoon" or pokemon_name == "dustox" or pokemon_name == "beautifly":
                    level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                    level_1.pack(side=LEFT)
                    level_2 = Frame(search_result_evolution)
                    level_2.pack(side=LEFT)
                    level_2_l1 = Label(level_2,
                                       text=f"{to_pascal_case(evolution_response['chain']['evolves_to'][0]['species']['name'])} ---> {to_pascal_case(evolution_response['chain']['evolves_to'][0]['evolves_to'][0]['species']['name'])}",
                                       font=FONT_3)
                    level_2_l1.pack()
                    level_2_l2 = Label(level_2,
                                       text=f"{to_pascal_case(evolution_response['chain']['evolves_to'][1]['species']['name'])} ---> {to_pascal_case(evolution_response['chain']['evolves_to'][0]['evolves_to'][0]['species']['name'])}",
                                       font=FONT_3)
                    level_2_l2.pack()
                else:
                    poke_2 = ""
                    poke_3 = ""
                    if len(evolution_response['chain']['evolves_to']):
                        poke_2 = evolution_response['chain']['evolves_to'][0]['species']['name']
                        if len(evolution_response['chain']['evolves_to'][0]['evolves_to']):
                            poke_3 = evolution_response['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
                    evol_str = to_pascal_case(base_poke)
                    if poke_2:
                        evol_str += f" ---> {to_pascal_case(poke_2)}"
                    if poke_3:
                        evol_str += f" ---> {to_pascal_case(poke_3)}"
                    evolution_label = Label(search_result_evolution, text=evol_str, font=FONT_3)
                    evolution_label.pack()

        pokemon_input.delete(0, END)
        search_button.config(state="normal")

    def gen_ran(inv_name):
        search_result.grid(row=1, column=0, columnspan=4, padx=40, pady=40)
        generate_random_button.config(state="disabled")
        index = random.randint(1, 1154)
        if index > 905:
            index += 9095
        try:
            respons = requests.get(f"https://pokeapi.co/api/v2/pokemon/{index}").json()
        except requests.exceptions.JSONDecodeError:
            print(index)
        else:
            pokemon_name = respons['name']
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}").json()
            if inv_name is not None:
                try:
                    inv_name.destroy()
                except:
                    print('Error')

            for widgets in search_result.winfo_children():
                widgets.destroy()
            search_result_name = LabelFrame(search_result, text="Name", font=FONT_2, padx=10, pady=5)
            search_result_name.grid(row=0, column=2, padx=(0, 10), pady=10)

            search_result_image = Label(search_result)

            search_result_stats = LabelFrame(search_result, text="Stats", highlightbackground="black",
                                             highlightthickness=2, font=FONT_2, padx=10, pady=10)
            search_result_stats.grid(row=2, column=2, padx=(0, 10), pady=10)
            hp_stat = Label(search_result_stats, font=FONT_3)
            att_stat = Label(search_result_stats, font=FONT_3)
            def_stat = Label(search_result_stats, font=FONT_3)

            search_result_types = LabelFrame(search_result, text="Type", highlightbackground="black",
                                             highlightthickness=2, font=FONT_2, padx=10, pady=10)
            search_result_types.grid(row=1, column=2, padx=(0, 10), pady=10)

            search_result_evolution = LabelFrame(search_result, text="Evolution Chain", highlightbackground="black",
                                                 highlightthickness=2, font=FONT_2, padx=10, pady=10)
            search_result_evolution.grid(row=3, column=2, padx=(0, 20), pady=10)

            actual_name = Label(search_result_name, text=f"{to_pascal_case(response['name'])}", font=FONT_1)
            actual_name.pack()

            image_url = f'{response["sprites"]["other"]["official-artwork"]["front_default"]}'
            r = requests.get(image_url)
            pilImage = Image.open(BytesIO(r.content))
            pilImage.mode = 'RGBA'
            pilImage = pilImage.resize((400, 400))
            image = ImageTk.PhotoImage(pilImage)
            search_result_image.config(image=image)
            search_result_image.image = image
            search_result_image.grid(row=0, column=0, columnspan=2, rowspan=4)

            stats = response["stats"]
            hp_stat.config(text=f"{stats[0]['base_stat']} HP")
            hp_stat.pack(anchor="w")
            att_stat.config(text=f"{stats[1]['base_stat']} Attack")
            att_stat.pack(anchor="w")
            def_stat.config(text=f"{stats[2]['base_stat']} Defense")
            def_stat.pack(anchor="w")

            poke_types = response["types"]
            for widgets in search_result_types.winfo_children():
                widgets.destroy()
            for item in poke_types:
                f = to_pascal_case(item['type']['name'])
                type_label = Label(search_result_types, text=f, bg=pokemon_types_color[f], font=FONT_3)
                type_label.pack(side=LEFT)

            for widgets in search_result_evolution.winfo_children():
                widgets.destroy()
            species_response = requests.get(response['species']['url']).json()
            evolution_response = requests.get(species_response['evolution_chain']['url']).json()
            base_poke = evolution_response['chain']['species']['name']
            if pokemon_name == "meowth" or pokemon_name == "persian" or pokemon_name == "perrserker" or pokemon_name == "slowbro" or pokemon_name == "slowpoke" or pokemon_name == "slowking" or pokemon_name == "nincada" or pokemon_name == "shedinja" or pokemon_name == "ninjask" or pokemon_name == "snorunt" or pokemon_name == "froslass" or pokemon_name == "glalie" or pokemon_name == "clamperl" or pokemon_name == "gorebyss" or pokemon_name == "huntail" or pokemon_name == "burmy" or pokemon_name == "mothim" or pokemon_name == "wormadam" or pokemon_name == "cofagrigus" or pokemon_name == "runerigus" or pokemon_name == "yamask" or pokemon_name == "applin" or pokemon_name == "appletun" or pokemon_name == "flapple":
                level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                level_1.pack(side=LEFT)
                level_2 = Frame(search_result_evolution)
                level_2.pack(side=LEFT)
                level_2_l1 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][0]['species']['name']),
                                   font=FONT_3)
                level_2_l1.pack()
                level_2_l2 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][1]['species']['name']),
                                   font=FONT_3)
                level_2_l2.pack()
            elif pokemon_name == "tyrogue" or pokemon_name == "hitmontop" or pokemon_name == "hitmonlee" or pokemon_name == "hitmonchan":
                level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                level_1.pack(side=LEFT)
                level_2 = Frame(search_result_evolution)
                level_2.pack(side=LEFT)
                level_2_l1 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][0]['species']['name']),
                                   font=FONT_3)
                level_2_l1.pack()
                level_2_l2 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][1]['species']['name']),
                                   font=FONT_3)
                level_2_l2.pack()
                level_2_l3 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][2]['species']['name']),
                                   font=FONT_3)
                level_2_l3.pack()
            elif pokemon_name == "eevee" or pokemon_name == "vaporeon" or pokemon_name == "jolteon" or pokemon_name == "flareon" or pokemon_name == "espeon" or pokemon_name == "umbreon" or pokemon_name == "sylveon" or pokemon_name == "leafeon" or pokemon_name == "glaceon":
                level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                level_1.pack(side=LEFT)
                level_2 = Frame(search_result_evolution)
                level_2.pack(side=LEFT)
                level_2_l1 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][0]['species']['name']),
                                   font=FONT_3)
                level_2_l1.pack()
                level_2_l2 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][1]['species']['name']),
                                   font=FONT_3)
                level_2_l2.pack()
                level_2_l3 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][2]['species']['name']),
                                   font=FONT_3)
                level_2_l3.pack()
                level_2_l4 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][3]['species']['name']),
                                   font=FONT_3)
                level_2_l4.pack()
                level_2_l5 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][4]['species']['name']),
                                   font=FONT_3)
                level_2_l5.pack()
                level_2_l6 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][5]['species']['name']),
                                   font=FONT_3)
                level_2_l6.pack()
                level_2_l7 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][6]['species']['name']),
                                   font=FONT_3)
                level_2_l7.pack()
                level_2_l8 = Label(level_2,
                                   text=to_pascal_case(evolution_response['chain']['evolves_to'][7]['species']['name']),
                                   font=FONT_3)
                level_2_l8.pack()
            elif pokemon_name == "wurmple" or pokemon_name == "silcoon" or pokemon_name == "cascoon" or pokemon_name == "dustox" or pokemon_name == "beautifly":
                level_1 = Label(search_result_evolution, text=to_pascal_case(base_poke), font=FONT_3)
                level_1.pack(side=LEFT)
                level_2 = Frame(search_result_evolution)
                level_2.pack(side=LEFT)
                level_2_l1 = Label(level_2,
                                   text=f"{to_pascal_case(evolution_response['chain']['evolves_to'][0]['species']['name'])} ---> {to_pascal_case(evolution_response['chain']['evolves_to'][0]['evolves_to'][0]['species']['name'])}",
                                   font=FONT_3)
                level_2_l1.pack()
                level_2_l2 = Label(level_2,
                                   text=f"{to_pascal_case(evolution_response['chain']['evolves_to'][1]['species']['name'])} ---> {to_pascal_case(evolution_response['chain']['evolves_to'][0]['evolves_to'][0]['species']['name'])}",
                                   font=FONT_3)
                level_2_l2.pack()
            else:
                poke_2 = ""
                poke_3 = ""
                if len(evolution_response['chain']['evolves_to']):
                    poke_2 = evolution_response['chain']['evolves_to'][0]['species']['name']
                    if len(evolution_response['chain']['evolves_to'][0]['evolves_to']):
                        poke_3 = evolution_response['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
                evol_str = to_pascal_case(base_poke)
                if poke_2:
                    evol_str += f" ---> {to_pascal_case(poke_2)}"
                if poke_3:
                    evol_str += f" ---> {to_pascal_case(poke_3)}"
                evolution_label = Label(search_result_evolution, text=evol_str, font=FONT_3)
                evolution_label.pack()

        pokemon_input.delete(0, END)
        generate_random_button.config(state="normal")

    def on_enter(e):
        e.widget.config(fg="black", highlightbackground='dark blue')

    def on_leave(e):
        e.widget.config(fg="black", highlightbackground='black')

    def on_active(e):
        e.widget.config(fg="black", highlightbackground='light blue')



    search_button = Button(root, text="Search", command=lambda :search(inv_name), highlightbackground='black', font=FONT_2)
    search_button.grid(row=0, column=2, padx=10, pady=20)
    search_button.bind("<Enter>", on_enter)
    search_button.bind("<Leave>", on_leave)
    search_button.bind("<ButtonPress>", on_active)
    search_button.bind("<ButtonRelease>", on_enter)
    search_button.bind("<Return>", lambda event: search())

    generate_random_button = Button(root, text="Surprise Me", command=lambda :gen_ran(inv_name), highlightbackground='black', font=FONT_2)
    generate_random_button.grid(row=0, column=3, padx=10, pady=20)
    generate_random_button.bind("<Enter>", on_enter)
    generate_random_button.bind("<Leave>", on_leave)
    generate_random_button.bind("<ButtonPress>", on_active)
    generate_random_button.bind("<ButtonRelease>", on_enter)
    generate_random_button.bind("<Return>", lambda event: gen_ran())

def guess_poke():
    for widgets in root.winfo_children():
        widgets.destroy()

    back_button = Button(root, text="<---", command=home)
    back_button.pack()

    index = random.randint(1, 905)
    respons = requests.get(f"https://pokeapi.co/api/v2/pokemon/{index}").json()
    pokemon_name = respons['name']
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}").json()

    image_url = f'{response["sprites"]["other"]["official-artwork"]["front_default"]}'
    r = requests.get(image_url)
    pilImage = Image.open(BytesIO(r.content))
    pilImage.mode = 'RGBA'
    pilImage = pilImage.resize((200, 200))
    image = ImageTk.PhotoImage(pilImage)
    guess_image_lbl=Label(root)
    guess_image_lbl.config(image=image)
    guess_image_lbl.image = image
    guess_image_lbl.pack()

    def check():
        real_name = response['name']
        staus_lbl=Label(root)
        staus_lbl.pack()

        if pokemon_input.get().lower() == real_name:
            staus_lbl.config(text="Congratulation you are right!!!")
        else:
            staus_lbl.config(text=f"Sorry , the correct answer is {real_name}")


    pokemon_input = Entry(root, font=FONT_2)
    pokemon_input.focus_set()
    pokemon_input.pack()

    check_btn=Button(root,text="Check Answer",command=check)
    check_btn.pack()

    next_btn = Button(root, text="Next", command=guess_poke)
    next_btn.pack()

def home():
    for widgets in root.winfo_children():
        widgets.destroy()
    main_search=Button(root,text="Search Pokemon !!!",command=search_poke,font=FONT_2)
    main_search.pack()
    # guess_name_btn=Button(root,text="Guess Pokémon name !!!",command=guess_poke,font=FONT_2)
    # guess_name_btn.pack()

home()

root.bind("<Escape>",lambda event:root.quit())
root.mainloop()
