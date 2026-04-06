import cmd
from rich.console import Console
from rich.table import Table
from rich.progress import track
from time import sleep as time_sleep
import questionary
import readline
from controller.controller import SimulationController
from interface.event_formats import EVENT_FORMATS

console = Console()

# Auto-complete commands for Mac/Linux
if readline.__doc__ and "libedit" in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


# TODO: ловить исключения из модели и контроллера
class EcosystemCLI(cmd.Cmd):
    prompt = "\033[1;36m❀(eco)*\033[0m "

    def __init__(self, controller: SimulationController):
        super().__init__()
        self.controller = controller

    def preloop(self):
        """Program logo print before program work"""
        console.print(r"""[bold #77CC08]
          .#H:    :H#.           █████╗ ███╗   ██╗██╗███╗   ███╗ █████╗ ██╗
        ~=##=~L  J~=##=~        ██╔══██╗████╗  ██║██║████╗ ████║██╔══██╗██║
        +=##=+|  |+=##=+        ███████║██╔██╗ ██║██║██╔████╔██║███████║██║
         H##WiT  TiW##H         ██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══██║██║
   t#t    TTT      TTT    t#t   ██║  ██║██║ ╚████║██║██║ ╚═╝ ██║██║  ██║███████╗
  .:#=+      .*=#=.      +=#:.  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝
 =gM##W;    *=%##%=*    ;W##Mg=  
 =gM##W!    =M%##%M=    !W##Mg= ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗
   :v#;  .wHW$@##@$WHw.  ;#v:   ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
         whW$@####@$Whw         ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
        .=w%%$####$%%w=.        ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
        \Y%%$##NMN##$%%Y/       ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
         .=*&8#####8&*=.         ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝[/bold #77CC08]
    """)
        console.print("[bold #6ABB00]✿ Animal World Simulation v1.0 ✿[/bold #6ABB00]\n")
        console.print("? Type [cyan]help[/] or [cyan]?[/] for list of commands.\n")

    def do_help(self, arg):
        """Show help.

        :param arg: command (optional)"""
        if arg:
            return super().do_help(arg)

        super().do_help(arg)

        console.print()
        console.print("[bold cyan]Quick start:[/bold cyan]")
        console.print("- [green]run[/]   — run / continue simulation")
        console.print("- [green]stats[/] — show statistics")
        console.print("- [green]bio_diversity[/]   — check biological diversity")
        console.print("- [green]eco_balance[/]   — check ecological balance")
        console.print("- [green]organism[/]   — organism operations")
        console.print("- [green]food_chain[/]   — food chain operations")
        console.print("- [green]load[/]   — load ecosystem from file")
        console.print("- [green]save[/]   — save ecosystem in file")
        console.print("- [green]exit[/]  — exit program\n")

    def do_run(self, arg):
        """Runs an ecosystem simulation for a specified number of steps.

        :param arg: number of steps
        :type arg: int (default: 1)"""
        if not arg:
            steps = 1
        else:
            try:
                steps = int(arg.strip())
                if steps <= 0:
                    raise ValueError("Steps cannot be negative")
            except ValueError:
                console.print(f"[red]Error: '{arg}' is not a positive integer.[/]")
                console.print("Usage: [cyan]run [N][/] — for example, [cyan]run 7[/]")
                return

        console.print(f"[green]Running simulation for {steps} step(s)...[/]")
        for step in track(range(steps), description="Simulating :) ..."):
            time_sleep(0.05)
        # TODO: make silent version for > 200 steps
        for step in range(steps):
            self.controller.run_steps(1)
            time_sleep(0.01)

            current_step = self.controller.get_current_step()
            console.print(f"\n[bold]Step: {current_step}[/bold]")

            logs = self.controller.get_latest_logs()
            if not logs:
                console.print("[dim]Nothing remarkable happened.[/dim]")
            else:
                console.print("[bold yellow]Events:[/bold yellow]")
                for log in logs:
                    formatter = EVENT_FORMATS.get(log["type"])
                    if formatter:
                        console.print(formatter(log))

    def do_stats(self, arg):
        """Show statistics of the ecosystem

        Details:
        Shows number of organisms, current state, simulation age, etc.
        """
        # TODO: предложение вывести статы каждого организма
        table = Table(title="Current population")
        table.add_column("Type", justify="left", style="cyan")
        table.add_column("Count", justify="right", style="magenta")

        stats = self.controller.get_population_stats()

        if not stats:
            table.add_row("Empty", "0")
        else:
            for org_type, count in stats.items():
                table.add_row(org_type, str(count))

        console.print(table)
        self.do_bio_diversity(arg)
        self.do_eco_balance(arg)

    def do_organism(self, arg):
        """Allows user to add organism / remove organism / view statistics of organism

        :param arg: operation name: add/remove/stats (optional)
        :type str"""
        operation: str = arg
        if not arg:
            operation = questionary.select(
                "Which operation to do?", choices=["add", "remove", "view"]
            ).ask()
        species_list = self.controller.get_available_species()
        species_stats = self.controller.get_population_stats()
        # TODO: перевести на list comprehension
        organism_types: list[str] = []
        for org in species_stats:
            organism_types.append(org)

        if operation == "view":
            org_name: str = questionary.text("Enter organism name:").ask()
            stats_list = self.controller.get_organism_stats(org_name)

            if not stats_list:
                console.print(
                    f"[red]No living organism named '{org_name}' found.[/red]"
                )
                return

            for stats in stats_list:
                table = Table(title=f"{stats['name']} ({stats['type']})")
                table.add_column("Parameter", style="cyan")
                table.add_column("Value", style="magenta")

                table.add_row("Health", str(stats["health"]))
                table.add_row("Energy", str(stats["energy"]))
                table.add_row("Age", str(stats["age"]))
                table.add_row("Size", f"{stats['size']:.2f}")

                console.print(table)
            return

        if operation == "add":
            organism_type: str = questionary.select(
                "Which organism would you like to choose?",
                choices=species_list,
            ).ask()
            # TODO: добавить валидацию всех полей
            # TODO: добавить преобразование в тип
            # ?: нужно ли давать доступ к vision radius
            org_name: str = questionary.text(
                "Enter the name of organism:",
            ).ask()
            org_x: int = int(
                questionary.text(
                    "Enter x coordinate of organism to spawn:",
                    validate=lambda text: (
                        text.isdigit() or "Please enter a valid number"
                    ),
                ).ask()
            )
            org_y: int = int(
                questionary.text(
                    "Enter y coordinate of organism to spawn:",
                    validate=lambda text: (
                        text.isdigit() or "Please enter a valid number"
                    ),
                ).ask()
            )
            self.controller.add_organism(organism_type, name=org_name, x=org_x, y=org_y)
            console.print(
                f"[green]{organism_type} '{org_name}' was successfully added.[/green]\n"
            )

        elif operation == "remove":
            organism_name = questionary.text(
                "Enter the name of organism to delete:",
            ).ask()
            matches = self.controller.find_organisms_by_name(organism_name)
            if len(matches) > 1:
                choice_to_id = {}
                found_choices = []
                for org in matches:
                    label = f"{org['name']} (id={org['id']}, type={org['type']})"
                    found_choices.append(label)
                    choice_to_id[label] = org["id"]
                choice = questionary.select(
                    "Found several organisms, choose one:",
                    choices=found_choices,
                ).ask()
                organism_id = choice_to_id[choice]

            elif len(matches) == 1:
                organism_id = matches[0]["id"]
            else:
                console.print(
                    f"[red]No living organism named '{organism_name}' found.[/red]"
                )
                return
            self.controller.remove_organism(organism_id)
        else:
            console.print(f"No such operation: {operation} (expected: add/remove/view)")

    # TODO: после param не надо двоеточие
    def do_food_chain(self, arg):
        """Allows user to modify food chain of the ecosystem, view current food chain

        :param arg: operation name add/remove/view (optional)
        :type arg: str
        """
        operation: str = arg
        operation = operation.capitalize()
        if not operation:
            operation = questionary.select(
                "Which operation to do?", choices=["Add", "Remove", "View"]
            ).ask()

        if operation == "View":
            food_chain = self.controller.get_food_chain()
            console.print("Food chain: \n---")
            for type, eats in food_chain.items():
                animal_name = type.__name__
                prey_names = [prey.__name__ for prey in eats]
                console.print(f"Species: {animal_name}")
                console.print(f"Eats: {prey_names}\n")
            return
        species_list = self.controller.get_available_species()

        if operation == "Add":
            eater = questionary.select("Choose eater:", choices=species_list).ask()
            eaten = questionary.select(
                "Choose pray(eaten):", choices=species_list
            ).ask()
            self.controller.food_chain_add(eater, eaten)
        elif operation == "Remove":
            eater = questionary.select("Choose eater:", choices=species_list).ask()
            eaten = questionary.select(
                "Choose pray(eaten):", choices=species_list
            ).ask()
            self.controller.food_chain_remove(eater, eaten)
        else:
            console.print(f"No such operation: {operation} (expected: add/remove/view)")

    def do_eco_balance(self, arg):
        """Check current eco balance of the ecosystem (ratio: carnivore/herbivore)"""
        console.print("Current eco balance:\n---")
        balance = self.controller.get_eco_balance()
        for role, count in balance.items():
            console.print(f"  {role:<12}: {count}")

    def do_bio_diversity(self, arg):
        """Check current biodiversity of the ecosystem"""
        bio_diversity_index = self.controller.get_bio_diversity()
        console.print(f"Current bio diversity index: {bio_diversity_index}")

    def do_save(self, arg):
        """Save the ecosystem to a file

        :param arg: file_path
        :type arg: str (default: "/save_files/ecosystem.json")"""

        # TODO: save("ecosystem.json")

    def do_load(self, arg):
        """Load the ecosystem from a file

        :param arg: file_path
        :type arg: str (default: "/save_files/ecosystem.json")"""

    # TODO: load("ecosystem.json")

    def do_exit(self, arg):
        """Exit the program"""
        console.print("[bold red]Stop program...[/bold red]")
        return True
