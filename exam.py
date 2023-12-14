# Кирик Володимир:

# Планувальник подорожей
# Створіть програму для планування подорожей. Користувачі можуть додавати міста, які хочуть відвідати, зазначати дати перебування,
# інтереси та бюджет. 
# Програма повинна генерувати оптимальний маршрут та рекомендації щодо відвідувань, з огляду на введені дані.




from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__)

class City:
    def __init__(self, name, interests, visit_date, budget, days):
        self.name = name
        self.interests = interests
        self.visit_date = visit_date
        self.budget = budget
        self.days = days

def generate_route(cities):
    graph = nx.Graph()
    for city in cities:
        graph.add_node(city.name, interests=city.interests, visit_date=city.visit_date, budget=city.budget, days=city.days)

    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            weight = len(set(cities[i].interests) & set(cities[j].interests)) + 1 / (cities[i].budget + cities[j].budget + 1) + 1 / (cities[i].days + cities[j].days + 1)
            graph.add_edge(cities[i].name, cities[j].name, weight=weight)

    route = nx.dijkstra_path(graph, source=cities[0].name, target=cities[-1].name, weight='weight')
    return route

def print_recommendations(city):
    recommendations = f"\nРекомендації для міста {city.name}:\n"
    recommendations += f"Інтереси: {city.interests}\n"
    recommendations += f"Дата відвідування: {city.visit_date.strftime('%d-%m-%Y')}\n"
    recommendations += f"Кількість днів: {city.days}\n"
    recommendations += f"Бюджет: {city.budget}\n"
    recommendations += "Тут можна відвідати... (додайте ваші рекомендації)"
    return recommendations

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cities_to_visit = []
        for i in range(1, int(request.form["city_count"]) + 1):
            city_name = request.form[f"city_name_{i}"]
            interests = request.form[f"interests_{i}"].split(',')
            visit_date_str = request.form[f"visit_date_{i}"]
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d')
            budget = float(request.form[f"budget_{i}"])
            days = int(request.form[f"days_{i}"])

            cities_to_visit.append(City(city_name, interests, visit_date, budget, days))

        optimal_route = generate_route(cities_to_visit)
        recommendations = [print_recommendations(next((c for c in cities_to_visit if c.name == city_name), None)) for city_name in optimal_route]

        return render_template("result.html", route=optimal_route, recommendations=recommendations)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
            