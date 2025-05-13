INSERT INTO app_socialmediatype (type) VALUES
('Facebook'),
('Twitter'),
('Instagram'),
('LinkedIn'),
('YouTube'),
('TikTok'),
('Pinterest'),
('Reddit'),
('Snapchat'),
('Telegram'),
('VKontakte'),
('Odnoklassniki'),
('WeChat'),
('WhatsApp'),
('Viber'),
('Line'),
('Tumblr'),
('Flickr'),
('Quora'),
('Medium'),
('Twitch'),
('Discord'),
('Signal'),
('Clubhouse'),
('Meetup'),
('Nextdoor'),
('Goodreads'),
('Xing'),
('Mix'),
('Periscope');

INSERT INTO app_reservationstatus (status) VALUES
('Оплачено'),
('Отменено'),
('Завершено'),
('Клиент не явился'),
('Ожидание оплаты'),
('Возврат средств'),
('Перенесено'),
('Отклонено');

-- Скрипт заполнения таблицы Company тестовыми данными
INSERT INTO app_company (name, phone, address, slug) VALUES
('ООО "Ромашка"', '79161234567', 'г. Москва, ул. Ленина, д. 10', 'romashka'),
('АО "ТехноПром"', '79031234567', 'г. Санкт-Петербург, Невский пр-т, д. 25', 'tehnoprom'),
('ИП Иванов И.И.', '79211234567', 'г. Новосибирск, ул. Кирова, д. 5', 'ip-ivanov-ii'),
('ЗАО "СтройГарант"', '79531234567', 'г. Екатеринбург, ул. Мира, д. 15', 'stroygarant'),
('ООО "АгроТех"', '79651234567', 'г. Казань, ул. Гагарина, д. 30', 'agroteh'),
('Фитнес клуб "Энерджи"', '79871234567', 'г. Сочи, ул. Приморская, д. 42', 'fitness-klub-enerdji'),
('Кафе "Уют"', '79991234567', 'г. Владивосток, ул. Портовая, д. 8', 'kafe-uyut'),
('Салон красоты "Элегант"', '79331234567', 'г. Калининград, ул. Балтийская, д. 12', 'salon-krasoty-elegant'),
('ООО "ИТ Сервис"', '79771234567', 'г. Нижний Новгород, ул. Горького, д. 50', 'it-servis'),
('Аптека "Здоровье"', '79441234567', 'г. Ростов-на-Дону, ул. Садовая, д. 20', 'apteka-zdorove');

-- Скрипт заполнения таблицы SocialMedia тестовыми данными
-- Предполагаем, что таблицы SocialMediaType и Company уже заполнены

INSERT INTO app_socialmedia (media_type_id, reference, target_id, date_to) VALUES
-- Для ООО "Ромашка" (id=1)
(1, 'https://facebook.com/romashka', 1, NOW() + INTERVAL '1 year'),
(3, 'https://instagram.com/romashka_official', 1, NOW() + INTERVAL '1 year'),

-- Для АО "ТехноПром" (id=2)
(1, 'https://facebook.com/tehnoprom', 2, NOW() + INTERVAL '1 year'),
(2, 'https://twitter.com/tehnoprom', 2, NOW() + INTERVAL '1 year'),
(4, 'https://linkedin.com/company/tehnoprom', 2, NOW() + INTERVAL '1 year'),

-- Для ИП Иванов И.И. (id=3)
(10, 'https://t.me/ivanov_business', 3, NOW() + INTERVAL '1 year'),
(14, 'whatsapp://send?phone=79211234567', 3, NOW() + INTERVAL '1 year'),

-- Для ЗАО "СтройГарант" (id=4)
(1, 'https://facebook.com/stroygarant', 4, NOW() + INTERVAL '1 year'),
(5, 'https://youtube.com/c/stroygarant', 4, NOW() + INTERVAL '1 year'),

-- Для Кафе "Уют" (id=7)
(3, 'https://instagram.com/cafe_uyut', 7, NOW() + INTERVAL '1 year'),
(6, 'https://tiktok.com/@cafe_uyut', 7, NOW() + INTERVAL '1 year'),
(7, 'https://pinterest.com/cafeuyut', 7, NOW() + INTERVAL '1 year');

-- Скрипт заполнения таблицы Tour тестовыми данными
-- Предполагаем, что таблица Company уже заполнена

INSERT INTO app_tour
(company_id, title, slug, img_preview_url, short_description) VALUES
-- Для ООО "Ромашка" (id=1)
(1, 'Экскурсия по Золотому Кольцу', 'golden-ring', 'https://example.com/img/golden-ring.jpg', '5-дневный тур по древним городам России'),

-- Для ООО "Ромашка" (id=1)
(1, 'Отдых на Байкале', 'baikal-vacation', 'https://example.com/img/baikal.jpg', 'Незабываемые выходные на берегу озера Байкал'),

-- Для АО "ТехноПром" (id=2)
(2, 'Промышленный тур по Москве', 'industrial-moscow', 'https://example.com/img/industrial.jpg', 'Экскурсии на ведущие предприятия столицы'),

-- Для ИП Иванов И.И. (id=3)
(3, 'Рыбалка на Волге', 'volga-fishing', 'https://example.com/img/fishing.jpg', 'Трофейная рыбалка с опытными гидами'),

-- Для ЗАО "СтройГарант" (id=4)
(4, 'Архитектурный Петербург', 'architecture-spb', 'https://example.com/img/spb-arch.jpg', 'Знакомство с архитектурными шедеврами Северной столицы'),

-- Для Кафе "Уют" (id=7)
(7, 'Гастрономический тур по Сочи', 'sochi-food', 'https://example.com/img/sochi-food.jpg', 'Дегустация местной кухни с посещением лучших ресторанов'),

-- Для Аптека "Здоровье" (id=10)
(10, 'Тур по здравницам Кавказа', 'kavkaz-spa', 'https://example.com/img/spa.jpg', 'Оздоровительные программы в лучших санаториях');

-- Скрипт заполнения таблицы TourInfo тестовыми данными
-- Предполагаем, что таблица Tour уже заполнена с id от 1 до 7

INSERT INTO app_tourinfo
(tour_id, description, price, img_url, img_background_url, placed) VALUES
(1, '5-дневный тур по древним городам России с проживанием в отелях 4*. Включено: транспорт, питание, экскурсии с гидом, входные билеты в музеи.', 35000.00,
 'https://example.com/img/golden-ring-detail.jpg',
 'https://example.com/img/golden-ring-bg.jpg',
 'Маршрут: Сергиев Посад → Переславль-Залесский → Ростов Великий → Ярославль → Кострома → Иваново → Суздаль → Владимир'),

(2, 'Выходные на Байкале с проживанием в гостевом доме. Включено: трансфер, 2-разовое питание, экскурсия на катере, посещение музея Байкала.', 12500.00,
 'https://example.com/img/baikal-detail.jpg',
 'https://example.com/img/baikal-bg.jpg',
 'Поселок Листвянка, Иркутская область'),

(3, 'Экскурсии на промышленные предприятия Москвы с экспертами. Включено: транспорт, обед, защитная экипировка, сувенирная продукция.', 8500.00,
 'https://example.com/img/industrial-detail.jpg',
 'https://example.com/img/industrial-bg.jpg',
 'Москва, предприятия: АвтоВАЗ, Ростех, Московский завод полиметаллов'),

(4, '3-дневная рыбалка с проживанием в домике у воды. Включено: аренда лодок, снаряжения, услуги егеря, обработка улова.', 18000.00,
 'https://example.com/img/fishing-detail.jpg',
 'https://example.com/img/fishing-bg.jpg',
 'Астраханская область, дельта реки Волги'),

(5, '3-дневный тур по архитектурным памятникам Петербурга с искусствоведом. Включено: проживание, завтраки, все экскурсии.', 22000.00,
 'https://example.com/img/spb-arch-detail.jpg',
 'https://example.com/img/spb-arch-bg.jpg',
 'Санкт-Петербург, основные локации: Дворцовая площадь, Петропавловская крепость, Исаакиевский собор'),

(6, '2-дневный гастротур с дегустацией 15 блюд. Включено: питание, мастер-классы от шеф-поваров, винные пары.', 9500.00,
 'https://example.com/img/sochi-food-detail.jpg',
 'https://example.com/img/sochi-food-bg.jpg',
 'Сочи, рестораны: "У моря", "Кавказский дворик", "Фрегат"'),

(7, '7-дневный оздоровительный тур с процедурами. Включено: проживание в санатории, диагностика, 3 процедуры в день, питание.', 42000.00,
 'https://example.com/img/spa-detail.jpg',
 'https://example.com/img/spa-bg.jpg',
 'КМВ, санатории: "Родник", "Эльбрус", "Виктория"');