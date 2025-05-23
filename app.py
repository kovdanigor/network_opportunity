
import networkx as nx
from ipysigma import Sigma
from shinyswatch import theme
from shiny import reactive, req
from shiny.express import input, ui, render
from shinywidgets import render_widget, render_plotly
import pandas as pd
import netfunction
import plotly.express as px
from faicons import icon_svg
import plotly.graph_objects as go


# Настройки страницы
ui.page_opts(
    title=ui.div(
        icon_svg("vector-square"),      # Иконка сети из faicons
        "Networks of Opportunity",
        style="display: flex; align-items: center;"
    ),
    fillable=True,
    id="page",
    theme=theme.journal
)

# Sidebar: Обработка данных и универсальные фильтры для графов
with ui.sidebar(width=400):
    # Обработка данных
    ui.HTML("<h5> ⚙️Обработка данных</h5>")
    ui.hr()

    with ui.card(full_screen=False):
        ui.input_file("file", "Загрузить данные:", accept=".xlsx", width='400px',
                      button_label='Обзор', placeholder='Файл отсутствует')

    ui.hr()

    # Универсальные фильтры для сетей
    with ui.card(full_screen=False):
        with ui.accordion(id="acc", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация данных'):
                ui.input_date_range(
                    "pub_date", "Дата публикации вакансии:",
                    start="2024-01-01", end="2024-12-31",
                    min="2024-01-01", max="2024-12-31", width='400px'
                )
                ui.input_selectize("employer", "Работодатель:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("industry", "Отрасль деятельности:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("key_skills", "Навыки:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("region", "Регион:", choices=[],
                                   multiple=True, width=200)

                ui.input_selectize("specialty", "Название специальности:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("employment_type", "Вид трудоустройства:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("experience", "Опыт работы:",
                                   choices=[], multiple=True, width='400px')

                ui.input_slider("salary", "Заработная плата:", min=0,
                                max=100000, value=[0, 100000])
    ui.hr()

    with ui.card(full_screen=False):
        with ui.accordion(id="acc2", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация двумодального графа'):
                col_choices = ['Название специальности', 'Работодатель',
                               'Название региона', 'Федеральный округ']
                row_choices = ['Название специальности', 'Обработанные навыки',
                               'Работодатель', 'Название региона', 'Федеральный округ',
                               'Профессиональный навык', 'Надпрофессиональный навык']
                ui.input_selectize(
                    "bipartite_col", "Выбор колонки:", choices=col_choices,
                    selected='Название специальности', width='400px')
                ui.input_selectize(
                    "bipartite_row", "Выбор строки:", choices=row_choices,
                    selected='Обработанные навыки', width='400px')

    with ui.card(full_screen=False):
        with ui.accordion(id="acc3", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация одномодального графа со-встречаемости'):
                choices = ['Обработанные навыки',
                           'Профессиональный навык',
                           'Надпрофессиональный навык']
                ui.input_selectize(
                    "onemode_semantic", "Выбор переменной для построения графа:", choices=choices,
                    selected='Обработанные навыки', width='400px')

    with ui.card(full_screen=False):
        with ui.accordion(id="acc4", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация одномодального графа схожести'):
                choices = ['Название специальности',
                           'Работодатель',
                           'Название региона',
                           'Федеральный округ']
                choices_2 = ['Обработанные навыки',
                             'Профессиональный навык',
                             'Надпрофессиональный навык']
                ui.input_selectize(
                    "onemode_similarity", "Выбор переменной для построения графа:", choices=choices,
                    selected='Название специальности', width='400px')

                ui.input_selectize(
                    "var_broker", "Переменная-брокер:", choices=choices_2,
                    selected='Обработанные навыки', width='400px')

    ui.hr()


# Реактивные вычисления и эффекты


@reactive.calc
def df():
    f = req(input.file())
    return pd.read_excel(f[0]['datapath'])


@reactive.calc
def processed_data():
    data = df()
    data['Обработанные навыки'] = data['Ключевые навыки'].apply(
        netfunction.parse_skills)
    data['Профессиональный навык'] = data['Профессиональный навык'].apply(eval)
    data['Надпрофессиональный навык'] = data['Надпрофессиональный навык'].apply(
        eval)
    data["Отрасль деятельности"] = data["Отрасль деятельности"].apply(eval)
    data['Отрасль деятельности'] = data['Отрасль деятельности'].apply(
        lambda x: ';'.join(x))
    data = data.dropna(subset=['Работодатель', 'Ключевые навыки'])
    data.reset_index(inplace=True, drop=True)
    data['Дата публикации'] = pd.to_datetime(data['Дата публикации'])
    data["Федеральный округ"] = data["Название региона"].apply(
        netfunction.get_federal_district)
    return data

# --- Остальное


@reactive.effect
def update_selects():
    row_val = input.bipartite_row()
    col_val = input.bipartite_col()

    new_row_choices = [r for r in row_choices if r != col_val]
    if row_val not in new_row_choices:
        row_val = new_row_choices[0] if new_row_choices else None

    new_col_choices = [c for c in col_choices if c != row_val]
    if col_val not in new_col_choices:
        col_val = new_col_choices[0] if new_col_choices else None

    ui.update_selectize(
        "bipartite_row", choices=new_row_choices, selected=row_val)
    ui.update_selectize(
        "bipartite_col", choices=new_col_choices, selected=col_val)


@reactive.effect
def update_filter_choices():
    data = processed_data()
    exp_choices = sorted(data["Опыт работы"].dropna().unique().tolist())
    region_choices = sorted(
        data["Название региона"].dropna().unique().tolist())
    employer_choices = sorted(data['Работодатель'].dropna().unique().tolist())
    specialty_choices = sorted(
        data["Название специальности"].dropna().unique().tolist())
    employment_choices = sorted(
        data["Вид трудоустройства"].dropna().unique().tolist())
    # industry_choices = sorted(data["Отрасль деятельности"].explode().dropna().unique().tolist())
    industry_choices = sorted(data["Отрасль деятельности"].str.split(
        ';').explode().dropna().unique().tolist())
    skills_choices = sorted(data["Ключевые навыки"].str.split(
        ';').explode().dropna().unique().tolist())

    ui.update_selectize("experience", choices=exp_choices)
    ui.update_selectize("region", choices=region_choices)
    ui.update_selectize("employer", choices=employer_choices)
    ui.update_selectize("specialty", choices=specialty_choices)
    ui.update_selectize("employment_type", choices=employment_choices)
    ui.update_selectize("industry", choices=industry_choices)
    ui.update_selectize("key_skills", choices=skills_choices)


@reactive.effect
def update_date_range():
    data = processed_data()
    if not data.empty:
        dates = data['Дата публикации']
        min_date = dates.min().date().isoformat()
        max_date = dates.max().date().isoformat()
        ui.update_date_range("pub_date", min=min_date,
                             max=max_date, start=min_date, end=max_date)


@reactive.effect
def update_salary_range():
    data = processed_data()
    if not data.empty:
        min_salary = int(data['Заработная плата'].min())
        max_salary = int(data['Заработная плата'].max())
        ui.update_slider("salary", min=min_salary,
                         max=max_salary, value=[min_salary, max_salary])


@reactive.calc
def filtered_data():
    data = processed_data()
    if input.pub_date():
        start_date, end_date = input.pub_date()
        data = data[(data['Дата публикации'] >= pd.to_datetime(start_date)) &
                    (data['Дата публикации'] <= pd.to_datetime(end_date))]
    if input.experience():
        data = data[data['Опыт работы'].isin(input.experience())]
    if input.region():
        data = data[data['Название региона'].isin(input.region())]
    if input.salary():
        min_salary, max_salary = input.salary()
        data = data[(data['Заработная плата'] >= min_salary) &
                    (data['Заработная плата'] <= max_salary)]
    if input.employer():
        data = data[data['Работодатель'].isin(input.employer())]
    if input.specialty():
        data = data[data['Название специальности'].isin(input.specialty())]
    if input.employment_type():
        data = data[data['Вид трудоустройства'].isin(input.employment_type())]
    if input.industry():
        pattern = '|'.join(input.industry())
        data = data[data['Отрасль деятельности'].str.contains(pattern)]
    if input.key_skills():
        pattern = '|'.join(input.key_skills())
        data = data[data['Ключевые навыки'].str.contains(pattern)]
    return data


@reactive.calc
def semantic_cooccurrence_matrix():
    data = filtered_data()
    if data.empty:
        return pd.DataFrame()
    return netfunction.create_co_occurrence_matrix(data, input.onemode_semantic())


@reactive.calc
def semantic_graph():
    matrix = semantic_cooccurrence_matrix()
    if matrix.empty:
        return None
    G = nx.from_pandas_adjacency(matrix)
    return G


@reactive.calc
def bipartite_matrix_custom():
    data = filtered_data()
    if data.empty:
        return pd.DataFrame()
    col_var = input.bipartite_col() or 'Название специальности'
    row_var = input.bipartite_row() or 'Обработанные навыки'
    return netfunction.create_group_values_matrix(data, col_var, row_var)


@reactive.calc
def bipartite_graph():
    matrix = bipartite_matrix_custom()
    if matrix.empty:
        return None
    return netfunction.create_bipartite_graph(matrix)


#  Одномодальный схожесть

@reactive.calc
def similarity_bipartite_matrix():
    data = filtered_data()
    if data.empty:
        return pd.DataFrame()
    return netfunction.create_group_values_matrix(data,
                                                  input.onemode_similarity(),
                                                  input.var_broker())


@reactive.calc
def similarity_graph():
    matrix = similarity_bipartite_matrix()
    matrix = netfunction.create_unimodal_matrix(matrix)
    if matrix.empty:
        return None
    G = nx.from_pandas_adjacency(matrix)
    return G


# --- Панели ---

ui.nav_spacer()

with ui.nav_panel('О проекте', icon=icon_svg("circle-info")):
    with ui.card(full_screen=True):
        ui.HTML(
            """
    <div>
       <h3>Основная суть проекта 🚀</h3>
       <p>
         <strong>Networks of Opportunity</strong> — это интерактивное веб-приложение для анализа данных о вакансиях, собранных в рамках проекта 
         <a href="https://rosnavyk.ru/" target="_blank" rel="noopener noreferrer">РосНавык</a>.
       </p>
       <h4>Функционал приложения</h4>
       <ul>
         <li><strong>Визуализировать связи</strong> 🔗 между навыками, специальностями, регионами, работодателями и другими переменными через двумодальные и одномодальные графы.</li>
         <li><strong>Анализировать данные</strong> 📊 с помощью фильтров (работодатель, навыки, заработная плата, опыт работы и др.).</li>
         <li><strong>Искать схожие узлы в графе</strong> 🔍 через векторное сходство.</li>
         <li><strong>Определять целевые навыки</strong> 🎯, необходимые для получения сразу нескольких квалификаций.</li>
         <li><strong>Анализировать кластеры компетенций</strong> 🧠 с помощью выделения сообществ в графе.</li>
         <li><strong>Оценивать ценность навыков</strong> 💰 через привязку к зарплатным предложениям.</li>
       </ul>
       <hr>
       <hr>
       <h4>Как можно использовать веб-приложение для анализа рынка труда и компетенций 🌐</h4>
       <ul>
         <li><strong>Выявлять</strong>, какие навыки чаще всего требуются совместно в вакансиях, чтобы строить актуальные профили компетенций для разных специальностей.</li>
         <li><strong>Определять</strong> пересекающиеся навыки между различными специальностями, чтобы находить универсальные и смежные компетенции для переквалификации или расширения профиля кандидата.</li>
         <li><strong>Находить</strong> группы похожих между собой специальностей по требуемым навыкам для планирования карьерных переходов и построения альтернативных карьерных траекторий.</li>
         <li><strong>Анализировать спрос</strong> на навыки и профессии со стороны компаний, чтобы выявлять возможности для партнерств, стажировок или усиления кадровой политики.</li>
         <li><strong>Разрабатывать</strong> новые продукты и сервисы в области образования, HR или рекрутинга на основе анализа текущего рынка требований к навыкам.</li>
         <li><strong>Фокусироваться</strong> на дорогостоящих и актуальных для топ-компаний навыках для создания коммерчески успешных программ и проектов.</li>
       </ul>
       <hr>
       <h4>Основные компоненты приложения</h4>
       <h5>1. Боковая панель 📑</h5>
       <ul>
         <li><strong>Загрузка данных</strong>: Загрузка Excel-файла с вакансиями.</li>
         <li>
           <strong>Фильтры данных</strong>:
           <ul>
             <li>Дата публикации, регион, заработная плата, опыт работы, специальность.</li>
             <li>Автоматическое обновление диапазонов фильтров на основе структуры загруженного датасета.</li>
           </ul>
         </li>
         <li><strong>Настройки графа</strong>: Выбор переменных для двумодального графа (например, "Специальность ↔ Навыки").</li>
         <li><strong>Порог фильтрации</strong> для графов по силе связей и настройка параметров визуализации (размер узлов, размер ребер, цветовая кодировка).</li>
       </ul>
       <h5>2. Основные панели для анализа данных 📚</h5>
       <ul>
         <li>
           <strong>Вкладка "Сеть"</strong>:
           <ul>
             <li><strong>Двумодальный граф</strong>: Визуализация связей между двумя категориями (например, "Работодатель ↔ Навыки").</li>
             <li><strong>Одномодальный граф</strong>: 
               <ul>
                 <li>Построение графа со-встречаемости по частоте совместного появления в вакансиях (например, "Навыки ↔ Навыки")</li>
                 <li>Построение графа схожести по связующей переменной (например, "Работодатель ↔ Работодатель" через Навыки)</li>
               </ul>
             </li>
           </ul>
         </li>
         <li>
           <strong>Вкладка "Рекомендации"</strong>:
           <ul>
             <li><strong>Схожие узлы</strong>: Топ-N элементов, наиболее похожих на выбранный узел.</li>
             <li><strong>Соседние узлы</strong>: Топ-N прямых соседей выбранного узла.</li>
           </ul>
         </li>
       </ul>
       <hr>
       <h4>Технические особенности ⚙️</h4>
       <ul>
         <li><strong>Визуализация графов</strong>: Библиотека <strong>ipysigma</strong> на основе <strong>Sigma.js</strong> и <strong>Graphology</strong>.</li>
         <li><strong>Сетевой анализ</strong>: Расчет метрик центральности (степень, близость, посредничество) через <strong>NetworkX</strong>.</li>
         <li><strong>Рекомендательная система</strong>: Поиск схожих узлов через
          <a href="https://www.tandfonline.com/doi/full/10.1080/12460125.2024.2354585" target="_blank" rel="noopener noreferrer">обобщенную меру Жаккара</a>.</li>
       </ul>
       <hr>
       <h4>Как начать работу 🏁</h4>
       <ol>
         <li><strong>Загрузите данные</strong> через боковую панель.</li>
         <li><strong>Настройте фильтры</strong> (работодатель, навыки, специальности, регион и др.).</li>
         <li><strong>Изучите графы</strong>: Выберите переменные для одномодальных и двумодальных графов, настройте визуализацию узлов и ребер.</li>
         <li><strong>Проведите сетевой анализ</strong>: Оцените структуры сообществ, центральность и схожесть узлов.</li>
         <li><strong>Получите рекомендации</strong>: Выберите узел и получите персонализированные рекомендации на основе структуры графа.</li>
       </ol>
       <hr>
    </div>
    """
        )
with ui.nav_panel("Данные", icon=icon_svg("table")):
    with ui.card(full_screen=True):
        ui.card_header("📖 Загруженные данные")

        @render.data_frame
        def table():
            return render.DataTable(processed_data(), filters=True, height='625px')


with ui.nav_panel("Визуализация", icon=icon_svg("chart-bar")):
    with ui.layout_columns(col_widths=(12, 12)):
        with ui.card(full_screen=True):
            ui.card_header(
                "💰 Распределение средней зарплаты: Федеральный округ → Специальность → Опыт работы")

            @render_plotly
            def sankey_chart():
                data = filtered_data()
                if data.empty:
                    return px.scatter(title="Нет данных для отображения ❌")

                df_sankey = data.groupby(["Федеральный округ", "Название специальности", "Опыт работы"])[
                    "Заработная плата"].agg(netfunction.nonzero_mean).reset_index()

                unique_districts = list(
                    df_sankey["Федеральный округ"].unique())
                unique_specialties = list(
                    df_sankey["Название специальности"].unique())
                unique_experience = list(df_sankey["Опыт работы"].unique())

                nodes = unique_districts + unique_specialties + unique_experience
                node_indices = {name: i for i, name in enumerate(nodes)}

                source_districts = df_sankey["Федеральный округ"].map(
                    node_indices).tolist()
                target_specialties = df_sankey["Название специальности"].map(
                    node_indices).tolist()
                values_districts = df_sankey["Заработная плата"].tolist()

                source_specialties = df_sankey["Название специальности"].map(
                    node_indices).tolist()
                target_experience = df_sankey["Опыт работы"].map(
                    node_indices).tolist()
                values_specialties = df_sankey["Заработная плата"].tolist()

                source = source_districts + source_specialties
                target = target_specialties + target_experience
                value = values_districts + values_specialties

                palette = px.colors.qualitative.Set2
                node_colors = {node: palette[i % len(
                    palette)] for i, node in enumerate(nodes)}

                opacity = 0.4
                link_colors = [node_colors[nodes[src]].replace(
                    ")", f", {opacity})").replace("rgb", "rgba") for src in source]

                fig = go.Figure(go.Sankey(
                    valueformat=".0f",
                    node=dict(
                        pad=15,
                        thickness=25,
                        line=dict(color="black", width=0.7),
                        label=nodes,
                        color=[node_colors[node]
                               for node in nodes],
                        hoverlabel=dict(
                            font=dict(size=14, family="Arial", color="black", weight="bold")),
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=value,
                        color=link_colors
                    )
                ))

                fig.update_layout(
                    title=None,
                    font=dict(size=14, family="Arial", color="black",
                              weight="bold"),
                    plot_bgcolor="white"
                )

                return fig

        with ui.card(full_screen=True):
            ui.card_header("📈 Динамика публикации вакансий по специальностям")

            @render_plotly
            def vacancies_trend():
                data = filtered_data()
                if data.empty:
                    return px.scatter(title="Нет данных для отображения")

                df_grouped = data.groupby(
                    [pd.Grouper(key="Дата публикации", freq="M"),
                     "Название специальности"]
                ).size().reset_index(name="Количество вакансий")

                fig = px.line(
                    df_grouped,
                    x="Дата публикации",
                    y="Количество вакансий",
                    color="Название специальности",
                    title="",
                    template="plotly_white",
                    markers=True
                ).update_layout(xaxis_title=None, yaxis_title=None, title=None)
                return fig


# Панель с графами
with ui.nav_panel("Сеть", icon=icon_svg('circle-nodes')):
    with ui.navset_card_underline(id="selected_navset_card_underline1"):

        with ui.nav_panel("Двумодальный граф"):
            with ui.layout_columns(col_widths=(4, 8)):
                with ui.card(full_screen=False):
                    ui.card_header("🔎 Фильтры визуализации")

                    ui.input_slider(
                        "edge_threshold_dm", "Порог силы связей:",
                        min=0, max=500, value=10, width=250
                    )

                    ui.input_selectize("node_color_dm", "Выделение цвета узла:",
                                       choices=['Модулярность', 'Модальность',
                                                'Уникальность/общность'],
                                       width=250)

                    ui.input_selectize(
                        "node_size_dm", "Метрика размера узла:",
                        choices=["Центральность по степени",
                                 "Центральность по близости", "Центральность по посредничеству"], width=250
                    )
                    ui.input_slider(
                        "node_size_range_dm", "Диапазон размера узла:",
                        min=1, max=50, value=[3, 15], width=250
                    )

                    ui.input_slider(
                        "edge_size_range_dm", "Диапазон размера ребра:",
                        min=1, max=50, value=[1, 10], width=250
                    )

                    ui.input_slider(
                        "louvain_resolution_dm", "Разрешение Louvain для модулярности:",
                        min=0, max=2, value=1, step=0.1, width=250
                    )
                with ui.card(full_screen=True):
                    ui.card_header("🔗 Граф")

                    @render_widget
                    def widget():
                        G = bipartite_graph()

                        if input.key_skills():
                            try:
                                skills = list(input.key_skills())
                                G = G.subgraph(skills + [n for node in skills for n in G.neighbors(node)])
                            except:
                                ui.notification_show("❌ Отфильтрованные навыки отсутствуют в выбранном графе",
                                                     type="error", duration=10
                                                     )

                        if G is None:
                            ui.notification_show(
                                "❌ Нет данных для построения графа",
                                type="error", duration=10
                            )
                            return None
                        # Выбор метрики для размера узлов

                        threshold = input.edge_threshold_dm() or 0
                        G = netfunction.filter_graph(G, threshold)

                        metric_choice = input.node_size_dm()
                        if metric_choice == "Центральность по степени":
                            metric = nx.degree_centrality(G)
                        elif metric_choice == "Центральность по близости":
                            metric = nx.closeness_centrality(G)
                        elif metric_choice == "Центральность по посредничеству":
                            metric = nx.betweenness_centrality(G)
                        else:
                            metric = nx.degree_centrality(G)
                        node_size_values = list(metric.values())

                        text_color = input.node_color_dm()
                        if text_color == 'Модулярность':
                            node_color = 'community'
                        elif text_color == 'Модальность':
                            node_color = 'bipartite'
                        elif text_color == 'Уникальность/общность':
                            node_color_dict = {}
                            for node, data in G.nodes(data=True):
                                if data.get("bipartite") == 2:  # Навыки
                                    neighbors = list(G.neighbors(node))
                                    if len(neighbors) == 1:
                                        # Уникальный навык — красный
                                        node_color_dict[node] = "#fc1717"
                                    else:
                                        # Общий навык — синий
                                        node_color_dict[node] = "#179efc"
                                else:
                                    node_color_dict[node] = "#19bb11"
                            nx.set_node_attributes(G, node_color_dict, "color")
                            node_color = 'color'

                        return Sigma(
                            G,
                            node_size=node_size_values,
                            node_size_range=input.node_size_range_dm() or (1, 10),
                            edge_size_range=input.edge_size_range_dm() or (1, 10),
                            node_metrics={"community": {
                                "name": "louvain", "resolution": input.louvain_resolution_dm() or 1}},
                            node_color=node_color,
                            hide_edges_on_move=True,
                            edge_size='weight',
                            node_border_color_from='node',
                            hide_info_panel=True
                        )

        with ui.nav_panel("Одномодальный граф со-встречаемости"):
            with ui.layout_columns(col_widths=(4, 8)):
                with ui.card(full_screen=False):
                    ui.card_header("🔎 Фильтры визуализации")
                    ui.input_slider(
                        "edge_threshold_om", "Порог силы связей:",
                        min=0, max=500, value=10, width=250
                    )

                    ui.input_selectize("node_color_om", "Выделение цвета узла:",
                                       choices=['Модулярность',
                                                'Отфильтрованные (целевые) узлы',
                                                'Заработная плата'],  width=250)

                    ui.input_selectize(
                        "node_size_om", "Метрика размера узла:",
                        choices=["Центральность по степени",
                                 "Центральность по близости", "Центральность по посредничеству"], width=250
                    )
                    ui.input_slider(
                        "node_size_range_om", "Диапазон размера узла:",
                        min=1, max=50, value=[3, 15], width=250
                    )

                    ui.input_slider(
                        "edge_size_range_om", "Диапазон размера ребра:",
                        min=1, max=50, value=[1, 10], width=250
                    )

                    ui.input_slider(
                        "louvain_resolution_om", "Разрешение Louvain для модулярности:",
                        min=0, max=2, value=1, step=0.1, width=250
                    )
                with ui.card(full_screen=True):
                    ui.card_header("🔗 Граф")

                    @render_widget
                    def widget_semantic():
                        G = semantic_graph()

                        if input.key_skills():
                            try:
                                skills = list(input.key_skills())
                                G = G.subgraph(
                                    skills + [n for node in skills for n in G.neighbors(node)])
                            except:
                                ui.notification_show("❌ Отфильтрованные навыки отсутствуют в выбранном графе",
                                                     type="error", duration=10
                                                     )

                        if G is None:
                            ui.notification_show("❌ Нет данных для построения графа",
                                                 type="error", duration=10
                                                 )
                            return None

                        threshold = input.edge_threshold_om() or 0
                        G = netfunction.filter_graph(G, threshold)
                        metric_choice = input.node_size_om()
                        if metric_choice == "Центральность по степени":
                            metric = nx.degree_centrality(G)
                        elif metric_choice == "Центральность по близости":
                            metric = nx.closeness_centrality(G)
                        elif metric_choice == "Центральность по посредничеству":
                            metric = nx.betweenness_centrality(G)
                        else:
                            metric = nx.degree_centrality(G)
                        node_size_values = list(metric.values())

                        gradient = None
                        text_color = input.node_color_om()
                        if text_color == 'Модулярность':
                            node_color = 'community'
                        elif text_color == 'Отфильтрованные (целевые) узлы':
                            try:
                                node_colors = []
                                for node in G.nodes():
                                    if node in skills:
                                        node_colors.append("red")
                                    else:
                                        node_colors.append("blue")
                                node_color = node_colors
                            except:
                                ui.notification_show("❌ Целевые узлы не выбраны в фильтрах",
                                                     type="error", duration=10
                                                     )
                                node_color = 'community'
                        elif text_color == 'Заработная плата':
                            data = filtered_data()
                            data = data[data['Заработная плата'] > 0]
                            data = data.explode(input.onemode_semantic())
                            median_salaries = data.groupby(input.onemode_semantic())[
                                'Заработная плата'].median().to_dict()
                            nx.set_node_attributes(
                                G, median_salaries, "median_salary")
                            node_color = "median_salary"
                            gradient = ("lightgreen", "darkgreen")

                        return Sigma(
                            G,
                            node_size=node_size_values,
                            node_size_range=input.node_size_range_om() or (3, 15),
                            edge_size_range=input.edge_size_range_om() or (1, 10),
                            node_metrics={"community": {
                                "name": "louvain", "resolution": input.louvain_resolution_om() or 1}},
                            node_color=node_color,
                            node_color_gradient=gradient,
                            hide_edges_on_move=True,
                            edge_size='weight',
                            node_border_color_from='node',
                            hide_info_panel=True
                        )

# ====== Одномодальные схожесть

        with ui.nav_panel("Одномодальный граф схожести"):
            with ui.layout_columns(col_widths=(4, 8)):
                with ui.card(full_screen=False):
                    ui.card_header("🔎 Фильтры визуализации")
                    ui.input_slider(
                        "similarity_threshold", "Порог схожести:",
                        min=0, max=100, value=30, width=250
                    )

                    ui.input_selectize("node_color_sim", "Выделение цвета узла:",
                                       choices=['Модулярность',
                                                'Заработная плата'],  width=250)

                    ui.input_selectize(
                        "node_size_sim", "Метрика размера узла:",
                        choices=["Центральность по степени",
                                 "Центральность по близости", "Центральность по посредничеству"], width=250
                    )
                    ui.input_slider(
                        "node_size_range_sim", "Диапазон размера узла:",
                        min=1, max=50, value=[3, 15], width=250
                    )

                    ui.input_slider(
                        "edge_size_range_sim", "Диапазон размера ребра:",
                        min=1, max=50, value=[1, 10], width=250
                    )

                    ui.input_slider(
                        "louvain_resolution_sim", "Разрешение Louvain для модулярности:",
                        min=0, max=2, value=1, step=0.1, width=250
                    )
                with ui.card(full_screen=True):
                    ui.card_header("🔗 Граф")

                    @render_widget
                    def widget_similarity():
                        G = similarity_graph()

                        if G is None:
                            ui.notification_show("❌ Нет данных для построения графа",
                                                 type="error", duration=10
                                                 )
                            return None

                        threshold = input.similarity_threshold() / 100

                        G = netfunction.filter_graph(G, threshold)
                        metric_choice = input.node_size_sim()
                        if metric_choice == "Центральность по степени":
                            metric = nx.degree_centrality(G)
                        elif metric_choice == "Центральность по близости":
                            metric = nx.closeness_centrality(G)
                        elif metric_choice == "Центральность по посредничеству":
                            metric = nx.betweenness_centrality(G)
                        else:
                            metric = nx.degree_centrality(G)
                        node_size_values = list(metric.values())

                        gradient = None
                        text_color = input.node_color_sim()
                        if text_color == 'Модулярность':
                            node_color = 'community'
                        elif text_color == 'Заработная плата':
                            data = filtered_data()
                            data = data[data['Заработная плата'] > 0]
                            median_salaries = data.groupby(input.onemode_similarity())[
                                "Заработная плата"].median().to_dict()
                            nx.set_node_attributes(
                                G, median_salaries, "median_salary")
                            node_color = "median_salary"
                            gradient = ("lightgreen", "darkgreen")

                        return Sigma(
                            G,
                            node_size=node_size_values,
                            node_size_range=input.node_size_range_sim() or (3, 15),
                            edge_size_range=input.edge_size_range_sim() or (1, 10),
                            node_metrics={"community": {
                                "name": "louvain", "resolution": input.louvain_resolution_sim() or 1}},
                            node_color=node_color,
                            node_color_gradient=gradient,
                            hide_edges_on_move=True,
                            edge_size='weight',
                            node_border_color_from='node',
                            hide_info_panel=True
                        )

# --- Рекомендации ----


def create_bar_chart(G, node, node_type, top_n, recommendation_func, x_label, title_template):
    """
    Создает график-бар с визуализацией рекомендаций.

    :param G: Граф, в котором ищутся рекомендации.
    :param node: Выбранный узел.
    :param node_type: Тип узла ("Специальность" или "Навык").
    :param top_n: Количество наблюдений (верхних рекомендаций).
    :param recommendation_func: Функция для получения рекомендаций.
    :param x_label: Подпись для оси X.
    :param title_template: Шаблон заголовка графика (с параметрами {top_n} и {node}).
    :param error_message: Сообщение, если узел не выбран или произошла ошибка.
    :return: Объект графика Plotly.
    """
    if not node:
        return px.bar(x=["Нет выделенных узлов"], y=[0], template="plotly_white").update_layout()

    level_target = "first" if node_type == "Колонка" else "second"

    try:
        recs = recommendation_func(
            G, node, level_target=level_target, top_n=top_n)
        recs.sort(key=lambda x: x[1], reverse=False)
        nodes, similarities = zip(*recs)

        if x_label != 'Вес':
            similarities = [el * 100 for el in similarities]
    except:
        return px.bar(x=["Нет выделенных узлов"], y=[0], template="plotly_white").update_layout()

    unique_nodes = list(set(nodes))
    colors = px.colors.qualitative.G10
    color_map = {n: colors[i % len(colors)]
                 for i, n in enumerate(unique_nodes)}

    fig = px.bar(
        y=nodes,
        x=similarities,
        labels={'x': x_label, 'y': ''},
        title=title_template.format(top_n=top_n, node=node),
        color=nodes,
        template="plotly_white",
        color_discrete_map=color_map
    ).update_layout(
        showlegend=False,
        title_x=0.5,
        title_font=dict(
            size=14, color="black", weight="bold"  # Жирный шрифт
        )
    )
    return fig


with ui.nav_panel("Рекомендация", icon=icon_svg('diagram-project')):
    with ui.navset_card_underline(id="selected_navset_card_underline"):
        with ui.nav_panel("Рекомендация схожих узлов"):
            with ui.layout_columns(col_widths=(6, 6)):
                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация схожих узлов № 1")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_1", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_1", "Количество наблюдений:", 3, min=1, max=30, width="750px")
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_1():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_1", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_1", choices=choices)

                    @render_plotly
                    def recommendations_plot_1():
                        if filtered_data().empty:
                            ui.notification_show(
                                "❌ Нет данных, соответствующих выбранным фильтрам", type="error", duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_1()
                            top_n = input.obs_1()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.recommend_similar_nodes,
                            x_label='Сходство в %',
                            title_template='Топ {top_n} схожих узлов для "{node}"'
                        )

                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация схожих узлов № 2")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_2", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_2", "Количество наблюдений:", 3, min=1, max=30, width='750px')
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_2():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_2", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_2", choices=choices)

                    @render_plotly
                    def recommendations_plot_2():
                        if filtered_data().empty:
                            ui.notification_show("❌ Нет данных, соответствующих выбранным фильтрам",
                                                 type="error", duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_2()
                            top_n = input.obs_2()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.recommend_similar_nodes,
                            x_label='Сходство в %',
                            title_template='Топ {top_n} схожих узлов для "{node}"'
                        )

        with ui.nav_panel("Рекомендация соседних узлов"):
            with ui.layout_columns(col_widths=(6, 6)):
                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация соседних узлов № 1")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_3", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_3", "Количество наблюдений:", 3, min=1, max=30, width='750px')
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_3():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_3", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_3", choices=choices)

                    @render_plotly
                    def neighbor_recommendations_plot_1():
                        if filtered_data().empty:
                            ui.notification_show("❌ Нет данных, соответствующих выбранным фильтрам",
                                                 type="error",
                                                 duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_3()
                            top_n = input.obs_3()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.neighbor_recommendations,
                            x_label='Вес',
                            title_template='Топ {top_n} соседних узла "{node}"'
                        )

                # Новый блок для второй рекомендации соседних узлов
                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация соседних узлов № 2")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_4", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_4", "Количество наблюдений:", 3, min=1, max=30, width='750px')
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_4():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_4", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_4", choices=choices)

                    @render_plotly
                    def neighbor_recommendations_plot_2():
                        if filtered_data().empty:
                            ui.notification_show("❌ Нет данных, соответствующих выбранным фильтрам",
                                                 type="error",
                                                 duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_4()
                            top_n = input.obs_4()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.neighbor_recommendations,
                            x_label='Вес',
                            title_template='Топ {top_n} соседних узла для "{node}"'
                        )


# ------ Chat ---------

# welcome = '''
# 🤗 **Добро пожаловать в Networks of Opportunity!**

# Я — ваш ассистент по анализу вакансий и рынка труда.
# Могу помочь сравнить специальности, навыки и работодателей, выявить ключевые требования для специальностей, а также понять региональные особенности рынка.'''

# prompt = ChatPromptTemplate.from_template(template)


# @reactive.effect
# def update_models():
#     if input.base_url1() == "https://bothub.chat/api/v2/openai/v1":
#         models = ["gpt-3.5-turbo", "gpt-4o",
#                   "gpt-4o-mini",
#                   'o1-mini',
#                   "claude-3.7-sonnet:thinking",
#                   "claude-3.5-haiku",
#                   "deepseek-chat",
#                   "deepseek-r1",
#                   "qwen-2.5-72b-instruct",
#                   "eva-qwen-2.5-32b"]
#         ui.update_selectize("chat_model", choices=models)
#     elif input.base_url1() == "https://openrouter.ai/api/v1":
#         models = ["cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
#                   "deepseek/deepseek-chat:free",
#                   "deepseek/deepseek-r1:free",
#                   "google/gemini-2.0-flash-thinking-exp:free",
#                   'nousresearch/deephermes-3-llama-3-8b-preview:free',
#                   'qwen/qwq-32b:free']
#         ui.update_selectize("chat_model", choices=models)


# with ui.nav_panel("Чат-бот", icon=icon_svg('robot')):
#     with ui.layout_columns(col_widths=(4, 8)):
#         with ui.card(full_screen=False):
#             ui.card_header("🔎 Фильтры для чат-бота")
#             ui.input_password("chat_token", "API-токен сервиса:",
#                               width='400px',
#                               placeholder="Введите токен")
#             ui.input_selectize("chat_model", "Языковая модель:",
#                                choices=[], width='400px')
#             ui.input_selectize("base_url1", "Базовый URL-адрес сервиса:",
#                                choices=["https://bothub.chat/api/v2/openai/v1",
#                                         "https://openrouter.ai/api/v1"],
#                                selected='https://openrouter.ai/api/v1', width='400px')
#             ui.input_slider("temp", "Температура:", min=0,
#                             max=1, value=0, step=0.1, width='400px')

#         # Правая колонка: Чат-бот
#         with ui.card(full_screen=True):
#             ui.card_header("🤖 Чат-бот")
#             welcome = ui.markdown(welcome)
#             chat = ui.Chat(id="chat", messages=[welcome])
#             chat.ui(placeholder='Введите запрос...',
#                     width='min(850px, 100%)')

#         @chat.on_user_submit
#         async def process_chat():
#             user_message = chat.user_input()

#             if user_message == "Очистить чат":
#                 await chat.clear_messages()
#                 await chat.append_message_stream('Чат очищен ✅')
#                 return

#             try:
#                 # Инициализация прогресс-бара с 2 основными этапами
#                 with ui.Progress(min=0, max=5) as p:
#                     p.set(0, message="Начало обработки запроса...")

#                     # Этап 1: Работа с данными и базой
#                     p.set(1, message="Загрузка данных",
#                           detail="Подключение к векторной базе")
#                     qdrant_client = QdrantClient(
#                         url=input.qdrant_url(),
#                         api_key=input.qdrant_api_key(),
#                     )

#                     if not qdrant_client.collection_exists(collection_name=input.collection_name()):
#                         await chat.append_message_stream('Коллекция не создана ❌')
#                         return

#                     try:
#                         p.set(2, message="Загрузка данных",
#                               detail="Подготовка документов")
#                         data = processed_data()
#                         data = data[['Название региона', 'Данные', 'Опыт работы']].sample(
#                             input.filter_data(), random_state=1)
#                         loader = DataFrameLoader(
#                             data, page_content_column="Данные")
#                         documents = loader.load()
#                         splitter = RecursiveCharacterTextSplitter()
#                         split_documents = splitter.split_documents(documents)
#                     except:
#                         await chat.append_message(f'Извините, данные не загружены ❌')
#                         return

#                     p.set(3, message="Загрузка данных",
#                           detail="Обращение к векторному хранилищу")
#                     vector_store = QdrantVectorStore(
#                         client=qdrant_client,
#                         collection_name=input.collection_name(),
#                         embedding=embeddings
#                     )
#                     ensemble = create_retrievers(vector_store, split_documents)

#                     p.set(4, message="Генерация ответа",
#                           detail="Инициализация модели")
#                     model = input.chat_model()
#                     temperature = input.temp()
#                     base_url_m = input.base_url1()
#                     api_key = input.chat_token() or None

#                     try:
#                         llm = ChatOpenAI(
#                             model_name=model,
#                             temperature=temperature,
#                             max_tokens=6000,
#                             base_url=base_url_m,
#                             openai_api_key=api_key
#                         )

#                         llm_chain = (
#                             {"context": ensemble | format_docs,
#                                 "question": RunnablePassthrough()}
#                             | prompt
#                             | llm
#                             | StrOutputParser()
#                         )

#                         p.set(5, message="Генерация ответа",
#                               detail="Обработка запроса")
#                         response = llm_chain.invoke(user_message)
#                         await chat.append_message_stream(response)

#                     except:
#                         await chat.append_message('Ошибка модели, попробуйте изменить фильтры чат-бота ❌')
#                         return

#             except:
#                 await chat.append_message('Ошибка при подготовке данных: загрузите данные, настройки векторную базу данных и фильтры чат-бота ❌')
