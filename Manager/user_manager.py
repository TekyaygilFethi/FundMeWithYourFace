import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from FaceRecognition.recognition import capture
import pandas as pd


def CheckUserRole():
    df = pd.read_csv(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data/Excel/Users.csv")
    )

    captured_user = capture()
    id = captured_user[0]
    name = captured_user[1]

    user_role = None

    if id is not None and name is not None:
        user_role = df[(df["User"] == name) & (df["Id"] == int(id))]["Role"][0]

    return (name, user_role)
