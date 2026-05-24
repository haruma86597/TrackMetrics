import pandas as pd

def export_to_csv(datalist: list[dict], file_path: str = "result.csv"):
    df = pd.DataFrame(datalist)
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
