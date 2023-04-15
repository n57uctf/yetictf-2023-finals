package Finteche.Bank.BankService.rest;
import Finteche.Bank.BankService.config.Global;
import Finteche.Bank.BankService.dto.ErrorDto;
import Finteche.Bank.BankService.dto.TransferDto;
import Finteche.Bank.BankService.models.Role;
import Finteche.Bank.BankService.models.Transfer;
import Finteche.Bank.BankService.models.User;
import Finteche.Bank.BankService.service.UserService;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.util.MimeTypeUtils;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

import static java.util.Arrays.stream;
import static org.springframework.http.HttpHeaders.AUTHORIZATION;
import static org.springframework.http.HttpStatus.FORBIDDEN;
import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;
@RestController
@RequestMapping(value = "/bank/user")
@Slf4j
public class UserController {
    @Autowired
    private UserService userService;

    @CrossOrigin(origins = "http://localhost:4200")
    @PostMapping("/transfer")
    public ResponseEntity<?> transfer(@RequestBody TransferDto transferBlanace, HttpServletRequest request) throws IllegalAccessException {
        String authorizationHeader = request.getHeader(AUTHORIZATION);
        String token = authorizationHeader.substring("Bearer ".length());
        Algorithm algorithm = Algorithm.HMAC256(Global.secret.getBytes());
        JWTVerifier verifier = JWT.require(algorithm).build();
        DecodedJWT decodedJWT = verifier.verify(token);
        String username = decodedJWT.getSubject();
        userService.makeTransfer(transferBlanace, username);
        return ResponseEntity.ok().build();
    }
    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/getAcNum")
    public ResponseEntity<?> UsrAcNum() throws IllegalAccessException {
        return ResponseEntity.ok().body(userService.allAcNum());
    }
    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/lastTransfer")
    public ResponseEntity<?> lastTransfer(HttpServletRequest request) throws IllegalAccessException {
        log.error("1");
        String authorizationHeader = request.getHeader(AUTHORIZATION);
        String token = authorizationHeader.substring("Bearer ".length());
        Algorithm algorithm = Algorithm.HMAC256(Global.secret.getBytes());
        JWTVerifier verifier = JWT.require(algorithm).build();
        DecodedJWT decodedJWT = verifier.verify(token);
        String username = decodedJWT.getSubject();
        return ResponseEntity.ok().body(userService.usrLastTransfer(username));
    }
    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/getInfo")
    public ResponseEntity<?>getInfo(HttpServletRequest request) throws IllegalAccessException {
        String authorizationHeader = request.getHeader(AUTHORIZATION);
        if(authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {
            try {
                String token = authorizationHeader.substring("Bearer ".length());
                Algorithm algorithm = Algorithm.HMAC256(Global.secret.getBytes());
                JWTVerifier verifier = JWT.require(algorithm).build();
                DecodedJWT decodedJWT = verifier.verify(token);
                String username = decodedJWT.getSubject();
                return ResponseEntity.ok().body(userService.findByUsername(username));
            }catch (Exception e){
                throw new IllegalAccessException(e.getMessage());
            }
        } else {
            throw new RuntimeException("Refresh token is missing");
        }
    }
    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/refresh")
    public void refreshToken (HttpServletRequest request, HttpServletResponse response) throws IOException {
        String authorizationHeader = request.getHeader(AUTHORIZATION);
        if(authorizationHeader != null && authorizationHeader.startsWith("Bearer ")){
            try {
                String refreshToken = authorizationHeader.substring("Bearer ".length());
                Algorithm algorithm = Algorithm.HMAC256(Global.secret.getBytes());
                JWTVerifier verifier = JWT.require(algorithm).build();
                DecodedJWT decodedJWT = verifier.verify(refreshToken);
                String username = decodedJWT.getSubject();
                User user = userService.findByUsername(username);
                String accessToken = JWT.create()
                        .withSubject(user.getUsername())
                        .withExpiresAt(new Date(System.currentTimeMillis() + 10 * 60 * 1000))
                        .withIssuer(request.getRequestURI().toString())
                        .withClaim("roles", user.getRoles().stream().map(Role::getName).collect(Collectors.toList()))
                        .sign(algorithm);
                Map<String, String> token = new HashMap<>();
                token.put("accessToken", accessToken);
                token.put("refreshToken",refreshToken);
                response.setContentType(MediaType.APPLICATION_JSON_VALUE);
                new ObjectMapper().writeValue(response.getOutputStream(), token);
            }catch (Exception e){
                log.error("Error loggin in: {}", e.getMessage());
                response.setHeader("error", e.getMessage());
                response.setStatus(FORBIDDEN.value());
                Map<String, String> error = new HashMap<>();
                error.put("error_message", e.getMessage());
                response.setContentType(MimeTypeUtils.APPLICATION_JSON_VALUE);
                new ObjectMapper().writeValue(response.getOutputStream(), error);
            }
        } else {
            throw new RuntimeException("Refresh token is missing");
        }
    }
    @ExceptionHandler
    public ResponseEntity<ErrorDto> handle(Exception e){
        log.error(e.getMessage());
        ErrorDto error = new ErrorDto();
        error.setErrorMessage(e);
        return ResponseEntity.ok().body(error);
    }
}
