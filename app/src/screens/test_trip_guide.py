from trip_guide import Day, TripGuideDay

# Criar o roteiro
trip = TripGuideDay("Roteiro para a Europa")

# Criar dias individuais
day1 = Day(
    date="2024-11-20",
    day_of_week="Segunda-feira",
    breakfast="Café da manhã no hotel",
    lunch="Almoço no Le Jules Verne",
    dinner="Jantar em restaurante francês"
)
day1.add_morning_activity("Visita à Torre Eiffel")
day1.add_morning_activity("Fotos no Trocadéro")
day1.add_afternoon_activity("Passeio no Museu do Louvre")
day1.add_evening_activity("Cruzeiro no Rio Sena")

day2 = Day(
    date="2024-11-21",
    day_of_week="Terça-feira",
    breakfast="Café da manhã no café local",
    lunch="Almoço em restaurante local",
    dinner="Jantar em bistrô clássico"
)
day2.add_morning_activity("Caminhada pelos Jardins de Luxemburgo")
day2.add_afternoon_activity("Tour em Montmartre")
day2.add_evening_activity("Show de cabaré")

# Adicionar dias ao roteiro
trip.add_day(day1)
trip.add_day(day2)
trip.add_day(day2)
trip.add_day(day2)
trip.add_day(day2)

# Exibir o roteiro completo
print(trip)
