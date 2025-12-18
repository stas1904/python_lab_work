import os

def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def main():
    # 1. Зчитування файлів
    try:
        math_scores = [int(x) for x in read_data('math.txt')]
        phys_scores = [int(x) for x in read_data('physics.txt')]
        stat_scores = [int(x) for x in read_data('statistics.txt')]
        names = read_data('student_names.txt')
    except FileNotFoundError:
        print("Помилка: Не знайдено один із файлів.")
        return

    # Обрізаємо списки до однакової довжини (безпека)
    count = min(len(math_scores), len(phys_scores), len(stat_scores), len(names))
    
    # 2. Створення словника
    # Структура: {'Name': {'Math': 90, 'Physics': 80...}}
    journal = {}
    for i in range(count):
        journal[names[i]] = {
            'Math': math_scores[i],
            'Physics': phys_scores[i],
            'Statistics': stat_scores[i]
        }

    # 3. Аналіз та вивід результатів
    print("-" * 40)
    print("РЕЗУЛЬТАТИ ОБРОБКИ ДАНИХ")
    print("-" * 40)

    # А) Статистика по студентах (ім'я та середній бал)
    # Заразом готуємо список для топу
    avg_list = []
    print("--- Успішність студентів ---")
    for name, subjects in journal.items():
        avg_score = sum(subjects.values()) / 3
        avg_list.append((name, avg_score))
        # print(f"Студент: {name}, середня оцінка: {avg_score:.2f}") 
        # (Закоментував вивід усіх 100 студентів, щоб не засмічувати скрін, але за завданням можна вивести)

    # Б) Топ-3 студентів
    print("\n--- Топ-3 студентів ---")
    top_students = sorted(avg_list, key=lambda x: x[1], reverse=True)[:3]
    for student in top_students:
        print(f"{student[0]} (Середній бал: {student[1]:.2f})")

    # В) Статистика по предметах 
    print("\n--- Статистика по предметах ---")
    print(f"Загальна кількість студентів: {count}")
    
    subjects_data = {
        'Math': math_scores[:count],
        'Physics': phys_scores[:count],
        'Statistics': stat_scores[:count]
    }

    for subj, scores in subjects_data.items():
        avg = sum(scores) / len(scores)
        print(f"Предмет: {subj:10} | Середня: {avg:.2f}, Min: {min(scores)}, Max: {max(scores)}")

    # Г) Найкращий студент з кожного предмету 
    print("\n--- Найкращі з предметів ---")
    for subj, scores in subjects_data.items():
        max_val = max(scores)
        # Знаходимо першого, у кого такий бал
        best_student = next(name for name, data in journal.items() if data[subj] == max_val)
        print(f"{subj:10}: {max_val} | Студент: {best_student}")

    # Д) Студенти з середнім балом < 50
    print("\n--- Студенти з балом нижче 50 ---")
    failed_students = [s[0] for s in avg_list if s[1] < 50]
    print(f"Кількість студентів: {len(failed_students)}")
    if failed_students:
        print(", ".join(failed_students))
    else:
        print("Немає таких студентів")

if __name__ == "__main__":
    main()