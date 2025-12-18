import sys

# ==========================================
# 3.1. Структура класів (Вузол дерева)
# ==========================================
class TreeNode:
    """
    Клас, що представляє вузол AVL-дерева.
    Зберігає ключ, висоту вузла та посилання на нащадків.
    """
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Початкова висота нового вузла - 1


# ==========================================
# Клас AVL-дерева (основна логіка)
# ==========================================
class AVLTree:
    """
    Клас для реалізації самобалансуючого двійкового дерева.
    """

    # ------------------------------------------
    # 3.2. Допоміжні методи (Висота та Баланс)
    # ------------------------------------------
    def get_height(self, node):
        """Повертає висоту вузла або 0, якщо вузол None."""
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """
        Обчислює фактор балансу вузла.
        Balance Factor = Height(Left) - Height(Right)
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # ------------------------------------------
    # 3.3. Реалізація обертань (Rotations)
    # ------------------------------------------
    def right_rotate(self, y):
        """
        Виконує мале праве обертання навколо вузла y.
        """
        x = y.left
        T2 = x.right

        # Виконання повороту
        x.right = y
        y.left = T2

        # Оновлення висот (спочатку y, потім x, бо x тепер вище)
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x  # Новий корінь піддерева

    def left_rotate(self, x):
        """
        Виконує мале ліве обертання навколо вузла x.
        """
        y = x.right
        T2 = y.left

        # Виконання повороту
        y.left = x
        x.right = T2

        # Оновлення висот
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y  # Новий корінь піддерева

    # ------------------------------------------
    # 3.4. Вставка та балансування
    # ------------------------------------------
    def insert(self, node, key):
        """
        Рекурсивна функція вставки ключа з автоматичним балансуванням.
        """
        # 1. Стандартна вставка BST (Binary Search Tree)
        if not node:
            return TreeNode(key)

        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            return node  # Дублікати ключів не додаємо

        # 2. Оновлення висоти поточного предка
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # 3. Отримання фактора балансу
        balance = self.get_balance(node)

        # 4. Балансування (4 сценарії)

        # Case 1 - Left Left (Перекіс вліво-вліво)
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Case 2 - Right Right (Перекіс вправо-вправо)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Case 3 - Left Right (Перекіс вліво, потім вправо)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Case 4 - Right Left (Перекіс вправо, потім вліво)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Метод-обгортка для зручного виклику
    def add_element(self, root, key):
        return self.insert(root, key)

    # ------------------------------------------
    # 3.5. Методи для виводу (Pre-order Traversal)
    # ------------------------------------------
    def pre_order(self, node):
        """Прямий обхід дерева: Корінь -> Ліве -> Праве"""
        if not node:
            return
        print(f"{node.key} ", end="")
        self.pre_order(node.left)
        self.pre_order(node.right)

# ==========================================
# 4. Main execution (Демонстрація роботи)
# ==========================================
if __name__ == "__main__":
    my_tree = AVLTree()
    root = None
    
    # Тестові дані, які у звичайному дереві дали б "лінію"
    data_to_insert = [10, 20, 30, 40, 50, 25]
    
    print(f"Вхідні дані: {data_to_insert}")

    # Вставка елементів
    for item in data_to_insert:
        root = my_tree.add_element(root, item)

    # Вивід результату
    print("\nРезультат (Pre-order traversal):")
    my_tree.pre_order(root)
    print(f"\n\nПоточний корінь дерева: {root.key}")
    print("Висота кореня:", root.height)