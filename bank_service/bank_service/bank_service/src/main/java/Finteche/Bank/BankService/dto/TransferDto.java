package Finteche.Bank.BankService.dto;

import lombok.Data;

@Data
public class TransferDto {
    private int to;
    private int amount;
    private String comment;
}
