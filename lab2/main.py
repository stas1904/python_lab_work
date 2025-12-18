import csv

FILENAME = 'netflix_list.csv'

def get_data(filename):
    """
    Завдання 1: Зчитування файлу та розбиття split(',')
    Повертає заголовок та дані.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Видаляємо переноси рядків і розбиваємо по комі
    # Увага: split(',') може ламати рядки, якщо в назві фільму є кома.
    # Але це вимога лабораторної.
    data = [line.strip().split(',') for line in lines]
    
    header = data[0]
    rows = data[1:]
    return header, rows

def get_col_index(header, col_name):
    """Допоміжна функція для пошуку індексу колонки за назвою"""
    try:
        return header.index(col_name)
    except ValueError:
        return -1

# --- Завдання 2: Comprehensions ---
def task_comprehensions(header, rows):
    idx_rating = get_col_index(header, 'rating')
    
    print("\n--- Завдання: Рейтинг > 7.5 та перші 5 колонок ---")
    # Фільтруємо: рейтинг > 7.5 (якщо рейтинг існує), беремо slice [:5]
    filtered_list = [
        row[:5] for row in rows 
        if len(row) > idx_rating and row[idx_rating].replace('.', '', 1).isdigit() and float(row[idx_rating]) > 7.5
    ]
    
    # Вивід перших 3 для прикладу
    for item in filtered_list[:3]:
        print(item)

# --- Завдання 3: Генераторна функція ---
def english_post_2015_generator(header, rows):
    idx_lang = get_col_index(header, 'language')
    idx_type = get_col_index(header, 'type')
    idx_end = get_col_index(header, 'endYear')
    
    for row in rows:
        # Перевірка на довжину рядка, щоб уникнути помилок index out of range
        if len(row) <= max(idx_lang, idx_type, idx_end): continue
            
        lang = row[idx_lang]
        end_year = row[idx_end]
        
        # Перевіряємо чи end_year є числом і > 2015
        if lang == 'English' and end_year.isdigit() and int(end_year) > 2015:
            yield row

# --- Завдання 4: Ітератор ---
class CastIterator:
    def __init__(self, header, rows):
        self.rows = rows
        self.idx_cast = get_col_index(header, 'cast')
        self.current = 0
        
    def __iter__(self):
        return self

    def __next__(self):
        while self.current < len(self.rows):
            row = self.rows[self.current]
            self.current += 1
            
            if len(row) > self.idx_cast:
                cast_text = row[self.idx_cast]
                # Умова: довжина рядка акторів > 50
                if len(cast_text) > 50:
                    return cast_text
        raise StopIteration

# --- Завдання 5: Статистика ---
def calculate_stats(header, rows):
    idx_adult = get_col_index(header, 'isAdult')
    idx_votes = get_col_index(header, 'numVotes')
    idx_rating = get_col_index(header, 'rating')
    
    adult_count = 0
    high_votes_ratings = []
    
    for row in rows:
        if len(row) <= max(idx_adult, idx_votes, idx_rating): continue
        
        # Рахуємо Adult content
        if row[idx_adult] == '1':
            adult_count += 1
            
        # Збираємо рейтинги для numVotes > 1000
        votes_str = row[idx_votes]
        rating_str = row[idx_rating]
        
        if votes_str.isdigit() and int(votes_str) > 1000:
            if rating_str.replace('.', '', 1).isdigit():
                high_votes_ratings.append(float(rating_str))
                
    avg_rating = sum(high_votes_ratings) / len(high_votes_ratings) if high_votes_ratings else 0
    
    print("\n--- Статистика ---")
    print(f"Кількість 'Adult' контенту: {adult_count}")
    print(f"Середній рейтинг (де голосів > 1000): {avg_rating:.2f}")
    return avg_rating # Повертаємо для наступного завдання

# --- Завдання 6: Генератор + Comprehensions (Складний фільтр) ---
def complex_filter(header, rows, avg_rating_global):
    idx_episodes = get_col_index(header, 'episodes') # Припускаємо, що така колонка є або це episodesOrSeasons
    if idx_episodes == -1: idx_episodes = get_col_index(header, 'episode') # Спроба знайти схожу назву
    idx_rating = get_col_index(header, 'rating')
    idx_title = get_col_index(header, 'title') # Припускаємо назву колонки title

    print("\n--- Шоу > 10 епізодів та рейтинг вище середнього ---")
    
    # Генератор
    def valid_show_gen():
        for row in rows:
            if len(row) <= max(idx_episodes, idx_rating, idx_title): continue
            
            eps = row[idx_episodes]
            rate = row[idx_rating]
            
            if eps.isdigit() and int(eps) > 10:
                if rate.replace('.', '', 1).isdigit() and float(rate) > avg_rating_global:
                    yield row[idx_title]

    # Comprehension для збору результатів з генератора
    top_shows = [title for title in valid_show_gen()]
    
    # Вивід перших 5
    for t in top_shows[:5]:
        print(t)

# --- Main Execution ---
if __name__ == "__main__":
    try:
        header, rows = get_data(FILENAME)
        
        # 1. Comprehensions
        task_comprehensions(header, rows)
        
        # 2. Generator Function
        print("\n--- Генератор (English, > 2015) [перші 3] ---")
        gen = english_post_2015_generator(header, rows)
        for _ in range(3):
            try:
                print(next(gen))
            except StopIteration:
                break
                
        # 3. Iterator Class
        print("\n--- Ітератор (Cast > 50 символів) [перші 10] ---")
        cast_iter = CastIterator(header, rows)
        count = 0
        for cast in cast_iter:
            print(f"- {cast[:60]}...") # Друкуємо початок, щоб не засмічувати консоль
            count += 1
            if count == 10:
                break
                
        # 4. Stats
        avg_global = calculate_stats(header, rows)
        
        # 5. Complex Filter
        complex_filter(header, rows, avg_global)

    except FileNotFoundError:
        print(f"Помилка: Файл {FILENAME} не знайдено.")
    except Exception as e:
        print(f"Виникла помилка: {e}")