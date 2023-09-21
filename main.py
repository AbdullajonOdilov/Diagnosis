from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.openapi.models import Info
from starlette.middleware.cors import CORSMiddleware

from routes import login, users, uploaded_files, categories, questions, question_types, question_states, \
    question_state_answers, question_state_options, diagnostic_options, diagnostics, customers

app = FastAPI(
    title="Diagnostika",
    version="0.1.0",
    openapi_info=Info(
        title="Diagnostika",
        version="2.1.0"
    )
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {"message": "Welcome"}



app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(customers.customers_router)
app.include_router(categories.categories_router)
app.include_router(question_types.question_types_router)
app.include_router(questions.questions_router)

app.include_router(question_states.question_states_router)
app.include_router(question_state_options.question_state_options_router)
app.include_router(question_state_answers.question_state_answers_router)

app.include_router(diagnostic_options.diagnostic_options_router)
app.include_router(diagnostics.diagnostics_router)
app.include_router(uploaded_files.uploaded_files_router)
