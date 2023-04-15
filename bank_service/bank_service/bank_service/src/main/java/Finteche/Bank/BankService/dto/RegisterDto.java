package Finteche.Bank.BankService.dto;

import lombok.Data;

import javax.persistence.Column;
import javax.validation.constraints.Pattern;

@Data
public class RegisterDto {
    private String username;

    @Pattern(regexp = "^[a-zA-Z0-9]{1,15}$",
            message = "password must be of 1 to 15 length with no special characters")
    private String password;
    @Pattern(regexp = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9.-]+$",
            message = "email must have normal view")
    private String email;
    @Pattern(regexp = "^[a-zA-Z0-9]{1,15}$",
            message = "firstname must be of 1 to 15 length with no special characters with latin letters")
    private String firstName;
    @Pattern(regexp = "^[a-zA-Z0-9]{1,15}$",
            message = "lastname must be of 1 to 15 length with no special characters with latin letters")
    private String lastName;
    @Pattern(regexp = "^[a-zA-Z0-9]{1,15}$",
            message = "patronymic must be of 1 to 15 length with no special characters with latin letters")
    private String patronymic;
}
