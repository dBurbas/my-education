# 🐾 Animal world (Ecosystem) model

## 🏁 Intro

```text
                                                        
            .#H:    :H#.             █████╗ ███╗   ██╗██╗███╗   ███╗ █████╗ ██╗
          ~=##=~L  J~=##=~          ██╔══██╗████╗  ██║██║████╗ ████║██╔══██╗██║
          +=##=+|  |+=##=+          ███████║██╔██╗ ██║██║██╔████╔██║███████║██║
           H##WiT  TiW##H           ██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══██║██║
     t#t    TTT      TTT    t#t     ██║  ██║██║ ╚████║██║██║ ╚═╝ ██║██║  ██║███████╗
    .:#=+      .*=#=.      +=#:.    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝
   =gM##W;    *=%##%=*    ;W##Mg=  
   =gM##W!    =M%##%M=    !W##Mg=   ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗
     :v#;  .wHW$@##@$WHw.  ;#v:     ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
           whW$@####@$Whw           ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
          .=w%%$####$%%w=.          ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
          \Y%%$##NMN##$%%Y/         ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
           .=*&8#####8&*=.           ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝
                
```

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Tests](https://img.shields.io/badge/Tests-Pytest-success)
[![Rich](https://img.shields.io/badge/Rich-CLI-purple)](https://rich.readthedocs.io/)
[![Questionary](https://img.shields.io/pypi/v/questionary?label=questionary&color=blue&logo=python)](https://pypi.org/project/questionary/)
> This is an interactive ecosystem simulation model.
## ⚙️ Installation & Running

### Requirements
...
### Run
...

---

## 📝 About
> !!! Project is in development 🧱    

Project was made based on Lab #1 PPOIS BSUIR.
> ### Lab work task:
> - **Project domain**: ecosystem and interaction of living things
> - **Key entities**: animals, plants, ecosystem, biodiversity, and food chain.
> - **Key operations**: ecosystem interaction  operation, reproduction and survival  operation, resource consumption operation,  ecological balance operation, and threat  protection operation.

### Architecture 
The project follows the **MVC** split:

| Layer | Module | Responsibility |
|---|---|---|
| **Model** | `core/` | Simulation logic — organisms, ecosystem, food chain, event system |
| **View** | `interface/` | CLI rendering via `rich` and `questionary` |
| **Controller** | `controller/` | Mediates CLI commands <-> model; buffers event logs |

Project architecture is built with educational versions of some architecture design patterns:
| Pattern | Where |
|---|---|
| **Command** | `core/commands.py` — every action (eat, move, rest, reproduce, sound, photosynthesis) is a `Command` object |
| **Observer (Pub/Sub)** | `core/event_manager.py` — `EventManager` decouples event producers from consumers |
| **Factory** | `core/factory.py` — `DefaultOrganismFactory` centralises organism creation and species registration |
| **Prototype** | `core/organisms.py` — `Organism.clone()` produces offspring without coupling to concrete classes |
| **Interface segregation** | `core/ecosystem.py` — `IEcosystem` ABC exposes only the methods the controller needs 
### Project Structure

```
src/
├── config.py                  # Global simulation constants
├── main.py                    # Entry point — wires all components and starts the CLI
├── core/
│   ├── base.py                # Position dataclass and distance helpers
│   ├── enums.py               # EcosystemStatus and EventType enumerations
│   ├── event_manager.py       # Pub/Sub EventManager
│   ├── organisms.py           # Organism, Animal, Plant abstract base classes
│   ├── species.py             # Concrete species: Wolf, Rabbit, Fox, Grass
│   ├── commands.py            # Command objects: Eat, Move, Rest, Reproduce, Sound, Photosynthesis
│   ├── ecosystem.py           # FoodChain, Habitat, IEcosystem, Ecosystem
│   └── factory.py             # OrganismFactory ABC + DefaultOrganismFactory
├── controller/
│   └── controller.py          # SimulationController
├── interface/
│   ├── ecosystem_cli.py       # cmd.Cmd-based interactive CLI
│   └── event_formats.py       # Rich-formatted strings for each event type
└── exception/
    └── animal_world_exceptions.py  # Full exception hierarchy
```


### Functions:
> !!! Project is in development 🧱.   

#### Available commands

| Command | Arguments | Description |
|---|---|---|
| `run [N]` | N: int (default 1) | Advance simulation N steps; prints events per step |
| `stats` | - | Population table + biodiversity + eco-balance |
| `bio_diversity` | - | Print Margalef biodiversity index |
| `eco_balance` | - | Print organism count by trophic role |
| `organism [add\|remove\|view]` | operation (optional) | Add / remove / inspect an organism |
| `food_chain [add\|remove\|view]` | operation (optional) | Modify or display food chain rules |
| `save [path]` | path (optional) | ⚠️ Not yet implemented |
| `load [path]` | path (optional) | ⚠️ Not yet implemented |
| `help \| ? [cmd]` | command (optional) | Show help |
| `exit` | - | Stop the program | 
...

## 🖥️ Interface

CLI is built on Python's `cmd.Cmd` module with `rich` for output and `questionary` for interactive prompts.

### Program start
![Program start](readme_images/program_start.png)

### Quick start
![Program quick start / Commands list help](readme_images/program_quick_start.png)

### Events logs
![Program quick start / Commands list help](readme_images/event_logs_example.png)

### Extra info
Auto-complete is enabled via `readline` (Tab on Linux/Mac).

## TODOs:

- [ ] Fix energy balance (`config.py` TODO)
- [ ] Implement `save` / `load` (JSON serialisation)
- [ ] Add asexual / paired reproduction trigger in `Animal.behave`
- [ ] Add custom species creation from CLI
- [ ] Move all magic numbers to `config.py`
- [ ] Fix handling model exceptions in CLI
- [ ] Fix escaping predator from predator (predator1 eats predator2, predator2 eats predator1)
- [ ] Add richer basic implementation in main (more organisms, larger map)

