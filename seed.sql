--
-- PostgreSQL database dump
--

\restrict nHpgtMUYDnd1XoNvgcBbRxrJ8fR8vP7YRFcQ3desh9EiCkkrBBtB1OvhkaMiz4L

-- Dumped from database version 15.19 (Debian 15.19-1.pgdg13+2)
-- Dumped by pg_dump version 15.19 (Debian 15.19-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.groups (id, name, level, year) FROM stdin;
\.


--
-- Data for Name: ra_disc; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.ra_disc (id, title, shorttitle, department_id) FROM stdin;
1	Психология и педагогика	Психология	5
2	Русский язык и культура речи	Русский язык	5
3	Системы автоматизированного проектирования 1/2	САПР 1/2	1
4	Системы массового обслуживания	СМО	1
5	Теория игр и исследование операций	1	1
6	Управление разработкой программного обеспечения	УРПО	1
7	Методы моделирования радиолокационных систем 2/2	ММРЛС 2/2	1
8	Методы оптимизации	МО	2
9	Основы проектирования трансляторов	ОПТ	1
10	Случайные процессы	СП	2
11	Научно-исследовательская работа 2/2	НИР 2/2	1
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.students (id, first_name, middle_name, last_name) FROM stdin;
1	Алексей	Тестов	Андреевич
2	Борис	Примеров	Борисович
3	Виктор	Данных	Викторович
4	Григорий	Фикстуров	Григорьевич
5	Дмитрий	Макетов	Дмитриевич
6	Елена	Условная	Евгеньевна
7	Жан	Безотчествов	\N
8	Захар	Демонстрационный	Захарович
9	Иван	Учебный	Иванович
10	Кирилл	Проверкин	Кириллович
11	Леонид	Тестовый	Леонидович
12	Максим	Пробный	Максимович
13	Николай	Макетный	Николаевич
14	Олег	Примерный	Олегович
15	Полина	Синтетическая	Павловна
16	Роман	Искусственный	Романович
17	Сергей	Отладочный	Сергеевич
18	Тимофей	Финальный	Тимофеевич
\.


--
-- Data for Name: students_to_groups; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.students_to_groups (stud_id, group_id) FROM stdin;
\.


--
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.groups_id_seq', 1, false);


--
-- Name: ra_disc_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ra_disc_id_seq', 11, true);


--
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.students_id_seq', 18, true);


--
-- PostgreSQL database dump complete
--

\unrestrict nHpgtMUYDnd1XoNvgcBbRxrJ8fR8vP7YRFcQ3desh9EiCkkrBBtB1OvhkaMiz4L

