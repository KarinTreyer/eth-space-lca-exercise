"""Helper functions for the FireSat II LCA exercise.

The notebook shows the Brightway steps that matter for understanding LCA. The code that only
reshapes tables or draws figures lives here, so that the notebook stays short.

Main idea: every LCIA score result is broken down to single exchanges of the foreground inventory
(one line of the Excel sheet = one row here). Each row carries
    contribution = (amount needed per functional unit) x (impact of 1 unit of the input)
and its data quality rating (DQR). The rows add up exactly to the total LCA score.
"""

import re
from pathlib import Path

import bw2calc as bc
import bw2data as bd
import bw2io as bi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize

FG = "firesat2"
EI = "ecoinvent-3.12-cutoff"
ESA = "ESA_LCA_selection_e3.12"
BIO = "ecoinvent-3.12-biosphere"
SPACE = "space_emissions"

# Flows that ecoinvent does not have. They get no characterisation factor in any method.
SPACE_FLOWS = {
    "al2o3_stratosphere": dict(name="Aluminium oxide, particles", categories=("air", "stratosphere")),
    "hcl_stratosphere": dict(name="Hydrogen chloride", categories=("air", "stratosphere")),
}

DQR_COLS = ["dqr_amount", "dqr_activity", "dqr_background_ds"]
DQR_CMAP = LinearSegmentedColormap.from_list("dqr", ["#c0392b", "#e67e22", "#f1c40f", "#27ae60"])
DQR_NORM = Normalize(vmin=1, vmax=4)


def short(method):
    """Readable label for an EF method tuple."""
    return method[2]


def unit_of(method):
    return bd.Method(method).metadata.get("unit", "")


def sig(x, n=5):
    """Number as text with n significant digits, e.g. 3,061,200 or 0.012346 (scientific only if tiny or huge)."""
    if x is None or not np.isfinite(x):
        return str(x)
    if x == 0:
        return "0"
    mag = int(np.floor(np.log10(abs(x))))
    if mag < -3 or mag >= 12:
        return f"{x:.{n - 1}e}"
    return f"{round(x, n - 1 - mag):,.{max(n - 1 - mag, 0)}f}"


# --------------------------------------------------------------------------- import

def ensure_space_flows():
    """Create the small biosphere database with flows that ecoinvent lacks (once per project)."""
    if SPACE in bd.databases:
        return
    bd.Database(SPACE).write({
        (SPACE, code): dict(flow, unit="kilogram", type="emission", database=SPACE)
        for code, flow in SPACE_FLOWS.items()
    })


def import_foreground(xlsx_path, db_name=FG):
    """Import the sheet 'lci' of the workbook as Brightway database `db_name`.

    Returns the importer. Raises an error with a table of unlinked exchanges if some
    names/locations/units in the Excel do not match an existing dataset.
    """
    ensure_space_flows()
    imp = bi.ExcelImporter(str(xlsx_path))
    imp.data = [ds for ds in imp.data if ds.get("database") == db_name]
    imp.apply_strategies()
    fields = ["name", "reference product", "unit", "location"]
    imp.match_database(fields=fields)
    imp.match_database(EI, fields=fields)
    imp.match_database(ESA, fields=fields)
    imp.match_database(BIO, fields=["name", "categories", "unit"])
    imp.match_database(SPACE, fields=["name", "categories", "unit"])

    unlinked = [
        {"activity": ds["name"], "input name": exc.get("name"), "reference product": exc.get("reference product"),
         "location": exc.get("location"), "unit": exc.get("unit"), "categories": exc.get("categories"),
         "database": exc.get("database")}
        for ds in imp.data for exc in ds.get("exchanges", []) if "input" not in exc
    ]
    if unlinked:
        table = pd.DataFrame(unlinked)
        print(table.to_string())
        raise ValueError(f"{len(unlinked)} exchange(s) could not be linked - check name, reference product, "
                         "location, unit and database in the Excel (table above).")
    if db_name in bd.databases:
        del bd.databases[db_name]
    imp.write_database()
    print(f"Imported {len(bd.Database(db_name))} activities into '{db_name}'.")
    return imp


def get_activity(name, db_name=FG):
    hits = [a for a in bd.Database(db_name) if a["name"] == name]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} activities called {name!r} in {db_name}")
    return hits[0]


def search(text, db_name=ESA, limit=20):
    """Search a database and return name, reference product, unit, location as a table."""
    rows = [{"name": a["name"], "reference product": a.get("reference product"), "unit": a["unit"],
             "location": a["location"]} for a in bd.Database(db_name).search(text, limit=limit)]
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- analysis

def exchange_table(fu_activity, amount=1.0):
    """Walk the foreground tree below the functional unit and list every background / biosphere exchange.

    `per_fu` is the amount of the input needed for the functional unit. `stage` is the first-level
    activity below the functional unit the exchange belongs to.
    """
    rows = []

    def walk(act, factor, stage):
        prod = sum(e["amount"] for e in act.production()) or 1.0
        for exc in act.exchanges():
            if exc["type"] == "production":
                continue
            inp = exc.input
            per_fu = factor * exc["amount"] / prod
            if exc["type"] == "technosphere" and inp["database"] == act["database"]:
                walk(inp, per_fu, stage or inp["name"])
                continue
            rows.append({
                "stage": stage or act["name"],
                "parent": act["name"],
                "input": inp["name"],
                "reference product": inp.get("reference product", ""),
                "location": inp.get("location", ""),
                "categories": "::".join(inp.get("categories", ())) if exc["type"] == "biosphere" else "",
                "database": inp["database"],
                "type": exc["type"],
                "amount": exc["amount"],
                "unit": inp["unit"],
                "per_fu": per_fu,
                **{c: exc.get(c) for c in DQR_COLS},
                "source": exc.get("source"),
                "comment": exc.get("comment"),
                "input_id": inp.id,
            })

    walk(fu_activity, amount, None)
    df = pd.DataFrame(rows)
    for c in DQR_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["dqr"] = df[DQR_COLS].mean(axis=1)
    return df


class Result:
    """Exchange-level LCA results for one functional unit and several impact categories."""

    def __init__(self, fu_activity, methods, table, unit_scores, cfs, totals):
        self.fu = fu_activity
        self.methods = methods
        self.table = table              # one row per foreground exchange
        self.unit_scores = unit_scores  # {input_id: {method: score per unit}}
        self.cfs = cfs                  # {flow_id: {method: CF}}
        self.totals = totals            # {method: total score from Brightway}

    def contributions(self, method):
        df = self.table.copy()
        df["score"] = [
            row.per_fu * (self.cfs[row.input_id][method] if row.type == "biosphere"
                          else self.unit_scores[row.input_id][method])
            for row in df.itertuples()
        ]
        df["share"] = df["score"] / df["score"].abs().sum()
        return df

    def check(self):
        """Contributions must add up to the Brightway total - a check that nothing was lost."""
        out = []
        for m in self.methods:
            s = self.contributions(m)["score"].sum()
            out.append({"impact category": short(m), "unit": unit_of(m), "Brightway total": self.totals[m],
                        "sum of contributions": s, "difference %": 100 * (s - self.totals[m]) / self.totals[m]})
        return pd.DataFrame(out)

    def summary_table(self):
        """Total score per impact category (numbers, used for the Excel export)."""
        return pd.DataFrame({"impact category": [short(m) for m in self.methods],
                             "unit": [unit_of(m) for m in self.methods],
                             "score": [self.totals[m] for m in self.methods]})

    def summary(self, digits=5):
        """Total score per impact category, shown with `digits` significant digits."""
        table = self.summary_table()
        table["score"] = table["score"].map(lambda x: sig(x, digits))
        return table


def unit_scores_for(input_ids, methods):
    """Impact of 1 unit of each input, all methods, with one MultiLCA (one matrix factorisation)."""
    config = {"impact_categories": list(methods)}
    demands = {str(i): {i: 1} for i in input_ids}
    data_objs = bd.get_multilca_data_objs(functional_units=demands, method_config=config)
    mlca = bc.MultiLCA(demands=demands, method_config=config, data_objs=data_objs)
    mlca.lci()
    mlca.lcia()
    return {i: {m: mlca.scores[(m, str(i))] for m in methods} for i in input_ids}, mlca


def as_demand(system):
    """Activity, activity name, or {activity or name: amount} -> {activity: amount}."""
    items = system.items() if isinstance(system, dict) else [(system, 1)]
    return {(get_activity(k) if isinstance(k, str) else k): float(v) for k, v in items}


def analyse(fu_activity, methods):
    """Run the LCA of the functional unit and break it down to single exchanges.

    `fu_activity` is one activity, or several with their amounts, e.g.
    {"FireSat II AIT and test campaign": 1, "FireSat II engineering, office work and travel": 1}.
    """
    demand = as_demand(fu_activity)
    table = pd.concat([exchange_table(act, amount) for act, amount in demand.items()], ignore_index=True)
    tech_ids = sorted(set(table.loc[table["type"] == "technosphere", "input_id"]))

    config = {"impact_categories": list(methods)}
    demands = {"FU": {act.id: amount for act, amount in demand.items()}, **{str(i): {i: 1} for i in tech_ids}}
    data_objs = bd.get_multilca_data_objs(functional_units=demands, method_config=config)
    mlca = bc.MultiLCA(demands=demands, method_config=config, data_objs=data_objs)
    mlca.lci()
    mlca.lcia()

    unit_scores = {i: {m: mlca.scores[(m, str(i))] for m in methods} for i in tech_ids}
    totals = {m: mlca.scores[(m, "FU")] for m in methods}
    cfs = {}
    for fid in set(table.loc[table["type"] == "biosphere", "input_id"]):
        row = mlca.dicts.biosphere[fid]
        cfs[fid] = {m: mlca.characterization_matrices[m][row, row] for m in methods}
    return Result(fu_activity, methods, table, unit_scores, cfs, totals)


# --------------------------------------------------------------------------- plots and tables

def plot_stages(res, title="Contribution of life cycle stages"):
    """Stacked bars: share of each stage per impact category (normalised by the sum of absolute values)."""
    data = {}
    for m in res.methods:
        c = res.contributions(m)
        data[short(m)] = c.groupby("stage")["score"].sum() / c["score"].abs().sum() * 100
    df = pd.DataFrame(data).T.fillna(0)
    ax = df.plot(kind="barh", stacked=True, figsize=(11, 0.6 * len(df) + 2), colormap="tab20", width=0.75)
    ax.set_xlabel("share of the total [%]")
    ax.set_title(title)
    ax.invert_yaxis()
    ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.show()
    return df.round(1)


def top_contributors(res, method, n=15):
    c = res.contributions(method)
    c["label"] = c["parent"].str.replace("FireSat II ", "", regex=False) + ": " + c["input"]
    c = c.reindex(c["score"].abs().sort_values(ascending=False).index).head(n)
    cols = ["label", "per_fu", "unit", "score", "share", "dqr"] + DQR_COLS + ["source", "comment"]
    return c[cols].reset_index(drop=True)


def plot_dqr_hotspots(res, method, n=15):
    """Largest contributors, coloured by their data quality (red = rough, green = very good)."""
    c = top_contributors(res, method, n)
    fig, ax = plt.subplots(figsize=(11, 0.4 * len(c) + 1.5))
    colours = [DQR_CMAP(DQR_NORM(d)) if pd.notna(d) else "lightgrey" for d in c["dqr"]]
    ax.barh(c["label"].str.slice(0, 70), c["share"] * 100, color=colours, edgecolor="black", linewidth=0.3)
    ax.invert_yaxis()
    ax.set_xlabel(f"share of total {short(method)} [%]")
    ax.set_title(f"Top {n} contributors to {short(method)}, coloured by data quality")
    sm = plt.cm.ScalarMappable(cmap=DQR_CMAP, norm=DQR_NORM)
    fig.colorbar(sm, ax=ax, label="mean DQR (1 rough - 4 very good); grey = not rated")
    plt.tight_layout()
    plt.show()


def plot_dqr_priority(res, method, label_top=8):
    """Where to collect better data first: large contribution AND low data quality (bottom-right corner)."""
    c = res.contributions(method)
    c = c[c["dqr"].notna()].copy()
    c["abs_share"] = c["share"].abs() * 100
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.axvspan(5, max(100, c["abs_share"].max() * 1.05), ymin=0, ymax=(2.5 - 0.8) / (4.2 - 0.8),
               color="#c0392b", alpha=0.08)
    ax.text(c["abs_share"].max() * 0.98, 0.9, "improve these data first", ha="right", color="#c0392b")
    ax.scatter(c["abs_share"], c["dqr"], s=40 + 4 * c["abs_share"], c=c["dqr"], cmap=DQR_CMAP, norm=DQR_NORM,
               edgecolor="black", linewidth=0.4)
    top = c.nlargest(label_top, "abs_share").reset_index(drop=True)
    for i, row in top.iterrows():
        ax.annotate(str(i + 1), (row.abs_share, row.dqr), fontsize=9, fontweight="bold",
                    xytext=(5, 5 + 7 * (i % 2)), textcoords="offset points")
    ax.set_xscale("symlog", linthresh=1)
    ax.set_ylim(0.8, 4.2)
    ax.set_xlabel(f"share of total {short(method)} [%] (log scale above 1 %)")
    ax.set_ylabel("mean DQR of the exchange (1 rough - 4 very good)")
    ax.set_title(f"Data collection priorities - {short(method)}")
    plt.tight_layout()
    plt.show()
    top.index = top.index + 1
    return top[["parent", "input", "abs_share", "dqr"]].rename(columns={"abs_share": "share %"}).round(2)


def dqr_summary(res):
    """Contribution-weighted DQR per impact category and per stage (ESA LCA Handbook Annex B logic).

    Unrated exchanges count as DQR 1 (as the Handbook rates missing information as worst quality).
    """
    out = {}
    for m in res.methods:
        c = res.contributions(m)
        w = c["score"].abs()
        d = c["dqr"].fillna(1)
        by_stage = (w * d).groupby(c["stage"]).sum() / w.groupby(c["stage"]).sum()
        out[short(m)] = pd.concat([pd.Series({"WHOLE SYSTEM": (w * d).sum() / w.sum()}), by_stage])
    df = pd.DataFrame(out)
    fig, ax = plt.subplots(figsize=(11, 0.5 * len(df) + 1.5))
    im = ax.imshow(df.values, cmap=DQR_CMAP, norm=DQR_NORM, aspect="auto")
    ax.set_xticks(range(df.shape[1]), df.columns, rotation=30, ha="right")
    ax.set_yticks(range(df.shape[0]), df.index)
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            ax.text(j, i, f"{df.values[i, j]:.1f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, label="contribution-weighted DQR")
    ax.set_title("How good are the data behind each result?")
    plt.tight_layout()
    plt.show()
    return df.round(2)


def flows_without_cf(res):
    """Direct emissions (biosphere exchanges in the foreground) with their amount and characterisation factors."""
    b = res.table[res.table["type"] == "biosphere"]
    if b.empty:
        return pd.DataFrame()
    rows = []
    for (flow, cat, fid), g in b.groupby(["input", "categories", "input_id"]):
        r = {"flow": flow, "compartment": cat, "kg per FU": g["per_fu"].sum()}
        for m in res.methods:
            r[f"CF {short(m)}"] = res.cfs[fid][m]
        rows.append(r)
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- what-if

def what_if(res, changes=(), add=(), name="variant"):
    """Recalculate the results after changing single exchanges, without touching the database.

    `changes` is a list of dicts with
        where   : function(row) -> True for the rows to change, e.g. lambda r: r.input.startswith("aluminium part")
        factor  : multiply the amount by this (optional, default 1; 0 removes the exchange)
        new     : a Brightway activity that replaces the input (optional)
    `add` is a list of (activity, amount per functional unit) to add, e.g. a variant from the Excel.
    Returns a table: base score, variant score and change in % per impact category.
    """
    table = res.table.copy()
    if add:
        extra_rows = pd.DataFrame([{"stage": "added in what-if", "parent": "what-if", "input": a["name"],
                                    "database": a["database"], "type": "technosphere", "unit": a["unit"],
                                    "per_fu": amount, "input_id": a.id} for a, amount in add])
        table = pd.concat([table, extra_rows], ignore_index=True)
    new_ids = {ch["new"].id for ch in changes if ch.get("new") is not None} | {a.id for a, _ in add}
    missing = sorted(new_ids - set(res.unit_scores))
    extra = unit_scores_for(missing, res.methods)[0] if missing else {}
    unit_scores = {**res.unit_scores, **extra}
    for ch in changes:
        mask = table.apply(ch["where"], axis=1)
        if not mask.any():
            print("Warning: a change matched no exchange")
        table.loc[mask, "per_fu"] *= ch.get("factor", 1.0)
        if ch.get("new") is not None:
            table.loc[mask, "input_id"] = ch["new"].id
            table.loc[mask, "input"] = ch["new"]["name"]
    var = Result(res.fu, res.methods, table, unit_scores, res.cfs, {})
    rows = []
    for m in res.methods:
        base = res.contributions(m)["score"].sum()
        new = var.contributions(m)["score"].sum()
        rows.append({"impact category": short(m), "unit": unit_of(m), "base": base, name: new,
                     "change %": 100 * (new - base) / base})
    return pd.DataFrame(rows)


def export(res, path):
    """Write all results (one sheet per impact category + summary) to Excel for your report."""
    path = Path(path)
    with pd.ExcelWriter(path) as xl:
        res.summary_table().to_excel(xl, sheet_name="summary", index=False)
        for m in res.methods:
            sheet = re.sub(r"[\[\]:*?/\\]", " ", short(m))[:31]
            res.contributions(m).drop(columns=["input_id"]).to_excel(xl, sheet_name=sheet, index=False)
    print("written", path.resolve())
