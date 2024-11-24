from typing import Any

import pandas as pd


def rename_columns(data: pd.DataFrame):
    data = data.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Last": "last",
            "Close": "close",
            "Number of Shares": "number_of_shares",
            "Number of Trades": "number_of_trades",
            "Turnover": "turnover",
        }
    )
    return data


def daily_currency_dataframe(data: dict[str, Any]):
    # Extract series data
    series_data = data["data"]["dataSets"][0]["series"]
    structure = data["data"]["structure"]["dimensions"]

    # Extract dimensions and observation details
    base_cur = structure["series"][1]["values"][0]["id"]
    quote_cur = structure["series"][2]["values"][0]["id"]
    time_periods = structure["observation"][0]["values"]
    observations = series_data["0:0:0:0"]["observations"]

    # Prepare data for DataFrame
    records = []
    for obs_key, obs_value in observations.items():
        time_period = time_periods[int(obs_key)]["id"]
        exchange_rate = obs_value[0]
        records.append(
            {
                "timestamp": time_period,
                "base_currency": base_cur,
                "quote_currency": quote_cur,
                "exchange_rate": float(exchange_rate),
            }
        )

    # Return DataFrame
    return pd.DataFrame(records)
