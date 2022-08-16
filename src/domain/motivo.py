from src.abstractions.csv_typed_row import CSVTypedRow


class MotivoRow(CSVTypedRow):
    cod: int
    motivo: str
