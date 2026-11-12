from pathlib import Path

Base_Dir = Path(__file__).resolve().parent
Output_Dir = Base_Dir / "output"
Output_Dir.mkdir(exist_ok=True)

Db_Path = Base_Dir / "history.db"

Default_Box_Size = 10
Default_Border = 4
Default_Fill_Color = "black"
Default_Back_Color = "white"
Default_Error_Level = "M"
Allowed_Formats = ("PNG", "JPG")
Default_Format = "PNG"
Logo_Max_Ratio = 0.25