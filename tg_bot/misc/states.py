from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


class SearchArticle(StatesGroup):
    step1 = State()
    step2 = State()
