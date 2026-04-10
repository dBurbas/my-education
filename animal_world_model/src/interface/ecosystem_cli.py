from controller.controller import SimulationController
from interface.event_formats import EVENT_FORMATS
from exception.animal_world_exceptions import AnimalWorldError
import cmd
from rich.console import Console
from rich.table import Table
from rich.progress import track
from time import sleep as time_sleep
import questionary
import readline

console = Console()

# Auto-complete commands for Mac/Linux
if readline.__doc__ and "libedit" in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


# TODO: add handling exit from operations
class EcosystemCLI(cmd.Cmd):
    """Interactive command-line interface for the Animal World simulation.

    Built on top of :mod:`cmd.Cmd`. Uses ``rich`` for formatted output and
    ``questionary`` for interactive prompts.

    :param controller: The simulation controller to delegate all commands to.
    :type controller: SimulationController
    """

    prompt = "\033[1;36m❀(eco)*\033[0m "

    def __init__(self, controller: SimulationController):
        super().__init__()
        self.controller = controller

    def preloop(self):
        """Print the ASCII-art logo and quick-start hint before entering the command loop."""
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
        console.print(
            "[bold #6ABB00]✿ Animal World Simulation v0.6.1 ✿[/bold #6ABB00]\n"
        )
        console.print("? Type [cyan]help[/] or [cyan]?[/] for list of commands.\n")

    def cmdloop(self, intro=""):
        while True:
            try:
                super().cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("^C")
                self.do_exit("")
                return True

    def do_help(self, arg):
        """Show the standard help listing, then print a quick-start command summary.

        :param arg: Optional command name to get help for.
        :type arg: str
        """
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
        console.print("- [dim]load[/]   — load ecosystem from file")
        console.print("- [dim]save[/]   — save ecosystem in file")
        console.print("- [green]exit[/]  — exit program\n")

    def do_run(self, arg):
        """Run the ecosystem simulation for N steps and display events per step.

        :param arg: Number of steps to run. Defaults to 1 if not set.
        :type arg: str
        """

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
        if steps > 200:
            console.print("Too many steps. (max: 200)")
            return
        console.print(f"[green]Running simulation for {steps} step(s)...[/]")
        for step in track(range(steps), description="Simulating :) ..."):
            time_sleep(0.03)

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
        """Display a population table followed by biodiversity and eco-balance summaries.

        :param arg: Unused.
        :type arg: str
        """
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
        try:
            self.do_bio_diversity(arg)
        except AnimalWorldError as error:
            console.print(f"[red]Bio diversity error: {error}[/]")
        self.do_eco_balance(arg)
        operation = questionary.confirm("Do you want to see all organisms stats?").ask()
        if operation:
            stats_list = self.controller.get_all_organisms_stats()
            for stats in stats_list:
                table = Table(title=f"{stats['name']} ({stats['type']})")
                table.add_column("Parameter", style="cyan")
                table.add_column("Value", style="magenta")

                table.add_row("Health", str(stats["health"]))
                table.add_row("Energy", str(stats["energy"]))
                table.add_row("Age", str(stats["age"]))
                table.add_row("Size", f"{stats['size']:.2f}")
                table.add_row("Cord. X", f"{stats['cord_x']:.1f}")
                table.add_row("Cord. Y", f"{stats['cord_y']:.1f}")
                console.print(table)

    def do_organism(self, arg):
        """Manage organisms: add a new one, remove an existing one, or view its stats.

        If ``arg`` is not set, an interactive selection prompt is shown.

        .. note::
            ``arg`` is capitalised before comparison, so ``add``, ``Add``, and ``ADD``
            are all accepted.

        :param arg: Operation name — one of ``add``, ``remove``, ``view``.
        :type arg: str
        """
        operation: str = arg
        if not arg:
            operation = questionary.select(
                "Which operation to do?", choices=["Add", "Remove", "View"]
            ).ask()

        operation = operation.capitalize()

        species_list = self.controller.get_available_species()

        if operation == "View":
            # TODO: remove duplicating code(enter name)
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
                table.add_row("Cord. X", f"{stats['cord_x']:.1f}")
                table.add_row("Cord. Y", f"{stats['cord_y']:.1f}")
                console.print(table)
            return

        if operation == "Add":
            organism_type: str = questionary.select(
                "Which organism would you like to choose?",
                choices=species_list,
            ).ask()
            org_name: str = questionary.text(
                "Enter the name of organism:",
                validate=lambda text: (
                    True if len(text.strip()) > 0 else "Name cannot be empty!"
                ),
            ).ask()
            org_x: int = int(
                questionary.text(
                    "Enter x coordinate of organism to spawn:",
                    validate=lambda text: (
                        (text.isdigit()) or "Please enter a valid number"
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
            is_changing_traits = questionary.confirm(
                "Do you want to change organism characteristics?(def:No)", default=False
            ).ask()
            extra_kwargs = {}
            if is_changing_traits:
                traits = self.controller.get_traits(organism_type)

                for trait_name, (trait_type, min_val, max_val) in traits.items():

                    def make_validator(t, lo, hi):
                        def validate(text):
                            if t is str:
                                return (
                                    True
                                    if len(text.strip()) > 0
                                    else "Field cannot be empty"
                                )
                            try:
                                v = t(text)
                                if lo <= v <= hi:
                                    return True
                                return f"Value must be between {lo} and {hi}"
                            except ValueError:
                                return f"Enter a valid {t.__name__}"

                        return validate

                    value = questionary.text(
                        f"{trait_name} ({trait_type.__name__}, {min_val}–{max_val}):",
                        validate=make_validator(trait_type, min_val, max_val),
                    ).ask()

                    extra_kwargs[trait_name] = trait_type(value)
            try:
                self.controller.add_organism(
                    organism_type, name=org_name, x=org_x, y=org_y, **extra_kwargs
                )
            except AnimalWorldError as error:
                console.print(f"[red]Error:{error}[/]")
            console.print(
                f"[green]{organism_type} '{org_name}' was successfully added.[/green]\n"
            )

        elif operation == "Remove":
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
            try:
                self.controller.remove_organism(organism_id)
            except AnimalWorldError as error:
                console.print(f"[red]Error:{error}[/]")
        else:
            console.print(f"No such operation: {operation} (expected: add/remove/view)")

    def do_food_chain(self, arg):
        """Manage the ecosystem food chain: add/remove rules, or view the current chain.

        If ``arg`` is not set, an interactive selection prompt is shown.

        .. note::
            ``arg`` is capitalised before comparison, so ``add``, ``Add``, and ``ADD``
            are all accepted.

        :param arg: Operation name — one of ``add``, ``remove``, ``view``.
        :type arg: str
        """
        operation: str = arg
        if not operation:
            operation = questionary.select(
                "Which operation to do?", choices=["Add", "Remove", "View"]
            ).ask()
        operation = operation.capitalize()
        if operation == "View":
            food_chain = self.controller.get_food_chain()
            console.print("Food chain: \n---")
            for org_type, eats in food_chain.items():
                animal_name = org_type.__name__
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
            try:
                self.controller.food_chain_add(eater, eaten)
            except AnimalWorldError as error:
                console.print(f"[red]Error:{error}[/]")
        elif operation == "Remove":
            eater = questionary.select("Choose eater:", choices=species_list).ask()
            eaten = questionary.select(
                "Choose pray(eaten):", choices=species_list
            ).ask()
            try:
                self.controller.food_chain_remove(eater, eaten)
            except AnimalWorldError as error:
                console.print(f"[red]Error:{error}[/]")
        else:
            console.print(f"No such operation: {operation} (expected: add/remove/view)")

    def do_eco_balance(self, arg):
        """Print the current ecological balance (count per trophic role).

        :param arg: Unused.
        :type arg: str
        """
        console.print("Current eco balance:\n---")
        balance = self.controller.get_eco_balance()
        for role, count in balance.items():
            console.print(f"  {role:<12}: {count}")

    def do_bio_diversity(self, arg):
        """Print the current Margalef biodiversity index.

        :param arg: Unused.
        :type arg: str
        """
        try:
            bio_diversity_index = self.controller.get_bio_diversity()
        except AnimalWorldError as error:
            console.print(f"[red]Bio diversity error: {error}[/]")
            return
        console.print(f"Current bio diversity index: {bio_diversity_index}")

    def do_save(self, arg):
        """Save the current ecosystem state to a file.

        .. warning::
            **Not implemented.** Method body is empty — will silently do nothing.

        :param arg: Target file path. Defaults to ``/save_files/ecosystem.json``.
        :type arg: str
        """
        console.print("[bold yellow]To be implemented...[/]")
        # TODO: save("ecosystem.json")

    def do_load(self, arg):
        """Load an ecosystem state from a file.

        .. warning::
            **Not implemented.** Method body is empty — will silently do nothing.

        :param arg: Source file path. Defaults to ``/save_files/ecosystem.json``.
        :type arg: str
        """
        console.print("[bold yellow]To be implemented...[/]")

    # TODO: load("ecosystem.json")

    def do_exit(self, arg):
        """Exit the CLI and stop the program.

        :param arg: Unused.
        :type arg: str
        :return: ``True`` to signal :meth:`cmd.Cmd.cmdloop` to terminate.
        :rtype: bool
        """
        console.print("[bold red]Stop program...[/bold red]")
        return True
