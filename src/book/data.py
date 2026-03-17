from src.book.schemas import Book

books: list[Book] = [
    Book(
        id=1,
        title="Think Python",
        author="Allen B. Downey",
        publisher="O'Reilly Media",
        published_date="2021-01-01",
        page_count=1234,
        language="English",
    ),
    Book(
        id=2,
        title="Django By Example",
        author="Antonio Mele",
        publisher="Packt Publishing Ltd",
        published_date="2022-01-19",
        page_count=1023,
        language="English",
    ),
]