--
-- PostgreSQL database dump
--

\restrict Bj8eRCgw9ARUSvHJbuPgEs8msQ75LZSZSson52rRLAAIoCdRxaQ31mdFqgtGufz

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    level integer,
    year integer
);


ALTER TABLE public.groups OWNER TO myuser;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_id_seq OWNER TO myuser;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- Name: ra_control; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ra_control (
    id integer NOT NULL,
    plan_id integer,
    disc_id integer,
    sem integer,
    form integer,
    max_grade integer
);


ALTER TABLE public.ra_control OWNER TO myuser;

--
-- Name: ra_control_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.ra_control_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ra_control_id_seq OWNER TO myuser;

--
-- Name: ra_control_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.ra_control_id_seq OWNED BY public.ra_control.id;


--
-- Name: ra_disc; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ra_disc (
    id integer NOT NULL,
    title text,
    shorttitle text,
    department_id integer
);


ALTER TABLE public.ra_disc OWNER TO myuser;

--
-- Name: ra_disc_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.ra_disc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ra_disc_id_seq OWNER TO myuser;

--
-- Name: ra_disc_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.ra_disc_id_seq OWNED BY public.ra_disc.id;


--
-- Name: ra_mark; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ra_mark (
    id integer NOT NULL,
    version_id integer,
    stud_id integer,
    control_id integer,
    grade integer
);


ALTER TABLE public.ra_mark OWNER TO myuser;

--
-- Name: ra_mark_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.ra_mark_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ra_mark_id_seq OWNER TO myuser;

--
-- Name: ra_mark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.ra_mark_id_seq OWNED BY public.ra_mark.id;


--
-- Name: ra_plan; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ra_plan (
    id integer NOT NULL,
    level integer,
    year integer
);


ALTER TABLE public.ra_plan OWNER TO myuser;

--
-- Name: ra_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.ra_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ra_plan_id_seq OWNER TO myuser;

--
-- Name: ra_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.ra_plan_id_seq OWNED BY public.ra_plan.id;


--
-- Name: ra_results; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ra_results (
    id integer NOT NULL,
    "position" integer,
    stud_id integer,
    cur_sem integer,
    open_sem integer,
    session_score integer,
    total_score integer,
    diff_score integer,
    vega integer,
    vm integer,
    other integer,
    percent real,
    diff_percent real
);


ALTER TABLE public.ra_results OWNER TO myuser;

--
-- Name: ra_results_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.ra_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ra_results_id_seq OWNER TO myuser;

--
-- Name: ra_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.ra_results_id_seq OWNED BY public.ra_results.id;


--
-- Name: ra_version; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ra_version (
    id integer NOT NULL,
    created timestamp without time zone,
    comment text
);


ALTER TABLE public.ra_version OWNER TO myuser;

--
-- Name: ra_version_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.ra_version_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ra_version_id_seq OWNER TO myuser;

--
-- Name: ra_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.ra_version_id_seq OWNED BY public.ra_version.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.students (
    id integer NOT NULL,
    first_name text NOT NULL,
    middle_name text NOT NULL,
    last_name text
);


ALTER TABLE public.students OWNER TO myuser;

--
-- Name: students_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.students_id_seq OWNER TO myuser;

--
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.students_id_seq OWNED BY public.students.id;


--
-- Name: students_to_groups; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.students_to_groups (
    stud_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.students_to_groups OWNER TO myuser;

--
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- Name: ra_control id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_control ALTER COLUMN id SET DEFAULT nextval('public.ra_control_id_seq'::regclass);


--
-- Name: ra_disc id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_disc ALTER COLUMN id SET DEFAULT nextval('public.ra_disc_id_seq'::regclass);


--
-- Name: ra_mark id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_mark ALTER COLUMN id SET DEFAULT nextval('public.ra_mark_id_seq'::regclass);


--
-- Name: ra_plan id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_plan ALTER COLUMN id SET DEFAULT nextval('public.ra_plan_id_seq'::regclass);


--
-- Name: ra_results id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_results ALTER COLUMN id SET DEFAULT nextval('public.ra_results_id_seq'::regclass);


--
-- Name: ra_version id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_version ALTER COLUMN id SET DEFAULT nextval('public.ra_version_id_seq'::regclass);


--
-- Name: students id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.students ALTER COLUMN id SET DEFAULT nextval('public.students_id_seq'::regclass);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.groups (id, name, level, year) FROM stdin;
\.


--
-- Data for Name: ra_control; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.ra_control (id, plan_id, disc_id, sem, form, max_grade) FROM stdin;
25	1	1	9	1	-3
26	1	2	9	1	-3
27	1	3	9	1	-3
28	1	4	9	1	-3
29	1	5	9	1	-3
30	1	6	9	4	5
31	1	7	9	3	5
32	1	8	9	3	5
33	1	9	9	3	5
34	1	10	9	3	5
35	1	6	9	3	5
36	1	11	9	2	5
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
-- Data for Name: ra_mark; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.ra_mark (id, version_id, stud_id, control_id, grade) FROM stdin;
433	3	1	25	-3
434	3	1	26	-3
435	3	1	27	-3
436	3	1	28	-3
437	3	1	29	-3
438	3	1	30	3
439	3	1	31	5
440	3	1	32	4
441	3	1	33	5
442	3	1	34	4
443	3	1	35	5
444	3	1	36	5
445	3	2	25	-9
446	3	2	26	-3
447	3	2	27	-3
448	3	2	28	-3
449	3	2	29	-3
450	3	2	30	-7
451	3	2	31	5
452	3	2	32	3
453	3	2	33	5
454	3	2	34	-7
455	3	2	35	5
456	3	2	36	3
457	3	3	25	-9
458	3	3	26	-3
459	3	3	27	-3
460	3	3	28	-3
461	3	3	29	-3
462	3	3	30	-7
463	3	3	31	5
464	3	3	32	3
465	3	3	33	5
466	3	3	34	3
467	3	3	35	4
468	3	3	36	5
469	3	4	25	-3
470	3	4	26	-3
471	3	4	27	-3
472	3	4	28	-3
473	3	4	29	-3
474	3	4	30	4
475	3	4	31	5
476	3	4	32	4
477	3	4	33	5
478	3	4	34	4
479	3	4	35	5
480	3	4	36	5
481	3	5	25	-3
482	3	5	26	-3
483	3	5	27	-3
484	3	5	28	-3
485	3	5	29	-3
486	3	5	30	4
487	3	5	31	5
488	3	5	32	4
489	3	5	33	5
490	3	5	34	3
491	3	5	35	5
492	3	5	36	5
493	3	6	25	-3
494	3	6	26	-3
495	3	6	27	-3
496	3	6	28	-3
497	3	6	29	-3
498	3	6	30	4
499	3	6	31	5
500	3	6	32	3
501	3	6	33	5
502	3	6	34	3
503	3	6	35	5
504	3	6	36	5
505	3	7	25	-3
506	3	7	26	-3
507	3	7	27	-3
508	3	7	28	-3
509	3	7	29	-3
510	3	7	30	4
511	3	7	31	5
512	3	7	32	4
513	3	7	33	5
514	3	7	34	3
515	3	7	35	5
516	3	7	36	5
517	3	8	25	-9
518	3	8	26	-3
519	3	8	27	-3
520	3	8	28	-3
521	3	8	29	-3
522	3	8	30	4
523	3	8	31	5
524	3	8	32	3
525	3	8	33	5
526	3	8	34	4
527	3	8	35	4
528	3	8	36	5
529	3	9	25	-3
530	3	9	26	-3
531	3	9	27	-3
532	3	9	28	-3
533	3	9	29	-3
534	3	9	30	-7
535	3	9	31	5
536	3	9	32	3
537	3	9	33	5
538	3	9	34	3
539	3	9	35	4
540	3	9	36	4
541	3	10	25	-3
542	3	10	26	-3
543	3	10	27	-3
544	3	10	28	-3
545	3	10	29	-3
546	3	10	30	-7
547	3	10	31	5
548	3	10	32	4
549	3	10	33	5
550	3	10	34	5
551	3	10	35	4
552	3	10	36	5
553	3	11	25	-3
554	3	11	26	-3
555	3	11	27	-3
556	3	11	28	-3
557	3	11	29	-3
558	3	11	30	5
559	3	11	31	5
560	3	11	32	4
561	3	11	33	5
562	3	11	34	4
563	3	11	35	4
564	3	11	36	5
565	3	12	25	-3
566	3	12	26	-3
567	3	12	27	-3
568	3	12	28	-3
569	3	12	29	-3
570	3	12	30	5
571	3	12	31	5
572	3	12	32	5
573	3	12	33	5
574	3	12	34	5
575	3	12	35	5
576	3	12	36	5
577	3	13	25	-9
578	3	13	26	-3
579	3	13	27	-3
580	3	13	28	-3
581	3	13	29	-3
582	3	13	30	-7
583	3	13	31	5
584	3	13	32	3
585	3	13	33	5
586	3	13	34	3
587	3	13	35	5
588	3	13	36	5
589	3	14	25	-9
590	3	14	26	-3
591	3	14	27	-3
592	3	14	28	-7
593	3	14	29	-3
594	3	14	30	3
595	3	14	31	5
596	3	14	32	3
597	3	14	33	4
598	3	14	34	-7
599	3	14	35	5
600	3	14	36	5
601	3	15	25	-3
602	3	15	26	-3
603	3	15	27	-3
604	3	15	28	-3
605	3	15	29	-3
606	3	15	30	5
607	3	15	31	5
608	3	15	32	5
609	3	15	33	5
610	3	15	34	5
611	3	15	35	5
612	3	15	36	5
613	3	16	25	-3
614	3	16	26	-3
615	3	16	27	-3
616	3	16	28	-3
617	3	16	29	-3
618	3	16	30	5
619	3	16	31	5
620	3	16	32	3
621	3	16	33	5
622	3	16	34	4
623	3	16	35	5
624	3	16	36	5
625	3	17	25	-3
626	3	17	26	-3
627	3	17	27	-3
628	3	17	28	-3
629	3	17	29	-3
630	3	17	30	-7
631	3	17	31	5
632	3	17	32	3
633	3	17	33	5
634	3	17	34	3
635	3	17	35	4
636	3	17	36	5
637	3	18	25	-3
638	3	18	26	-3
639	3	18	27	-3
640	3	18	28	-3
641	3	18	29	-3
642	3	18	30	4
643	3	18	31	5
644	3	18	32	3
645	3	18	33	5
646	3	18	34	4
647	3	18	35	4
648	3	18	36	5
\.


--
-- Data for Name: ra_plan; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.ra_plan (id, level, year) FROM stdin;
1	1	21
\.


--
-- Data for Name: ra_results; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.ra_results (id, "position", stud_id, cur_sem, open_sem, session_score, total_score, diff_score, vega, vm, other, percent, diff_percent) FROM stdin;
37	1	12	9	0	50	50	0	34	10	6	100	0
38	2	15	9	0	50	50	0	34	10	6	100	0
39	3	10	9	9	43	43	0	28	9	6	95.56	0
40	4	4	9	0	47	47	0	33	8	6	94	0
41	5	11	9	0	47	47	0	33	8	6	94	0
42	6	16	9	0	47	47	0	34	7	6	94	0
43	7	1	9	0	46	46	0	32	8	6	92	0
44	8	5	9	0	46	46	0	33	7	6	92	0
45	9	7	9	0	46	46	0	33	7	6	92	0
46	10	13	9	9	38	38	0	29	6	3	90.48	0
47	11	6	9	0	45	45	0	33	6	6	90	0
48	12	18	9	0	45	45	0	32	7	6	90	0
49	13	8	9	9	42	42	0	32	7	3	89.36	0
50	14	2	9	9	33	33	0	27	3	3	89.19	0
51	15	17	9	9	40	40	0	28	6	6	88.89	0
52	16	3	9	9	37	37	0	28	6	3	88.1	0
53	17	14	9	9	34	34	0	28	3	3	87.18	0
54	18	9	9	9	39	39	0	27	6	6	86.67	0
\.


--
-- Data for Name: ra_version; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.ra_version (id, created, comment) FROM stdin;
3	2025-09-29 17:33:38.928688	Добавление оценок студентов от 2025-09-29 17:33:38.928652
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.students (id, first_name, middle_name, last_name) FROM stdin;
1	Павел	Александров	Владимирович
2	Диляра	Байрамова	Хакимовна
3	Пётр	Балыков	Дмитриевич
4	Владимир	Бредихин	Александрович
5	Михаил	Долбилов	Анатольевич
6	Диана	Евсеева	Андреевна
7	Константин	Импрота	\N
8	Никита	Католиков	Сергеевич
9	Игорь	Кузьмич	Владимирович
10	Ксения	Малышева	Александровна
11	Вячеслав	Мещеряков	Владимирович
12	Юрий	Мысин	Александрович
13	Константин	Подколзин	Сергеевич
14	Дмитрий	Пронин	Андреевич
15	Виктория	Сибова	Сергеевна
16	Дмитрий	Сидоров	Алексеевич
17	Денис	Торкин	Андреевич
18	Роман	Фединишин	Ярославович
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
-- Name: ra_control_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ra_control_id_seq', 36, true);


--
-- Name: ra_disc_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ra_disc_id_seq', 11, true);


--
-- Name: ra_mark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ra_mark_id_seq', 648, true);


--
-- Name: ra_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ra_plan_id_seq', 1, true);


--
-- Name: ra_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ra_results_id_seq', 54, true);


--
-- Name: ra_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ra_version_id_seq', 3, true);


--
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.students_id_seq', 18, true);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: ra_control ra_control_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_control
    ADD CONSTRAINT ra_control_pkey PRIMARY KEY (id);


--
-- Name: ra_disc ra_disc_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_disc
    ADD CONSTRAINT ra_disc_pkey PRIMARY KEY (id);


--
-- Name: ra_mark ra_mark_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_mark
    ADD CONSTRAINT ra_mark_pkey PRIMARY KEY (id);


--
-- Name: ra_plan ra_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_plan
    ADD CONSTRAINT ra_plan_pkey PRIMARY KEY (id);


--
-- Name: ra_results ra_results_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_results
    ADD CONSTRAINT ra_results_pkey PRIMARY KEY (id);


--
-- Name: ra_version ra_version_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_version
    ADD CONSTRAINT ra_version_pkey PRIMARY KEY (id);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- Name: students_to_groups students_to_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.students_to_groups
    ADD CONSTRAINT students_to_groups_pkey PRIMARY KEY (stud_id, group_id);


--
-- Name: ra_control ra_control_disc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_control
    ADD CONSTRAINT ra_control_disc_id_fkey FOREIGN KEY (disc_id) REFERENCES public.ra_disc(id);


--
-- Name: ra_control ra_control_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_control
    ADD CONSTRAINT ra_control_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.ra_plan(id);


--
-- Name: ra_mark ra_mark_control_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_mark
    ADD CONSTRAINT ra_mark_control_id_fkey FOREIGN KEY (control_id) REFERENCES public.ra_control(id);


--
-- Name: ra_mark ra_mark_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ra_mark
    ADD CONSTRAINT ra_mark_version_id_fkey FOREIGN KEY (version_id) REFERENCES public.ra_version(id);


--
-- Name: students_to_groups students_to_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.students_to_groups
    ADD CONSTRAINT students_to_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id) ON DELETE CASCADE;


--
-- Name: students_to_groups students_to_groups_stud_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.students_to_groups
    ADD CONSTRAINT students_to_groups_stud_id_fkey FOREIGN KEY (stud_id) REFERENCES public.students(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Bj8eRCgw9ARUSvHJbuPgEs8msQ75LZSZSson52rRLAAIoCdRxaQ31mdFqgtGufz

