## ⚙️ 1. Definição de Modelos

Um **modelo** é uma classe Python que representa uma **tabela** no banco de dados.  
O SQLAlchemy utiliza o conceito de **ORM (Object-Relational Mapping)**, que converte objetos Python em registros de banco.

### 🧱 Exemplo básico

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Classe base para todos os modelos
class Base(DeclarativeBase):
    pass

# Modelo User (tabela users)
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)

    def __repr__(self):
        return f"(nome={self.nome})"
````

### 🔍 Conceitos principais

| Elemento           | Função       | Descrição                     |
| ------------------ | ------------ | ----------------------------- |
| `DeclarativeBase`  | Classe base  | Permite criar modelos ORM     |
| `Mapped`           | Tipo anotado | Define o tipo Python do campo |
| `mapped_column()`  | Função       | Cria a coluna na tabela       |
| `primary_key=True` | Parâmetro    | Define a chave primária       |
| `unique=True`      | Parâmetro    | Impede valores duplicados     |

---

## 🔗 2. Relacionamento 1:N (Um para Muitos)

Um **usuário pode ter várias receitas**, mas cada **receita pertence a um único usuário**.

### 🧱 Exemplo

```python
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # Um usuário tem várias receitas
    recipes = relationship('Recipe', backref='user')

class Recipe(Base):
    __tablename__ = 'recipes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
```

### 🧠 Como funciona

* `ForeignKey("users.id")` → cria o vínculo entre `Recipe` e `User`.
* `relationship('Recipe', backref='user')` → conecta as classes nos dois sentidos.

### 💻 Teste prático

```python
user = session.query(User).first()
print(user.recipes)  # receitas do usuário

recipe = session.query(Recipe).first()
print(recipe.user)   # dono da receita
```

---

## 🔄 3. Relacionamento N:N (Muitos para Muitos)

Um **estudante** pode estar em **vários cursos**, e um **curso** pode ter **vários estudantes**.
Para isso, usamos uma **tabela intermediária** (de associação).

### 🧱 Tabela de associação

```python
from sqlalchemy import Table, ForeignKey, Column

student_course_table = Table(
    "student_course",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)
```

### 🧱 Modelos

```python
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    age: Mapped[int]

    courses: Mapped[list["Course"]] = relationship(
        secondary=student_course_table, back_populates="students"
    )

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    students: Mapped[list["Student"]] = relationship(
        secondary=student_course_table, back_populates="courses"
    )
```

### 🔍 Conceitos importantes

| Elemento            | Descrição                                                         |
| ------------------- | ----------------------------------------------------------------- |
| `secondary`         | Indica a tabela de associação                                     |
| `back_populates`    | Cria ligação nos dois sentidos                                    |
| `Mapped[list[...]]` | Indica uma lista de objetos (ex: um aluno pode ter vários cursos) |

### 💻 Teste prático

```python
student = session.query(Student).first()
print(student.courses)  # cursos do aluno

course = session.query(Course).first()
print(course.students)  # alunos do curso
```

---

## 🔁 4. Autorelacionamento (Relacionamento com a Mesma Tabela)

Um exemplo comum é quando **um usuário pode ser gerente de outros usuários**.

### 🧱 Exemplo

```python
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    gerente_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    # Auto-relacionamento
    gerenciados: Mapped[list['User']] = relationship(
        'User', back_populates='gerente'
    )
    gerente = relationship(
        'User', back_populates='gerenciados', remote_side=[id]
    )
```

### 🔍 Explicação

* `gerente_id` → chave estrangeira que aponta para o próprio modelo.
* `remote_side=[id]` → usado para autoreferências (liga um usuário a outro).
* `back_populates` → cria a relação nos dois sentidos (gerente ↔ gerenciados).

### 💻 Exemplo prático

```python
user1 = User(nome='Bastim')            # gerente
user2 = User(nome='Tião', gerente_id=1)
user3 = User(nome='Munda', gerente_id=1)

session.add_all([user1, user2, user3])
session.commit()

print(user1.gerente)       # None
print(user1.gerenciados)   # [Tião, Munda]
```

---

## 🧠 5. Resumo Geral

| Tipo de Relacionamento | Exemplo          | Características                          |
| ---------------------- | ---------------- | ---------------------------------------- |
| 1:N                    | User → Recipe    | Um usuário tem várias receitas           |
| N:N                    | Student ↔ Course | Uma tabela de associação conecta as duas |
| Auto                   | User ↔ User      | Um usuário pode ser gerente de outro     |

---

## 📘 Dicas Finais

* Sempre importe:

  ```python
  from sqlalchemy.orm import Mapped, mapped_column, relationship
  from sqlalchemy import ForeignKey
  ```
* Use `Base.metadata.create_all(engine)` para gerar as tabelas automaticamente.
* Prefira **type hints** (`Mapped[int]`, `Mapped[str]`) para código mais legível.
* `backref` cria o relacionamento inverso automaticamente.
* `back_populates` exige definição nos dois lados do relacionamento.

---
