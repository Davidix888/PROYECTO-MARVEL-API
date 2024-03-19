from marvel import Marvel

class Comic:
    def __init__(self, title, release_date, thumbnail_path, thumbnail_extension):
        self.title = title
        self.release_date = release_date
        self.thumbnail_path = thumbnail_path
        self.thumbnail_extension = thumbnail_extension
        self.next = None

    def display(self):
        print("Título:", self.title)
        print("Fecha de lanzamiento:", self.release_date)
        print("Imagen de referencia:", self.thumbnail_path + "/portrait_uncanny." + self.thumbnail_extension)
        print("Botón de detalle: <URL del detalle>")  # Aquí deberías colocar la URL real del detalle del cómic

class ComicList:
    def __init__(self):
        self.head = None

    def append(self, comic):
        if not isinstance(comic, Comic):
            raise ValueError("Se espera un objeto de tipo Comic.")
        if not self.head:
            self.head = comic
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = comic

    def display(self):
        current = self.head
        while current:
            current.display()
            current = current.next

def listar_todos_comics():
    marvel = Marvel(PUBLIC_KEY="058bfc8399d452e011be32a08c89ec22", PRIVATE_KEY="d0d3897f351a05612129a56a28fab348d45c99aa")
    comics_api = marvel.comics

    offset = 0
    limit = 10

    comics_list = ComicList()

    while True:
        print("Listado de Comics:")
        response = comics_api.all(limit=limit, offset=offset)
        results = response["data"]["results"]

        for comic_data in results:
            comic = Comic(
                title=comic_data["title"],
                release_date=comic_data["dates"][0]["date"],
                thumbnail_path=comic_data["thumbnail"]["path"],
                thumbnail_extension=comic_data["thumbnail"]["extension"]
            )
            comics_list.append(comic)

        comics_list.display()

        if len(results) < limit:
            break

        opcion = input("\nPresiona 'Enter' para ver más cómics o ingresa 'q' para salir: ")
        if opcion.lower() == "q":
            break
        
        offset += limit

def buscar_comics_por_nombre_y_anio():
    nombre = input("Ingresa el nombre del cómic: ")
    anio = input("Ingresa el año de lanzamiento del cómic: ")

    marvel = Marvel(PUBLIC_KEY="058bfc8399d452e011be32a08c89ec22", PRIVATE_KEY="d0d3897f351a05612129a56a28fab348d45c99aa")
    comics_api = marvel.comics

    response = comics_api.all(titleStartsWith=nombre, startYear=anio)
    results = response["data"]["results"]

    if results:
        print("\nResultados de la búsqueda:")
        comics_list = ComicList()

        for comic_data in results:
            comic = Comic(
                title=comic_data["title"],
                release_date=comic_data["dates"][0]["date"],
                thumbnail_path=comic_data["thumbnail"]["path"],
                thumbnail_extension=comic_data["thumbnail"]["extension"]
            )
            comics_list.append(comic)

        comics_list.display()
    else:
        print("No se encontraron cómics con los criterios de búsqueda especificados.")

def main():
    opciones_menu = {
        "1": listar_todos_comics,
        "2": buscar_comics_por_nombre_y_anio,
        "3": exit
    }

    while True:
        print("\nMenú:")
        print("1. Listar todos los cómics")
        print("2. Buscar cómics por nombre y año de lanzamiento")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")
        if opcion in opciones_menu:
            opciones_menu[opcion]()
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    main()
