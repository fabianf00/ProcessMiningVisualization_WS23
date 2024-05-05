import pandas as pd
from transformations.utils import cases_list_to_dict


class DataframeTransformations:
    def __init__(self):
        self.dataframe = None

    def set_dataframe(self, dataframe: pd.DataFrame) -> None:
        """setter for dataframe

        Parameters
        ----------
        dataframe : pd.DataFrame
            The DataFrame to be set
        """
        self.dataframe = dataframe

    def dataframe_to_cases_list(
        self,
        time_label: str = "timestamp",
        case_label: str = "case",
        event_label: str = "event",
    ) -> list[list[str, ...]]:
        """Transforms a DataFrame into a list of cases. Each case is a list of events.
        The events are sorted by timestamp and grouped by case.

        Parameters
        ----------
        time_label : str, optional
            column name of the timestamp column, by default "timestamp"
        case_label : str, optional
            column name of the case column, by default "case"
        event_label : str, optional
            column name of the event column, by default "event"

        Returns
        -------
        list[list[str, ...]]
            A list of cases, where each case is a list of events.

        Raises
        ------
        ValueError
            If a selected column is not found in the DataFrame
        """
        required_columns = [time_label, case_label, event_label]
        if not all(col in self.dataframe.columns for col in required_columns):
            # TODO: raise a custom exception
            raise ValueError("Selected columns not found in DataFrame")
        # Sort by timestamp
        sorted_dataframe = self.dataframe.sort_values(by=[time_label])

        result = (
            sorted_dataframe.groupby(case_label)[event_label]
            .apply(list)
            .reset_index(name="events")
        )
        return result["events"].tolist()

    def dataframe_to_cases_dict(
        timeLabel: str = "timestamp",
        caseLabel: str = "case",
        eventLabel: str = "event",
        **additional_columns
    ) -> dict[tuple[str, ...], int]:
        """transform a DataFrame into a dictionary of cases. Each case is a tuple of events.
        The dictionary maps each case to the number of occurrences.
        The events are sorted by timestamp and grouped by case.

        Parameters
        ----------
        time_label : str, optional
            column name of the timestamp column, by default "timestamp"
        case_label : str, optional
            column name of the case column, by default "case"
        event_label : str, optional
            column name of the event column, by default "event"

        Returns
        -------
        dict[tuple[str, ...], int]
            A dictionary of cases, where each case is a tuple of events, mapped to the number of occurrences.
        """
        cases_list = dataframe_to_cases_list(self.df, timeLabel, caseLabel, eventLabel)
        return cases_list_to_dict(cases_list)
