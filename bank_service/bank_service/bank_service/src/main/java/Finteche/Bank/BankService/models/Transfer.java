package Finteche.Bank.BankService.models;

import lombok.Data;

import javax.persistence.*;

@Entity
@Table(name = "transfer")
@Data
public class Transfer extends BaseEntity {

//    @Column(name = "user_id")
//    private Long user_id;
    @Column(name = "account_number_from")
    private int from;
    @Column(name = "account_number_to")
    private int to;
    @Column(name = "amount")
    private int amount;
    @Column(name = "comments")
    private String comments;
}