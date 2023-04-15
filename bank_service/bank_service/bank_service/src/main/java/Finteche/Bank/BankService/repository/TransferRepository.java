package Finteche.Bank.BankService.repository;

import Finteche.Bank.BankService.models.Transfer;
import antlr.collections.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TransferRepository extends JpaRepository<Transfer, Long> {
    Transfer findByFrom(int accountNum);
}
