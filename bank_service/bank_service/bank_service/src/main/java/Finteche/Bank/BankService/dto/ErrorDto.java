package Finteche.Bank.BankService.dto;

public class ErrorDto {
    private String errorMessage;

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(Exception e) {
        this.errorMessage = e.getMessage();
    }

}
