from fastapi import FastAPI
from fastapi.openapi.models import Info
from routes import login, users, uploaded_files, categories, questions, question_types,question_states,\
    question_state_answers,question_state_options,diagnostic_options,diagnostics

app = FastAPI(
    title="Diagnostika",
    version="0.1.0",
    openapi_info=Info(
        title="Diagnostika",
        version="2.1.0"
    )
)
@app.get('/')
def home():
    return {"message": "Welcome"}

app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(categories.categories_router)

app.include_router(questions.questions_router)
app.include_router(question_types.question_types_router)
app.include_router(question_states.question_states_router)
app.include_router(question_state_answers.question_state_answers_router)
app.include_router(question_state_options.question_state_options_router)
app.include_router(diagnostic_options.diagnostic_options_router)
app.include_router(diagnostics.diagnostics_router)
app.include_router(uploaded_files.uploaded_files_router)
