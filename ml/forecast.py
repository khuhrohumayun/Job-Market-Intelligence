"""Small, explainable baseline for hiring-demand forecasting."""
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

def forecast_daily_demand(trend: pd.DataFrame, horizon_days: int = 30) -> tuple[pd.DataFrame, float | None]:
    """Fit a regularized linear trend; replace with time-series models after enough history exists."""
    series = trend.copy()
    series["posted_at"] = pd.to_datetime(series["posted_at"])
    series = series.groupby("posted_at", as_index=False)["jobs"].sum().sort_values("posted_at")
    if len(series) < 5: return pd.DataFrame(columns=["posted_at", "predicted_jobs"]), None
    series["day_index"] = (series.posted_at - series.posted_at.min()).dt.days
    split = max(3, int(len(series) * .8)); model = Ridge(alpha=1.0).fit(series[["day_index"]].iloc[:split], series.jobs.iloc[:split])
    mae = mean_absolute_error(series.jobs.iloc[split:], model.predict(series[["day_index"]].iloc[split:])) if split < len(series) else None
    future = pd.DataFrame({"day_index": range(int(series.day_index.max()) + 1, int(series.day_index.max()) + 1 + horizon_days)})
    future["posted_at"] = series.posted_at.min() + pd.to_timedelta(future.day_index, unit="D")
    future["predicted_jobs"] = model.predict(future[["day_index"]]).clip(0)
    return future[["posted_at", "predicted_jobs"]], mae
