# Installation - please finish before the course day

You need about 6 GB of free disk space and a laptop with Windows, macOS or Linux.
If you get stuck, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) and contact the TAs **before** the course day.

## 1  Install Miniforge (recommended)

Download and install Miniforge: <https://conda-forge.org/download/>.
On Windows, use the *Miniforge Prompt* from the start menu for all commands below.

(If you already work with Python 3.12 and `venv`, you can use that instead - see step 3b.)

## 2  Get the course material

Either `git clone https://github.com/KarinTreyer/eth-space-lca-exercise.git` or, on the
[repository page](https://github.com/KarinTreyer/eth-space-lca-exercise), click *Code → Download ZIP* and unzip it.
Open the prompt in the repository folder (the folder that contains `EXERCISE.md`).

## 3  Create the Python environment

### 3a  With Miniforge

```bash
conda create -n eth-lca python=3.12 -y
conda activate eth-lca
python -m pip install -r envs/requirements.txt
```

Install **everything with pip** as shown. Do not add conda packages such as `pyside2`, `pyside6` or
`activity-browser` from conda channels to this environment - mixing Qt libraries from conda and pip is the most common reason why Activity Browser does not start.

### 3b  Alternative: plain Python 3.12 with venv

```bash
python3.12 -m venv .venv              # Windows: py -3.12 -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -m pip install -r envs/requirements.txt
```

## 4  Restore the course database (Brightway project)
Download the project backup file `brightway2-project-eth_space_lca_2026-backup.tar.gz` (about 1-2 GB). 
!!! By downloading and using this file, you accept that you must not share the project and not use it other than for the purpose of this course and a dedicated project work in the spring semester. !!!
Do not share it: it contains ecoinvent (ETH teaching licence) and a selection of the ESA LCA database (which requires a valid ecoinvent license).

With the environment activated:

```bash
python -c "import bw2io as bi; bi.restore_project_directory(r'PATH/TO/brightway2-project-eth_space_lca_2026-backup.tar.gz')"
```

## 5  Check everything

```bash
jupyter lab
```

Open `notebooks/00_setup_check.ipynb` and run all cells. The last cell must print `All good`.

## 6  Start Activity Browser once

In the activated environment:

```bash
activity-browser
```

**If the terminal says "There is an update available for the Activity Browser ... Press any key to continue
without updating": press Enter and do NOT update.** The update would replace the tested versions and Activity Browser would most likely no longer start.

The first start can take a minute. Select the project `eth_space_lca_2026` (drop-down at the top left) and search for "solar array" in the database `ESA_LCA_selection_e3.12`.

If Activity Browser does not start, report the error message to karin.treyer@psi.ch . You can still do the whole exercise in the notebook.
