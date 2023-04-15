package Finteche.Bank.BankService.rest;

import Finteche.Bank.BankService.dto.ErrorDto;
import Finteche.Bank.BankService.dto.RegisterDto;
import Finteche.Bank.BankService.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.validation.Errors;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;


@RestController
@RequestMapping(value = "/bank")
@Slf4j
public class RegisterController {

    @Autowired
    private UserService userService;

    @CrossOrigin(origins = "http://localhost:4200")
    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterDto registerDto, Errors errors, Model model) throws IllegalAccessException {
        if(errors.hasErrors()) throw new IllegalAccessException(errors.toString());
        userService.register(registerDto);
        return ResponseEntity.ok().build();
    }

    @ExceptionHandler
    public ResponseEntity<ErrorDto> handle(Exception e){
        log.error(e.getMessage());
        ErrorDto error = new ErrorDto();
        error.setErrorMessage(e);
        return ResponseEntity.ok().body(error);
    }

}
