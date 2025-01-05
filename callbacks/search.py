import datetime
import requests as req
from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from my_secrets import API_URL, API_KEY
from models.search_model import SearchResult

router = Router()


@router.inline_query()
async def handle(query: InlineQuery):
    filter_text = query.query
    if filter_text == "" or filter_text is None:
        return query.answer(
            [
                InlineQueryResultArticle(
                    id=str(-1),
                    title="Замены уксивтика",
                    description="Добавь текст для поиска",
                    url="uksivt.xyz",
                    thumbnail_url="https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/00020_3223582996_Cyber_Whale__blue__gradient_background._4k._realistic._Technologt__cyberpunk._photo_realistic__Neomorphism._Beatiful_whale_arrow.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzLzAwMDIwXzMyMjM1ODI5OTZfQ3liZXJfV2hhbGVfX2JsdWVfX2dyYWRpZW50X2JhY2tncm91bmQuXzRrLl9yZWFsaXN0aWMuX1RlY2hub2xvZ3RfX2N5YmVycHVuay5fcGhvdG9fcmVhbGlzdGljX19OZW9tb3JwaGlzbS5fQmVhdGlmdWxfd2hhbGVfYXJyb3cuanBnIiwiaWF0IjoxNzIwMzg5NDc3LCJleHAiOjE3NTE5MjU0Nzd9.OVlPHGRQT0cKQHoIf2q5W7BHUmIbGeMO5k1kyUoIntc&t=2024-07-07T21%3A57%3A56.837Z",
                    input_message_content=InputTextMessageContent(
                        message_text="uksivt.xyz",
                    ),
                )
            ],
            cache_time=1,
            is_personal=True,
        )
    response: list[dict] = req.get(
        f"{API_URL}search/search/{filter_text}", headers={"X-API-KEY": API_KEY}
    ).json()
    print(response)
    if len(response) == 0:
        return query.answer(
            [
                InlineQueryResultArticle(
                    id=str(-1),
                    title="Нет результатов",
                    description="Попробуй что-то другое",
                    url="uksivt.xyz",
                    thumbnail_url="https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/Group%201573.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL0dyb3VwIDE1NzMucG5nIiwiaWF0IjoxNzI0Mzk1MjQ4LCJleHAiOjIwMzk3NTUyNDh9.LQH1lSml7HUaWSrkRnxxxS8DJMiRvQJEHp_ErZZLsRE&t=2024-08-23T06%3A40%3A47.304Z",
                    input_message_content=InputTextMessageContent(
                        message_text="что я выбрал",
                    ),
                )
            ],
            cache_time=1,
            is_personal=True,
        )
    if len(response) > 50:
        return query.answer(
            [
                InlineQueryResultArticle(
                    id=str(-1),
                    title="Слишком много результатов",
                    description="Уточни конкретнее",
                    url="uksivt.xyz",
                    thumbnail_url="https://ojbsikxdqcbuvamygezd.supabase.co/storage/v1/object/sign/zamenas/python_(1).png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJ6YW1lbmFzL3B5dGhvbl8oMSkucG5nIiwiaWF0IjoxNzIwMzg2MDg0LCJleHAiOjE3NTE5MjIwODR9.Xn_fkGftIEKCGFwQRK8JY0HPNnJax6uU8RtxmDUD0A0&t=2024-07-07T21%3A01%3A23.755Z",
                    input_message_content=InputTextMessageContent(
                        message_text="что я выбрал",
                    ),
                )
            ],
            cache_time=1,
            is_personal=True,
        )
    search_items: list[SearchResult] = [
        SearchResult(**search_item) for search_item in response
    ]
    results = []
    for search_item in search_items:
        results.append(
            InlineQueryResultArticle(
                id=str(search_item.search_id),
                title=search_item.search_name,
                url="uksivt.xyz",
                input_message_content=InputTextMessageContent(
                    message_text=f"/{search_item.search_type} {search_item.search_id} {datetime.datetime.now().timestamp()}",
                ),
                thumbnail_url=search_item.search_image,
            )
        )
    await query.answer(results, cache_time=300, is_personal=False)
