from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def support(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    answer_text = """<b>F.A.Q</b>

                
<b>1️⃣Допускается ли нахождение в одной команде учащихся из разных школ?</b>
Да, допускается.

<b>2️⃣Как я могу поучаствовать в турнире?</b>
Для начала - необходимо собрать команду из 5 человек. После этого 
каждому члену команды необходимо пройти регистрацию с помощью Телеграм-бота.
                        
<b>3️⃣Как проходит процесс регистрации?</b>
В Телеграм-боте вам необходимо будет ввести следующие данные: ФИО, 
придуманный никнейм, используемый для идентификации игрока 
непосредственно в рамках турнира, Ваши аккаунты в Discrod и Fastcup.
                                                     
<b>4️⃣Как верифицируются участники турнира?</b>
В процессе регистрации вам будет предложено отправить фотографию 
документа, удостоверяющего личность. От участника не требуется 
изображение всего документа, на изображении должны быть видны только 
дата рождения, ФИО и фотография участника.
                                      
<b>5️⃣На основе какой площадки проводится турнир?</b>

Площадка, на основе которой проводится турнир - Fastcup.
                                                   
<b>6️⃣Будет ли турнир транслироваться в прямом эфире?</b>
Да, прямая трансляция будет проходить на Youtube.
                                                 
<b>7️⃣Есть ли помимо сайта еще какие-либо информационные ресурсы турнира?</b>
Официальный канал в Телеграме https://t.me/burning_cup - используется для публикации 
актуальных новостей и важных сообщений. 
Discord сервер https://discord.gg/7NHjPA4UhP - используется для координации взаимодействия 
между непосредственными участниками и организаторами турнира. Доступ к 
нему имеют только игроки и организаторы. Официальная группа СПК в Вконтакте https://t.me/SPKCSGOBOT                      
                            
<b>8️⃣Я хочу ознакомиться с более подробной информацией о проведении турнира. Где мне ее найти?</b>
Ознакомиться с регламентом турнира можно на сайте https://burning-cup.ru/ или в соответствующем разделе бота.
                     
Если вы не нашли ответ на вопрос, который Вас интересовал пишите: https://t.me/Trofimkt, https://t.me/aheregoznaet

Если вы нашли ошибку на сайте или в боте пишите: https://t.me/lxrd1995."""

    await call.message.answer(text=answer_text)


def register_handlers_support(dp: Dispatcher):
    dp.register_callback_query_handler(support, text=["support"], state="*")
