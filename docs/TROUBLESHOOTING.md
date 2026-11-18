# Troubleshooting

## Activity Browser does not start

| Message | Cause | Fix |
|---|---|---|
| `QtBindingsNotFound`, `No Qt bindings could be found`, `DLL load failed` while importing PySide6 | Two Qt libraries in one environment (e.g. `pyside2` or `qt-main` from conda next to `PySide6` from pip), or a PySide6 version Activity Browser does not support (6.12 or newer) | Create a fresh environment and install only with `pip install -r envs/requirements.txt` (INSTALL.md, step 3). Check with `pip list | grep -i pyside` (Windows: `pip list | findstr /i pyside`): only PySide6 6.11.2 may appear. |
| Activity Browser hangs at the start; the terminal shows `got multiple values for argument 'dataset'` | bw2data 4.8 was installed (e.g. by `pip install -U ...`) | `python -m pip install "bw2data==4.7"` |
| Windows: `DLL load failed` although only PySide6 6.11.2 is installed | Missing Microsoft C++ runtime | Install the "Microsoft Visual C++ Redistributable" (x64) from Microsoft and restart. |
| macOS: the window does not open, `could not find the Qt platform plugin "cocoa"` | Environment mixes conda and pip Qt | Fresh environment as above. |

Never run `pip install -U activity-browser` or `pip install -U bw2data` in the course environment - the versions
are pinned on purpose. Activity Browser suggests this update at every start ("There is an update
available ... Press any key to continue without updating"): press Enter and ignore it. If you did update,
reinstall with `python -m pip install -r envs/requirements.txt`.

## Jupyter

- **`ModuleNotFoundError: No module named 'bw2data'` in the notebook:** the notebook runs in another Python.
  In the activated environment run `python -m ipykernel install --user --name eth-lca` and select the kernel
  `eth-lca` in Jupyter (top right).
- **`ModuleNotFoundError: No module named 'lca_helpers'`:** start Jupyter from the repository folder and open
  the notebook from the `notebooks` folder.

## Brightway

- **`Project not found`:** the project archive has not been restored (INSTALL.md, step 4).
  `import bw2data as bd; print(bd.projects.dir)` shows where Brightway stores projects.
- **`... exchange(s) could not be linked`** after editing the Excel: the table above the error shows the line.
  Name, reference product, location and unit must be exactly as in the database (also upper/lower case and
  spaces). Copy them from Activity Browser or from `h.search("...")`.
- **The Excel file cannot be read or saved:** close it in Excel before re-running the import, or at least save it.
- **A result looks absurd:** check units first (kg vs. t, hour vs. day, man-hour vs. man-year), then read the
  dataset's comment. That is not a software problem, it is LCA.
