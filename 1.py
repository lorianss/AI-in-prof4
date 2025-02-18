import networkx as nx
import matplotlib.pyplot as plt

# Шаг 1: Создание списка населённых пунктов и расстояний между ними
places = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Омск", "Самара", "Ростов-на-Дону",
    "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград", "Краснодар",
    "Саратов", "Тюмень", "Тольятти", "Ижевск", "Барнаул"
]

# Матрица расстояний
distances = {
    ("Москва", "Санкт-Петербург"): 650,
    ("Москва", "Казань"): 800,
    ("Москва", "Нижний Новгород"): 450,
    ("Санкт-Петербург", "Новосибирск"): 3200,
    ("Санкт-Петербург", "Казань"): 1000,
    ("Новосибирск", "Екатеринбург"): 1700,
    ("Екатеринбург", "Казань"): 1200,
    ("Екатеринбург", "Челябинск"): 300,
    ("Екатеринбург", "Омск"): 900,
    ("Казань", "Нижний Новгород"): 200,
    ("Казань", "Самара"): 600,
    ("Нижний Новгород", "Челябинск"): 1500,
    ("Челябинск", "Омск"): 800,
    ("Омск", "Красноярск"): 1200,
    ("Самара", "Ростов-на-Дону"): 1100,
    ("Самара", "Уфа"): 400,
    ("Ростов-на-Дону", "Краснодар"): 400,
    ("Уфа", "Красноярск"): 2000,
    ("Уфа", "Пермь"): 500,
    ("Уфа", "Екатеринбург"): 500,
    ("Казань", "Екатеринбург"): 1200,
    ("Красноярск", "Воронеж"): 3000,
    ("Пермь", "Волгоград"): 1000,
    ("Волгоград", "Краснодар"): 500,
    ("Краснодар", "Саратов"): 700,
    ("Саратов", "Тюмень"): 1200,
    ("Тюмень", "Тольятти"): 1300,
    ("Тольятти", "Ижевск"): 400,
    ("Ижевск", "Барнаул"): 2000,
}

# Шаг 2: Создание графа
G = nx.Graph()

# Добавление узлов (населённых пунктов)
G.add_nodes_from(places)

# Добавление рёбер с весами (расстояниями)
for (place1, place2), distance in distances.items():
    G.add_edge(place1, place2, weight=distance)

# Шаг 3: Алгоритм поиска с ограничением глубины (DLS)
def depth_limited_search(graph, start, end, max_depth):
    # Проверка, существуют ли стартовый и конечный узлы в графе
    if not graph.has_node(start) or not graph.has_node(end):
        return None, float('inf'), -1

    # Инициализация переменных
    min_distance = float('inf')
    best_path = None
    solution_depth = -1

    def dls(current_node, current_path, current_distance, current_depth):
        nonlocal min_distance, best_path, solution_depth

        # Если достигли целевой узел
        if current_node == end:
            if current_distance < min_distance:
                min_distance = current_distance
                best_path = current_path[:]
                solution_depth = current_depth
            return

        # Если достигнута максимальная глубина
        if current_depth >= max_depth:
            return

        # Исследуем соседей
        for neighbor in graph.neighbors(current_node):
            if neighbor not in current_path:  # Избегаем циклов
                edge_weight = graph[current_node][neighbor]['weight']
                current_path.append(neighbor)
                dls(neighbor, current_path, current_distance + edge_weight, current_depth + 1)
                current_path.pop()  # Возвращаемся назад (backtracking)

    # Запуск DLS
    dls(start, [start], 0, 0)

    return best_path, min_distance, solution_depth

# Шаг 4: Выбор начального и конечного пунктов
start_city = "Москва"
end_city = "Екатеринбург"

# Ограничение глубины поиска
max_depth = 5  # Максимальная глубина дерева поиска

# Поиск минимального расстояния с помощью DLS
best_path, min_distance, solution_depth = depth_limited_search(G, start_city, end_city, max_depth)

# Вывод результатов
if best_path is None:
    print(f"Путь между {start_city} и {end_city} не найден на глубине {max_depth}.")
else:
    print(f"Минимальное расстояние между {start_city} и {end_city}: {min_distance} км")
    print(f"Оптимальный маршрут: {best_path}")
    print(f"Глубина дерева поиска, на которой найдено решение: {solution_depth}")

# Сравнение с решением, полученным вручную
# Предположим, что вручную вычисленное расстояние равно 2450 км
manual_distance = 2450
print(f"Расстояние, вычисленное вручную: {manual_distance} км")
print(f"Разница между автоматическим и ручным решением: {abs(min_distance - manual_distance)} км")

# Визуализация графа и маршрута
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10, font_weight="bold")

# Выделение маршрута (если он найден)
if best_path:
    route_edges = [(best_path[i], best_path[i + 1]) for i in range(len(best_path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='red', width=2)

plt.title("Граф дорог между населёнными пунктами")
plt.show()