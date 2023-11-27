from aiogram.types import FSInputFile
from keyboards import kb_utils
from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import KEYBOARDS
from states.user_states import FSMAutoParsing
import pandas as pd
from dataframe_image import export
from seaborn import relplot

# Вспомогательные методы для парсера


async def time_calc(ads_number) -> int:  # Подсчёт времени на выгрузку
    return ads_number // 100 + 1 if ads_number // 100 > 0 else 1


async def get_url(message, state, parser, bot_message=None) -> None:  # Первоначальный поиск объявлений и начало парсинга
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await state.set_state(FSMAutoParsing.statistics)
    data = await state.get_data()
    url = await parser.find_clicker(data)
    if bot_message:
        await bot_message.delete()
    if url != "no-results":
        await message.answer(
            text=f'<a href="{url}">' + LEXICON_RU["link"] + "</a>",
            parse_mode="HTML",
        )
        await start_parse(message, url, parser, state)
    else:
        await message.answer(
            text=LEXICON_RU["not_found"] + LEXICON_RU["check_search"],
            reply_markup=keyboard,
        )


async def start_parse(message, url, parser, state) -> None:
    await state.set_state(FSMAutoParsing.statistics)
    pending_message = await message.answer(text=LEXICON_RU["time_to_unload"])
    parse_info = await parser.data_analyse(url)
    keyboard = kb_utils.create_reply_kb(2, *KEYBOARDS["start_menu"])
    await pending_message.delete()
    if parse_info == "no-results":
        await message.answer(text=LEXICON_RU["not_found"],
                             reply_markup=keyboard,
                             )
    elif parse_info[0] > 1000:
        await message.answer(text=LEXICON_RU["many_ads"],
                             reply_markup=keyboard,
                             )
    else:
        time_message = await message.answer(
            text=LEXICON_RU["ads_found"]
                 + f"{parse_info[0]}"
                 + LEXICON_RU["unloading_time"]
                 + f"{parse_info[1]}"
                 + LEXICON_RU["minutes"]
        )
        file = await parser.data_parse(url, message.from_user.id, parse_info[0])
        await state.update_data(file=file)
        await time_message.delete()
        keyboard = kb_utils.create_inline_kb(2, *KEYBOARDS["statistics"], skip=None)
        await message.answer_document(FSInputFile(file), reply_markup=keyboard)


async def get_statistics(file, user_id) -> FSInputFile:
    df_loaded = await load_df(file)
    mean_df = df_loaded.groupby("year")[["price", "mileage"]].mean()
    max_df = df_loaded.groupby("year")[["price", "mileage"]].max()
    min_df = df_loaded.groupby("year")[["price", "mileage"]].min()
    count_df = df_loaded.groupby("year")[["mileage"]].count()
    temp_df = pd.concat([mean_df, max_df, min_df, count_df], axis=1)
    temp_df = temp_df.set_axis(
        [
            "Сред. цена",
            "Сред. пробег",
            "Макс. цена",
            "Макс. пробег",
            "Мин. цена",
            "Мин. пробег",
            "Объявлений",
        ],
        axis=1,
    )
    lst = [
        df_loaded.price.mean(),
        df_loaded.mileage.mean(),
        df_loaded.price.max(),
        df_loaded.mileage.max(),
        df_loaded.price.min(),
        df_loaded.mileage.min(),
        df_loaded.mileage.count(),
    ]
    df_all = pd.DataFrame(lst).transpose()
    df_all = df_all.set_axis(
        [
            "Сред. цена",
            "Сред. пробег",
            "Макс. цена",
            "Макс. пробег",
            "Мин. цена",
            "Мин. пробег",
            "Объявлений",
        ],
        axis=1,
    )
    df_all = df_all.set_axis(["Все"], axis=0)
    result_df = pd.concat([df_all, temp_df])
    export(result_df, f"{user_id}.png")
    return FSInputFile(f"{user_id}.png")


async def get_plot(file, user_id) -> FSInputFile:
    df_loaded = await load_df(file)
    plot = relplot(
        x="price",
        y="mileage",
        marker="^",
        color="green",
        data=df_loaded[["price", "mileage"]],
    )
    ticks = plot.axes[0][0].get_xticks()
    digits_format = "{:,.1f}"
    if len(str(ticks)) < 9:
        digits_format = "{:,.2f}"
    labels = [digits_format.format(x) for x in ticks / 10 ** 6]
    plot.set_xticklabels(labels)
    plot.set_xlabels("Стоимость (млн)")
    plot.set_ylabels("Пробег")
    plot.savefig(f"{user_id}.png")
    return FSInputFile(f"{user_id}.png")


async def load_df(file) -> pd.DataFrame:
    pd.options.display.float_format = "{:,.0f}".format
    df_loaded = pd.read_csv(file, sep=";", usecols=["price", "year", "mileage"])
    df_loaded.dropna(how="all", inplace=True)
    df_loaded[["price", "mileage"]] = df_loaded[["price", "mileage"]].astype("float")
    df_loaded[["year"]] = df_loaded[["year"]].astype("int")
    return df_loaded
