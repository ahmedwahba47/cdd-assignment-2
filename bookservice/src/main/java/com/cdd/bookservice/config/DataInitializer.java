package com.cdd.bookservice.config;

import com.cdd.bookservice.model.Book;
import com.cdd.bookservice.repository.BookRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;

@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataInitializer.class);

    private final BookRepository bookRepository;

    public DataInitializer(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    @Override
    public void run(String... args) {
        if (bookRepository.count() == 0) {
            log.info("Initializing sample book data...");

            Book book1 = new Book();
            book1.setTitle("Clean Code");
            book1.setAuthor("Robert C. Martin");
            book1.setIsbn("978-0132350884");
            book1.setPrice(new BigDecimal("34.99"));
            book1.setDescription("A Handbook of Agile Software Craftsmanship");
            book1.setPublishedYear(2008);
            book1.setQuantity(50);

            Book book2 = new Book();
            book2.setTitle("Design Patterns");
            book2.setAuthor("Gang of Four");
            book2.setIsbn("978-0201633610");
            book2.setPrice(new BigDecimal("49.99"));
            book2.setDescription("Elements of Reusable Object-Oriented Software");
            book2.setPublishedYear(1994);
            book2.setQuantity(30);

            Book book3 = new Book();
            book3.setTitle("The Pragmatic Programmer");
            book3.setAuthor("David Thomas, Andrew Hunt");
            book3.setIsbn("978-0135957059");
            book3.setPrice(new BigDecimal("44.99"));
            book3.setDescription("Your Journey to Mastery, 20th Anniversary Edition");
            book3.setPublishedYear(2019);
            book3.setQuantity(40);

            Book book4 = new Book();
            book4.setTitle("Docker Deep Dive");
            book4.setAuthor("Nigel Poulton");
            book4.setIsbn("978-1916585256");
            book4.setPrice(new BigDecimal("29.99"));
            book4.setDescription("Zero to Docker in a single book");
            book4.setPublishedYear(2023);
            book4.setQuantity(25);

            Book book5 = new Book();
            book5.setTitle("Kubernetes in Action");
            book5.setAuthor("Marko Luksa");
            book5.setIsbn("978-1617293726");
            book5.setPrice(new BigDecimal("59.99"));
            book5.setDescription("Comprehensive guide to container orchestration");
            book5.setPublishedYear(2018);
            book5.setQuantity(35);

            bookRepository.save(book1);
            bookRepository.save(book2);
            bookRepository.save(book3);
            bookRepository.save(book4);
            bookRepository.save(book5);

            log.info("Sample data initialization complete. {} books added.", bookRepository.count());
        } else {
            log.info("Database already contains {} books. Skipping initialization.", bookRepository.count());
        }
    }
}
