from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import CommonSG
from keyboards import common_kbs


router = Router()


@router.message(CommonSG.choosing_action, F.text.casefold() == 'book')
async def book(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer("choose booking date: ", reply_markup=common_kbs.get_weekday_kb())
    await state.set_state(CommonSG.choosing_date)


@router.callback_query(CommonSG.choosing_date)
async def get_date(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date=callback.data)
    await callback.answer()
    await callback.message.answer('date: ' + callback.data, reply_markup=ReplyKeyboardRemove())
    await callback.message.answer('\nchoose time (hh:mm): ', reply_markup=common_kbs.get_timeslot_kb())
    await state.set_state(CommonSG.choosing_time)


@router.message(CommonSG.choosing_time, F.text.regexp(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'))
async def choose_time(message: Message, state: FSMContext):
    await state.update_data(booking_time=message.text)
    await message.answer("booked!", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CommonSG.booking)


@router.message(CommonSG.choosing_time)
async def invalid_time(message: Message):
    await message.answer("invalid time", reply_markup=ReplyKeyboardRemove())



@router.message(CommonSG.choosing_action, F.text.casefold() == 'list')
async def list(message: Message, state: FSMContext):
    await message.answer("your bookings", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CommonSG.choosing_time)
