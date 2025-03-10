import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Julia"]
usernames = ["alice", "bob", "charlie", "david", "eve", "frank", "grace", "hannah", "ivan", "julia"]
passwords = ["XXX", "XXX", "XXX", "XXX", "XXX", "XXX", "XXX", "XXX", "XXX", "XXX"]

hashed_passwords = stauth.Hasher(passwords)

file_path = Path(__file__).parent / "hashed_psw.pkl"

with open(file_path, "wb") as f:
    pickle.dump(hashed_passwords, f)