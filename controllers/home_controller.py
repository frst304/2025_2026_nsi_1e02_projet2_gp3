import pandas as pd

from models.region_service import DATE_COL_CANDIDATES, first_existing_column


class HomeController:

    def __init__(self, donnees, view):
        self.donnees = donnees
        self.view = view
        self.refresh()

    def refresh(self):
        total_hosp, total_deces = self._resume_national()
        self.view.set_stats(total_hosp=total_hosp, total_deces=total_deces)

    def _resume_national(self):
        date_col = first_existing_column(self.donnees, DATE_COL_CANDIDATES)
        if date_col:
            donnees_dates = self.donnees.copy()
            donnees_dates[date_col] = pd.to_datetime(
                donnees_dates[date_col], errors="coerce"
            )
            date_max = donnees_dates[date_col].max()
            if pd.notna(date_max):
                donnees_filtrees = donnees_dates[
                    donnees_dates[date_col] == date_max
                ]
            else:
                donnees_filtrees = self.donnees
        else:
            donnees_filtrees = self.donnees

        total_hosp = (
            donnees_filtrees["hosp"].sum()
            if "hosp" in donnees_filtrees.columns
            else None
        )
        total_deces = (
            donnees_filtrees["dchosp"].sum()
            if "dchosp" in donnees_filtrees.columns
            else None
        )
        return total_hosp, total_deces
