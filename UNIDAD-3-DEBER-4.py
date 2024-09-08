# sistema de gestion de biblioteca digital
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.titulo = titulo
        self.autor = autor  # Autor será una tupla (nombre, apellido)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"{self.titulo} por {self.autor[0]} {self.autor[1]} (ISBN: {self.isbn})"


class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []

    def prestar_libro(self, libro):
        self.libros_prestados.append(libro)

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            self.libros_prestados.remove(libro)

    def __str__(self):
        libros = ', '.join([libro.titulo for libro in self.libros_prestados])
        return f"{self.nombre} (ID: {self.id_usuario}) - Libros prestados: {libros}"


class Biblioteca:
    def __init__(self):
        self.libros = {}
        self.usuarios = set()

    def añadir_libro(self, libro):
        if libro.isbn not in self.libros:
            self.libros[libro.isbn] = libro
        else:
            print(f"El libro con ISBN {libro.isbn} ya está en la biblioteca.")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            del self.libros[isbn]
        else:
            print(f"No se encontró un libro con ISBN {isbn}.")

    def registrar_usuario(self, nombre, id_usuario):
        if id_usuario not in [usuario.id_usuario for usuario in self.usuarios]:
            self.usuarios.add(Usuario(nombre, id_usuario))
        else:
            print(f"El usuario con ID {id_usuario} ya está registrado.")

    def dar_baja_usuario(self, id_usuario):
        self.usuarios = {usuario for usuario in self.usuarios if usuario.id_usuario != id_usuario}

    def prestar_libro(self, isbn, id_usuario):
        if isbn in self.libros:
            libro = self.libros[isbn]
            usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
            if usuario:
                usuario.prestar_libro(libro)
                del self.libros[isbn]
            else:
                print(f"No se encontró un usuario con ID {id_usuario}.")
        else:
            print(f"No se encontró un libro con ISBN {isbn}.")

    def devolver_libro(self, isbn, id_usuario):
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        if usuario:
            libro = next((l for l in usuario.libros_prestados if l.isbn == isbn), None)
            if libro:
                usuario.devolver_libro(libro)
                self.libros[isbn] = libro
            else:
                print(f"El usuario con ID {id_usuario} no tiene el libro con ISBN {isbn}.")
        else:
            print(f"No se encontró un usuario con ID {id_usuario}.")

    def buscar_libros(self, **kwargs):
        resultados = [libro for libro in self.libros.values()
                      if all(getattr(libro, k, None) == v for k, v in kwargs.items())]
        return resultados

    def listar_libros_prestados(self, id_usuario):
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        if usuario:
            return usuario.libros_prestados
        else:
            print(f"No se encontró un usuario con ID {id_usuario}.")
            return []

    def __str__(self):
        libros = ', '.join([str(libro) for libro in self.libros.values()])
        usuarios = ', '.join([str(usuario) for usuario in self.usuarios])
        return f"Libros en biblioteca: {libros}\nUsuarios registrados: {usuarios}"


# Crear la biblioteca
biblioteca = Biblioteca()

# Crear y añadir libros
libro1 = Libro("Cien años de soledad", ("Gabriel", "García Márquez"), "Novela", "978-3-16-148410-0")
libro2 = Libro("Don Quijote de la Mancha", ("Miguel", "de Cervantes"), "Novela", "978-1-234-56789-7")
libro3 = Libro("Romeo y Julieta", ("William", "Shakespeare"), "Drama", "978-0-14-071472-6")

biblioteca.añadir_libro(libro1)
biblioteca.añadir_libro(libro2)
biblioteca.añadir_libro(libro3)

# Registrar usuarios
biblioteca.registrar_usuario("Juan Pérez", "user123")
biblioteca.registrar_usuario("Ana López", "user456")

# Prestar libro
biblioteca.prestar_libro("978-0-14-071472-6", "user123")  # Prestar "Romeo y Julieta" a Juan Pérez

# Buscar libros
print("Buscar por título 'Romeo y Julieta':", biblioteca.buscar_libros(titulo="Romeo y Julieta"))

# Listar libros prestados
print("Libros prestados a user123:", biblioteca.listar_libros_prestados("user123"))

# Devolver libro
biblioteca.devolver_libro("978-0-14-071472-6", "user123")  # Devolver "Romeo y Julieta" por Juan Pérez

# Listar libros en biblioteca
print(biblioteca)

  resultados_busqueda = biblioteca.buscar_libros(titulo="Romeo y Julieta")
print("Buscar por título 'Romeo y Julieta':")
for libro in resultados_busqueda:
    print(libro)