package com.cdd.bookservice.service;

import com.cdd.bookservice.model.Book;
import com.cdd.bookservice.repository.BookRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class BookService {

    private static final Logger log = LoggerFactory.getLogger(BookService.class);

    private final BookRepository bookRepository;

    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public List<Book> getAllBooks() {
        log.info("Fetching all books");
        return bookRepository.findAll();
    }

    public Optional<Book> getBookById(Long id) {
        log.info("Fetching book with id: {}", id);
        return bookRepository.findById(id);
    }

    public Optional<Book> getBookByIsbn(String isbn) {
        log.info("Fetching book with ISBN: {}", isbn);
        return bookRepository.findByIsbn(isbn);
    }

    public List<Book> searchByAuthor(String author) {
        log.info("Searching books by author: {}", author);
        return bookRepository.findByAuthorContainingIgnoreCase(author);
    }

    public List<Book> searchByTitle(String title) {
        log.info("Searching books by title: {}", title);
        return bookRepository.findByTitleContainingIgnoreCase(title);
    }

    public Book createBook(Book book) {
        log.info("Creating new book: {}", book.getTitle());
        if (bookRepository.existsByIsbn(book.getIsbn())) {
            throw new IllegalArgumentException("Book with ISBN " + book.getIsbn() + " already exists");
        }
        return bookRepository.save(book);
    }

    public Optional<Book> updateBook(Long id, Book bookDetails) {
        log.info("Updating book with id: {}", id);
        return bookRepository.findById(id)
                .map(existingBook -> {
                    existingBook.setTitle(bookDetails.getTitle());
                    existingBook.setAuthor(bookDetails.getAuthor());
                    existingBook.setIsbn(bookDetails.getIsbn());
                    existingBook.setPrice(bookDetails.getPrice());
                    existingBook.setDescription(bookDetails.getDescription());
                    existingBook.setPublishedYear(bookDetails.getPublishedYear());
                    existingBook.setQuantity(bookDetails.getQuantity());
                    return bookRepository.save(existingBook);
                });
    }

    public boolean deleteBook(Long id) {
        log.info("Deleting book with id: {}", id);
        if (bookRepository.existsById(id)) {
            bookRepository.deleteById(id);
            return true;
        }
        return false;
    }

    public long getBookCount() {
        return bookRepository.count();
    }
}
