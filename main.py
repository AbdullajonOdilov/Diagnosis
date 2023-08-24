from fastapi import FastAPI

from routes import login, users, uploaded_files

app = FastAPI()


app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(uploaded_files.uploaded_files_router)
