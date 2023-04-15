package Finteche.Bank.BankService.repository;

import Finteche.Bank.BankService.models.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
    User findByUsername(String username);
    User findByAccountNumber(int accountNumber);
    User findByEmail(String email);
}
